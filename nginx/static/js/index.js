// ========== CONFIGURATION ==========
const CONFIG = {
    ML: {
        PRICE: '$0.10',
        MIN_LENGTH: 5,
        MAX_LENGTH: 200,
        PRICE_ICON: '💰',
        LENGTH_ICON: '📏'
    },
    POLLING: {
        INTERVAL: 2000,
        MAX_ATTEMPTS: 60
    },
    TRANSACTIONS: {
        PAGE_SIZE: 5
    },
    PREDICTIONS: {
        PAGE_SIZE: 5
    },
    MESSAGES: {
        LOADING: 'Loading...',
        ANALYZING: 'Analyzing text...',
        NETWORK_ERROR: 'Please check your connection and try again',
        LOADING_TRANSACTIONS: 'Loading transactions...',
        NO_TRANSACTIONS: 'No transactions yet',
        LOADING_PREDICTIONS: 'Loading prediction history...',
        NO_PREDICTIONS: 'No prediction history yet'
    }
};

// ========== STATE ==========
let currentUser = null;
let pollingInterval = null;

// Transactions state
let transactionsVisible = false;
let allTransactions = [];
let transactionsCurrentPage = 1;
let transactionsTotalPages = 1;

// Predictions state
let predictionsVisible = false;
let allPredictions = [];
let predictionsCurrentPage = 1;
let predictionsTotalPages = 1;

// ========== UTILS ==========
const formatCurrency = (amount = 0, currency = 'USD') => {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency,
        minimumFractionDigits: 2
    }).format(amount);
};

const formatDate = (dateString) => {
    const date = new Date(dateString);
    return new Intl.DateTimeFormat('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit'
    }).format(date);
};

const formatTransactionAmount = (amount, type) => {
    const formatted = new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD',
        minimumFractionDigits: 2
    }).format(amount);
    return type === 'deposit' ? `+${formatted}` : `-${formatted}`;
};

const getAvatarLetter = (username) => username ? username[0].toUpperCase() : '?';

const getTransactionIcon = (type) => type === 'deposit' ? '💰' : '💸';
const getTransactionClass = (type) => type === 'deposit' ? 'transaction-deposit' : 'transaction-withdraw';
const getPredictionIcon = () => '✅';

const getEmotionBadges = (emotions) => {
    if (!emotions?.length) return '<span class="badge neutral">none</span>';
    return emotions.map(e => `<span class="badge emotion">${e}</span>`).join('');
};

const escapeHtmlAttr = (s) => {
    const map = { '&': '&amp;', '"': '&quot;', '<': '&lt;', '>': '&gt;' };
    return String(s).replace(/[&"<>]/g, (ch) => map[ch]);
};

// ========== API CALLS ==========
const fetchOpts = { credentials: 'include' };
const api = {
    getCurrentUser: () => fetch('/api/users/current', fetchOpts),
    runMLTask: (inputText) => fetch('/api/ml-tasks/run', {
        ...fetchOpts,
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ input_text: inputText })
    }),
    getTaskStatus: (taskId) => fetch(`/api/ml-tasks/${taskId}`, fetchOpts),
    deposit: (amount) => fetch('/api/transactions/deposit', {
        ...fetchOpts,
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ amount })
    }),
    logout: () => fetch('/api/sign-out', { method: 'POST', ...fetchOpts }),
    getAllTransactions: () => fetch('/api/transactions', fetchOpts),
    getAllPredictions: () => fetch('/api/ml-tasks', fetchOpts)
};

async function fetchSortedList(fetchFn, dateKey = 'created_at') {
    const response = await fetchFn();
    const data = response.ok ? await response.json() : null;
    if (data) data.sort((a, b) => new Date(b[dateKey]) - new Date(a[dateKey]));
    return { data, response };
}

