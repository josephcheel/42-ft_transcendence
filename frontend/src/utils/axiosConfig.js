import axios from 'axios';
import { fetchCSRFToken, getCSRFToken } from './csrf';

axios.defaults.withCredentials = true;

axios.interceptors.request.use(async config => {
    await fetchCSRFToken(); 
    const csrftoken = getCSRFToken(); 
    if (csrftoken) {
        config.headers['X-CSRFToken'] = csrftoken; 
    }
    return config;
}, error => {
    console.error('Axios Request Error:', error); 
    return Promise.reject(error);
});

export default axios;