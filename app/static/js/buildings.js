// Search functionality
// document.getElementById('searchBuilding').addEventListener('keyup', function(e) {
//     const searchTerm = e.target.value.toLowerCase();
//     const buildingCards = document.querySelectorAll('.building-card');
//
//     buildingCards.forEach(card => {
//         const buildingName = card.querySelector('.card-title').textContent.toLowerCase();
//         if (buildingName.includes(searchTerm)) {
//             card.closest('.col-md-6').style.display = '';
//         } else {
//             card.closest('.col-md-6').style.display = 'none';
//         }
//     });
// });
//
// // Status filter
// document.getElementById('statusFilter').addEventListener('change', function(e) {
//     const status = e.target.value.toLowerCase();
//     const buildingCards = document.querySelectorAll('.building-card');
//
//     buildingCards.forEach(card => {
//         const buildingStatus = card.querySelector('.status-badge').textContent.trim().toLowerCase();
//         if (status === '' || buildingStatus === status) {
//             card.closest('.col-md-6').style.display = '';
//         } else {
//             card.closest('.col-md-6').style.display = 'none';
//         }
//     });
// });

// Function to update existing building card
function updateBuildingCard(building) {
    const buildingCard = document.querySelector(`[data-building-id="${building.id}"]`);
    if (buildingCard) {
        // Update building name
        buildingCard.querySelector('.card-title').textContent = building.name;

        // Update floors
        const floorsElement = buildingCard.querySelector('.fa-building').nextElementSibling;
        if (floorsElement) {
            floorsElement.textContent = `${building.total_floors} Floors`;
        }

        // Update status badge
        const statusBadge = buildingCard.querySelector('.status-badge');
        if (statusBadge) {
            statusBadge.className = `status-badge ${building.is_deleted ? 'status-inactive' : 'status-active'}`;
            statusBadge.textContent = building.is_deleted ? 'Deleted' : 'Active';
        }

        // Update description if it exists
        const descriptionElement = buildingCard.querySelector('.building-description');
        if (descriptionElement && building.description) {
            descriptionElement.textContent = building.description;
        }

        // Add animation to show the card was updated
        buildingCard.classList.add('building-updated');
        setTimeout(() => {
            buildingCard.classList.remove('building-updated');
        }, 1000);

        // Update dynamic data
        const updateInfo = buildingCard.querySelector('.update-info');
        if (updateInfo) {
            updateInfo.textContent = `Updated: ${building.updated_at}`;
        }

        // Add CSS animation to highlight the update
        buildingCard.style.transition = 'background-color 0.5s ease';
        buildingCard.style.backgroundColor = '#e8f5e9';
        setTimeout(() => {
            buildingCard.style.backgroundColor = '';
        }, 1500);

        // Translate any new content
        langManager.translatePage();
    } else {
        // If card doesn't exist, reload the page
        console.log('Building card not found, reloading page...');
        window.location.reload();
    }
}

