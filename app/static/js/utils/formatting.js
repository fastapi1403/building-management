/**
 * Property Management System - Data Formatting Module
 * Version: 2.1.0
 * Last Updated: 2025-01-08 18:33:40 UTC
 * Author: Development Team
 */

class FormattingManager {
    constructor() {
        this.defaultOptions = {
            locale: 'en-US',
            currency: 'USD',
            decimals: 2,
            dateFormat: 'MM/DD/YYYY',
            timeFormat: '24',
            numberFormat: 'standard', // standard, compact, scientific
            useGrouping: true,
            currencyDisplay: 'symbol' // symbol, code, name
        };

        this.formatters = new Map();
    }

    /**
     * Format currency value
     * @param {number} value Value to format
     * @param {Object} options Formatting options
     * @returns {string} Formatted currency string
     */
    formatCurrency(value, options = {}) {
        const opts = { ...this.defaultOptions, ...options };
        const key = `currency-${opts.locale}-${opts.currency}-${opts.currencyDisplay}`;

        if (!this.formatters.has(key)) {
            this.formatters.set(key, new Intl.NumberFormat(opts.locale, {
                style: 'currency',
                currency: opts.currency,
                currencyDisplay: opts.currencyDisplay
            }));
        }

        return this.formatters.get(key).format(value);
    }

    /**
     * Format number value
     * @param {number} value Value to format
     * @param {Object} options Formatting options
     * @returns {string} Formatted number string
     */
    formatNumber(value, options = {}) {
        const opts = { ...this.defaultOptions, ...options };
        const key = `number-${opts.locale}-${opts.numberFormat}-${opts.decimals}`;

        if (!this.formatters.has(key)) {
            const formatOptions = {
                style: 'decimal',
                minimumFractionDigits: opts.decimals,
                maximumFractionDigits: opts.decimals,
                useGrouping: opts.useGrouping
            };

            if (opts.numberFormat === 'compact') {
                formatOptions.notation = 'compact';
            } else if (opts.numberFormat === 'scientific') {
                formatOptions.notation = 'scientific';
            }

            this.formatters.set(key, new Intl.NumberFormat(opts.locale, formatOptions));
        }

        return this.formatters.get(key).format(value);
    }

    /**
     * Format percentage value
     * @param {number} value Value to format (0-1)
     * @param {Object} options Formatting options
     * @returns {string} Formatted percentage string
     */
    formatPercentage(value, options = {}) {
        const opts = { ...this.defaultOptions, ...options };
        const key = `percentage-${opts.locale}-${opts.decimals}`;

        if (!this.formatters.has(key)) {
            this.formatters.set(key, new Intl.NumberFormat(opts.locale, {
                style: 'percent',
                minimumFractionDigits: opts.decimals,
                maximumFractionDigits: opts.decimals
            }));
        }

        return this.formatters.get(key).format(value);
    }

    /**
     * Format date value
     * @param {Date|string|number} value Date to format
     * @param {Object} options Formatting options
     * @returns {string} Formatted date string
     */
    formatDate(value, options = {}) {
        const opts = { ...this.defaultOptions, ...options };
        const date = value instanceof Date ? value : new Date(value);
        const key = `date-${opts.locale}-${opts.dateFormat}`;

        if (!this.formatters.has(key)) {
            const formatOptions = {
                year: 'numeric',
                month: '2-digit',
                day: '2-digit'
            };

            this.formatters.set(key, new Intl.DateTimeFormat(opts.locale, formatOptions));
        }

        return this.formatters.get(key).format(date);
    }

    /**
     * Format file size
     * @param {number} bytes Size in bytes
     * @param {Object} options Formatting options
     * @returns {string} Formatted file size string
     */
    formatFileSize(bytes, options = {}) {
        const units = ['B', 'KB', 'MB', 'GB', 'TB', 'PB'];
        const opts = { ...this.defaultOptions, ...options };

        let value = bytes;
        let unitIndex = 0;

        while (value >= 1024 && unitIndex < units.length - 1) {
            value /= 1024;
            unitIndex++;
        }

        return `${this.formatNumber(value, { decimals: unitIndex === 0 ? 0 : opts.decimals })} ${units[unitIndex]}`;
    }

    /**
     * Format duration
     * @param {number} seconds Duration in seconds
     * @param {Object} options Formatting options
     * @returns {string} Formatted duration string
     */
    formatDuration(seconds, options = {}) {
        const opts = { ...this.defaultOptions, ...options };
        const units = {
            year: 31536000,
            month: 2592000,
            day: 86400,
            hour: 3600,
            minute: 60,
            second: 1
        };

        let remaining = seconds;
        const parts = [];

        for (const [unit, value] of Object.entries(units)) {
            if (remaining >= value) {
                const count = Math.floor(remaining / value);
                remaining %= value;
                parts.push(`${count} ${unit}${count !== 1 ? 's' : ''}`);
            }
        }

        return parts.join(' ');
    }

    /**
     * Format phone number
     * @param {string} number Phone number to format
     * @param {Object} options Formatting options
     * @returns {string} Formatted phone number
     */
    formatPhoneNumber(number, options = {}) {
        const opts = { ...this.defaultOptions, ...options };
        const cleaned = number.replace(/\D/g, '');

        if (opts.locale === 'en-US') {
            if (cleaned.length === 10) {
                return `(${cleaned.slice(0, 3)}) ${cleaned.slice(3, 6)}-${cleaned.slice(6)}`;
            }
        }

        return cleaned;
    }

    /**
     * Format credit card number
     * @param {string} number Credit card number
     * @returns {string} Formatted credit card number
     */
    formatCreditCard(number) {
        const cleaned = number.replace(/\D/g, '');
        const groups = cleaned.match(/.{1,4}/g);
        return groups ? groups.join(' ') : cleaned;
    }

    /**
     * Format list of items
     * @param {Array} items Items to format
     * @param {Object} options Formatting options
     * @returns {string} Formatted list string
     */
    formatList(items, options = {}) {
        const opts = { ...this.defaultOptions, ...options };
        const formatter = new Intl.ListFormat(opts.locale, {
            style: 'long',
            type: 'conjunction'
        });

        return formatter.format(items);
    }

    /**
     * Format relative time
     * @param {Date|number} date Date to format
     * @param {Object} options Formatting options
     * @returns {string} Formatted relative time string
     */
    formatRelativeTime(date, options = {}) {
        const opts = { ...this.defaultOptions, ...options };
        const now = new Date();
        const diff = (date instanceof Date ? date : new Date(date)) - now;

        const rtf = new Intl.RelativeTimeFormat(opts.locale, {
            numeric: 'auto'
        });

        const seconds = Math.round(diff / 1000);
        const minutes = Math.round(seconds / 60);
        const hours = Math.round(minutes / 60);
        const days = Math.round(hours / 24);
        const months = Math.round(days / 30);
        const years = Math.round(months / 12);

        if (Math.abs(years) > 0) return rtf.format(years, 'year');
        if (Math.abs(months) > 0) return rtf.format(months, 'month');
        if (Math.abs(days) > 0) return rtf.format(days, 'day');
        if (Math.abs(hours) > 0) return rtf.format(hours, 'hour');
        if (Math.abs(minutes) > 0) return rtf.format(minutes, 'minute');
        return rtf.format(seconds, 'second');
    }
}

// Create global instance
const formattingManager = new FormattingManager();

// Export for module usage
export default formattingManager;