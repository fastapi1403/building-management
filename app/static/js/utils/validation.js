/**
 * Property Management System - Validation Module
 * Version: 2.1.0
 * Last Updated: 2025-01-08 18:35:06 UTC
 * Author: Development Team
 */

class ValidationManager {
    constructor() {
        this.rules = new Map();
        this.customValidators = new Map();
        this.defaultMessages = {
            required: 'This field is required.',
            email: 'Please enter a valid email address.',
            minLength: 'Please enter at least {min} characters.',
            maxLength: 'Please enter no more than {max} characters.',
            min: 'Please enter a value greater than or equal to {min}.',
            max: 'Please enter a value less than or equal to {max}.',
            pattern: 'Please enter a valid value.',
            match: 'Fields do not match.',
            url: 'Please enter a valid URL.',
            date: 'Please enter a valid date.',
            phone: 'Please enter a valid phone number.',
            creditCard: 'Please enter a valid credit card number.',
            numeric: 'Please enter a valid number.',
            integer: 'Please enter a whole number.',
            alphanumeric: 'Please enter only letters and numbers.',
            currency: 'Please enter a valid currency amount.'
        };
    }

    /**
     * Add validation rule
     * @param {string} field Field identifier
     * @param {Object} rules Validation rules
     */
    addRule(field, rules) {
        this.rules.set(field, rules);
    }

    /**
     * Add custom validator
     * @param {string} name Validator name
     * @param {Function} validator Validator function
     */
    addCustomValidator(name, validator) {
        this.customValidators.set(name, validator);
    }

    /**
     * Validate single value
     * @param {string} field Field identifier
     * @param {*} value Value to validate
     * @returns {Object} Validation result
     */
    async validate(field, value) {
        const rules = this.rules.get(field);
        if (!rules) return { isValid: true };

        const errors = [];

        for (const [ruleName, ruleValue] of Object.entries(rules)) {
            const error = await this.validateRule(ruleName, value, ruleValue, rules);
            if (error) errors.push(error);
        }

        return {
            isValid: errors.length === 0,
            errors
        };
    }

    /**
     * Validate form data
     * @param {Object} data Form data
     * @returns {Object} Validation results
     */
    async validateForm(data) {
        const results = new Map();
        const promises = [];

        for (const [field, value] of Object.entries(data)) {
            if (this.rules.has(field)) {
                promises.push(
                    this.validate(field, value).then(result => {
                        results.set(field, result);
                    })
                );
            }
        }

        await Promise.all(promises);
        return results;
    }

    /**
     * Validate single rule
     * @param {string} ruleName Rule identifier
     * @param {*} value Value to validate
     * @param {*} ruleValue Rule configuration
     * @param {Object} allRules All rules for the field
     * @returns {string|null} Error message or null
     */
    async validateRule(ruleName, value, ruleValue, allRules) {
        // Skip validation if field is empty and not required
        if (!allRules.required && (value === '' || value === null || value === undefined)) {
            return null;
        }

        switch (ruleName) {
            case 'required':
                if (ruleValue && !value) {
                    return this.formatMessage('required');
                }
                break;

            case 'email':
                if (ruleValue && !this.isValidEmail(value)) {
                    return this.formatMessage('email');
                }
                break;

            case 'minLength':
                if (value.length < ruleValue) {
                    return this.formatMessage('minLength', { min: ruleValue });
                }
                break;

            case 'maxLength':
                if (value.length > ruleValue) {
                    return this.formatMessage('maxLength', { max: ruleValue });
                }
                break;

            case 'min':
                if (parseFloat(value) < ruleValue) {
                    return this.formatMessage('min', { min: ruleValue });
                }
                break;

            case 'max':
                if (parseFloat(value) > ruleValue) {
                    return this.formatMessage('max', { max: ruleValue });
                }
                break;

            case 'pattern':
                if (!new RegExp(ruleValue).test(value)) {
                    return this.formatMessage('pattern');
                }
                break;

            case 'match':
                if (value !== allRules.matchValue) {
                    return this.formatMessage('match');
                }
                break;

            case 'url':
                if (ruleValue && !this.isValidUrl(value)) {
                    return this.formatMessage('url');
                }
                break;

            case 'date':
                if (ruleValue && !this.isValidDate(value)) {
                    return this.formatMessage('date');
                }
                break;

            case 'phone':
                if (ruleValue && !this.isValidPhone(value)) {
                    return this.formatMessage('phone');
                }
                break;

            case 'creditCard':
                if (ruleValue && !this.isValidCreditCard(value)) {
                    return this.formatMessage('creditCard');
                }
                break;

            case 'numeric':
                if (ruleValue && !this.isNumeric(value)) {
                    return this.formatMessage('numeric');
                }
                break;

            case 'integer':
                if (ruleValue && !this.isInteger(value)) {
                    return this.formatMessage('integer');
                }
                break;

            case 'alphanumeric':
                if (ruleValue && !this.isAlphanumeric(value)) {
                    return this.formatMessage('alphanumeric');
                }
                break;

            case 'currency':
                if (ruleValue && !this.isValidCurrency(value)) {
                    return this.formatMessage('currency');
                }
                break;

            default:
                if (this.customValidators.has(ruleName)) {
                    const validator = this.customValidators.get(ruleName);
                    const result = await validator(value, ruleValue);
                    if (!result.isValid) {
                        return result.message;
                    }
                }
                break;
        }

        return null;
    }

