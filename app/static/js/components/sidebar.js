/**
 * Property Management System - Sidebar Module
 * Version: 2.1.0
 * Last Updated: 2025-01-08 18:28:03 UTC
 * Author: Development Team
 */

class SidebarManager {
    constructor() {
        this.instances = new Map();
        this.defaultOptions = {
            theme: 'light',
            collapsed: false,
            position: 'left',
            overlay: true,
            animate: true,
            breakpoint: 992,
            rememberState: true,
            enableDrag: false,
            autoCollapse: true,
            closeOnEsc: true,
            closeOnClickOutside: true
        };
    }

    /**
     * Initialize sidebar
     * @param {string|HTMLElement} sidebar Sidebar element or selector
     * @param {Object} options Configuration options
     */
    init(sidebar, options = {}) {
        const sidebarElement = typeof sidebar === 'string'
            ? document.querySelector(sidebar)
            : sidebar;

        if (!sidebarElement) throw new Error('Sidebar element not found');

        const sidebarId = sidebarElement.id || `sidebar-${Date.now()}`;
        const sidebarOptions = { ...this.defaultOptions, ...options };

        this.instances.set(sidebarId, {
            element: sidebarElement,
            options: sidebarOptions,
            state: {
                collapsed: sidebarOptions.collapsed,
                hidden: false,
                dragging: false
            }
        });

        this.setupSidebar(sidebarId);
        this.loadState(sidebarId);
        this.setupEventListeners(sidebarId);
    }

    /**
     * Set up sidebar structure and initial state
     * @param {string} sidebarId Sidebar identifier
     */
    setupSidebar(sidebarId) {
        const { element, options } = this.instances.get(sidebarId);

        // Add necessary classes
        element.classList.add('sidebar');
        element.classList.add(`sidebar-${options.position}`);
        if (options.animate) element.classList.add('sidebar-animate');
        if (options.theme) element.setAttribute('data-theme', options.theme);

        // Create backdrop if overlay is enabled
        if (options.overlay) {
            const backdrop = document.createElement('div');
            backdrop.className = 'sidebar-backdrop';
            document.body.appendChild(backdrop);
        }

        // Setup nested navigation
        this.setupNestedNavigation(element);
    }

    /**
     * Set up nested navigation functionality
     * @param {HTMLElement} element Sidebar element
     */
    setupNestedNavigation(element) {
        const submenuTriggers = element.querySelectorAll('.nav-link[data-toggle="collapse"]');

        submenuTriggers.forEach(trigger => {
            const submenu = trigger.nextElementSibling;
            if (!submenu) return;

            // Add necessary classes
            submenu.classList.add('nav-submenu');
            trigger.classList.add('has-submenu');

            // Add arrow indicator
            const arrow = document.createElement('span');
            arrow.className = 'submenu-arrow';
            trigger.appendChild(arrow);

            // Setup click handler
            trigger.addEventListener('click', (e) => {
                e.preventDefault();
                this.toggleSubmenu(trigger);
            });
        });
    }

    /**
     * Set up event listeners
     * @param {string} sidebarId Sidebar identifier
     */
    setupEventListeners(sidebarId) {
        const instance = this.instances.get(sidebarId);
        const { element, options } = instance;

        // Window resize handler
        window.addEventListener('resize', this.debounce(() => {
            this.handleResize(sidebarId);
        }, 250));

        // ESC key handler
        if (options.closeOnEsc) {
            document.addEventListener('keydown', (e) => {
                if (e.key === 'Escape') this.hide(sidebarId);
            });
        }

        // Click outside handler
        if (options.closeOnClickOutside) {
            document.addEventListener('click', (e) => {
                if (!element.contains(e.target) && !element.classList.contains('collapsed')) {
                    this.hide(sidebarId);
                }
            });
        }

        // Drag functionality
        if (options.enableDrag) {
            this.setupDragFunctionality(sidebarId);
        }
    }

    /**
     * Toggle submenu state
     * @param {HTMLElement} trigger Submenu trigger element
     */
    toggleSubmenu(trigger) {
        const submenu = trigger.nextElementSibling;
        const isOpen = trigger.classList.contains('active');

        // Close other open submenus at the same level
        const parent = trigger.closest('.nav-item');
        const siblings = parent.parentElement.children;
        Array.from(siblings).forEach(sibling => {
            if (sibling !== parent) {
                const siblingTrigger = sibling.querySelector('.nav-link');
                const siblingSubmenu = sibling.querySelector('.nav-submenu');
                if (siblingTrigger && siblingSubmenu) {
                    siblingTrigger.classList.remove('active');
                    siblingSubmenu.style.maxHeight = null;
                }
            }
        });

        // Toggle current submenu
        trigger.classList.toggle('active');
        if (!isOpen) {
            submenu.style.maxHeight = `${submenu.scrollHeight}px`;
        } else {
            submenu.style.maxHeight = null;
        }
    }

