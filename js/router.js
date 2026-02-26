// LifeLine QR - Router Module

const Router = {
    // Navigate to a page
    navigate(path) {
        window.location.href = path;
    },

    // Get URL parameters
    getParams() {
        const params = {};
        const queryString = window.location.search;
        const urlParams = new URLSearchParams(queryString);

        for (const [key, value] of urlParams) {
            params[key] = value;
        }

        return params;
    },

    // Get single parameter
    getParam(name) {
        const params = this.getParams();
        return params[name] || null;
    },

    // Redirect based on user role
    redirectByRole() {
        const user = Auth.getCurrentUser();

        if (!user) {
            this.navigate('./pages/login.html');
            return;
        }

        if (user.role === CONFIG.ROLES.STUDENT) {
            this.navigate('./pages/student-dashboard.html');
        } else if (user.role === CONFIG.ROLES.DOCTOR) {
            this.navigate('./pages/doctor-dashboard.html');
        } else {
            this.navigate('./index.html');
        }
    },

    // Go back
    goBack() {
        window.history.back();
    }
};
