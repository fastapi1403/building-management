/**
 * Property Management System - Pagination Module
 * Version: 2.1.0
 * Last Updated: 2025-01-08 18:19:39 UTC
 * Author: Development Team
 */

class PaginationManager {
    constructor() {
        this.instances = new Map();
        this.defaultOptions = {
            itemsPerPage: 10,
            visiblePages: 5,
            showFirstLast: true,
            showPrevNext: true,
            showPageNumbers: true,
            showItemsPerPage: true,
            showItemsInfo: true,
            itemsPerPageOptions: [5, 10, 25, 50, 100],
            labels: {
                first: '«',
                last: '»',
                prev: '‹',
                next: '›',
                itemsPerPage: 'Items per page:',
                showing: 'Showing',
                to: 'to',
                of: 'of',
                entries: 'entries'
            }
        };
    }

    /**
     * Initialize pagination for a container
     * @param {string|HTMLElement} container Container element or selector
     * @param {Object} options Pagination options
     * @param {Function} dataCallback Callback function to fetch data
     */
    init(container, options = {}, dataCallback) {
        const containerElement = typeof container === 'string'
            ? document.querySelector(container)
            : container;

        if (!containerElement) throw new Error('Container element not found');

        const instanceId = containerElement.id || `pagination-${Date.now()}`;
        const paginationOptions = { ...this.defaultOptions, ...options };

        this.instances.set(instanceId, {
            container: containerElement,
            options: paginationOptions,
            currentPage: 1,
            totalItems: 0,
            dataCallback,
            isLoading: false
        });

        this.createPaginationElements(instanceId);
        this.loadData(instanceId);
    }

    /**
     * Create pagination UI elements
     * @param {string} instanceId Pagination instance identifier
     */
    createPaginationElements(instanceId) {
        const instance = this.instances.get(instanceId);
        const { container, options } = instance;

        // Create wrapper
        const wrapper = document.createElement('div');
        wrapper.className = 'pagination-wrapper';

        // Create controls container
        const controls = document.createElement('div');
        controls.className = 'pagination-controls';

        // Items per page selector
        if (options.showItemsPerPage) {
            const itemsPerPage = this.createItemsPerPageSelector(instanceId);
            controls.appendChild(itemsPerPage);
        }

        // Pagination container
        const pagination = document.createElement('ul');
        pagination.className = 'pagination';
        controls.appendChild(pagination);

        // Items info
        if (options.showItemsInfo) {
            const info = document.createElement('div');
            info.className = 'pagination-info';
            controls.appendChild(info);
        }

        wrapper.appendChild(controls);
        container.appendChild(wrapper);
    }

    /**
     * Create items per page selector
     * @param {string} instanceId Pagination instance identifier
     * @returns {HTMLElement} Items per page selector element
     */
    createItemsPerPageSelector(instanceId) {
        const { options } = this.instances.get(instanceId);
        const container = document.createElement('div');
        container.className = 'items-per-page';

        const label = document.createElement('label');
        label.className = 'items-per-page-label';
        label.textContent = options.labels.itemsPerPage;

        const select = document.createElement('select');
        select.className = 'items-per-page-select';

        options.itemsPerPageOptions.forEach(value => {
            const option = document.createElement('option');
            option.value = value;
            option.textContent = value;
            if (value === options.itemsPerPage) option.selected = true;
            select.appendChild(option);
        });

        select.addEventListener('change', () => {
            this.updateItemsPerPage(instanceId, parseInt(select.value));
        });

        container.appendChild(label);
        container.appendChild(select);

        return container;
    }

    /**
     * Update pagination UI
     * @param {string} instanceId Pagination instance identifier
     */
    updateUI(instanceId) {
        const instance = this.instances.get(instanceId);
        const { container, options, currentPage, totalItems } = instance;

        const totalPages = Math.ceil(totalItems / options.itemsPerPage);
        const pagination = container.querySelector('.pagination');
        pagination.innerHTML = '';

        // First page button
        if (options.showFirstLast) {
            this.addPageButton(pagination, 1, options.labels.first, currentPage === 1, instanceId);
        }

        // Previous button
        if (options.showPrevNext) {
            this.addPageButton(pagination, currentPage - 1, options.labels.prev,
                currentPage === 1, instanceId);
        }

        // Page numbers
        if (options.showPageNumbers) {
            const pages = this.calculateVisiblePages(currentPage, totalPages, options.visiblePages);
            pages.forEach(page => {
                this.addPageButton(pagination, page, page, false, instanceId, page === currentPage);
            });
        }

        // Next button
        if (options.showPrevNext) {
            this.addPageButton(pagination, currentPage + 1, options.labels.next,
                currentPage === totalPages, instanceId);
        }

        // Last page button
        if (options.showFirstLast) {
            this.addPageButton(pagination, totalPages, options.labels.last,
                currentPage === totalPages, instanceId);
        }

        // Update info text
        if (options.showItemsInfo) {
            this.updateInfoText(instanceId);
        }
    }

