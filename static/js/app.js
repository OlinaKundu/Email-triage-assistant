// ===== State Management =====
let currentResults = null;
let isDarkMode = localStorage.getItem('darkMode') === 'true';

// ===== DOM Elements =====
const elements = {
    emailInput: document.getElementById('emailInput'),
    sampleSelect: document.getElementById('sampleSelect'),
    clearBtn: document.getElementById('clearBtn'),
    processBtn: document.getElementById('processBtn'),
    darkModeToggle: document.getElementById('darkModeToggle'),
    loadingState: document.getElementById('loadingState'),
    resultsSection: document.getElementById('resultsSection'),
    errorDisplay: document.getElementById('errorDisplay'),
    errorMessage: document.getElementById('errorMessage'),
    normalView: document.getElementById('normalView'),
    focusView: document.getElementById('focusView'),
    normalViewBtn: document.getElementById('normalViewBtn'),
    focusViewBtn: document.getElementById('focusViewBtn'),
    copyFocusBtn: document.getElementById('copyFocusBtn'),
};

// ===== Initialization =====
document.addEventListener('DOMContentLoaded', () => {
    initializeDarkMode();
    attachEventListeners();
    console.log('🚀 Email Triage Assistant initialized');
});

function initializeDarkMode() {
    if (isDarkMode) {
        document.documentElement.setAttribute('data-theme', 'dark');
        elements.darkModeToggle.querySelector('.icon').textContent = '☀️';
    }
}

function attachEventListeners() {
    elements.processBtn.addEventListener('click', processEmail);
    elements.clearBtn.addEventListener('click', clearInput);
    elements.darkModeToggle.addEventListener('click', toggleDarkMode);
    elements.sampleSelect.addEventListener('change', loadSample);
    elements.normalViewBtn.addEventListener('click', () => switchView('normal'));
    elements.focusViewBtn.addEventListener('click', () => switchView('focus'));
    elements.copyFocusBtn.addEventListener('click', copyFocusMode);
    
    // Allow Enter key to process (with Ctrl/Cmd)
    elements.emailInput.addEventListener('keydown', (e) => {
        if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
            processEmail();
        }
    });
}

// ===== Dark Mode =====
function toggleDarkMode() {
    isDarkMode = !isDarkMode;
    localStorage.setItem('darkMode', isDarkMode);
    
    if (isDarkMode) {
        document.documentElement.setAttribute('data-theme', 'dark');
        elements.darkModeToggle.querySelector('.icon').textContent = '☀️';
    } else {
        document.documentElement.removeAttribute('data-theme');
        elements.darkModeToggle.querySelector('.icon').textContent = '🌙';
    }
}

// ===== Sample Loading =====
async function loadSample() {
    const sampleKey = elements.sampleSelect.value;
    if (!sampleKey) return;
    
    try {
        const response = await fetch(`/api/sample/${sampleKey}`);
        const data = await response.json();
        
        if (data.success) {
            elements.emailInput.value = data.sample;
            elements.sampleSelect.value = '';
        }
    } catch (error) {
        console.error('Error loading sample:', error);
    }
}

// ===== Input Management =====
function clearInput() {
    elements.emailInput.value = '';
    hideResults();
    hideError();
}

// ===== Email Processing =====
async function processEmail() {
    const emailText = elements.emailInput.value.trim();
    
    if (!emailText) {
        showError('Please enter an email to analyze');
        return;
    }
    
    hideError();
    hideResults();
    showLoading();
    
    try {
        const response = await fetch('/api/process', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ email_text: emailText }),
        });
        
        const data = await response.json();
        
        if (data.success) {
            currentResults = data.data;
            displayResults(data.data);
        } else {
            showError(data.error || 'Failed to process email');
        }
    } catch (error) {
        console.error('Processing error:', error);
        showError('Network error. Please check your connection and try again.');
    } finally {
        hideLoading();
    }
}

// ===== Display Results =====
function displayResults(data) {
    // Priority Badge
    displayPriorityBadge(data.priority);
    
    // Summary
    displaySummary(data.summary);
    
    // Action Items
    displayActionItems(data.action_items);
    
    // Metadata
    displayMetadata(data.metadata);
    
    // Priority Breakdown
    displayPriorityBreakdown(data.priority);
    
    // Focus Mode
    displayFocusMode(data.focus_mode_text);
    
    // Show results
    showResults();
}

function displayPriorityBadge(priority) {
    if (!priority) return;
    
    const badge = elements.resultsSection.querySelector('#priorityBadge');
    const emoji = {
        'critical': '🔴',
        'high': '🟠',
        'medium': '🔵',
        'low': '⚪'
    }[priority.level] || '⚪';
    
    badge.textContent = `${emoji} ${priority.level.toUpperCase()} PRIORITY (${priority.score}/100)`;
    badge.style.background = priority.color;
    badge.style.color = 'white';
}

function displaySummary(summary) {
    const summaryText = document.getElementById('summaryText');
    const keyPoints = document.getElementById('keyPoints');
    const toneBadge = document.getElementById('toneBadge');
    
    summaryText.textContent = summary.summary || 'No summary available';
    toneBadge.textContent = `Tone: ${summary.tone}`;
    
    if (summary.key_points && summary.key_points.length > 0) {
        keyPoints.innerHTML = `
            <h4>Key Points:</h4>
            <ul>
                ${summary.key_points.map(point => `<li>${escapeHtml(point)}</li>`).join('')}
            </ul>
        `;
    } else {
        keyPoints.innerHTML = '';
    }
}