// ========== TEMPLATES ==========
const templates = {
    loading: () => `
        <div class="loading-state">
            <div class="loading-spinner"></div>
            <p>${CONFIG.MESSAGES.LOADING}</p>
        </div>
    `,

    sectionLoading: (message) => `<div class="spinner-sm"></div><span>${message}</span>`,

    error: (message) => templates.sectionError(message, 'retryProfileBtn'),

    sectionError: (message, retryButtonId) => `
        <div class="error-state">
            <p class="text-error">❌ ${message}</p>
            <button type="button" id="${retryButtonId}" class="btn btn-primary btn-sm">Try again</button>
        </div>
    `,

    emptyState: (icon, message) => `
        <div class="empty-state">
            <div class="empty-icon">${icon}</div>
            <p>${message}</p>
        </div>
    `,

    logo: () => `
        <div class="logo">
            <span class="logo-icon">🧠</span>
            <span class="logo-text">feel</span>
            <span class="logo-dot">.ai</span>
        </div>
    `,

    mlCard: (isAuthenticated) => {
        const exampleButtons = templates.exampleButtons();

        return `
            <div class="card-gradient">
                <div class="ml-header">
                    <span class="ml-title">Emotion analysis</span>
                    <div class="badge-group">
                        <span class="badge">${CONFIG.ML.PRICE_ICON} ${CONFIG.ML.PRICE}</span>
                        <span class="badge">${CONFIG.ML.LENGTH_ICON} ${CONFIG.ML.MIN_LENGTH}-${CONFIG.ML.MAX_LENGTH}</span>
                    </div>
                </div>
                <div class="ml-description">Understand the emotions hidden in your text</div>
                <div class="ml-form">
                    <div class="ml-input-group">
                        <textarea id="mlInput" class="ml-input"
                            placeholder="I'm so happy today! This is amazing..." rows="3"></textarea>
                    </div>
                    <div class="ml-actions">
                        ${isAuthenticated
                            ? `<button onclick="handleRunTask()" id="runTaskBtn" class="ml-btn">Analyze</button>`
                            : `<button class="ml-btn" disabled title="Sign in to analyze text">Sign in to analyze</button>`
                        }
                        ${isAuthenticated
                            ? `<button onclick="togglePredictions()" id="togglePredictionsBtn" class="ml-history-btn">
                                ${predictionsVisible ? 'Hide History' : 'History'}
                               </button>`
                            : `<button class="ml-history-btn" disabled title="Sign in to view history">History</button>`
                        }
                    </div>
                </div>
                <div class="ml-examples">${exampleButtons}</div>
                <div id="mlResult"></div>
            </div>
        `;
    },

    exampleButtons: () => {
        const examples = [
            { text: 'This is absolutely wonderful! So excited! 😊', label: '😊 Happy' },
            { text: 'This is so frustrating, I want to give up...', label: '😠 Angry' },
            { text: 'That was such a scary experience!', label: '😨 Scared' },
            { text: 'Just another ordinary day. Nothing special.', label: '😐 Neutral' }
        ];
        return examples.map(ex =>
            `<button type="button" class="example-btn" data-example="${escapeHtmlAttr(ex.text)}">${ex.label}</button>`
        ).join('');
    },

    authButtons: () => `
        <div class="auth-buttons">
            <a href="/sign-in" class="btn btn-outline btn-sm">Sign in</a>
            <a href="/sign-up" class="btn btn-primary btn-sm">Sign up</a>
        </div>
    `,

    userSection: (user) => `
        <div class="user-section">
            <div class="avatar">${getAvatarLetter(user.username)}</div>
            <div class="user-info">
                <span class="user-name">${user.username}</span>
                <span class="user-email">${user.email}</span>
            </div>
            <button onclick="handleLogout()" id="logoutBtn" class="btn btn-outline-danger btn-sm">Logout</button>
        </div>
    `,

    balanceCard: (balance, isAuthenticated, isVisible) => `
        <div class="balance-card">
            <div class="balance-info">
                <div class="balance-details">
                    <span class="balance-label">Current balance</span>
                    <span class="balance-amount">${formatCurrency(balance.amount, balance.currency)}</span>
                </div>
            </div>
            <div class="balance-actions">
                <div class="deposit-group">
                    <input type="number" id="depositAmount" class="deposit-input" placeholder="$" min="1" step="1">
                    <button onclick="handleDeposit()" id="depositBtn" class="btn btn-white">Add</button>
                </div>
                ${isAuthenticated
                    ? `<button onclick="toggleTransactions()" id="toggleTransactionsBtn" class="btn btn-outline">
                        ${isVisible ? 'Hide History' : 'History'}
                       </button>`
                    : `<a href="/sign-in" class="btn btn-outline">History</a>`
                }
            </div>
        </div>
    `,

    topBar: (content) => `
        <div class="top-bar">
            <div class="top-bar-left">${templates.logo()}</div>
            <div class="top-bar-right">${content}</div>
        </div>
    `,

    // ========== TABLES ==========
    transactionsTable: () => {
        if (!allTransactions.length) {
            return templates.emptyState('📭', CONFIG.MESSAGES.NO_TRANSACTIONS);
        }

        const start = (transactionsCurrentPage - 1) * CONFIG.TRANSACTIONS.PAGE_SIZE;
        const pageTransactions = allTransactions.slice(start, start + CONFIG.TRANSACTIONS.PAGE_SIZE);

        let html = `
            <div class="table-container">
                <table class="transaction-table">
                    <thead>
                        <tr>
                            <th></th>
                            <th>Date & Time</th>
                            <th>Transaction ID</th>
                            <th>Type</th>
                            <th class="text-right">Amount</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${pageTransactions.map(t => `
                            <tr>
                                <td class="transaction-icon">${getTransactionIcon(t.transaction_type)}</td>
                                <td class="transaction-date">${formatDate(t.created_at)}</td>
                                <td class="transaction-id" title="${t.id}">${t.id.split('-')[0]}...</td>
                                <td class="transaction-type">
                                    <span class="badge ${t.transaction_type}">${t.transaction_type}</span>
                                </td>
                                <td class="transaction-amount ${getTransactionClass(t.transaction_type)} text-right">
                                    ${formatTransactionAmount(t.amount, t.transaction_type)}
                                </td>
                            </tr>
                        `).join('')}
                    </tbody>
                </table>
            </div>
        `;

        if (transactionsTotalPages > 1) {
            html += templates.pagination('transactions', transactionsCurrentPage, transactionsTotalPages);
        }
        return html;
    },

    predictionsTable: () => {
        if (!allPredictions.length) {
            return templates.emptyState('🤖', CONFIG.MESSAGES.NO_PREDICTIONS);
        }

        const start = (predictionsCurrentPage - 1) * CONFIG.PREDICTIONS.PAGE_SIZE;
        const pagePredictions = allPredictions.slice(start, start + CONFIG.PREDICTIONS.PAGE_SIZE);

        let html = `
            <div class="table-container">
                <table class="prediction-table">
                    <thead>
                        <tr>
                            <th></th>
                            <th>Date & Time</th>
                            <th>Input Text</th>
                            <th>Emotions</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${pagePredictions.map(p => `
                            <tr>
                                <td class="prediction-icon">${getPredictionIcon()}</td>
                                <td class="prediction-date">${formatDate(p.created_at)}</td>
                                <td class="prediction-text" title="${p.input_text}">
                                    ${p.input_text.substring(0, 50)}${p.input_text.length > 50 ? '...' : ''}
                                </td>
                                <td class="prediction-emotions">${getEmotionBadges(p.prediction)}</td>
                            </tr>
                        `).join('')}
                    </tbody>
                </table>
            </div>
        `;

        if (predictionsTotalPages > 1) {
            html += templates.pagination('predictions', predictionsCurrentPage, predictionsTotalPages);
        }
        return html;
    },

    pagination: (type, currentPage, totalPages) => `
        <div class="pagination">
            <button onclick="changePage('${type}', ${currentPage - 1})"
                    ${currentPage === 1 ? 'disabled' : ''}
                    class="pagination-btn">← Previous</button>
            <span class="pagination-info">Page ${currentPage} of ${totalPages}</span>
            <button onclick="changePage('${type}', ${currentPage + 1})"
                    ${currentPage === totalPages ? 'disabled' : ''}
                    class="pagination-btn">Next →</button>
        </div>
    `,

    transactionsLoading: () => `
        <div class="transactions-loading">${templates.sectionLoading(CONFIG.MESSAGES.LOADING_TRANSACTIONS)}</div>
    `,

    predictionsLoading: () => `
        <div class="predictions-loading">${templates.sectionLoading(CONFIG.MESSAGES.LOADING_PREDICTIONS)}</div>
    `,

    transactionsError: () => templates.sectionError('Failed to load transactions', 'retryTransactionsBtn'),

    predictionsError: () => templates.sectionError('Failed to load prediction history', 'retryPredictionsBtn')
};

