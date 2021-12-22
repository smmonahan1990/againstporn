import axios from 'axios';
const API_URL = '/api';

export default class ArchivesService {
    getArchives(subreddit, params) {
        const url = `${API_URL}${subreddit}${params}`;
        return axios.get(url).then(response => response.data);
    }

    getArchivesByURL(path) {
        const url = `${API_URL}/${path}`;
        return axios.get(url).then(response => response.data);
    }

}