// Update saveBuilding function to handle the response better
async function saveBuilding() {
    const buildingId = document.getElementById('buildingId')?.value;
    const isEditing = !!buildingId;

    const buildingData = {
        name: document.getElementById('buildingName').value,
        total_floors: parseInt(document.getElementById('buildingFloors').value),
        description: document.getElementById('buildingDescription').value,
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

        // Make API call to save/update building
        const url = isEditing
            ? `/api/v1/buildings/${buildingId}`
            : '/api/v1/buildings';

        const response = await fetch(url, {
            method: isEditing ? 'PUT' : 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCsrfToken(),
                'Accept': 'application/json'
            },
            body: JSON.stringify(buildingData)
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || langManager.translate('buildings.messages.saveError'));
        }

        const savedBuilding = await response.json();

        // Success message with translations
        await Swal.fire({
            title: langManager.translate('common.success'),
            text: langManager.translate(isEditing ? 'buildings.messages.updateSuccess' : 'buildings.messages.createSuccess'),
            icon: 'success',
            confirmButtonColor: '#198754',
            timer: 2000,
            timerProgressBar: true
        });

        // Update UI
        if (isEditing) {
            updateBuildingCard(savedBuilding);
        } else {
            addNewBuildingCard(savedBuilding);
        }

        // Close modal
        const modal = bootstrap.Modal.getInstance(document.getElementById('addBuildingModal'));
        if (modal) {
            modal.hide();
        }

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
                                    <span>${building.total_floors} <span data-i18n="buildings.floors"></span>
                                </div>
                            </div>
                            <div class="col-6">
                                <div class="d-flex align-items-center">
                                    <i class="fas fa-door-open me-2"></i>
                                    <span>28 <span data-i18n="buildings.units"></span></span>
                                </div>
                            </div>
                            <div class="col-6">
                                <div class="d-flex align-items-center">
                                    <i class="fas fa-user-check me-2"></i>
                                    <span>100% <span data-i18n="buildings.occupied"></span></span>
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
                        <div class="">
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
async function editBuilding(buildingId) {
    try {
        await Swal.fire({
            title: langManager.translate('common.loading'),
            text: langManager.translate('buildings.messages.loading'),
            allowOutsideClick: false,
            allowEscapeKey: false,
            showConfirmButton: false,
            didOpen: () => {
                Swal.showLoading();
            }
        });

        const response = await fetch(`/api/v1/buildings/${buildingId}`);
        if (!response.ok) {
            throw new Error(langManager.translate('buildings.messages.fetchError'));
        }

        const building = await response.json();

        // Ensure modal exists in DOM
        let modal = document.getElementById('addBuildingModal');
        if (!modal) {
            // If modal doesn't exist, create it
            const modalHTML = `
                <div class="modal fade" id="addBuildingModal" tabindex="-1" aria-labelledby="addBuildingModalLabel" aria-hidden="true">
                    <div class="modal-dialog">
                        <div class="modal-content">
                            <div class="modal-header">
                                <h5 class="modal-title" id="addBuildingModalLabel">${langManager.translate('buildings.edit')}</h5>
                                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                            </div>
                            <div class="modal-body">
                                <form id="buildingForm">
                                    <input type="hidden" id="buildingId">
                                    <div class="mb-3">
                                        <label for="buildingName" class="form-label" data-i18n="buildings.name"></label>
                                        <input type="text" class="form-control" id="buildingName" required>
                                    </div>
                                    <div class="mb-3">
                                        <label for="buildingFloors" class="form-label" data-i18n="buildings.floors"></label>
                                        <input type="number" class="form-control" id="buildingFloors" required min="1">
                                    </div>
                                    <div class="mb-3">
                                        <label for="buildingDescription" class="form-label" data-i18n="buildings.description"></label>
                                        <textarea class="form-control" id="buildingDescription" rows="3"></textarea>
                                    </div>
                                </form>
                            </div>
                            <div class="modal-footer">
                                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal" data-i18n="common.cancel"></button>
                                <button type="button" class="btn btn-primary" onclick="saveBuilding()" data-i18n="common.save"></button>
                            </div>
                        </div>
                    </div>
                </div>
            `;
            document.body.insertAdjacentHTML('beforeend', modalHTML);
            modal = document.getElementById('addBuildingModal');
        }

        // Now we can safely access modal elements
        const modalTitle = modal.querySelector('.modal-title');
        if (modalTitle) {
            modalTitle.textContent = langManager.translate('buildings.edit');
        }

        // Set form values
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

        // Close loading dialog
        await Swal.close();

        // Show modal
        const bsModal = new bootstrap.Modal(modal);
        bsModal.show();

        // Initialize translations for new modal content
        langManager.translatePage();

    } catch (error) {
        console.error('Error:', error);
        Swal.fire({
            title: langManager.translate('common.error'),
            text: error.message || langManager.translate('buildings.messages.editError'),
            icon: 'error',
            confirmButtonColor: '#dc3545'
        });
    }
}


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

// Building Detail Page Functions
function restoreBuilding(buildingId) {
    return Swal.fire({
        title: langManager.translate('buildings.restore'),
        text: langManager.translate('buildings.restoreConfirmation'),
        icon: 'question',
        showCancelButton: true,
        confirmButtonColor: '#198754',
        cancelButtonColor: '#6c757d',
        confirmButtonText: langManager.translate('buildings.restoreConfirmButton'),
        cancelButtonText: langManager.translate('common.cancel')
    }).then(async (result) => {
        if (result.isConfirmed) {
            try {
                const response = await fetch(`/api/v1/buildings/${buildingId}/restore`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCsrfToken()
                    }
                });

                if (!response.ok) throw new Error(langManager.translate('buildings.restoreFail'));

                await Swal.fire({
                    title: langManager.translate('common.success'),
                    text: langManager.translate('buildings.restoreSuccess'),
                    icon: 'success',
                    timer: 2000
                });

                // Refresh the page to show updated status
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
    });
}

// Modified editBuilding for detail page
function editBuildingDetail(buildingId) {
    window.location.href = `/buildings#edit-${buildingId}`;
}

// Initialize the page functionality based on existing elements
function initializePage() {
    // Only initialize features if we're on the buildings list page
    // Check if we're on the buildings list page by looking for a unique element
    const isBuildingsListPage = !!document.querySelector('.buildings-container');

    if (isBuildingsListPage) {
        // Search functionality - only initialize if search element exists
        const searchBuilding = document.getElementById('searchBuilding');
        if (searchBuilding) {
            searchBuilding.addEventListener('keyup', function(e) {
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

        // Status filter - only initialize if filter element exists
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

        // Form initialization - only if form exists
        const buildingForm = document.getElementById('buildingForm');
        if (buildingForm) {
            buildingForm.addEventListener('submit', function(e) {
                e.preventDefault();
                saveBuilding();
            });

            // Form validation on input
            buildingForm.querySelectorAll('input, select').forEach(element => {
                element.addEventListener('input', function(e) {
                    this.classList.remove('is-invalid', 'is-valid');
                    this.classList.add(this.checkValidity() ? 'is-valid' : 'is-invalid');
                });
            });
        }

        // Modal initialization - only if modal exists
        const addBuildingModal = document.getElementById('addBuildingModal');
        if (addBuildingModal) {
            addBuildingModal.addEventListener('hidden.bs.modal', function() {
                resetForm();
            });
        }
    }

}

// Call initialization when DOM is ready
document.addEventListener('DOMContentLoaded', initializePage);