// ========== RENDERERS ==========
function renderUnauthenticated(container) {
    container.innerHTML = templates.topBar(templates.authButtons()) + templates.mlCard(false);
}

function renderDashboard(container, user) {
    transactionsVisible = false;
    predictionsVisible = false;
    allTransactions = [];
    allPredictions = [];
    transactionsCurrentPage = predictionsCurrentPage = 1;
    transactionsTotalPages = predictionsTotalPages = 1;

    container.innerHTML =
        templates.topBar(templates.userSection(user)) +
        templates.mlCard(true) +
        `<div id="predictionsContainer" class="hidden"></div>` +
        templates.balanceCard(user.balance || { amount: 0, currency: 'USD' }, true, false) +
        `<div id="transactionsContainer" class="hidden"></div>`;
}

// ========== USER PROFILE ==========
async function loadUserProfile() {
    const content = document.getElementById('dashboard-content');
    content.innerHTML = templates.loading();

    try {
        const response = await api.getCurrentUser();
        if (response.ok) {
            currentUser = await response.json();
            renderDashboard(content, currentUser);
        } else if (response.status === 401) {
            currentUser = null;
            renderUnauthenticated(content);
        } else {
            throw new Error('Failed to load profile');
        }
    } catch (error) {
        console.error('Error:', error);
        content.innerHTML = templates.error('Something went wrong');
        const retryBtn = content.querySelector('#retryProfileBtn');
        if (retryBtn) retryBtn.addEventListener('click', loadUserProfile);
    }
}

