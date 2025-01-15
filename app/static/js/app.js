/**
 * Property Management System Main Application JavaScript
 * Version: 2.1.0
 * Last Updated: 2025-01-08 16:33:30 UTC
 * Author: Development Team
 */

// Global Configuration
const APP_CONFIG = {
    currentUser: 'hnejadi',
    apiBaseUrl: '/api/v1',
    dateFormat: 'YYYY-MM-DD',
    timeFormat: 'HH:mm:ss',
    defaultPageSize: 25,
    refreshInterval: 300000, // 5 minutes
    toastDuration: 5000,
    maxFileSize: 5242880, // 5MB
    allowedFileTypes: '.jpg,.png,.pdf,.doc,.docx',
    currency: 'USD'
};

// Application Initialization
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

function initializeApp() {
    setupAjaxDefaults();
    initializeComponents();
    setupGlobalEventListeners();
    startAutoRefresh();
}

// Ajax Setup
function setupAjaxDefaults() {
    $.ajaxSetup({
        headers: {
            'X-User': APP_CONFIG.currentUser,
            'X-Timestamp': moment.utc().format(),
            'X-CSRF-TOKEN': document.querySelector('meta[name="csrf-token"]')?.content
        },
        error: handleAjaxError
    });
}

// Component Initialization
function initializeComponents() {
    // Initialize select2 dropdowns
    $('.select2-field').select2({
        theme: 'bootstrap4',
        width: '100%'
    });

    // Initialize datepickers
    $('.datepicker').daterangepicker({
        singleDatePicker: true,
        showDropdowns: true,
        locale: {
            format: APP_CONFIG.dateFormat
        }
    });

    // Initialize tooltips
    $('[data-toggle="tooltip"]').tooltip();

    // Initialize popovers
    $('[data-toggle="popover"]').popover();

    // Initialize datatables
    initializeDataTables();
}

// DataTables Configuration
function initializeDataTables() {
    $('.datatable').DataTable({
        pageLength: APP_CONFIG.defaultPageSize,
        responsive: true,
        dom: 'Bfrtip',
        buttons: ['copy', 'csv', 'excel', 'pdf', 'print'],
        language: {
            search: "Search:",
            lengthMenu: "Show _MENU_ entries",
            info: "Showing _START_ to _END_ of _TOTAL_ entries",
            infoEmpty: "Showing 0 to 0 of 0 entries",
            infoFiltered: "(filtered from _MAX_ total entries)"
        }
    });
}

// Event Listeners
function setupGlobalEventListeners() {
    // Form submission handling
    document.addEventListener('submit', handleFormSubmission);

    // Modal handling
    $('.modal').on('show.bs.modal', handleModalShow);

    // Navigation confirmation
    window.addEventListener('beforeunload', handlePageLeave);

    // Theme switching
    document.getElementById('themeSwitch')?.addEventListener('change', handleThemeSwitch);
}

// Form Handling
async function handleFormSubmission(event) {
    if (event.target.classList.contains('needs-validation')) {
        event.preventDefault();

        if (validateForm(event.target)) {
            try {
                await submitForm(event.target);
            } catch (error) {
                console.error('Form submission error:', error);
                showToast('Error submitting form', 'error');
            }
        }
    }
}

function validateForm(form) {
    if (!form.checkValidity()) {
        form.classList.add('was-validated');
        highlightInvalidFields(form);
        return false;
    }
    return true;
}

async function submitForm(form) {
    const formData = new FormData(form);
    formData.append('_user', APP_CONFIG.currentUser);
    formData.append('_timestamp', moment.utc().format());

    const response = await fetch(form.action, {
        method: form.method,
        body: formData
    });

    if (response.ok) {
        showToast('Form submitted successfully', 'success');
        handleFormSuccess(form);
    } else {
        throw new Error('Form submission failed');
    }
}

// Toast Notifications
function showToast(message, type = 'info') {
    const toast = createToastElement(message, type);
    document.getElementById('toastContainer').appendChild(toast);
    $(toast).toast('show');

    setTimeout(() => {
        $(toast).toast('hide');
    }, APP_CONFIG.toastDuration);
}

function createToastElement(message, type) {
    const toast = document.createElement('div');
    toast.className = `toast bg-${type}`;
    toast.setAttribute('role', 'alert');
    toast.setAttribute('aria-live', 'assertive');
    toast.setAttribute('aria-atomic', 'true');

    toast.innerHTML = `
        <div class="toast-header">
            <strong class="mr-auto">Notification</strong>
            <small>${moment().format(APP_CONFIG.timeFormat)}</small>
            <button type="button" class="ml-2 mb-1 close" data-dismiss="toast">&times;</button>
        </div>
        <div class="toast-body text-white">
            ${message}
        </div>
    `;

    return toast;
}

// Error Handling
function handleAjaxError(jqXHR, textStatus, errorThrown) {
    console.error('Ajax Error:', textStatus, errorThrown);

    let errorMessage = 'An error occurred while processing your request.';
    if (jqXHR.responseJSON?.message) {
        errorMessage = jqXHR.responseJSON.message;
    }

    showToast(errorMessage, 'error');
}

// Utility Functions
function formatCurrency(amount) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: APP_CONFIG.currency
    }).format(amount);
}

function formatDate(date) {
    return moment(date).format(APP_CONFIG.dateFormat);
}

function formatDateTime(datetime) {
    return moment(datetime).format(`${APP_CONFIG.dateFormat} ${APP_CONFIG.timeFormat}`);
}

function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Auto Refresh
function startAutoRefresh() {
    setInterval(() => {
        refreshDashboardData();
        updateTimestamps();
    }, APP_CONFIG.refreshInterval);
}

function refreshDashboardData() {
    // Refresh dashboard widgets and data
    $('.datatable').DataTable().ajax.reload(null, false);
    updateNotifications();
    updateMetrics();
}

function updateTimestamps() {
    document.querySelectorAll('[data-timestamp]').forEach(element => {
        const timestamp = element.dataset.timestamp;
        element.textContent = moment(timestamp).fromNow();
    });
}

// Export utilities for testing
window.appUtils = {
    formatCurrency,
    formatDate,
    formatDateTime,
    showToast,
    handleAjaxError
};