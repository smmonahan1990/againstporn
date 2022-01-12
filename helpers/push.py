import os, pandas as pd
from pathlib import PosixPath
from reactdev.logging_config import CustomLogger as CL, logging
from reactdev.settings import BASE_DIR
from pmaw import PushshiftAPI as API
from urllib3 import add_stderr_logger
from datetime import datetime as dt, timezone as tz, timedelta as td
from django.db.models import QuerySet

logger = CL(__name__)
pushlogger = logging.getLogger('pmaw.PushshiftAPIBase')
pushlogger.setLevel('INFO')
handler = logging.StreamHandler()
handler.setLevel('INFO')
pushlogger.addHandler(handler)
handler2 = add_stderr_logger()
handler2.setLevel('DEBUG')
logger.addHandler(handler)
logger.addHandler(handler2)

class PMAWHelper:
    api = API()

    def _get_comments_or_submissions_from_ids(self, _ids, d=500):
        if not isinstance(_ids, list):
            if isinstance(_ids, pd.DataFrame):
                _ids = _ids.id.to_list()
            elif isinstance(_ids,QuerySet):
                _ids = list(_ids.values_list('id',flat=True))
            return self._get_comments_or_submissions_from_ids(_ids, d)
        x, y = all(len(i) == 7 for i in _ids), all(len(i) == 6 for i in _ids)
        assert x or y
        query = ('comments','submissions')[bool(y)]
        d = (d, 100)[query == 'submissions']
        inc, _ = divmod(len(_ids),d)
        k = []
        try:
            for i in range(inc+1):
                k.extend([i for i in getattr(self.api, 'search_%s' % query)(ids=_ids[i*d:(i+1)*d])])
                logger.debug("%d of %d batches complete.",i+1,inc+1)
                if len(k) > 50000:
                    df = pd.DataFrame(k)
                    try:
                        self._save(df)
                        k = []
                    except Exception as e:
                        logger.error(e)
                        if df:
                            return df
            df = pd.DataFrame(k)
            self._save(df)
            return df
        except Exception as e:
            logger.error(e)
        if k:
            return k
        return pd.DataFrame({})

    def get(self, _ids, d=None):
        if isinstance(d, int):
            return self._get_comments_or_submissions_from_ids(_ids, d)
        return self._get_comments_or_submissions_from_ids(_ids)

    def get_comments(self, _ids, to_df=True):
        if isinstance(_ids, pd.DataFrame):
            _ids = _ids.id.to_list()
            return self.get_comments(_ids, to_df)
        inc, r = divmod(len(_ids), 100)
        k = []
        for i in range(inc+1):
            k.extend([i for i in self.api.search_submission_comment_ids(_ids[i*100:(i+1)*100])])
            logger.debug('batch %d of %d complete.',i+1, inc+1)
        if to_df:
            return self._get_comments_or_submissions_from_ids(k)
        return k

    def _save(self, df):
        folder = df.subreddit[0]
        if not folder in os.listdir(BASE_DIR / 'csv'):
            os.mkdir(BASE_DIR / 'csv' / folder)
        if not 'raw' in os.listdir(BASE_DIR / 'csv' / folder):
            os.mkdir(BASE_DIR / 'csv' / folder / 'raw')
        subdir  = ('comments', 'posts')[len(df.id[0]) == 6]
        if not subdir in os.listdir(BASE_DIR / 'csv' / folder / 'raw'):
            os.mkdir(BASE_DIR / 'csv' / folder / 'raw' / subdir)
        df.to_csv(BASE_DIR / 'csv' / folder / 'raw' / subdir / ('%d.csv' % dt.now(tz=tz.utc).timestamp())[-10:], index=False)
        logger.debug(df.shape)