// ========== TOGGLE SECTION HELPER ==========
function createToggle(getVisible, setVisible, btnId, containerId, loadingTemplate, loadFn) {
    return async function () {
        const btn = document.getElementById(btnId);
        const container = document.getElementById(containerId);
        if (!container) return;
        setVisible(!getVisible());
        btn.innerText = getVisible() ? 'Hide History' : 'History';
        container.style.display = getVisible() ? 'block' : 'none';
        if (getVisible()) {
            container.innerHTML = loadingTemplate();
            await loadFn();
        } else {
            container.innerHTML = '';
        }
    };
}

const toggleTransactions = createToggle(
    () => transactionsVisible,
    (v) => { transactionsVisible = v; },
    'toggleTransactionsBtn',
    'transactionsContainer',
    templates.transactionsLoading,
    loadTransactions
);

const togglePredictions = createToggle(
    () => predictionsVisible,
    (v) => { predictionsVisible = v; },
    'togglePredictionsBtn',
    'predictionsContainer',
    templates.predictionsLoading,
    loadPredictions
);

async function loadTransactions() {
    try {
        const { data, response } = await fetchSortedList(api.getAllTransactions);
        if (!response.ok) {
            if (response.status === 401) window.location.href = '/sign-in';
            return;
        }
        allTransactions = data;
        transactionsTotalPages = Math.ceil(allTransactions.length / CONFIG.TRANSACTIONS.PAGE_SIZE);
        transactionsCurrentPage = 1;
        const container = document.getElementById('transactionsContainer');
        if (container) container.innerHTML = templates.transactionsTable();
    } catch (error) {
        console.error('Error loading transactions:', error);
        const container = document.getElementById('transactionsContainer');
        if (container) {
            container.innerHTML = templates.transactionsError();
            container.querySelector('#retryTransactionsBtn')?.addEventListener('click', loadTransactions);
        }
    }
}

