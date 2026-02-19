document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('signInForm');
    const submitBtn = document.getElementById('submitBtn');

    if (form) {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            const login = document.getElementById('email_or_username').value.trim();
            const password = document.getElementById('plain_password').value;
            if (!login || !password) {
                showAuthMessage('❌ Please fill in all fields', 'error');
                return;
            }
            submitAuthForm({
                url: '/api/sign-in',
                body: { email_or_username: login, plain_password: password },
                submitBtn,
                loadingText: 'Signing in...',
                doneText: 'Sign in',
                successMessage: '✅ Signed in successfully',
                redirectUrl: '/',
                redirectDelay: 1000
            });
        });
    }
});