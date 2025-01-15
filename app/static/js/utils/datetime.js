/**
 * Property Management System - DateTime Module
 * Version: 2.1.0
 * Last Updated: 2025-01-08 18:32:22 UTC
 * Author: Development Team
 */

class DateTimeManager {
    constructor() {
        this.instances = new Map();
        this.defaultOptions = {
            format: 'YYYY-MM-DD HH:mm:ss',
            timezone: 'UTC',
            locale: 'en-US',
            updateInterval: 1000,
            autoUpdate: true,
            showSeconds: true,
            use24Hours: true,
            includeWeekday: false,
            includeTimezone: true
        };
    }

    /**
     * Initialize datetime instance
     * @param {string|HTMLElement} element Element or selector
     * @param {Object} options Configuration options
     */
    init(element, options = {}) {
        const targetElement = typeof element === 'string'
            ? document.querySelector(element)
            : element;

        if (!targetElement) throw new Error('Target element not found');

        const instanceId = targetElement.id || `datetime-${Date.now()}`;
        const instanceOptions = { ...this.defaultOptions, ...options };

        this.instances.set(instanceId, {
            element: targetElement,
            options: instanceOptions,
            interval: null,
            currentValue: null
        });

        this.initializeDateTime(instanceId);
    }

    /**
     * Initialize datetime display
     * @param {string} instanceId Instance identifier
     */
    initializeDateTime(instanceId) {
        const instance = this.instances.get(instanceId);
        const { options } = instance;

        // Set up initial display
        this.updateDateTime(instanceId);

        // Set up auto-update if enabled
        if (options.autoUpdate) {
            instance.interval = setInterval(() => {
                this.updateDateTime(instanceId);
            }, options.updateInterval);
        }
    }

    /**
     * Update datetime display
     * @param {string} instanceId Instance identifier
     */
    updateDateTime(instanceId) {
        const instance = this.instances.get(instanceId);
        const { element, options } = instance;
        const now = new Date();

        const formattedDate = this.formatDateTime(now, options);
        if (formattedDate !== instance.currentValue) {
            element.textContent = formattedDate;
            instance.currentValue = formattedDate;

            // Dispatch change event
            const event = new CustomEvent('datetime-update', {
                detail: {
                    value: formattedDate,
                    timestamp: now.getTime()
                }
            });
            element.dispatchEvent(event);
        }
    }

    /**
     * Format datetime according to options
     * @param {Date} date Date object to format
     * @param {Object} options Formatting options
     * @returns {string} Formatted datetime string
     */
    formatDateTime(date, options) {
        const formatter = new Intl.DateTimeFormat(options.locale, {
            weekday: options.includeWeekday ? 'long' : undefined,
            year: 'numeric',
            month: '2-digit',
            day: '2-digit',
            hour: '2-digit',
            minute: '2-digit',
            second: options.showSeconds ? '2-digit' : undefined,
            hour12: !options.use24Hours,
            timeZone: options.timezone,
            timeZoneName: options.includeTimezone ? 'short' : undefined
        });

        return formatter.format(date);
    }

    /**
     * Parse datetime string
     * @param {string} dateString DateTime string to parse
     * @param {string} format Format of the input string
     * @returns {Date} Parsed Date object
     */
    parseDateTime(dateString, format = this.defaultOptions.format) {
        if (!dateString) return null;

        // Handle ISO format
        if (format === 'ISO' || format === 'YYYY-MM-DDTHH:mm:ssZ') {
            return new Date(dateString);
        }

        // Handle custom format
        const parts = this.extractDateParts(dateString, format);
        if (!parts) return null;

        return new Date(
            parts.year,
            (parts.month || 1) - 1,
            parts.day || 1,
            parts.hours || 0,
            parts.minutes || 0,
            parts.seconds || 0
        );
    }

    /**
     * Extract date parts from string based on format
     * @param {string} dateString DateTime string
     * @param {string} format Format string
     * @returns {Object} Object containing date parts
     */
    extractDateParts(dateString, format) {
        const patterns = {
            YYYY: '(\\d{4})',
            MM: '(\\d{2})',
            DD: '(\\d{2})',
            HH: '(\\d{2})',
            mm: '(\\d{2})',
            ss: '(\\d{2})'
        };

        let regex = format;
        const keys = [];

        // Build regex pattern and collect keys
        Object.entries(patterns).forEach(([key, pattern]) => {
            if (format.includes(key)) {
                regex = regex.replace(key, pattern);
                keys.push(key.toLowerCase());
            }
        });

        const match = dateString.match(new RegExp(regex));
        if (!match) return null;

        // Build result object
        const result = {};
        keys.forEach((key, index) => {
            const value = parseInt(match[index + 1], 10);
            switch (key) {
                case 'yyyy': result.year = value; break;
                case 'mm': result.month = value; break;
                case 'dd': result.day = value; break;
                case 'hh': result.hours = value; break;
                case 'mm': result.minutes = value; break;
                case 'ss': result.seconds = value; break;
            }
        });

        return result;
    }

    /**
     * Format relative time
     * @param {Date|number} date Date object or timestamp
     * @param {Object} options Formatting options
     * @returns {string} Relative time string
     */
    formatRelative(date, options = {}) {
        const now = new Date();
        const targetDate = date instanceof Date ? date : new Date(date);
        const diff = now - targetDate;
        const seconds = Math.floor(diff / 1000);
        const minutes = Math.floor(seconds / 60);
        const hours = Math.floor(minutes / 60);
        const days = Math.floor(hours / 24);

        if (days > 7) {
            return this.formatDateTime(targetDate, this.defaultOptions);
        }

        if (days > 0) return `${days} day${days > 1 ? 's' : ''} ago`;
        if (hours > 0) return `${hours} hour${hours > 1 ? 's' : ''} ago`;
        if (minutes > 0) return `${minutes} minute${minutes > 1 ? 's' : ''} ago`;
        return 'just now';
    }

    /**
     * Clean up instance
     * @param {string} instanceId Instance identifier
     */
    destroy(instanceId) {
        const instance = this.instances.get(instanceId);
        if (!instance) return;

        if (instance.interval) {
            clearInterval(instance.interval);
        }

        this.instances.delete(instanceId);
    }

    /**
     * Get current value
     * @param {string} instanceId Instance identifier
     * @returns {string} Current datetime value
     */
    getValue(instanceId) {
        const instance = this.instances.get(instanceId);
        return instance ? instance.currentValue : null;
    }

    /**
     * Update options
     * @param {string} instanceId Instance identifier
     * @param {Object} newOptions New options to apply
     */
    updateOptions(instanceId, newOptions) {
        const instance = this.instances.get(instanceId);
        if (!instance) return;

        instance.options = { ...instance.options, ...newOptions };
        this.updateDateTime(instanceId);
    }
}

// Create global instance
const dateTimeManager = new DateTimeManager();

// Export for module usage
export default dateTimeManager;