async function loadPredictions() {
    try {
        const { data, response } = await fetchSortedList(api.getAllPredictions);
        if (!response.ok) {
            if (response.status === 401) window.location.href = '/sign-in';
            return;
        }
        allPredictions = data;
        predictionsTotalPages = Math.ceil(allPredictions.length / CONFIG.PREDICTIONS.PAGE_SIZE);
        predictionsCurrentPage = 1;
        const container = document.getElementById('predictionsContainer');
        if (container) container.innerHTML = templates.predictionsTable();
    } catch (error) {
        console.error('Error loading predictions:', error);
        const container = document.getElementById('predictionsContainer');
        if (container) {
            container.innerHTML = templates.predictionsError();
            container.querySelector('#retryPredictionsBtn')?.addEventListener('click', loadPredictions);
        }
    }
}

// ========== PAGINATION ==========
function changePage(type, page) {
    if (type === 'transactions') {
        if (page < 1 || page > transactionsTotalPages) return;
        transactionsCurrentPage = page;
        const container = document.getElementById('transactionsContainer');
        if (container) container.innerHTML = templates.transactionsTable();
    } else {
        if (page < 1 || page > predictionsTotalPages) return;
        predictionsCurrentPage = page;
        const container = document.getElementById('predictionsContainer');
        if (container) container.innerHTML = templates.predictionsTable();
    }
}

async function refreshTransactions() {
    if (!transactionsVisible) return;
    try {
        const { data, response } = await fetchSortedList(api.getAllTransactions);
        if (!response?.ok || !data) return;
        allTransactions = data;
        transactionsTotalPages = Math.ceil(allTransactions.length / CONFIG.TRANSACTIONS.PAGE_SIZE);
        if (transactionsCurrentPage > transactionsTotalPages) {
            transactionsCurrentPage = transactionsTotalPages || 1;
        }
        const container = document.getElementById('transactionsContainer');
        if (container) container.innerHTML = templates.transactionsTable();
    } catch (error) {
        console.error('Error refreshing transactions:', error);
    }
}

async function refreshPredictions() {
    if (!predictionsVisible) return;
    try {
        const { data, response } = await fetchSortedList(api.getAllPredictions);
        if (!response?.ok || !data) return;
        allPredictions = data;
        predictionsTotalPages = Math.ceil(allPredictions.length / CONFIG.PREDICTIONS.PAGE_SIZE);
        if (predictionsCurrentPage > predictionsTotalPages) {
            predictionsCurrentPage = predictionsTotalPages || 1;
        }
        const container = document.getElementById('predictionsContainer');
        if (container) container.innerHTML = templates.predictionsTable();
    } catch (error) {
        console.error('Error refreshing predictions:', error);
    }
}

// ========== ML TASKS ==========
function validateInput(text) {
    if (!text || text.trim().length < CONFIG.ML.MIN_LENGTH) {
        return {
            valid: false,
            icon: '📏',
            title: 'Text is too short',
            message: `Minimum ${CONFIG.ML.MIN_LENGTH} characters required`
        };
    }
    if (text.length > CONFIG.ML.MAX_LENGTH) {
        return {
            valid: false,
            icon: '📏',
            title: 'Text is too long',
            message: `Maximum ${CONFIG.ML.MAX_LENGTH} characters allowed`
        };
    }
    return { valid: true };
}

async function handleRunTask() {
    const input = document.getElementById('mlInput');
    const runBtn = document.getElementById('runTaskBtn');
    const mlCard = document.querySelector('.card-gradient');

    const validation = validateInput(input.value);
    if (!validation.valid) {
        showError(validation.icon, validation.title, validation.message);
        return;
    }

    try {
        runBtn.disabled = true;
        runBtn.innerText = '...';
        clearPreviousResults();

        const processingIndicator = document.createElement('div');
        processingIndicator.className = 'processing-indicator';
        processingIndicator.id = 'processingIndicator';
        processingIndicator.innerHTML = `
            <div class="spinner-sm"></div>
            <span class="processing-text">${CONFIG.MESSAGES.ANALYZING}</span>
        `;
        mlCard.appendChild(processingIndicator);

        const response = await api.runMLTask(input.value.trim());
        const result = await response.json();

        if (response.ok) {
            startPolling(result.id);
        } else {
            handleTaskError(response, result, runBtn);
        }
    } catch (error) {
        console.error('Task error:', error);
        handleNetworkError(runBtn);
    }
}

