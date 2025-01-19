// Floor management functions
async function createFloor() {
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

        let modal = document.getElementById('addFloorModal');
        if (!modal) {
            const modalHTML = `
                <div class="modal fade" id="addFloorModal" tabindex="-1" aria-labelledby="addFloorModalLabel" aria-hidden="true">
                    <div class="modal-dialog">
                        <div class="modal-content">
                            <div class="modal-header">
                                <h5 class="modal-title" id="addFloorModalLabel">${langManager.translate('floors.add')}</h5>
                                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                            </div>
                            <div class="modal-body">
                                <form id="floorForm">
                                    <input type="hidden" id="floorId">
                                    <div class="mb-3">
                                        <label for="buildingId" class="form-label">${langManager.translate('floors.form.building')}</label>
                                        <select class="form-select" id="buildingId" required>
                                            <option value="">${langManager.translate('floors.form.selectBuilding')}</option>
                                            ${buildingOptions}
                                        </select>
                                    </div>
                                    <div class="mb-3">
                                        <label for="floorName" class="form-label">${langManager.translate('floors.formName')}</label>
                                        <input type="text" class="form-control" id="floorName" required>
                                    </div>
                                    <div class="mb-3">
                                        <label for="floorNumber" class="form-label">${langManager.translate('floors.formNumber')}</label>
                                        <input type="number" class="form-control" id="floorNumber" required min="1">
                                    </div>
                                    <div class="mb-3">
                                        <label for="totalUnits" class="form-label">${langManager.translate('floors.formUnits')}</label>
                                        <input type="number" class="form-control" id="totalUnits" required min="1">
                                    </div>
                                    <div class="mb-3">
                                        <label for="description" class="form-label">${langManager.translate('floors.form.description')}</label>
                                        <textarea class="form-control" id="description" rows="3" 
                                                 placeholder="${langManager.translate('floors.form.descriptionPlaceholder')}"></textarea>
                                    </div>
                                </form>
                            </div>
                            <div class="modal-footer">
                                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">
                                    ${langManager.translate('floors.formCancel')}
                                </button>
                                <button type="button" class="btn btn-primary" onclick="saveFloor()">
                                    ${langManager.translate('floors.formSave')}
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            `;
            document.body.insertAdjacentHTML('beforeend', modalHTML);
            modal = document.getElementById('addFloorModal');
        }

        resetForm();
        const bsModal = new bootstrap.Modal(modal);
        bsModal.show();
        langManager.translatePage();
    } catch (error) {
        console.error('Error:', error);
        Swal.fire({
            title: langManager.translate('common.error'),
            text: error.message || langManager.translate('floors.messages.createError'),
            icon: 'error',
            confirmButtonColor: '#dc3545'
        });
    }
}

// Update the saveFloor function to include building_id and description
let currentFloorId = null;

async function editFloor(floorId) {
    try {
        currentFloorId = floorId;

        // Show loading spinner
        const loadingSpinner = document.getElementById('loadingSpinner');
        if (loadingSpinner) loadingSpinner.classList.remove('d-none');

        // Fetch floor data
        const floorResponse = await fetch(`/api/v1/floors/${floorId}`);
        if (!floorResponse.ok) throw new Error('Failed to fetch floor data');
        const floor = await floorResponse.json();

        // Fetch buildings data
        const buildingsResponse = await fetch('/api/v1/buildings');
        if (!buildingsResponse.ok) throw new Error('Failed to fetch buildings data');
        const buildings = await buildingsResponse.json();

        // Populate buildings dropdown
        const buildingSelect = document.getElementById('buildingSelect');
        buildingSelect.innerHTML = '<option value="">Select Building</option>';
        buildings.forEach(building => {
            const option = new Option(building.name, building.id);
            buildingSelect.add(option);
        });

        // Set form values
        document.getElementById('floorId').value = floor.id;
        document.getElementById('floorName').value = floor.name || '';
        document.getElementById('floorNumber').value = floor.number || '';
        document.getElementById('totalUnits').value = floor.total_units || '';
        document.getElementById('buildingSelect').value = floor.building_id || '';
        document.getElementById('description').value = floor.description || '';

        // Hide loading spinner
        if (loadingSpinner) loadingSpinner.classList.add('d-none');

        // Show modal
        const modal = new bootstrap.Modal(document.getElementById('editFloorModal'));
        modal.show();

    } catch (error) {
        console.error('Error:', error);
        // Hide loading spinner
        const loadingSpinner = document.getElementById('loadingSpinner');
        if (loadingSpinner) loadingSpinner.classList.add('d-none');

        // Show error message
        alert('Error loading floor data: ' + error.message);
    }
}

