document.addEventListener('DOMContentLoaded', function() {
    console.log('✅ Sign-in page loaded');

    const form = document.getElementById('signInForm');
    const submitBtn = document.getElementById('submitBtn');

    if (form) {
        form.addEventListener('submit', async function(e) {
            e.preventDefault();

            const login = document.getElementById('email_or_username').value.trim();
            const password = document.getElementById('plain_password').value;

            if (!login || !password) {
                showMessage('❌ Please fill in all fields', 'error');
                return;
            }

            try {
                submitBtn.disabled = true;
                submitBtn.innerText = 'Signing in...';

                const response = await fetch('/api/sign-in', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        email_or_username: login,
                        plain_password: password
                    })
                });

                const result = await response.json();

                if (response.ok) {
                    showMessage('✅ Signed in successfully', 'success');
                    setTimeout(() => {
                        window.location.href = '/';
                    }, 1000);
                } else {
                    if (Array.isArray(result.detail)) {
                        const firstError = result.detail[0];
                        showMessage('❌ ' + (firstError.msg || 'Authentication failed'), 'error');
                    }
                    else if (result.detail && typeof result.detail === 'string') {
                        let errorMsg = result.detail;
                        if (errorMsg.toLowerCase().includes('invalid')) {
                            errorMsg = 'Invalid email/username or password';
                        }
                        showMessage('❌ ' + errorMsg, 'error');
                    }
                    else {
                        showMessage('❌ Authentication failed', 'error');
                    }
                }
            } catch (error) {
                console.error('Error:', error);
                showMessage('❌ Network error', 'error');
            } finally {
                submitBtn.disabled = false;
                submitBtn.innerText = 'Sign in';
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