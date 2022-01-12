import useAuth from '../Auth/useAuth';

export default function Report() {
  const { authData, 
          modeHandler: { setMode } } = useAuth();
  const superUser = !!authData?.verificationStatus;
  const button_id = document.location.pathname.split('/')[2];
  const reported = authData?.reports || '';
  const report_made = reported.match(button_id) ? 'fa fa-flag small mt-n4 btn-danger' : 'fa fa-flag mt-n4 text-muted';
  return (
   <>
    {superUser && <i id={button_id} className={report_made} onClick={() => setMode(11)}></i>}
   </>
  )
}
