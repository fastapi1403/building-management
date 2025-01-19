// Owner management functions
async function createOwner() {
    try {
        // First, fetch the buildings list
        const buildingsResponse = await fetch('/api/v1/buildings');
        if (!buildingsResponse.ok) {
            throw new Error('Failed to fetch buildings');
        }
        const buildings = await buildingsResponse.json();

        // Create building options HTML
        const buildingOptions = buildings
            .filter(building => !building.is_deleted)
            .map(building => `
                <option value="${building.id}">${building.name}</option>
            `).join('');

        let modal = document.getElementById('addOwnerModal');
        if (!modal) {
            const modalHTML = `
                <div class="modal fade" id="addOwnerModal" tabindex="-1" aria-labelledby="addOwnerModalLabel" aria-hidden="true">
                    <div class="modal-dialog">
                        <div class="modal-content">
                            <div class="modal-header">
                                <h5 class="modal-title" id="addOwnerModalLabel">${langManager.translate('owners.add')}</h5>
                                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                            </div>
                            <div class="modal-body">
                                <form id="ownerForm">
                                    <input type="hidden" id="ownerId">
                                    <div class="mb-3">
                                        <label for="buildingId" class="form-label">${langManager.translate('owners.form.building')}</label>
                                        <select class="form-select" id="buildingId" required>
                                            <option value="">${langManager.translate('owners.form.selectBuilding')}</option>
                                            ${buildingOptions}
                                        </select>
                                    </div>
                                    <div class="mb-3">
                                        <label for="ownerName" class="form-label">${langManager.translate('owners.formName')}</label>
                                        <input type="text" class="form-control" id="ownerName" required>
                                    </div>
                                    <div class="mb-3">
                                        <label for="ownerNumber" class="form-label">${langManager.translate('owners.formNumber')}</label>
                                        <input type="number" class="form-control" id="ownerNumber" required min="1">
                                    </div>
                                    <div class="mb-3">
                                        <label for="totalUnits" class="form-label">${langManager.translate('owners.formUnits')}</label>
                                        <input type="number" class="form-control" id="totalUnits" required min="1">
                                    </div>
                                    <div class="mb-3">
                                        <label for="description" class="form-label">${langManager.translate('owners.form.description')}</label>
                                        <textarea class="form-control" id="description" rows="3" 
                                                 placeholder="${langManager.translate('owners.form.descriptionPlaceholder')}"></textarea>
                                    </div>
                                </form>
                            </div>
                            <div class="modal-footer">
                                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">
                                    ${langManager.translate('owners.formCancel')}
                                </button>
                                <button type="button" class="btn btn-primary" onclick="saveOwner()">
                                    ${langManager.translate('owners.formSave')}
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            `;
            document.body.insertAdjacentHTML('beforeend', modalHTML);
            modal = document.getElementById('addOwnerModal');
        }

        resetForm();
        const bsModal = new bootstrap.Modal(modal);
        bsModal.show();
        langManager.translatePage();
    } catch (error) {
        console.error('Error:', error);
        Swal.fire({
            title: langManager.translate('common.error'),
            text: error.message || langManager.translate('owners.messages.createError'),
            icon: 'error',
            confirmButtonColor: '#dc3545'
        });
    }
}