function displayActionItems(actionItems) {
    const actionItemsList = document.getElementById('actionItemsList');
    const actionCount = document.getElementById('actionCount');
    const actionItemsCard = document.getElementById('actionItemsCard');
    
    if (!actionItems || actionItems.length === 0) {
        actionItemsCard.classList.add('hidden');
        return;
    }
    
    actionItemsCard.classList.remove('hidden');
    actionCount.textContent = actionItems.length;
    
    actionItemsList.innerHTML = actionItems.map((item, index) => {
        const confidenceColor = {
            'high': '#10b981',
            'medium': '#f59e0b',
            'low': '#6b7280'
        }[item.confidence] || '#6b7280';
        
        return `
            <div class="action-item" style="border-left-color: ${confidenceColor}">
                <div class="action-item-text">${escapeHtml(item.text)}</div>
                <div class="action-item-meta">
                    ${item.assignee !== 'unspecified' ? `<span>👤 ${escapeHtml(item.assignee)}</span>` : ''}
                    ${item.deadline !== 'none' ? `<span>📅 ${escapeHtml(item.deadline)}</span>` : ''}
                    <span style="color: ${confidenceColor}">● ${item.confidence} confidence</span>
                </div>
            </div>
        `;
    }).join('');
}

function displayMetadata(metadata) {
    const metadataContent = document.getElementById('metadataContent');
    
    const items = [];
    
    if (metadata.subject) {
        items.push({ label: 'Subject', value: metadata.subject });
    }
    if (metadata.from) {
        items.push({ label: 'From', value: metadata.from });
    }
    if (metadata.to && metadata.to.length > 0) {
        items.push({ label: 'To', value: metadata.to.join(', ') });
    }
    if (metadata.date) {
        items.push({ label: 'Date', value: metadata.date });
    }
    
    if (items.length === 0) {
        items.push({ label: 'Info', value: 'No metadata extracted' });
    }
    
    metadataContent.innerHTML = items.map(item => `
        <div class="metadata-item">
            <div class="metadata-label">${item.label}</div>
            <div class="metadata-value">${escapeHtml(item.value)}</div>
        </div>
    `).join('');
}

function displayPriorityBreakdown(priority) {
    if (!priority || !priority.breakdown) return;
    
    const breakdown = document.getElementById('priorityBreakdown');
    const metrics = priority.breakdown;
    
    breakdown.innerHTML = Object.entries(metrics).map(([key, value]) => `
        <div class="priority-metric">
            <span class="priority-metric-label">${key.replace('_', ' ')}</span>
            <div class="priority-metric-bar">
                <div class="priority-metric-fill" style="width: ${value}%"></div>
            </div>
            <span class="priority-metric-value">${Math.round(value)}</span>
        </div>
    `).join('');
}

function displayFocusMode(focusText) {
    const focusModeContent = document.getElementById('focusModeContent');
    focusModeContent.textContent = focusText || 'No focus mode content available';
}

// ===== View Switching =====
function switchView(view) {
    if (view === 'normal') {
        elements.normalView.classList.remove('hidden');
        elements.focusView.classList.add('hidden');
        elements.normalViewBtn.classList.add('active');
        elements.focusViewBtn.classList.remove('active');
    } else {
        elements.normalView.classList.add('hidden');
        elements.focusView.classList.remove('hidden');
        elements.normalViewBtn.classList.remove('active');
        elements.focusViewBtn.classList.add('active');
    }
}

// ===== Copy to Clipboard =====
async function copyFocusMode() {
    const focusText = document.getElementById('focusModeContent').textContent;
    
    try {
        await navigator.clipboard.writeText(focusText);
        
        // Visual feedback
        const originalText = elements.copyFocusBtn.innerHTML;
        elements.copyFocusBtn.innerHTML = '<span class="icon">✓</span> Copied!';
        elements.copyFocusBtn.style.background = 'var(--success)';
        elements.copyFocusBtn.style.color = 'white';
        
        setTimeout(() => {
            elements.copyFocusBtn.innerHTML = originalText;
            elements.copyFocusBtn.style.background = '';
            elements.copyFocusBtn.style.color = '';
        }, 2000);
    } catch (error) {
        console.error('Copy failed:', error);
        showError('Failed to copy to clipboard');
    }
}

// ===== UI State Management =====
function showLoading() {
    elements.loadingState.classList.remove('hidden');
}

function hideLoading() {
    elements.loadingState.classList.add('hidden');
}

function showResults() {
    elements.resultsSection.classList.remove('hidden');
    switchView('normal');
    
    // Smooth scroll to results
    setTimeout(() => {
        elements.resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }, 100);
}

function hideResults() {
    elements.resultsSection.classList.add('hidden');
}

function showError(message) {
    elements.errorMessage.textContent = message;
    elements.errorDisplay.classList.remove('hidden');
    
    // Auto-hide after 5 seconds
    setTimeout(() => {
        hideError();
    }, 5000);
}

function hideError() {
    elements.errorDisplay.classList.add('hidden');
}

// ===== Utility Functions =====
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// ===== Console Easter Egg =====
console.log('%c🚀 Email Triage Assistant', 'font-size: 20px; font-weight: bold; color: #667eea;');
console.log('%cBuilt with ❤️ by Olina Kundu', 'font-size: 12px; color: #64748b;');
console.log('%cPowered by AI & ScaleDown Compression', 'font-size: 12px; color: #64748b;');
