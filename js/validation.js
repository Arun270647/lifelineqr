// LifeLine QR - Form Validation Module

const Validation = {
    // Email validation
    isValidEmail(email) {
        const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return regex.test(email);
    },

    // Phone validation (Indian format)
    isValidPhone(phone) {
        const regex = /^[6-9]\d{9}$/;
        return regex.test(phone.replace(/[\s-]/g, ''));
    },

    // Password validation
    isValidPassword(password) {
        // At least 6 characters
        return password && password.length >= 6;
    },

    // Required field validation
    isRequired(value) {
        if (typeof value === 'string') {
            return value.trim() !== '';
        }
        return value !== null && value !== undefined;
    },

    // Number validation
    isNumber(value) {
        return !isNaN(parseFloat(value)) && isFinite(value);
    },

    // Age validation
    isValidAge(age) {
        const numAge = parseInt(age);
        return numAge >= 1 && numAge <= 120;
    },

    // Show error on field
    showError(field, message) {
        field.classList.add('error');

        let errorDiv = field.nextElementSibling;
        if (!errorDiv || !errorDiv.classList.contains('form-error')) {
            errorDiv = document.createElement('div');
            errorDiv.className = 'form-error';
            field.parentNode.insertBefore(errorDiv, field.nextSibling);
        }

        errorDiv.textContent = message;
        errorDiv.style.display = 'block';
    },

    // Clear error from field
    clearError(field) {
        field.classList.remove('error');

        const errorDiv = field.nextElementSibling;
        if (errorDiv && errorDiv.classList.contains('form-error')) {
            errorDiv.style.display = 'none';
        }
    },

    // Validate form field
    validateField(field) {
        const value = field.value;
        const type = field.type;
        const required = field.hasAttribute('required');

        // Clear previous error
        this.clearError(field);

        // Check required
        if (required && !this.isRequired(value)) {
            this.showError(field, 'This field is required');
            return false;
        }

        // If empty and not required, it's valid
        if (!value && !required) {
            return true;
        }

        // Type-specific validation
        if (type === 'email' && !this.isValidEmail(value)) {
            this.showError(field, 'Please enter a valid email address');
            return false;
        }

        if (type === 'tel' && !this.isValidPhone(value)) {
            this.showError(field, 'Please enter a valid 10-digit phone number');
            return false;
        }

        if (type === 'password' && !this.isValidPassword(value)) {
            this.showError(field, 'Password must be at least 6 characters');
            return false;
        }

        if (field.dataset.validation === 'age' && !this.isValidAge(value)) {
            this.showError(field, 'Please enter a valid age (1-120)');
            return false;
        }

        return true;
    },

    // Validate entire form
    validateForm(form) {
        const fields = form.querySelectorAll('input, select, textarea');
        let isValid = true;

        fields.forEach(field => {
            if (!this.validateField(field)) {
                isValid = false;
            }
        });

        return isValid;
    },

    // Setup real-time validation
    setupLiveValidation(form) {
        const fields = form.querySelectorAll('input, select, textarea');

        fields.forEach(field => {
            field.addEventListener('blur', () => {
                this.validateField(field);
            });

            field.addEventListener('input', () => {
                if (field.classList.contains('error')) {
                    this.validateField(field);
                }
            });
        });
    }
};
