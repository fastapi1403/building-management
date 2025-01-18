// Search functionality
document.getElementById('searchBuilding').addEventListener('keyup', function(e) {
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

// Status filter
document.getElementById('statusFilter').addEventListener('change', function(e) {
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

async function saveBuilding() {
    const buildingId = document.getElementById('buildingId')?.value;
    const isEditing = !!buildingId;

    const buildingData = {
        name: document.getElementById('buildingName').value,
        total_floors: parseInt(document.getElementById('buildingFloors').value),
        description: document.getElementById('buildingDescription').value,
        created_at: isEditing ? null : '2025-01-18 07:52:04',
        created_by: isEditing ? null : 'fastapi1403',
        updated_at: '2025-01-18 07:52:04',
        updated_by: 'fastapi1403'
    };

    // Form validation with translations
    if (!validateBuildingData(buildingData)) {
        return false;
    }

    try {
        // Show loading state with translations
        Swal.fire({
            title: langManager.translate('common.loading'),
            text: langManager.translate(isEditing ? 'buildings.messages.updating' : 'buildings.messages.saving'),
            allowOutsideClick: false,
            allowEscapeKey: false,
            showConfirmButton: false,
            didOpen: () => {
                Swal.showLoading();
            }
        });

        // Success message with translations
        await Swal.fire({
            title: langManager.translate('common.success'),
            text: langManager.translate(isEditing ? 'buildings.messages.updateSuccess' : 'buildings.messages.createSuccess'),
            icon: 'success',
            confirmButtonColor: '#198754',
            timer: 2000,
            timerProgressBar: true
        });

    } catch (error) {
        console.error('Error:', error);
        Swal.fire({
            title: langManager.translate('common.error'),
            text: error.message || langManager.translate('buildings.messages.saveError'),
            icon: 'error',
            confirmButtonColor: '#dc3545'
        });
    }
}

// Function to add a new building card to the UI
function addNewBuildingCard(building) {
    const buildingsContainer = document.querySelector('.row.g-4');
    const newBuildingHtml = `
        <div class="col-md-6 col-lg-4" data-building-id="${building.id}">
            <div class="card building-card">
                <div class="card-body">
                    <div class="d-flex justify-content-between align-items-center mb-3">
                        <h5 class="card-title mb-0">${building.name}</h5>
                        <span class="status-badge ${building.is_deleted ? 'status-inactive' : 'status-active'}">
                            ${building.is_deleted ? 'Deleted' : 'Active'}
                        </span>
                    </div>

                    <div class="building-stats mb-3">
                        <div class="row g-2">
                            <div class="col-6">
                                <div class="d-flex align-items-center">
                                    <i class="fas fa-building me-2"></i>
                                    <span>${building.total_floors} Floors</span>
                                </div>
                            </div>
                            <div class="col-6">
                                <div class="d-flex align-items-center">
                                    <i class="fas fa-door-open me-2"></i>
                                    <span>28 Units</span>
                                </div>
                            </div>
                            <div class="col-6">
                                <div class="d-flex align-items-center">
                                    <i class="fas fa-user-check me-2"></i>
                                    <span>100% Occupied</span>
                                </div>
                            </div>
                            <div class="col-6">
                                <div class="d-flex align-items-center">
                                    <i class="fas fa-calendar-check me-2"></i>
                                    <span>2025</span>
                                </div>
                            </div>
                        </div>
                    </div>

                    <div class="progress mb-3" style="height: 6px;">
                        <div class="progress-bar bg-success"
                             role="progressbar"
                             style="width: 50%"
                             aria-valuenow="50"
                             aria-valuemin="0"
                             aria-valuemax="100">
                        </div>
                    </div>

                    <div class="d-flex justify-content-between align-items-center action-buttons">
                        <a href="" class="btn btn-outline-primary">
                            <i class="fas fa-eye me-1"></i>Details
                        </a>
                        <div class="btn-group">
                            <button type="button"
                                    class="btn btn-outline-secondary"
                                    onclick="editBuilding('${building.id}')">
                                <i class="fas fa-edit"></i>
                            </button>
                            <button type="button"
                                    class="btn btn-outline-danger"
                                    onclick="deleteBuilding('${building.id}')">
                                <i class="fas fa-trash"></i>
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `;

    // Add the new building card to the beginning of the container
    buildingsContainer.insertAdjacentHTML('afterbegin', newBuildingHtml);
}

// Function to update existing building card
function updateBuildingCard(building) {
    const buildingCard = document.querySelector(`[data-building-id="${building.id}"]`);
    if (buildingCard) {
        buildingCard.querySelector('.card-title').textContent = building.name;
        const floorsElement = buildingCard.querySelector('.fa-building').nextElementSibling;
        if (floorsElement) {
            floorsElement.textContent = `${building.total_floors} Floors`;
        }
        const statusBadge = buildingCard.querySelector('.status-badge');
        if (statusBadge) {
            statusBadge.className = `status-badge ${building.is_deleted ? 'status-inactive' : 'status-active'}`;
            statusBadge.textContent = building.is_deleted ? 'Deleted' : 'Active';
        }
        buildingCard.classList.add('building-updated');
        setTimeout(() => {
            buildingCard.classList.remove('building-updated');
        }, 1000);
    }
}

// Helper function to reset form and validation states
function resetForm() {
    const form = document.getElementById('buildingForm');
    form.reset();

    const buildingIdInput = document.getElementById('buildingId');
    if (buildingIdInput) {
        buildingIdInput.value = '';
    }

    form.querySelectorAll('.is-valid, .is-invalid').forEach(element => {
        element.classList.remove('is-valid', 'is-invalid');
    });

    const modalTitle = document.querySelector('#addBuildingModal .modal-title');
    if (modalTitle) {
        modalTitle.textContent = 'Add New Building';
    }
}

// Modified editBuilding function to prepare the form for editing
function editBuilding(buildingId) {
    try {
        Swal.fire({
            title: 'Loading...',
            text: 'Fetching building details',
            allowOutsideClick: false,
            allowEscapeKey: false,
            showConfirmButton: false,
            didOpen: () => {
                Swal.showLoading();
            }
        });

        fetch(`/api/v1/buildings/${buildingId}`)
            .then(response => {
                if (!response.ok) throw new Error('Failed to fetch building details');
                return response.json();
            })
            .then(building => {
                const modalTitle = document.querySelector('#addBuildingModal .modal-title');
                modalTitle.textContent = 'Edit Building';

                const buildingIdInput = document.getElementById('buildingId');
                if (!buildingIdInput) {
                    const input = document.createElement('input');
                    input.type = 'hidden';
                    input.id = 'buildingId';
                    document.getElementById('buildingForm').appendChild(input);
                }
                document.getElementById('buildingId').value = buildingId;

                document.getElementById('buildingName').value = building.name || '';
                document.getElementById('buildingFloors').value = building.total_floors || '';
                document.getElementById('buildingDescription').value = building.description || '';

                Swal.close();
                const modal = new bootstrap.Modal(document.getElementById('addBuildingModal'));
                modal.show();
            })
            .catch(error => {
                console.error('Error:', error);
                Swal.fire({
                    title: 'Error!',
                    text: 'Failed to load building details. Please try again.',
                    icon: 'error',
                    confirmButtonColor: '#dc3545'
                });
            });
    } catch (error) {
        console.error('Error:', error);
        Swal.fire({
            title: 'Error!',
            text: 'An unexpected error occurred. Please try again.',
            icon: 'error',
            confirmButtonColor: '#dc3545'
        });
    }
}

// Add event listeners when document is ready
document.addEventListener('DOMContentLoaded', function() {
    // Initialize form validation
    const form = document.getElementById('buildingForm');
    form.addEventListener('submit', function(e) {
        e.preventDefault();
        saveBuilding();
    });

    // Add modal hidden event listener to reset form
    const modal = document.getElementById('addBuildingModal');
    modal.addEventListener('hidden.bs.modal', function() {
        resetForm();
    });

    // Initialize translations
    langManager.translatePage();

    // Form validation on input
    document.querySelectorAll('#buildingForm input, #buildingForm select').forEach(element => {
        element.addEventListener('input', function(e) {
            this.classList.remove('is-invalid', 'is-valid');
            this.classList.add(this.checkValidity() ? 'is-valid' : 'is-invalid');
        });
    });
});

// Building operations
async function deleteBuilding(buildingId) {
    const result = await Swal.fire({
        title: langManager.translate('buildings.delete'),
        text: langManager.translate('buildings.deleteConfirmation'),
        icon: langManager.translate('common.warning'),
        showCancelButton: true,
        confirmButtonColor: '#dc3545',
        cancelButtonColor: '#6c757d',
        confirmButtonText: langManager.translate('buildings.deleteConfirmButton'),
        cancelButtonText: langManager.translate('common.cancel'),
        reverseButtons: true
    });

    if (result.isConfirmed) {
        try {
            Swal.fire({
                title: langManager.translate('buildings.deleting'),
                text: langManager.translate('buildings.deleteWait'),
                allowOutsideClick: false,
                allowEscapeKey: false,
                showConfirmButton: false,
                didOpen: () => {
                    Swal.showLoading();
                }
            });

            const response = await fetch(`/api/v1/buildings/${buildingId}`, {
                method: 'DELETE',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCsrfToken(),
                    'Accept': 'application/json'
                }
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || langManager.translate('buildings.deleteFail'));
            }

            await Swal.fire({
                title: langManager.translate('buildings.statusDeleted') + '!',
                text: langManager.translate('buildings.deleteSuccess'),
                icon: langManager.translate('common.success'),
                confirmButtonColor: '#198754',
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
                icon: 'error',
                confirmButtonColor: '#dc3545'
            });
        }
    }
}

// Validation function
function validateBuildingData(data) {
    const requiredFields = ['name', 'total_floors'];

    for (const field of requiredFields) {
        if (!data[field]) {
            Swal.fire({
                title: langManager.translate('buildings.validationError'),
                text: `${field.replace('_', ' ').toUpperCase()} ${langManager.translate('buildings.required')}`,
                icon: 'error',
                confirmButtonText: 'OK'
            });
            return false;
        }
    }

    if (data.total_floors < 1) {
        Swal.fire({
            title: langManager.translate('buildings.validationError'),
            text: langManager.translate('buildings.validationFloors'),
            icon: langManager.translate('common.error'),
            confirmButtonText: langManager.translate('common.ok')
        });
        return false;
    }

    return true;
}