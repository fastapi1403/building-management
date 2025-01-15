/**
 * Property Management System - Form Management Module
 * Version: 2.1.0
 * Last Updated: 2025-01-08 18:17:16 UTC
 * Author: Development Team
 */

class FormManager {
    constructor() {
        this.forms = new Map();
        this.validators = new Map();
        this.defaultOptions = {
            validateOnInput: true,
            validateOnBlur: true,
            submitHandler: null,
            errorClass: 'is-invalid',
            successClass: 'is-valid',
            errorMessageClass: 'invalid-feedback',
            successMessageClass: 'valid-feedback'
        };
    }

    /**
     * Initialize a form with validation and submission handling
     * @param {string|HTMLFormElement} form Form element or selector
     * @param {Object} options Form configuration options
     */
    init(form, options = {}) {
        const formElement = typeof form === 'string' ? document.querySelector(form) : form;
        if (!formElement) throw new Error('Form element not found');

        const formId = formElement.id || `form-${Date.now()}`;
        const formOptions = { ...this.defaultOptions, ...options };

        this.forms.set(formId, {
            element: formElement,
            options: formOptions,
            fields: new Map(),
            isSubmitting: false
        });

        this.setupFormListeners(formId);
        this.setupFieldValidation(formId);
    }

    /**
     * Set up form event listeners
     * @param {string} formId Form identifier
     */
    setupFormListeners(formId) {
        const form = this.forms.get(formId);
        const { element, options } = form;

        element.addEventListener('submit', async (event) => {
            event.preventDefault();

            if (form.isSubmitting) return;

            const isValid = await this.validateForm(formId);
            if (!isValid) return;

            form.isSubmitting = true;
            this.setFormLoading(element, true);

            try {
                if (options.submitHandler) {
                    const formData = this.getFormData(element);
                    await options.submitHandler(formData);
                }
            } catch (error) {
                this.handleSubmissionError(error, element);
            } finally {
                form.isSubmitting = false;
                this.setFormLoading(element, false);
            }
        });
    }

    /**
     * Set up field validation listeners
     * @param {string} formId Form identifier
     */
    setupFieldValidation(formId) {
        const { element, options } = this.forms.get(formId);
        const fields = element.querySelectorAll('input, select, textarea');

        fields.forEach(field => {
            const fieldId = field.id || field.name;
            if (!fieldId) return;

            this.forms.get(formId).fields.set(fieldId, {
                element: field,
                validators: []
            });

            if (options.validateOnInput) {
                field.addEventListener('input', () => this.validateField(formId, fieldId));
            }

            if (options.validateOnBlur) {
                field.addEventListener('blur', () => this.validateField(formId, fieldId));
            }
        });
    }

    /**
     * Add a validator to a field
     * @param {string} formId Form identifier
     * @param {string} fieldId Field identifier
     * @param {Function} validator Validation function
     * @param {string} message Error message
     */
    addValidator(formId, fieldId, validator, message) {
        const form = this.forms.get(formId);
        if (!form) throw new Error('Form not found');

        const field = form.fields.get(fieldId);
        if (!field) throw new Error('Field not found');

        field.validators.push({
            validate: validator,
            message
        });
    }

    /**
     * Validate a specific field
     * @param {string} formId Form identifier
     * @param {string} fieldId Field identifier
     * @returns {Promise<boolean>} Validation result
     */
    async validateField(formId, fieldId) {
        const form = this.forms.get(formId);
        const field = form.fields.get(fieldId);
        const { element } = field;
        const value = element.value;

        for (const validator of field.validators) {
            try {
                const isValid = await validator.validate(value);
                if (!isValid) {
                    this.showFieldError(element, validator.message, form.options);
                    return false;
                }
            } catch (error) {
                this.showFieldError(element, 'Validation error occurred', form.options);
                return false;
            }
        }

        this.showFieldSuccess(element, form.options);
        return true;
    }

    /**
     * Validate entire form
     * @param {string} formId Form identifier
     * @returns {Promise<boolean>} Validation result
     */
    async validateForm(formId) {
        const form = this.forms.get(formId);
        const results = await Promise.all(
            Array.from(form.fields.keys()).map(fieldId =>
                this.validateField(formId, fieldId)
            )
        );
        return results.every(result => result === true);
    }

    /**
     * Show field error state
     * @param {HTMLElement} field Field element
     * @param {string} message Error message
     * @param {Object} options Form options
     */
    showFieldError(field, message, options) {
        field.classList.remove(options.successClass);
        field.classList.add(options.errorClass);

        let errorElement = field.nextElementSibling;
        if (!errorElement || !errorElement.classList.contains(options.errorMessageClass)) {
            errorElement = document.createElement('div');
            errorElement.className = options.errorMessageClass;
            field.parentNode.insertBefore(errorElement, field.nextSibling);
        }
        errorElement.textContent = message;
    }

    /**
     * Show field success state
     * @param {HTMLElement} field Field element
     * @param {Object} options Form options
     */
    showFieldSuccess(field, options) {
        field.classList.remove(options.errorClass);
        field.classList.add(options.successClass);

        const errorElement = field.nextElementSibling;
        if (errorElement && errorElement.classList.contains(options.errorMessageClass)) {
            errorElement.remove();
        }
    }

    /**
     * Set form loading state
     * @param {HTMLFormElement} form Form element
     * @param {boolean} isLoading Loading state
     */
    setFormLoading(form, isLoading) {
        form.classList.toggle('form-loading', isLoading);
        const submitButton = form.querySelector('[type="submit"]');
        if (submitButton) {
            submitButton.disabled = isLoading;
        }
    }

    /**
     * Get form data as object
     * @param {HTMLFormElement} form Form element
     * @returns {Object} Form data
     */
    getFormData(form) {
        const formData = new FormData(form);
        const data = {};
        for (const [key, value] of formData.entries()) {
            if (data[key]) {
                if (!Array.isArray(data[key])) {
                    data[key] = [data[key]];
                }
                data[key].push(value);
            } else {
                data[key] = value;
            }
        }
        return data;
    }

    /**
     * Handle form submission error
     * @param {Error} error Error object
     * @param {HTMLFormElement} form Form element
     */
    handleSubmissionError(error, form) {
        console.error('Form submission error:', error);
        const errorAlert = document.createElement('div');
        errorAlert.className = 'alert alert-danger mt-3';
        errorAlert.textContent = 'An error occurred while submitting the form. Please try again.';
        form.insertAdjacentElement('beforeend', errorAlert);

        setTimeout(() => errorAlert.remove(), 5000);
    }

    /**
     * Reset form to initial state
     * @param {string} formId Form identifier
     */
    reset(formId) {
        const form = this.forms.get(formId);
        if (!form) return;

        form.element.reset();
        form.fields.forEach(field => {
            field.element.classList.remove(form.options.errorClass, form.options.successClass);
            const feedback = field.element.nextElementSibling;
            if (feedback && (
                feedback.classList.contains(form.options.errorMessageClass) ||
                feedback.classList.contains(form.options.successMessageClass)
            )) {
                feedback.remove();
            }
        });
    }
}

// Create global instance
const formManager = new FormManager();

// Export for module usage
export default formManager;