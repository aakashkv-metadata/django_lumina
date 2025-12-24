const API_BASE = '/api';

class LuminaAPI {
    static getAccessToken() {
        return localStorage.getItem('access_token');
    }

    static getRefreshToken() {
        return localStorage.getItem('refresh_token');
    }

    static setTokens(access, refresh) {
        localStorage.setItem('access_token', access);
        if (refresh) localStorage.setItem('refresh_token', refresh);
    }

    static clearTokens() {
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
    }

    static async request(endpoint, options = {}) {
        let token = this.getAccessToken();
        let headers = {
            'Content-Type': 'application/json',
            ...options.headers
        };

        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
        }

        let response = await fetch(`${API_BASE}${endpoint}`, {
            ...options,
            headers
        });

        if (response.status === 401) {
            // Try refresh
            const refresh = this.getRefreshToken();
            if (refresh) {
                try {
                    const refreshRes = await fetch(`${API_BASE}/token/refresh/`, {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({refresh: refresh})
                    });
                    
                    if (refreshRes.ok) {
                        const data = await refreshRes.json();
                        this.setTokens(data.access, data.refresh); // Some servers rotate refresh tokens
                        
                        // Retry original request
                        headers['Authorization'] = `Bearer ${data.access}`;
                        response = await fetch(`${API_BASE}${endpoint}`, {
                            ...options,
                            headers
                        });
                    } else {
                         throw new Error('Refresh failed');
                    }
                } catch (e) {
                    this.logout();
                    return null;
                }
            } else {
                this.logout();
                return null;
            }
        }

        return response;
    }

    static logout() {
        this.clearTokens();
        if (!window.location.pathname.includes('/login') && !window.location.pathname.includes('/signup')) {
            window.location.href = '/login/';
        }
    }

    static async login(username, password) {
        const res = await fetch(`${API_BASE}/login/`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({username, password})
        });
        if (res.ok) {
            const data = await res.json();
            this.setTokens(data.access, data.refresh);
            return true;
        }
        return false;
    }

    static async signup(username, email, password) {
        const res = await fetch(`${API_BASE}/signup/`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({username, email, password})
        });
        return res.ok;
    }
}
