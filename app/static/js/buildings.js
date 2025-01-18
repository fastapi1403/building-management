// buildings.js

// Global language manager for translations
const BuildingManager = {
    // Initialize all event listeners and setup
    init: function() {
        document.addEventListener('DOMContentLoaded', () => {
            // Initialize translations
            langManager.translatePage();

            // Initialize search functionality
            this.initSearch();

            // Initialize status filter
            this.initStatusFilter();

            // Initialize form validation
            this.initFormValidation();

            // Initialize modal events
            this.initModalEvents();
        });
    },

    // Search functionality
    initSearch: function() {
        const searchInput = document.getElementById('searchBuilding');
        if (searchInput) {
            searchInput.addEventListener('keyup', function(e) {
                const searchTerm = e.target.value.toLowerCase();
                const buildingCards = document.querySelectorAll('.building-card');

                buildingCards.forEach(card => {
                    const buildingName = card.querySelector('.card-title').textContent.toLowerCase();
                    if (buildingName.includes(searchTerm)) {
                        card.closest('.col-md-6').style.display = '';
                    } else {
                        card.closest('.col-md-6').style.display = 'none';
                    }
                });
            });
        }
    },

    // Status filter initialization
    initStatusFilter: function() {
        const statusFilter = document.getElementById('statusFilter');
        if (statusFilter) {
            statusFilter.addEventListener('change', function(e) {
                const status = e.target.value.toLowerCase();
                const buildingCards = document.querySelectorAll('.building-card');

                buildingCards.forEach(card => {
                    const buildingStatus = card.querySelector('.status-badge').textContent.trim().toLowerCase();
                    if (status === '' || buildingStatus === status) {
                        card.closest('.col-md-6').style.display = '';
                    } else {
                        card.closest('.col-md-6').style.display = 'none';
                    }
                });
            });
        }
    },

    // Form validation initialization
    initFormValidation: function() {
        const form = document.getElementById('buildingForm');
        if (form) {
            form.addEventListener('submit', function(e) {
                e.preventDefault();
                BuildingManager.saveBuilding();
            });

            form.querySelectorAll('input, textarea').forEach(element => {
                element.addEventListener('input', function() {
                    this.classList.remove('is-invalid', 'is-valid');
                    this.classList.add(this.checkValidity() ? 'is-valid' : 'is-invalid');
                });
            });
        }
    },

    // Modal events initialization
    initModalEvents: function() {
        const modal = document.getElementById('addBuildingModal');
        if (modal) {
            modal.addEventListener('hidden.bs.modal', function() {
                BuildingManager.resetForm();
            });
        }
    },

    // Save building function
    saveBuilding: async function() {
        const buildingId = document.getElementById('buildingId')?.value;
        const isEditing = !!buildingId;

        const buildingData = {
            name: document.getElementById('buildingName').value,
            total_floors: parseInt(document.getElementById('buildingFloors').value),
            description: document.getElementById('buildingDescription').value,
            created_at: isEditing ? null : '2025-01-18 16:32:19',
            created_by: isEditing ? null : 'fastapi1403',
            updated_at: '2025-01-18 16:32:19',
            updated_by: 'fastapi1403'
        };

        if (!this.validateBuildingData(buildingData)) {
            return false;
        }

        try {
            await Swal.fire({
                title: langManager.translate('common.loading'),
                text: langManager.translate(isEditing ? 'buildings.messages.updating' : 'buildings.messages.saving'),
                allowOutsideClick: false,
                didOpen: () => Swal.showLoading()
            });

            const url = buildingId ? `/buildings/${buildingId}/edit` : '/buildings';
            const method = buildingId ? 'PUT' : 'POST';

            const response = await fetch(url, {
                method: method,
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': this.getCsrfToken()
                },
                body: JSON.stringify(buildingData)
            });

            if (!response.ok) {
                throw new Error(await response.text());
            }

            const result = await response.json();

            await Swal.fire({
                title: langManager.translate('common.success'),
                text: langManager.translate(isEditing ? 'buildings.messages.updateSuccess' : 'buildings.messages.createSuccess'),
                icon: 'success',
                timer: 2000,
                timerProgressBar: true
            });

            if (isEditing) {
                this.updateBuildingCard(result);
            } else {
                this.addNewBuildingCard(result);
            }

            bootstrap.Modal.getInstance(document.getElementById('addBuildingModal')).hide();

        } catch (error) {
            console.error('Error:', error);
            Swal.fire({
                title: langManager.translate('common.error'),
                text: error.message || langManager.translate('buildings.messages.saveError'),
                icon: 'error'
            });
        }
    },

    // Edit building function
    editBuilding: async function(buildingId) {
        if (document.querySelector(`[data-building-id="${buildingId}"] .status-badge`).classList.contains('status-inactive')) {
            Swal.fire({
                title: langManager.translate('common.error'),
                text: langManager.translate('buildings.cannotEditDeleted'),
                icon: 'error'
            });
            return;
        }

        try {
            await Swal.fire({
                title: langManager.translate('buildings.loading'),
                text: langManager.translate('buildings.fetchingDetails'),
                allowOutsideClick: false,
                didOpen: () => Swal.showLoading()
            });

            const response = await fetch(`/api/v1/buildings/${buildingId}`);
            if (!response.ok) throw new Error('Failed to fetch building details');

            const building = await response.json();

            document.getElementById('buildingId').value = buildingId;
            document.getElementById('buildingName').value = building.name;
            document.getElementById('buildingFloors').value = building.total_floors;
            document.getElementById('buildingDescription').value = building.description;

            document.querySelector('#addBuildingModal .modal-title').textContent =
                langManager.translate('buildings.editBuilding');

            Swal.close();
            const modal = new bootstrap.Modal(document.getElementById('addBuildingModal'));
            modal.show();

        } catch (error) {
            console.error('Error:', error);
            Swal.fire({
                title: langManager.translate('common.error'),
                text: langManager.translate('buildings.loadError'),
                icon: 'error'
            });
        }
    },

    // Delete building function
    deleteBuilding: async function(buildingId) {
        const result = await Swal.fire({
            title: langManager.translate('buildings.delete'),
            text: langManager.translate('buildings.deleteConfirmation'),
            icon: 'warning',
            showCancelButton: true,
            confirmButtonColor: '#dc3545',
            cancelButtonColor: '#6c757d',
            confirmButtonText: langManager.translate('buildings.deleteConfirmButton'),
            cancelButtonText: langManager.translate('common.cancel')
        });

        if (result.isConfirmed) {
            try {
                await Swal.fire({
                    title: langManager.translate('buildings.deleting'),
                    text: langManager.translate('buildings.deleteWait'),
                    allowOutsideClick: false,
                    didOpen: () => Swal.showLoading()
                });

                const response = await fetch(`/api/v1/buildings/${buildingId}`, {
                    method: 'DELETE',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': this.getCsrfToken()
                    }
                });

                if (!response.ok) {
                    const errorData = await response.json();
                    throw new Error(errorData.detail || langManager.translate('buildings.deleteFail'));
                }

                await Swal.fire({
                    title: langManager.translate('common.success'),
                    text: langManager.translate('buildings.deleteSuccess'),
                    icon: 'success',
                    timer: 2000,
                    timerProgressBar: true
                });

                const buildingElement = document.querySelector(`[data-building-id="${buildingId}"]`);
                if (buildingElement) {
                    buildingElement.remove();
                } else {
                    window.location.reload();
                }

            } catch (error) {
                console.error(langManager.translate('buildings.errorDeletingBuilding'), error);
                Swal.fire({
                    title: langManager.translate('common.error'),
                    text: error.message || langManager.translate('buildings.deleteError'),
                    icon: 'error'
                });
            }
        }
    },

    // Restore building function
    restoreBuilding: async function(buildingId) {
        const result = await Swal.fire({
            title: langManager.translate('buildings.restore'),
            text: langManager.translate('buildings.restoreConfirmation'),
            icon: 'question',
            showCancelButton: true,
            confirmButtonColor: '#198754',
            cancelButtonColor: '#6c757d',
            confirmButtonText: langManager.translate('buildings.restoreConfirmButton'),
            cancelButtonText: langManager.translate('common.cancel')
        });

        if (result.isConfirmed) {
            try {
                const response = await fetch(`/api/v1/buildings/${buildingId}/restore`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': this.getCsrfToken()
                    }
                });

                if (!response.ok) throw new Error(langManager.translate('buildings.restoreFail'));

                await Swal.fire({
                    title: langManager.translate('common.success'),
                    text: langManager.translate('buildings.restoreSuccess'),
                    icon: 'success',
                    timer: 2000
                });

                window.location.reload();
            } catch (error) {
                console.error('Error:', error);
                Swal.fire({
                    title: langManager.translate('common.error'),
                    text: error.message,
                    icon: 'error'
                });
            }
        }
    },

    // Utility functions
    validateBuildingData: function(data) {
        const requiredFields = ['name', 'total_floors'];

        for (const field of requiredFields) {
            if (!data[field]) {
                Swal.fire({
                    title: langManager.translate('buildings.validationError'),
                    text: `${field.replace('_', ' ').toUpperCase()} ${langManager.translate('buildings.required')}`,
                    icon: 'error'
                });
                return false;
            }
        }

        if (data.total_floors < 1) {
            Swal.fire({
                title: langManager.translate('buildings.validationError'),
                text: langManager.translate('buildings.validationFloors'),
                icon: 'error'
            });
            return false;
        }

        return true;
    },

    resetForm: function() {
        const form = document.getElementById('buildingForm');
        if (form) {
            form.reset();
            form.querySelectorAll('.is-valid, .is-invalid').forEach(element => {
                element.classList.remove('is-valid', 'is-invalid');
            });
            document.getElementById('buildingId').value = '';
            document.querySelector('#addBuildingModal .modal-title').textContent =
                langManager.translate('buildings.addNew');
        }
    },

    getCsrfToken: function() {
        const name = 'csrftoken';
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    },

    // DOM manipulation functions
    addNewBuildingCard: function(building) {
        const buildingsContainer = document.querySelector('.row.g-4');
        const newBuildingHtml = this.generateBuildingCardHtml(building);
        buildingsContainer.insertAdjacentHTML('afterbegin', newBuildingHtml);
    },

    updateBuildingCard: function(building) {
        const buildingCard = document.querySelector(`[data-building-id="${building.id}"]`);
        if (buildingCard) {
            buildingCard.querySelector('.card-title').textContent = building.name;
            buildingCard.querySelector('.fa-building').nextElementSibling.textContent =
                `${building.total_floors} ${langManager.translate('buildings.floors')}`;

            buildingCard.classList.add('building-updated');
            setTimeout(() => buildingCard.classList.remove('building-updated'), 1000);
        }
    },

    generateBuildingCardHtml: function(building) {
        return `
            <div class="col-md-6 col-lg-4" data-building-id="${building.id}">
                <!-- Building card HTML template -->
            </div>
        `;
    }
};

// Initialize the BuildingManager when the script loads
BuildingManager.init();

// Export for module usage if needed
if (typeof module !== 'undefined' && module.exports) {
    module.exports = BuildingManager;
}