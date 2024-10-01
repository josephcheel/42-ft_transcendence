export async function fetchCSRFToken() {
    try {
        const response = await fetch('http://localhost:8000/get_cookie/', {
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