function handleTaskError(response, result, runBtn) {
    removeProcessingIndicator();

    if (response.status === 401) {
        showError('🔐', 'Authentication required', 'Please sign in to analyze text');
    } else if (Array.isArray(result.detail)) {
        const error = result.detail[0];
        const errorConfig = {
            string_too_short: {
                icon: '📏',
                title: 'Text is too short',
                message: `Minimum ${error.ctx?.min_length || CONFIG.ML.MIN_LENGTH} characters required`
            },
            string_too_long: {
                icon: '📏',
                title: 'Text is too long',
                message: `Maximum ${error.ctx?.max_length || CONFIG.ML.MAX_LENGTH} characters allowed`
            },
            value_error: {
                icon: '⚠️',
                title: 'Invalid input',
                message: error.msg || 'Please check your text'
            }
        };
        const err = errorConfig[error.type];
        if (err) showError(err.icon, err.title, err.message);
        else showError('⚠️', 'Validation error', error.msg || 'Please check your input');
    } else if (result.detail?.toLowerCase().includes('insufficient') ||
               result.detail?.toLowerCase().includes('balance') ||
               response.status === 402) {
        showError('💸', 'Insufficient balance', `${CONFIG.ML.PRICE} required per analysis`);
    } else {
        showError('⚠️', 'Analysis failed', result.detail || 'Please try again later');
    }

    resetButton(runBtn, 'Analyze');
}

function handleNetworkError(runBtn) {
    removeProcessingIndicator();
    showError('⚠️', 'Network error', CONFIG.MESSAGES.NETWORK_ERROR);
    resetButton(runBtn, 'Analyze');
}

function resetButton(btn, text) {
    if (btn) {
        btn.disabled = false;
        btn.innerText = text;
    }
}

function showError(icon, title, message) {
    const mlCard = document.querySelector('.card-gradient');
    if (!mlCard) return;

    clearPreviousResults();
    const errorContainer = document.createElement('div');
    errorContainer.id = 'mlResult';
    errorContainer.className = 'error-container';
    errorContainer.innerHTML = `
        <div class="flex items-center gap-3">
            <span class="ml-error-icon">${icon}</span>
            <div>
                <div class="ml-error-title">${title}</div>
                <div class="ml-error-message">${message}</div>
            </div>
        </div>
    `;
    mlCard.appendChild(errorContainer);
}

function clearPreviousResults() {
    document.getElementById('mlResult')?.remove();
    removeProcessingIndicator();
}

function removeProcessingIndicator() {
    document.getElementById('processingIndicator')?.remove();
}

// ========== POLLING ==========
function startPolling(taskId) {
    stopPolling();
    let attempts = 0;

    pollingInterval = setInterval(async () => {
        attempts++;
        try {
            const response = await api.getTaskStatus(taskId);
            if (response.ok) {
                const task = await response.json();
                if (task.task_status === 'completed') {
                    handleTaskComplete(task);
                } else if (task.task_status === 'failed') {
                    handleTaskFailed();
                }
            }
            if (attempts >= CONFIG.POLLING.MAX_ATTEMPTS) handlePollingTimeout();
        } catch (error) {
            console.error('Polling error:', error);
            if (attempts >= CONFIG.POLLING.MAX_ATTEMPTS) handlePollingTimeout();
        }
    }, CONFIG.POLLING.INTERVAL);
}

function stopPolling() {
    if (pollingInterval) {
        clearInterval(pollingInterval);
        pollingInterval = null;
    }
}

function handleTaskComplete(task) {
    removeProcessingIndicator();
    renderTaskResult(task);
    if (currentUser) {
        refreshBalance();
        refreshTransactions();
        refreshPredictions();
    }
    stopPolling();
    resetButton(document.getElementById('runTaskBtn'), 'Analyze');
}

