document.addEventListener('DOMContentLoaded', function() {
    console.log('✅ Sign-up page loaded');

    const form = document.getElementById('signUpForm');
    const submitBtn = document.getElementById('submitBtn');
    const passwordInput = document.getElementById('plain_password');
    const confirmInput = document.getElementById('confirm_password');

    // Простая валидация совпадения паролей
    function checkPasswordMatch() {
        const password = passwordInput.value;
        const confirm = confirmInput.value;

        if (confirm.length === 0) return;

        if (password === confirm) {
            confirmInput.style.borderColor = '#28a745';
        } else {
            confirmInput.style.borderColor = '#dc3545';
        }
    }

    passwordInput.addEventListener('input', checkPasswordMatch);
    confirmInput.addEventListener('input', checkPasswordMatch);

    if (form) {
        form.addEventListener('submit', async function(e) {
            e.preventDefault();

            const email = document.getElementById('email').value.trim();
            const username = document.getElementById('username').value.trim();
            const password = passwordInput.value;
            const confirm = confirmInput.value;

            if (!email || !username || !password || !confirm) {
                showMessage('❌ Please fill in all fields', 'error');
                return;
            }

            if (password.length < 8) {
                showMessage('❌ Password must be at least 8 characters', 'error');
                return;
            }

            if (password !== confirm) {
                showMessage('❌ Passwords do not match', 'error');
                return;
            }

            try {
                submitBtn.disabled = true;
                submitBtn.innerText = 'Creating account...';

                const response = await fetch('/api/sign-up', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        email: email,
                        username: username,
                        plain_password: password
                    })
                });

                const result = await response.json();

                if (response.ok) {
                    showMessage('✅ Account successfully created', 'success');
                    setTimeout(() => {
                        window.location.href = '/';
                    }, 2000);
                } else {
                    if (Array.isArray(result.detail)) {
                        const error = result.detail[0];
                        showMessage('❌ ' + (error.msg || 'Registration failed'), 'error');
                    }
                    else if (result.detail && typeof result.detail === 'string') {
                        showMessage('❌ ' + result.detail, 'error');
                    }
                    else {
                        showMessage('❌ Registration failed', 'error');
                    }
                }
            } catch (error) {
                console.error('Error:', error);
                showMessage('❌ Network error', 'error');
            } finally {
                submitBtn.disabled = false;
                submitBtn.innerText = 'Create account';
            }
        });
    }
});

function showMessage(text, type = 'info') {
    const result = document.getElementById('result');
    if (result) {
        const messageClass = {
            'success': 'message-success',
            'error': 'message-error',
            'info': 'message-info'
        }[type] || 'message-info';

        result.innerHTML = `<p class="${messageClass}">${text}</p>`;

        setTimeout(() => {
            if (result.innerHTML.includes(text)) {
                result.innerHTML = '';
            }
        }, 5000);
    }
}