async function saveFloor() {
    try {
        if (!currentFloorId) throw new Error('No floor selected');

        const formData = {
            name: document.getElementById('floorName').value,
            number: parseInt(document.getElementById('floorNumber').value),
            total_units: parseInt(document.getElementById('totalUnits').value),
            building_id: parseInt(document.getElementById('buildingSelect').value),
            description: document.getElementById('description').value
        };

        // Validate form data
        if (!formData.name || !formData.number || !formData.total_units || !formData.building_id) {
            alert('Please fill in all required fields');
            return;
        }

        const response = await fetch(`/api/v1/floors/${currentFloorId}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCsrfToken()
            },
            body: JSON.stringify(formData)
        });

        if (!response.ok) throw new Error('Failed to update floor');

        // Hide modal
        const modal = bootstrap.Modal.getInstance(document.getElementById('editFloorModal'));
        modal.hide();

        // Refresh page
        window.location.reload();

    } catch (error) {
        console.error('Error:', error);
        alert('Error saving floor: ' + error.message);
    }
}

// Update the validation function to include building_id
function validateFloorData(data) {
    if (!data.building_id) {
        Swal.fire({
            icon: 'error',
            title: langManager.translate('common.error'),
            text: langManager.translate('floors.form.buildingRequired'),
            confirmButtonColor: '#dc3545'
        });
        return false;
    }

    if (!data.name || !data.number || !data.total_units) {
        Swal.fire({
            icon: 'error',
            title: langManager.translate('common.error'),
            text: langManager.translate('floors.validation.requiredFields'),
            confirmButtonColor: '#dc3545'
        });
        return false;
    }

    if (data.number <= 0) {
        Swal.fire({
            icon: 'error',
            title: langManager.translate('common.error'),
            text: langManager.translate('floors.validation.invalidNumber'),
            confirmButtonColor: '#dc3545'
        });
        return false;
    }

    if (data.total_units <= 0) {
        Swal.fire({
            icon: 'error',
            title: langManager.translate('common.error'),
            text: langManager.translate('floors.validation.invalidUnits'),
            confirmButtonColor: '#dc3545'
        });
        return false;
    }

    return true;
}


async function deleteFloor(floorId) {
    const result = await Swal.fire({
        title: langManager.translate('floors.delete'),
        text: langManager.translate('floors.deleteConfirmation'),
        icon: langManager.translate('common.warning'),
        showCancelButton: true,
        confirmButtonColor: '#dc3545',
        cancelButtonColor: '#6c757d',
        confirmButtonText: langManager.translate('floors.deleteConfirmButton'),
        cancelButtonText: langManager.translate('common.cancel')
    });

    if (result.isConfirmed) {
        try {
            const response = await fetch(`/api/v1/floors/${floorId}`, {
                method: 'DELETE',
                headers: {
                    'X-CSRFToken': getCsrfToken()
                }
            });

            if (!response.ok) {
                throw new Error(langManager.translate('floors.messages.deleteFail'));
            }

            await Swal.fire({
                icon: 'success',
                title: langManager.translate('floors.messages.deleteSuccess'),
                showConfirmButton: false,
                timer: 1500
            });

            window.location.reload();
        } catch (error) {
            console.error('Error:', error);
            Swal.fire({
                title: langManager.translate('common.error'),
                text: error.message || langManager.translate('floors.messages.deleteError'),
                icon: 'error',
                confirmButtonColor: '#dc3545'
            });
        }
    }
}

async function restoreFloor(floorId) {
    const result = await Swal.fire({
        title: langManager.translate('floors.restore'),
        text: langManager.translate('floors.restoreConfirmation'),
        icon: 'question',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: langManager.translate('floors.restoreConfirmButton'),
        cancelButtonText: langManager.translate('common.cancel')
    });

    if (result.isConfirmed) {
        try {
            const response = await fetch(`/api/v1/floors/${floorId}/restore`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCsrfToken()
                }
            });

            if (!response.ok) {
                throw new Error(langManager.translate('floors.messages.restoreFail'));
            }

            await Swal.fire({
                icon: 'success',
                title: langManager.translate('floors.messages.restoreSuccess'),
                showConfirmButton: false,
                timer: 1500
            });

            window.location.reload();
        } catch (error) {
            console.error('Error:', error);
            Swal.fire({
                title: langManager.translate('common.error'),
                text: error.message || langManager.translate('floors.messages.restoreFail'),
                icon: 'error',
                confirmButtonColor: '#dc3545'
            });
        }
    }
}

// Filter and sort functionality
function filterFloors() {
    const searchTerm = searchInput.value.toLowerCase();
    const status = statusFilter.value;
    const sortValue = sortBy.value;

    const floorCards = document.querySelectorAll('.floor-card');
    const floorGrid = document.querySelector('.row.g-4');
    const floorArray = Array.from(floorCards);

    floorArray.forEach(card => {
        const floorName = card.querySelector('.card-title').textContent.toLowerCase();
        const isDeleted = card.querySelector('.status-badge').classList.contains('status-inactive');

        const matchesSearch = floorName.includes(searchTerm);
        const matchesStatus = (status === "1" && !isDeleted) || (status === "0" && isDeleted);

        card.closest('.col-md-6').style.display =
            matchesSearch && matchesStatus ? 'block' : 'none';
    });

    // Sorting
    floorArray.sort((a, b) => {
        if (sortValue === 'name') {
            const nameA = a.querySelector('.card-title').textContent.toLowerCase();
            const nameB = b.querySelector('.card-title').textContent.toLowerCase();
            return nameA.localeCompare(nameB);
        } else if (sortValue === 'units') {
            const unitsA = parseInt(a.querySelector('[data-i18n="floors.units"]').parentElement.textContent);
            const unitsB = parseInt(b.querySelector('[data-i18n="floors.units"]').parentElement.textContent);
            return unitsB - unitsA;
        }
    });

    floorArray.forEach(card => {
        floorGrid.appendChild(card.closest('.col-md-6'));
    });
}

// Function to add a new floor card to the UI
function addNewFloorCard(floor) {
    const floorGrid = document.querySelector('.floor-grid');
    if (!floorGrid) return;

    const floorCard = createFloorCardHTML(floor);
    const newColumn = document.createElement('div');
    newColumn.className = 'col-md-6 col-lg-4 mb-4';
    newColumn.innerHTML = floorCard;
    floorGrid.insertBefore(newColumn, floorGrid.firstChild);

    // Initialize any tooltips or other Bootstrap components
    const tooltips = newColumn.querySelectorAll('[data-bs-toggle="tooltip"]');
    tooltips.forEach(tooltip => new bootstrap.Tooltip(tooltip));
}

// Function to update existing floor card
function updateFloorCard(floor) {
    const floorCard = document.querySelector(`#floor-${floor.id}`);
    if (floorCard) {
        const newCardHtml = createFloorCardHTML(floor);
        floorCard.outerHTML = newCardHtml;

        // Reinitialize tooltips
        const tooltips = document.querySelectorAll(`#floor-${floor.id} [data-bs-toggle="tooltip"]`);
        tooltips.forEach(tooltip => new bootstrap.Tooltip(tooltip));
    }
}

// Function to create floor card HTML
function createFloorCardHTML(floor) {
    const statusClass = floor.is_deleted ? 'status-inactive' : 'status-active';
    const statusBadge = floor.is_deleted ?
        `<span class="badge bg-danger status-badge">${langManager.translate('common.inactive')}</span>` :
        `<span class="badge bg-success status-badge">${langManager.translate('common.active')}</span>`;

    return `
        <div class="card floor-card h-100" id="floor-${floor.id}">
            <div class="card-body">
                <div class="d-flex justify-content-between align-items-start mb-3">
                    <h5 class="card-title">${escapeHtml(floor.name)}</h5>
                    ${statusBadge}
                </div>
                <div class="floor-info">
                    <p class="mb-2">
                        <i class="bi bi-building"></i>
                        <span data-i18n="floors.formNumber">${langManager.translate('floors.formNumber')}</span>: ${floor.number}
                    </p>
                    <p class="mb-2">
                        <i class="bi bi-house-door"></i>
                        <span data-i18n="floors.formUnits">${langManager.translate('floors.formUnits')}</span>: ${floor.total_units}
                    </p>
                    ${floor.description ? `
                    <p class="mb-2">
                        <i class="bi bi-info-circle"></i>
                        <span data-i18n="floors.form.description">${langManager.translate('floors.form.description')}</span>: 
                        ${escapeHtml(floor.description)}
                    </p>
                    ` : ''}
                </div>
                <div class="card-actions mt-3">
                    <button class="btn btn-sm btn-primary" 
                            onclick="editFloor(${floor.id})"
                            data-bs-toggle="tooltip"
                            title="${langManager.translate('floors.edit')}">
                        <i class="bi bi-pencil"></i>
                    </button>
                    ${floor.is_deleted ? `
                        <button class="btn btn-sm btn-success" 
                                onclick="restoreFloor(${floor.id})"
                                data-bs-toggle="tooltip"
<!--                                title="${langManager.translate('floors.restore')}">-->
                            <i class="bi bi-arrow-counterclockwise"></i>
                        </button>
                    ` : `
                        <button class="btn btn-sm btn-danger" 
                                onclick="deleteFloor(${floor.id})"
                                data-bs-toggle="tooltip"
<!--                                title="${langManager.translate('floors.delete')}">-->
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
    const form = document.getElementById('floorForm');
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
        const floorId = document.getElementById('floorId');
        if (floorId) {
            floorId.value = '';
        }
    }
}

// Add event listener for when modal is hidden
document.addEventListener('DOMContentLoaded', function() {
    const addFloorModal = document.getElementById('addFloorModal');
    if (addFloorModal) {
        addFloorModal.addEventListener('hidden.bs.modal', function () {
            resetForm();
        });
    }
});