    /**
     * Add page button to pagination
     * @param {HTMLElement} container Pagination container
     * @param {number} page Page number
     * @param {string} label Button label
     * @param {boolean} disabled Disabled state
     * @param {string} instanceId Pagination instance identifier
     * @param {boolean} active Active state
     */
    addPageButton(container, page, label, disabled, instanceId, active = false) {
        const li = document.createElement('li');
        li.className = `page-item${disabled ? ' disabled' : ''}${active ? ' active' : ''}`;

        const button = document.createElement('button');
        button.className = 'page-link';
        button.textContent = label;
        button.disabled = disabled;

        if (!disabled) {
            button.addEventListener('click', () => this.goToPage(instanceId, page));
        }

        li.appendChild(button);
        container.appendChild(li);
    }

    /**
     * Calculate visible page numbers
     * @param {number} currentPage Current page number
     * @param {number} totalPages Total number of pages
     * @param {number} visiblePages Number of visible page buttons
     * @returns {Array} Array of visible page numbers
     */
    calculateVisiblePages(currentPage, totalPages, visiblePages) {
        let start = Math.max(1, currentPage - Math.floor(visiblePages / 2));
        let end = start + visiblePages - 1;

        if (end > totalPages) {
            end = totalPages;
            start = Math.max(1, end - visiblePages + 1);
        }

        return Array.from({length: end - start + 1}, (_, i) => start + i);
    }

    /**
     * Update items per page
     * @param {string} instanceId Pagination instance identifier
     * @param {number} value New items per page value
     */
    updateItemsPerPage(instanceId, value) {
        const instance = this.instances.get(instanceId);
        instance.options.itemsPerPage = value;
        instance.currentPage = 1;
        this.loadData(instanceId);
    }

    /**
     * Go to specific page
     * @param {string} instanceId Pagination instance identifier
     * @param {number} page Target page number
     */
    goToPage(instanceId, page) {
        const instance = this.instances.get(instanceId);
        if (instance.isLoading) return;

        instance.currentPage = page;
        this.loadData(instanceId);
    }

    /**
     * Load data for current page
     * @param {string} instanceId Pagination instance identifier
     */
    async loadData(instanceId) {
        const instance = this.instances.get(instanceId);
        if (!instance.dataCallback) return;

        instance.isLoading = true;
        this.setLoading(instanceId, true);

        try {
            const { currentPage, options } = instance;
            const response = await instance.dataCallback({
                page: currentPage,
                itemsPerPage: options.itemsPerPage
            });

            instance.totalItems = response.total;
            this.updateUI(instanceId);
        } catch (error) {
            console.error('Error loading pagination data:', error);
            this.showError(instanceId);
        } finally {
            instance.isLoading = false;
            this.setLoading(instanceId, false);
        }
    }

    /**
     * Update info text
     * @param {string} instanceId Pagination instance identifier
     */
    updateInfoText(instanceId) {
        const instance = this.instances.get(instanceId);
        const { container, options, currentPage, totalItems } = instance;
        const info = container.querySelector('.pagination-info');

        const start = (currentPage - 1) * options.itemsPerPage + 1;
        const end = Math.min(currentPage * options.itemsPerPage, totalItems);

        info.textContent = `${options.labels.showing} ${start} ${options.labels.to} ${end} ${options.labels.of} ${totalItems} ${options.labels.entries}`;
    }

    /**
     * Set loading state
     * @param {string} instanceId Pagination instance identifier
     * @param {boolean} loading Loading state
     */
    setLoading(instanceId, loading) {
        const instance = this.instances.get(instanceId);
        instance.container.classList.toggle('pagination-loading', loading);
    }

    /**
     * Show error message
     * @param {string} instanceId Pagination instance identifier
     */
    showError(instanceId) {
        const instance = this.instances.get(instanceId);
        const error = document.createElement('div');
        error.className = 'pagination-error alert alert-danger';
        error.textContent = 'Error loading data. Please try again.';

        instance.container.appendChild(error);
        setTimeout(() => error.remove(), 5000);
    }
}

// Create global instance
const paginationManager = new PaginationManager();

// Export for module usage
export default paginationManager;