// Update the saveOwner function to include building_id and description
async function saveOwner() {
    try {
        const ownerId = document.getElementById('ownerId')?.value;
        const isEditing = !!ownerId;

        const ownerData = {
            building_id: document.getElementById('buildingId').value,
            name: document.getElementById('ownerName').value,
            number: parseInt(document.getElementById('ownerNumber').value),
            total_units: parseInt(document.getElementById('totalUnits').value),
            description: document.getElementById('description').value
        };

        // Validate data
        if (!validateOwnerData(ownerData)) {
            return false;
        }

        // Show loading state
        Swal.fire({
            title: langManager.translate(isEditing ? 'owners.messages.updating' : 'owners.messages.saving'),
            allowOutsideClick: false,
            allowEscapeKey: false,
            showConfirmButton: false,
            didOpen: () => {
                Swal.showLoading();
            }
        });

        const url = isEditing ? `/api/v1/owners/${ownerId}` : '/api/v1/owners';
        const method = isEditing ? 'PUT' : 'POST';

        const response = await fetch(url, {
            method: method,
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCsrfToken()
            },
            body: JSON.stringify(ownerData)
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || langManager.translate(
                isEditing ? 'owners.messages.updateError' : 'owners.messages.saveError'
            ));
        }

        const savedOwner = await response.json();

        await Swal.fire({
            icon: 'success',
            title: langManager.translate(
                isEditing ? 'owners.messages.updateSuccess' : 'owners.messages.saveSuccess'
            ),
            timer: 1500,
            showConfirmButton: false,
            timerProgressBar: true
        });

        if (isEditing) {
            updateOwnerCard(savedOwner);
        } else {
            addNewOwnerCard(savedOwner);
        }

        const modal = bootstrap.Modal.getInstance(document.getElementById('addOwnerModal'));
        if (modal) {
            modal.hide();
        }

        return true;

    } catch (error) {
        console.error('Error:', error);
        Swal.fire({
            icon: 'error',
            title: langManager.translate('common.error'),
            text: error.message,
            confirmButtonColor: '#dc3545'
        });
        return false;
    }
}

// Update the validation function to include building_id
function validateOwnerData(data) {
    if (!data.building_id) {
        Swal.fire({
            icon: 'error',
            title: langManager.translate('common.error'),
            text: langManager.translate('owners.form.buildingRequired'),
            confirmButtonColor: '#dc3545'
        });
        return false;
    }

    if (!data.name || !data.number || !data.total_units) {
        Swal.fire({
            icon: 'error',
            title: langManager.translate('common.error'),
            text: langManager.translate('owners.validation.requiredFields'),
            confirmButtonColor: '#dc3545'
        });
        return false;
    }

    if (data.number <= 0) {
        Swal.fire({
            icon: 'error',
            title: langManager.translate('common.error'),
            text: langManager.translate('owners.validation.invalidNumber'),
            confirmButtonColor: '#dc3545'
        });
        return false;
    }

    if (data.total_units <= 0) {
        Swal.fire({
            icon: 'error',
            title: langManager.translate('common.error'),
            text: langManager.translate('owners.validation.invalidUnits'),
            confirmButtonColor: '#dc3545'
        });
        return false;
    }

    return true;
}

