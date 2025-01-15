/**
 * Property Management System - Alert Management Module
 * Version: 2.1.0
 * Last Updated: 2025-01-08 18:13:50 UTC
 * Author: Development Team
 */

class AlertManager {
    constructor() {
        this.alertContainer = this.createAlertContainer();
        this.alerts = new Map();
        this.config = {
            defaultDuration: 5000,
            maxAlerts: 5,
            position: 'top-right',
            animations: true
        };
    }

    /**
     * Creates and appends the alert container to the DOM
     * @returns {HTMLElement} The alert container element
     */
    createAlertContainer() {
        const container = document.createElement('div');
        container.className = 'alerts-wrapper';
        document.body.appendChild(container);
        return container;
    }

    /**
     * Shows an alert message
     * @param {Object} options Alert options
     * @param {string} options.message The alert message
     * @param {string} options.type The alert type (success, error, warning, info)
     * @param {number} options.duration Duration in milliseconds
     * @param {boolean} options.dismissible Whether the alert can be dismissed
     * @param {string} options.icon Custom icon class
     * @returns {string} Alert ID
     */
    show({ message, type = 'info', duration, dismissible = true, icon }) {
        // Generate unique ID for the alert
        const alertId = `alert-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;

        // Create alert element
        const alertElement = this.createAlertElement({
            id: alertId,
            message,
            type,
            dismissible,
            icon
        });

        // Manage maximum alerts
        if (this.alerts.size >= this.config.maxAlerts) {
            const oldestAlert = this.alertContainer.firstChild;
            if (oldestAlert) {
                this.dismiss(oldestAlert.id);
            }
        }

        // Add alert to container
        this.alertContainer.appendChild(alertElement);
        this.alerts.set(alertId, alertElement);

        // Trigger entrance animation
        requestAnimationFrame(() => {
            alertElement.classList.add('show');
        });

        // Set up auto-dismiss
        const alertDuration = duration || this.config.defaultDuration;
        if (alertDuration > 0) {
            this.setupAutoDismiss(alertId, alertDuration);
        }

        // Add progress bar if duration is set
        if (alertDuration > 0) {
            this.addProgressBar(alertElement, alertDuration);
        }

        return alertId;
    }

    /**
     * Creates the alert DOM element
     * @param {Object} options Alert element options
     * @returns {HTMLElement} The alert element
     */
    createAlertElement({ id, message, type, dismissible, icon }) {
        const alert = document.createElement('div');
        alert.id = id;
        alert.className = `alert alert-${type}`;
        alert.setAttribute('role', 'alert');

        // Add icon
        if (icon) {
            const iconElement = document.createElement('i');
            iconElement.className = `alert-icon ${icon}`;
            alert.appendChild(iconElement);
        }

        // Add content wrapper
        const contentWrapper = document.createElement('div');
        contentWrapper.className = 'alert-content';

        // Add message
        const messageElement = document.createElement('div');
        messageElement.className = 'alert-message';
        messageElement.textContent = message;
        contentWrapper.appendChild(messageElement);

        // Add timestamp
        const timestamp = document.createElement('div');
        timestamp.className = 'alert-timestamp';
        timestamp.textContent = new Date().toLocaleTimeString();
        contentWrapper.appendChild(timestamp);

        alert.appendChild(contentWrapper);

        // Add dismiss button if dismissible
        if (dismissible) {
            const dismissButton = document.createElement('button');
            dismissButton.type = 'button';
            dismissButton.className = 'close';
            dismissButton.innerHTML = '&times;';
            dismissButton.addEventListener('click', () => this.dismiss(id));
            alert.appendChild(dismissButton);
        }

        return alert;
    }

    /**
     * Adds a progress bar to the alert
     * @param {HTMLElement} alertElement The alert element
     * @param {number} duration Duration in milliseconds
     */
    addProgressBar(alertElement, duration) {
        const progressBar = document.createElement('div');
        progressBar.className = 'alert-progress';
        alertElement.appendChild(progressBar);

        progressBar.style.transition = `width ${duration}ms linear`;
        requestAnimationFrame(() => {
            progressBar.style.width = '0%';
        });
    }

    /**
     * Sets up auto-dismiss for an alert
     * @param {string} alertId The alert ID
     * @param {number} duration Duration in milliseconds
     */
    setupAutoDismiss(alertId, duration) {
        setTimeout(() => {
            this.dismiss(alertId);
        }, duration);
    }

    /**
     * Dismisses an alert
     * @param {string} alertId The alert ID
     */
    dismiss(alertId) {
        const alert = this.alerts.get(alertId);
        if (!alert) return;

        // Add exit animation
        alert.classList.remove('show');
        alert.classList.add('alert-exit');

        // Remove alert after animation
        setTimeout(() => {
            if (alert.parentNode === this.alertContainer) {
                this.alertContainer.removeChild(alert);
            }
            this.alerts.delete(alertId);
        }, 300);
    }

    /**
     * Success alert shorthand
     * @param {string} message The alert message
     * @param {Object} options Additional options
     */
    success(message, options = {}) {
        return this.show({
            message,
            type: 'success',
            icon: 'fas fa-check-circle',
            ...options
        });
    }

    /**
     * Error alert shorthand
     * @param {string} message The alert message
     * @param {Object} options Additional options
     */
    error(message, options = {}) {
        return this.show({
            message,
            type: 'danger',
            icon: 'fas fa-exclamation-circle',
            ...options
        });
    }

    /**
     * Warning alert shorthand
     * @param {string} message The alert message
     * @param {Object} options Additional options
     */
    warning(message, options = {}) {
        return this.show({
            message,
            type: 'warning',
            icon: 'fas fa-exclamation-triangle',
            ...options
        });
    }

    /**
     * Info alert shorthand
     * @param {string} message The alert message
     * @param {Object} options Additional options
     */
    info(message, options = {}) {
        return this.show({
            message,
            type: 'info',
            icon: 'fas fa-info-circle',
            ...options
        });
    }
}

// Create global instance
const alertManager = new AlertManager();

// Export for module usage
export default alertManager;