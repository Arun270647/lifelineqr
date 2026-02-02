// LifeLine QR - Authentication Module (Updated for API)

const Auth = {
    // Register new user
    async register(userData) {
        // Validate required fields
        const requiredFields = ['email', 'password', 'name', 'role'];
        for (let field of requiredFields) {
            if (!userData[field]) {
                return {
                    success: false,
                    error: `${field} is required`
                };
            }
        }

        // Create user via API
        const result = await UserStorage.createUser(userData);

        return result;
    },

    // Login user
    async login(email, password) {
        // Call login API
        const result = await Storage.apiCall('auth.php', 'POST', {
            email: email,
            password: password
        });

        if (!result.success) {
            return result;
        }

        // Create session
        this.createSession(result.user);

        return result;
    },

    // Create user session
    createSession(user) {
        sessionStorage.setItem(CONFIG.STORAGE_KEYS.CURRENT_USER, JSON.stringify(user));
    },

    // Get current user
    getCurrentUser() {
        const userData = sessionStorage.getItem(CONFIG.STORAGE_KEYS.CURRENT_USER);
        return userData ? JSON.parse(userData) : null;
    },

    // Check if user is logged in
    isLoggedIn() {
        return this.getCurrentUser() !== null;
    },

    // Check user role
    isRole(role) {
        const user = this.getCurrentUser();
        return user && user.role === role;
    },

    // Logout user
    logout() {
        sessionStorage.removeItem(CONFIG.STORAGE_KEYS.CURRENT_USER);
    },

    // Require authentication
    requireAuth() {
        if (!this.isLoggedIn()) {
            window.location.href = '../pages/login.html';
            return false;
        }
        return true;
    },

    // Require specific role
    requireRole(role) {
        if (!this.requireAuth()) return false;

        if (!this.isRole(role)) {
            Utils.showAlert('Access denied', 'error');
            window.location.href = '../index.html';
            return false;
        }
        return true;
    },

    // Reset password (via API)
    async resetPassword(email) {
        const result = await Storage.apiCall('auth.php', 'PUT', {
            email: email
        });

        return result;
    },

    // Change password
    async changePassword(currentPassword, newPassword) {
        const user = this.getCurrentUser();
        if (!user) return { success: false, error: 'Not logged in' };

        // Get full user from API
        const fullUser = await UserStorage.getUserById(user.id);

        // Verify current password
        if (!Utils.verifyPassword(currentPassword, fullUser.password)) {
            return { success: false, error: 'Current password is incorrect' };
        }

        // Update password
        const updates = {
            password: Utils.hashPassword(newPassword)
        };

        const success = await UserStorage.updateUser(user.id, updates);

        return success ?
            { success: true, message: 'Password changed successfully' } :
            { success: false, error: 'Failed to update password' };
    }
};
