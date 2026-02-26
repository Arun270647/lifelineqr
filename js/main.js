// LifeLine QR - Main Application Logic

// Initialize app when DOM is loaded
document.addEventListener('DOMContentLoaded', function () {
    initializeApp();
});

function initializeApp() {
    // Update navigation based on auth status
    updateNavigation();

    // Setup modal close handlers
    setupModals();

    // Check for user greeting
    displayUserGreeting();
}

// Update navigation based on authentication
function updateNavigation() {
    const user = Auth.getCurrentUser();
    const authLinks = document.querySelectorAll('.auth-link');
    const userInfo = document.getElementById('userInfo');

    if (user) {
        // Hide login/signup links
        authLinks.forEach(link => {
            if (link.textContent.includes('Login') || link.textContent.includes('Sign Up')) {
                link.style.display = 'none';
            }
        });

        // Show user info if element exists
        if (userInfo) {
            userInfo.innerHTML = `
                <span>Welcome, ${user.name}</span>
                <button class="btn btn-sm btn-secondary" onclick="handleLogout()">Logout</button>
            `;
        }
    }
}

// Handle logout
function handleLogout() {
    if (confirm('Are you sure you want to logout?')) {
        Auth.logout();
        window.location.href = '../index.html';
    }
}

// Display user greeting
function displayUserGreeting() {
    const user = Auth.getCurrentUser();
    if (user) {
        const greetingElement = document.getElementById('userGreeting');
        if (greetingElement) {
            greetingElement.textContent = `Welcome back, ${user.name}!`;
        }
    }
}

// Setup modal handlers
function setupModals() {
    const modal = document.getElementById('modal');
    if (!modal) return;

    const closeBtn = modal.querySelector('.modal-close');
    if (closeBtn) {
        closeBtn.addEventListener('click', Utils.closeModal);
    }

    // Close on outside click
    modal.addEventListener('click', function (e) {
        if (e.target === modal) {
            Utils.closeModal();
        }
    });
}

// Format student info for display
function formatStudentInfo(student) {
    return `
        <div class="info-grid">
            <div class="info-item">
                <div class="info-label">Name:</div>
                <div class="info-value">${student.name}</div>
            </div>
            <div class="info-item">
                <div class="info-label">Age:</div>
                <div class="info-value">${student.age} years</div>
            </div>
            <div class="info-item">
                <div class="info-label">Blood Group:</div>
                <div class="info-value"><span class="badge badge-danger">${student.bloodGroup}</span></div>
            </div>
            <div class="info-item">
                <div class="info-label">Allergies:</div>
                <div class="info-value">${student.allergies || 'None'}</div>
            </div>
            <div class="info-item">
                <div class="info-label">Medical Conditions:</div>
                <div class="info-value">${student.medicalConditions || 'None'}</div>
            </div>
            <div class="info-item">
                <div class="info-label">Regular Medications:</div>
                <div class="info-value">${student.regularMedications || 'None'}</div>
            </div>
            <div class="info-item">
                <div class="info-label">Emergency Contacts:</div>
                <div class="info-value">${student.emergencyContacts || 'Not provided'}</div>
            </div>
            <div class="info-item">
                <div class="info-label">Address:</div>
                <div class="info-value">${student.address || 'Not provided'}</div>
            </div>
        </div>
    `;
}

// Format emergency info (limited)
function formatEmergencyInfo(student) {
    return `
        <div class="alert alert-warning">
            <strong>Emergency Information Only</strong><br>
            Login as a doctor to view full medical profile
        </div>
        <div class="info-grid">
            <div class="info-item">
                <div class="info-label">Name:</div>
                <div class="info-value">${student.name}</div>
            </div>
            <div class="info-item">
                <div class="info-label">Age:</div>
                <div class="info-value">${student.age} years</div>
            </div>
            <div class="info-item">
                <div class="info-label">Blood Group:</div>
                <div class="info-value"><span class="badge badge-danger">${student.bloodGroup}</span></div>
            </div>
            <div class="info-item">
                <div class="info-label">Allergies:</div>
                <div class="info-value">${student.allergies || 'None'}</div>
            </div>
            <div class="info-item">
                <div class="info-label">Emergency Contacts:</div>
                <div class="info-value">${student.emergencyContacts || 'Not provided'}</div>
            </div>
        </div>
    `;
}

// Export functions for global access
window.handleLogout = handleLogout;
window.formatStudentInfo = formatStudentInfo;
window.formatEmergencyInfo = formatEmergencyInfo;
