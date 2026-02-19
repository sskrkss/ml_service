/**
 * Shared utilities for sign-in and sign-up pages.
 */
const authFetchOpts = { credentials: 'include', headers: { 'Content-Type': 'application/json' } };

function authApiPost(url, body) {
    return fetch(url, {
        ...authFetchOpts,
        method: 'POST',
        body: JSON.stringify(body)
    });
}

function showAuthMessage(text, type) {
    const result = document.getElementById('result');
    if (!result) return;
    const messageClass = {
        success: 'message-success',
        error: 'message-error',
        info: 'message-info'
    }[type] || 'message-info';
    result.innerHTML = `<p class="${messageClass}">${text}</p>`;
    setTimeout(() => {
        if (result.innerHTML.includes(text)) result.innerHTML = '';
    }, 5000);
}

function parseAuthError(result) {
    if (Array.isArray(result.detail)) {
        const first = result.detail[0];
        return first?.msg || 'Request failed';
    }
    if (result.detail && typeof result.detail === 'string') {
        return result.detail.toLowerCase().includes('invalid') ? 'Invalid email/username or password' : result.detail;
    }
    return 'Request failed';
}

async function submitAuthForm(options) {
    const {
        url,
        body,
        submitBtn,
        loadingText,
        doneText,
        successMessage,
        redirectUrl,
        redirectDelay = 1000,
        getErrorMsg = parseAuthError
    } = options;
    if (!submitBtn) return;
    submitBtn.disabled = true;
    submitBtn.innerText = loadingText;
    try {
        const response = await authApiPost(url, body);
        const result = await response.json();
        if (response.ok) {
            showAuthMessage(successMessage, 'success');
            if (redirectUrl) setTimeout(() => { window.location.href = redirectUrl; }, redirectDelay);
        } else {
            showAuthMessage('❌ ' + getErrorMsg(result), 'error');
        }
    } catch (error) {
        console.error('Error:', error);
        showAuthMessage('❌ Network error', 'error');
    } finally {
        submitBtn.disabled = false;
        submitBtn.innerText = doneText;
    }
}
