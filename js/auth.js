// LifeLine QR - Authentication Module

const Auth = {
    // Register new user
    register(userData) {
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

        // Create user
        const result = UserStorage.createUser(userData);

        if (result.success) {
            // If student, create QR code
            if (userData.role === CONFIG.ROLES.STUDENT) {
                const qrCode = Utils.generateId();
                QRStorage.createMapping(result.user.id, qrCode);
            }
        }

        return result;
    },

    // Login user
    login(email, password) {
        // Get user by email
        const user = UserStorage.getUserByEmail(email);

        if (!user) {
            return {
                success: false,
                error: 'Invalid email or password'
            };
        }

        // Verify password
        if (!Utils.verifyPassword(password, user.password)) {
            return {
                success: false,
                error: 'Invalid email or password'
            };
        }

        // Create session
        this.createSession(user);

        return {
            success: true,
            user
        };
    },

    // Create user session
    createSession(user) {
        // Don't store password in session
        const sessionUser = { ...user };
        delete sessionUser.password;

        sessionStorage.setItem(CONFIG.STORAGE_KEYS.CURRENT_USER, JSON.stringify(sessionUser));
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

    // Reset password (simulated)
    resetPassword(email) {
        const user = UserStorage.getUserByEmail(email);

        if (!user) {
            return {
                success: false,
                error: 'Email not found'
            };
        }

        // In a real app, this would send an email
        // For now, we'll just generate a temporary password
        const tempPassword = 'Temp' + Math.floor(Math.random() * 10000);

        // Update user password
        const updates = {
            password: Utils.hashPassword(tempPassword)
        };

        Storage.update(CONFIG.STORAGE_KEYS.USERS, user.id, updates);

        return {
            success: true,
            message: `Temporary password: ${tempPassword}`,
            tempPassword
        };
    },

    // Change password
    changePassword(currentPassword, newPassword) {
        const user = this.getCurrentUser();
        if (!user) return { success: false, error: 'Not logged in' };

        const fullUser = UserStorage.getUserById(user.id);

        // Verify current password
        if (!Utils.verifyPassword(currentPassword, fullUser.password)) {
            return { success: false, error: 'Current password is incorrect' };
        }

        // Update password
        const updates = {
            password: Utils.hashPassword(newPassword)
        };

        Storage.update(CONFIG.STORAGE_KEYS.USERS, user.id, updates);

        return { success: true, message: 'Password changed successfully' };
    }
};
