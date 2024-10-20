export async function fetchCSRFToken() {
    const ORIGIN_IP =  process.env.VUE_APP_ORIGIN_IP
    try {
        const response = await fetch('https://${ORIGIN_IP}:8000/api/get_cookie/', {
            credentials: 'include',
        });

        if (!response.ok) {
            throw new Error('Failed to fetch CSRF token');
        }
    } catch (error) {
        console.error('Error fetching CSRF token:', error);
        throw error; 
    }
}

export function getCSRFToken() {
    const cookies = document.cookie.split('; ');
    const csrftoken = cookies.find(cookie => cookie.startsWith('csrftoken='));

    if (csrftoken) {
        return csrftoken.split('=')[1];
    }

    return null;
}