async function editOwner(ownerId) {
    try {
        const response = await fetch(`/api/v1/owners/${ownerId}`);
        const owner = await response.json();

        // First, fetch the buildings list
        const buildingsResponse = await fetch('/api/v1/buildings');
        if (!buildingsResponse.ok) {
            throw new Error('Failed to fetch buildings');
        }
        const buildings = await buildingsResponse.json();

        // Create building options HTML
        const buildingOptions = buildings
            .filter(building => !building.is_deleted)
            .map(building =>
                `<option value="${building.id}"` +
                (building.id === owner.building_id ? ' selected="selected"' : '') +
                `>${building.name}</option>`
            ).join('');

        let modal = document.getElementById('editOwnerModal');
        if (!modal) {
            const modalHTML = `
                <div class="modal fade" id="editOwnerModal" tabindex="-1" aria-labelledby="editOwnerModalLabel" aria-hidden="true">
                    <div class="modal-dialog">
                        <div class="modal-content">
                            <div class="modal-header">
                                <h5 class="modal-title" id="editOwnerModalLabel">${langManager.translate('owners.edit')}</h5>
                                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                            </div>
                            <div class="modal-body">
                                <form id="ownerForm">
                                    <input type="hidden" id="ownerId">
                                    <div class="mb-3">
                                        <label for="buildingId" class="form-label">${langManager.translate('owners.form.building')}</label>
                                        <select class="form-select" id="buildingId" required>
                                            <option value="">${langManager.translate('owners.form.selectBuilding')}</option>
                                            ${buildingOptions}
                                        </select>
                                    </div>
                                    <div class="mb-3">
                                        <label for="ownerName" class="form-label">${langManager.translate('owners.formName')}</label>
                                        <input type="text" class="form-control" id="ownerName" value="${owner.name}" required>
                                    </div>
                                    <div class="mb-3">
                                        <label for="ownerNumber" class="form-label">${langManager.translate('owners.formNumber')}</label>
                                        <input type="number" class="form-control" id="ownerNumber" value="${owner.number}" required min="1">
                                    </div>
                                    <div class="mb-3">
                                        <label for="totalUnits" class="form-label">${langManager.translate('owners.formUnits')}</label>
                                        <input type="number" class="form-control" id="totalUnits" value="${owner.total_units}" required min="1">
                                    </div>
                                    <div class="mb-3">
                                        <label for="description" class="form-label">${langManager.translate('owners.form.description')}</label>
                                        <textarea class="form-control" id="description" rows="3" 
                                                 placeholder="${langManager.translate('owners.form.descriptionPlaceholder')}">${owner.description}</textarea>
                                    </div>
                                </form>
                            </div>
                            <div class="modal-footer">
                                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">
                                    ${langManager.translate('owners.formCancel')}
                                </button>
                                <button type="button" class="btn btn-primary" onclick="saveOwner()">
                                    ${langManager.translate('owners.formSave')}
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            `;
            document.body.insertAdjacentHTML('beforeend', modalHTML);
            modal = document.getElementById('editOwnerModal');
        }

        const bsModal = new bootstrap.Modal(modal);
        bsModal.show();
        langManager.translatePage();

        // const response = await fetch(`/api/v1/owners/${ownerId}`);
        // const owner = await response.json();
        //
        // const { value: formValues } = await Swal.fire({
        //     title: langManager.translate('owners.edit'),
        //     html: `
        //         <input id="ownerName" class="swal2-input"
        //                placeholder="${langManager.translate('owners.formName')}" value="${owner.name}">
        //         <input id="ownerNumber" type="number" class="swal2-input"
        //                placeholder="${langManager.translate('owners.formNumber')}" value="${owner.number}">
        //         <input id="totalUnits" type="number" class="swal2-input"
        //                placeholder="${langManager.translate('owners.formUnits')}" value="${owner.total_units}">
        //         <input id="totalUnits" type="number" class="swal2-input"
        //                placeholder="${langManager.translate('owners.formDescription')}" value="${owner.total_units}">
        //     `,
        //     focusConfirm: false,
        //     showCancelButton: true,
        //     confirmButtonText: langManager.translate('owners.formSave'),
        //     cancelButtonText: langManager.translate('owners.formCancel'),
        //     preConfirm: () => {
        //         return {
        //             name: document.getElementById('ownerName').value,
        //             number: document.getElementById('ownerNumber').value,
        //             total_units: document.getElementById('totalUnits').value
        //         }
        //     }
        // });
        //
        // if (formValues) {
        //     const response = await fetch(`/api/v1/owners/${ownerId}`, {
        //         method: 'PUT',
        //         headers: {
        //             'Content-Type': 'application/json',
        //             'X-CSRFToken': getCsrfToken()
        //         },
        //         body: JSON.stringify(formValues)
        //     });
        //
        //     if (!response.ok) {
        //         throw new Error(langManager.translate('owners.messages.saveError'));
        //     }
        //
        //     await Swal.fire({
        //         icon: 'success',
        //         title: langManager.translate('owners.messages.updateSuccess'),
        //         showConfirmButton: false,
        //         timer: 1500
        //     });
        //
        //     window.location.reload();
        // }
    } catch (error) {
        console.error('Error:', error);
        Swal.fire({
            title: langManager.translate('common.error'),
            text: error.message || langManager.translate('owners.messages.editError'),
            icon: 'error',
            confirmButtonColor: '#dc3545'
        });
    }
}