    /**
     * Handle window resize
     * @param {string} sidebarId Sidebar identifier
     */
    handleResize(sidebarId) {
        const instance = this.instances.get(sidebarId);
        const { options, state } = instance;

        if (window.innerWidth < options.breakpoint) {
            if (options.autoCollapse && !state.collapsed) {
                this.collapse(sidebarId);
            }
        } else {
            if (state.hidden) {
                this.show(sidebarId);
            }
        }
    }

    /**
     * Set up drag functionality
     * @param {string} sidebarId Sidebar identifier
     */
    setupDragFunctionality(sidebarId) {
        const instance = this.instances.get(sidebarId);
        const { element, state } = instance;
        let startX, startWidth;

        const dragHandle = document.createElement('div');
        dragHandle.className = 'sidebar-drag-handle';
        element.appendChild(dragHandle);

        dragHandle.addEventListener('mousedown', (e) => {
            state.dragging = true;
            startX = e.clientX;
            startWidth = element.offsetWidth;
            document.addEventListener('mousemove', handleDrag);
            document.addEventListener('mouseup', stopDrag);
        });

        const handleDrag = (e) => {
            if (!state.dragging) return;
            const diff = e.clientX - startX;
            const newWidth = startWidth + (instance.options.position === 'left' ? diff : -diff);
            element.style.width = `${Math.max(200, Math.min(newWidth, 600))}px`;
        };

        const stopDrag = () => {
            state.dragging = false;
            document.removeEventListener('mousemove', handleDrag);
            document.removeEventListener('mouseup', stopDrag);
        };
    }

    /**
     * Toggle sidebar state
     * @param {string} sidebarId Sidebar identifier
     */
    toggle(sidebarId) {
        const instance = this.instances.get(sidebarId);
        if (instance.state.collapsed) {
            this.expand(sidebarId);
        } else {
            this.collapse(sidebarId);
        }
    }

    /**
     * Collapse sidebar
     * @param {string} sidebarId Sidebar identifier
     */
    collapse(sidebarId) {
        const instance = this.instances.get(sidebarId);
        instance.state.collapsed = true;
        instance.element.classList.add('collapsed');
        this.saveState(sidebarId);
    }

    /**
     * Expand sidebar
     * @param {string} sidebarId Sidebar identifier
     */
    expand(sidebarId) {
        const instance = this.instances.get(sidebarId);
        instance.state.collapsed = false;
        instance.element.classList.remove('collapsed');
        this.saveState(sidebarId);
    }

    /**
     * Hide sidebar
     * @param {string} sidebarId Sidebar identifier
     */
    hide(sidebarId) {
        const instance = this.instances.get(sidebarId);
        instance.state.hidden = true;
        instance.element.classList.add('hidden');
        if (instance.options.overlay) {
            document.querySelector('.sidebar-backdrop').classList.remove('show');
        }
    }

    /**
     * Show sidebar
     * @param {string} sidebarId Sidebar identifier
     */
    show(sidebarId) {
        const instance = this.instances.get(sidebarId);
        instance.state.hidden = false;
        instance.element.classList.remove('hidden');
        if (instance.options.overlay) {
            document.querySelector('.sidebar-backdrop').classList.add('show');
        }
    }

    /**
     * Save sidebar state
     * @param {string} sidebarId Sidebar identifier
     */
    saveState(sidebarId) {
        const instance = this.instances.get(sidebarId);
        if (instance.options.rememberState) {
            localStorage.setItem(`sidebar_${sidebarId}`, JSON.stringify({
                collapsed: instance.state.collapsed
            }));
        }
    }

    /**
     * Load saved sidebar state
     * @param {string} sidebarId Sidebar identifier
     */
    loadState(sidebarId) {
        const instance = this.instances.get(sidebarId);
        if (instance.options.rememberState) {
            const saved = localStorage.getItem(`sidebar_${sidebarId}`);
            if (saved) {
                const state = JSON.parse(saved);
                if (state.collapsed) {
                    this.collapse(sidebarId);
                } else {
                    this.expand(sidebarId);
                }
            }
        }
    }

    /**
     * Debounce function
     * @param {Function} func Function to debounce
     * @param {number} wait Wait time in milliseconds
     * @returns {Function} Debounced function
     */
    debounce(func, wait) {
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
}

// Create global instance
const sidebarManager = new SidebarManager();

// Export for module usage
export default sidebarManager;