    /**
     * Format error message
     * @param {string} key Message key
     * @param {Object} params Message parameters
     * @returns {string} Formatted message
     */
    formatMessage(key, params = {}) {
        let message = this.defaultMessages[key];
        Object.entries(params).forEach(([param, value]) => {
            message = message.replace(`{${param}}`, value);
        });
        return message;
    }

    /**
     * Validate email format
     * @param {string} value Email address
     * @returns {boolean} Validation result
     */
    isValidEmail(value) {
        const pattern = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
        return pattern.test(value);
    }

    /**
     * Validate URL format
     * @param {string} value URL
     * @returns {boolean} Validation result
     */
    isValidUrl(value) {
        try {
            new URL(value);
            return true;
        } catch {
            return false;
        }
    }

    /**
     * Validate date format
     * @param {string} value Date string
     * @returns {boolean} Validation result
     */
    isValidDate(value) {
        const date = new Date(value);
        return date instanceof Date && !isNaN(date);
    }

    /**
     * Validate phone number format
     * @param {string} value Phone number
     * @returns {boolean} Validation result
     */
    isValidPhone(value) {
        const pattern = /^\+?[\d\s-()]{10,}$/;
        return pattern.test(value);
    }

    /**
     * Validate credit card number format
     * @param {string} value Credit card number
     * @returns {boolean} Validation result
     */
    isValidCreditCard(value) {
        const cleaned = value.replace(/\D/g, '');
        if (cleaned.length < 13 || cleaned.length > 19) return false;

        // Luhn algorithm
        let sum = 0;
        let isEven = false;

        for (let i = cleaned.length - 1; i >= 0; i--) {
            let digit = parseInt(cleaned[i], 10);

            if (isEven) {
                digit *= 2;
                if (digit > 9) digit -= 9;
            }

            sum += digit;
            isEven = !isEven;
        }

        return sum % 10 === 0;
    }

    /**
     * Check if value is numeric
     * @param {*} value Value to check
     * @returns {boolean} Check result
     */
    isNumeric(value) {
        return !isNaN(parseFloat(value)) && isFinite(value);
    }

    /**
     * Check if value is integer
     * @param {*} value Value to check
     * @returns {boolean} Check result
     */
    isInteger(value) {
        return Number.isInteger(Number(value));
    }

    /**
     * Check if value is alphanumeric
     * @param {string} value Value to check
     * @returns {boolean} Check result
     */
    isAlphanumeric(value) {
        return /^[a-zA-Z0-9]+$/.test(value);
    }

    /**
     * Validate currency format
     * @param {string} value Currency amount
     * @returns {boolean} Validation result
     */
    isValidCurrency(value) {
        return /^\$?\d+(\.\d{2})?$/.test(value);
    }
}

// Create global instance
const validationManager = new ValidationManager();

// Export for module usage
export default validationManager;