async function deleteOwner(ownerId) {
    const result = await Swal.fire({
        title: langManager.translate('owners.delete'),
        text: langManager.translate('owners.deleteConfirmation'),
        icon: langManager.translate('common.warning'),
        showCancelButton: true,
        confirmButtonColor: '#dc3545',
        cancelButtonColor: '#6c757d',
        confirmButtonText: langManager.translate('owners.deleteConfirmButton'),
        cancelButtonText: langManager.translate('common.cancel')
    });

    if (result.isConfirmed) {
        try {
            const response = await fetch(`/api/v1/owners/${ownerId}`, {
                method: 'DELETE',
                headers: {
                    'X-CSRFToken': getCsrfToken()
                }
            });

            if (!response.ok) {
                throw new Error(langManager.translate('owners.messages.deleteFail'));
            }

            await Swal.fire({
                icon: 'success',
                title: langManager.translate('owners.messages.deleteSuccess'),
                showConfirmButton: false,
                timer: 1500
            });

            window.location.reload();
        } catch (error) {
            console.error('Error:', error);
            Swal.fire({
                title: langManager.translate('common.error'),
                text: error.message || langManager.translate('owners.messages.deleteError'),
                icon: 'error',
                confirmButtonColor: '#dc3545'
            });
        }
    }
}

async function restoreOwner(ownerId) {
    const result = await Swal.fire({
        title: langManager.translate('owners.restore'),
        text: langManager.translate('owners.restoreConfirmation'),
        icon: 'question',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: langManager.translate('owners.restoreConfirmButton'),
        cancelButtonText: langManager.translate('common.cancel')
    });

    if (result.isConfirmed) {
        try {
            const response = await fetch(`/api/v1/owners/${ownerId}/restore`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCsrfToken()
                }
            });

            if (!response.ok) {
                throw new Error(langManager.translate('owners.messages.restoreFail'));
            }

            await Swal.fire({
                icon: 'success',
                title: langManager.translate('owners.messages.restoreSuccess'),
                showConfirmButton: false,
                timer: 1500
            });

            window.location.reload();
        } catch (error) {
            console.error('Error:', error);
            Swal.fire({
                title: langManager.translate('common.error'),
                text: error.message || langManager.translate('owners.messages.restoreFail'),
                icon: 'error',
                confirmButtonColor: '#dc3545'
            });
        }
    }
}

// Filter and sort functionality
function filterOwners() {
    const searchTerm = searchInput.value.toLowerCase();
    const status = statusFilter.value;
    const sortValue = sortBy.value;

    const ownerCards = document.querySelectorAll('.owner-card');
    const ownerGrid = document.querySelector('.row.g-4');
    const ownerArray = Array.from(ownerCards);

    ownerArray.forEach(card => {
        const ownerName = card.querySelector('.card-title').textContent.toLowerCase();
        const isDeleted = card.querySelector('.status-badge').classList.contains('status-inactive');

        const matchesSearch = ownerName.includes(searchTerm);
        const matchesStatus = (status === "1" && !isDeleted) || (status === "0" && isDeleted);

        card.closest('.col-md-6').style.display =
            matchesSearch && matchesStatus ? 'block' : 'none';
    });

    // Sorting
    ownerArray.sort((a, b) => {
        if (sortValue === 'name') {
            const nameA = a.querySelector('.card-title').textContent.toLowerCase();
            const nameB = b.querySelector('.card-title').textContent.toLowerCase();
            return nameA.localeCompare(nameB);
        } else if (sortValue === 'units') {
            const unitsA = parseInt(a.querySelector('[data-i18n="owners.units"]').parentElement.textContent);
            const unitsB = parseInt(b.querySelector('[data-i18n="owners.units"]').parentElement.textContent);
            return unitsB - unitsA;
        }
    });

    ownerArray.forEach(card => {
        ownerGrid.appendChild(card.closest('.col-md-6'));
    });
}

// Function to add a new owner card to the UI
function addNewOwnerCard(owner) {
    const ownerGrid = document.querySelector('.owner-grid');
    if (!ownerGrid) return;

    const ownerCard = createOwnerCardHTML(owner);
    const newColumn = document.createElement('div');
    newColumn.className = 'col-md-6 col-lg-4 mb-4';
    newColumn.innerHTML = ownerCard;
    ownerGrid.insertBefore(newColumn, ownerGrid.firstChild);

    // Initialize any tooltips or other Bootstrap components
    const tooltips = newColumn.querySelectorAll('[data-bs-toggle="tooltip"]');
    tooltips.forEach(tooltip => new bootstrap.Tooltip(tooltip));
}

