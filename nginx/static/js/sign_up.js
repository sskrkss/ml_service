document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('signUpForm');
    const submitBtn = document.getElementById('submitBtn');
    const passwordInput = document.getElementById('plain_password');
    const confirmInput = document.getElementById('confirm_password');

    function checkPasswordMatch() {
        confirmInput.classList.remove('password-match', 'password-mismatch');
        if (confirmInput.value.length === 0) return;
        if (passwordInput.value === confirmInput.value) {
            confirmInput.classList.add('password-match');
        } else {
            confirmInput.classList.add('password-mismatch');
        }
    }

    passwordInput.addEventListener('input', checkPasswordMatch);
    confirmInput.addEventListener('input', checkPasswordMatch);

    if (form) {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            const email = document.getElementById('email').value.trim();
            const username = document.getElementById('username').value.trim();
            const password = passwordInput.value;
            const confirm = confirmInput.value;

            if (!email || !username || !password || !confirm) {
                showAuthMessage('❌ Please fill in all fields', 'error');
                return;
            }
            if (password.length < 8) {
                showAuthMessage('❌ Password must be at least 8 characters', 'error');
                return;
            }
            if (password !== confirm) {
                showAuthMessage('❌ Passwords do not match', 'error');
                return;
            }

            submitAuthForm({
                url: '/api/sign-up',
                body: { email, username, plain_password: password },
                submitBtn,
                loadingText: 'Creating account...',
                doneText: 'Create account',
                successMessage: '✅ Account successfully created',
                redirectUrl: '/',
                redirectDelay: 2000,
                getErrorMsg: (result) => {
                    if (Array.isArray(result.detail)) return result.detail[0]?.msg || 'Registration failed';
                    if (typeof result.detail === 'string') return result.detail;
                    return 'Registration failed';
                }
            });
        });
    }
});