function handleTaskFailed() {
    removeProcessingIndicator();
    stopPolling();
    resetButton(document.getElementById('runTaskBtn'), 'Analyze');
}

function handlePollingTimeout() {
    removeProcessingIndicator();
    stopPolling();
    resetButton(document.getElementById('runTaskBtn'), 'Analyze');
}

function renderTaskResult(task) {
    const mlCard = document.querySelector('.card-gradient');
    if (!mlCard) return;

    clearPreviousResults();
    const resultContainer = document.createElement('div');
    resultContainer.id = 'mlResult';
    resultContainer.className = 'result-container';

    if (task.prediction?.length > 0) {
        resultContainer.innerHTML = `
            <div class="flex items-center gap-2 mb-3">
                <span class="ml-result-icon">🎯</span>
                <span class="ml-result-title">Detected emotions</span>
            </div>
            <div class="emotions-list">
                ${task.prediction.map(emotion => `<span class="emotion-tag">${emotion}</span>`).join('')}
            </div>
        `;
    } else {
        resultContainer.innerHTML = `
            <div class="flex items-center gap-2">
                <span class="ml-result-icon">😐</span>
                <span class="ml-result-title">No strong emotions detected</span>
            </div>
        `;
    }
    mlCard.appendChild(resultContainer);
}

function setExampleText(example) {
    const input = document.getElementById('mlInput');
    if (input) input.value = example;
}

// ========== BALANCE ==========
async function handleDeposit() {
    if (!currentUser) {
        window.location.href = '/sign-in';
        return;
    }

    const amountInput = document.getElementById('depositAmount');
    const depositBtn = document.getElementById('depositBtn');
    const amount = parseFloat(amountInput?.value);
    if (!amount || amount <= 0) return;

    try {
        depositBtn.disabled = true;
        depositBtn.innerText = '...';
        const response = await api.deposit(amount);
        if (response.ok) {
            amountInput.value = '';
            await refreshBalance();
            await refreshTransactions();
        }
    } catch (error) {
        console.error('Deposit error:', error);
    } finally {
        depositBtn.disabled = false;
        depositBtn.innerText = 'Add';
    }
}

async function refreshBalance() {
    if (!currentUser) return;
    try {
        const response = await api.getCurrentUser();
        if (response.ok) {
            const user = await response.json();
            currentUser = user;

            const balanceAmountEl = document.querySelector('.balance-amount');
            if (balanceAmountEl) {
                balanceAmountEl.innerText = formatCurrency(user.balance?.amount, user.balance?.currency);
            }

            const userNameEl = document.querySelector('.user-name');
            if (userNameEl) {
                userNameEl.innerText = user.username;
            }

            const userEmailEl = document.querySelector('.user-email');
            if (userEmailEl) {
                userEmailEl.innerText = user.email;
            }

            const avatarEl = document.querySelector('.avatar');
            if (avatarEl) {
                avatarEl.innerText = getAvatarLetter(user.username);
            }
        }
    } catch (error) {
        console.error('Refresh balance error:', error);
    }
}

// ========== LOGOUT ==========
async function handleLogout() {
    const logoutBtn = document.getElementById('logoutBtn');
    const originalText = logoutBtn.innerText;

    try {
        logoutBtn.disabled = true;
        logoutBtn.innerText = '...';
        const response = await api.logout();
        if (response.ok) {
            currentUser = null;
            setTimeout(() => window.location.href = '/', 500);
        }
    } catch (error) {
        console.error('Logout error:', error);
        logoutBtn.disabled = false;
        logoutBtn.innerText = originalText;
    }
}

// ========== INIT ==========
document.addEventListener('DOMContentLoaded', () => {
    loadUserProfile();
    document.body.addEventListener('click', (e) => {
        const btn = e.target.closest('.example-btn');
        if (btn && btn.dataset.example !== undefined) {
            setExampleText(btn.dataset.example);
        }
    });
});