// Function to update existing owner card
function updateOwnerCard(owner) {
    const ownerCard = document.querySelector(`#owner-${owner.id}`);
    if (ownerCard) {
        const newCardHtml = createOwnerCardHTML(owner);
        ownerCard.outerHTML = newCardHtml;

        // Reinitialize tooltips
        const tooltips = document.querySelectorAll(`#owner-${owner.id} [data-bs-toggle="tooltip"]`);
        tooltips.forEach(tooltip => new bootstrap.Tooltip(tooltip));
    }
}

// Function to create owner card HTML
function createOwnerCardHTML(owner) {
    const statusClass = owner.is_deleted ? 'status-inactive' : 'status-active';
    const statusBadge = owner.is_deleted ?
        `<span class="badge bg-danger status-badge">${langManager.translate('common.inactive')}</span>` :
        `<span class="badge bg-success status-badge">${langManager.translate('common.active')}</span>`;

    return `
        <div class="card owner-card h-100" id="owner-${owner.id}">
            <div class="card-body">
                <div class="d-flex justify-content-between align-items-start mb-3">
                    <h5 class="card-title">${escapeHtml(owner.name)}</h5>
                    ${statusBadge}
                </div>
                <div class="owner-info">
                    <p class="mb-2">
                        <i class="bi bi-building"></i>
                        <span data-i18n="owners.formNumber">${langManager.translate('owners.formNumber')}</span>: ${owner.number}
                    </p>
                    <p class="mb-2">
                        <i class="bi bi-house-door"></i>
                        <span data-i18n="owners.formUnits">${langManager.translate('owners.formUnits')}</span>: ${owner.total_units}
                    </p>
                    ${owner.description ? `
                    <p class="mb-2">
                        <i class="bi bi-info-circle"></i>
                        <span data-i18n="owners.form.description">${langManager.translate('owners.form.description')}</span>: 
                        ${escapeHtml(owner.description)}
                    </p>
                    ` : ''}
                </div>
                <div class="card-actions mt-3">
                    <button class="btn btn-sm btn-primary" 
                            onclick="editOwner(${owner.id})"
                            data-bs-toggle="tooltip"
                            title="${langManager.translate('owners.edit')}">
                        <i class="bi bi-pencil"></i>
                    </button>
                    ${owner.is_deleted ? `
                        <button class="btn btn-sm btn-success" 
                                onclick="restoreOwner(${owner.id})"
                                data-bs-toggle="tooltip"
<!--                                title="${langManager.translate('owners.restore')}">-->
                            <i class="bi bi-arrow-counterclockwise"></i>
                        </button>
                    ` : `
                        <button class="btn btn-sm btn-danger" 
                                onclick="deleteOwner(${owner.id})"
                                data-bs-toggle="tooltip"
<!--                                title="${langManager.translate('owners.delete')}">-->
                            <i class="bi bi-trash"></i>
                        </button>
                    `}
                </div>
            </div>
        </div>
    `;
}

// Helper function to escape HTML to prevent XSS
function escapeHtml(unsafe) {
    return unsafe
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}

// Function to reset form with validation states
function resetForm() {
    const form = document.getElementById('ownerForm');
    if (form) {
        form.reset();
        // Clear any validation classes
        form.querySelectorAll('.is-valid, .is-invalid').forEach(element => {
            element.classList.remove('is-valid', 'is-invalid');
        });
        // Reset select elements to default
        const buildingSelect = document.getElementById('buildingId');
        if (buildingSelect) {
            buildingSelect.value = '';
        }
        // Clear hidden fields
        const ownerId = document.getElementById('ownerId');
        if (ownerId) {
            ownerId.value = '';
        }
    }
}

// Add event listener for when modal is hidden
document.addEventListener('DOMContentLoaded', function() {
    const addOwnerModal = document.getElementById('addOwnerModal');
    if (addOwnerModal) {
        addOwnerModal.addEventListener('hidden.bs.modal', function () {
            resetForm();
        });
    }
});
