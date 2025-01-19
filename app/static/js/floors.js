// Floor management functions
async function createFloor() {
    try {
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
            text: langManager.translate('floors.messages.saveError'),
            icon: 'error',
            confirmButtonColor: '#dc3545'
        });
    }
}

async function saveFloor() {
    try {
        // Get form data
        const floorId = document.getElementById('floorId')?.value;
        const isEditing = !!floorId;

        const floorData = {
            name: document.getElementById('floorName').value,
            number: parseInt(document.getElementById('floorNumber').value),
            total_units: parseInt(document.getElementById('totalUnits').value)
        };

        // Validate data
        if (!validateFloorData(floorData)) {
            return false;
        }

        // Show loading state
        Swal.fire({
            title: langManager.translate(isEditing ? 'floors.messages.updating' : 'floors.messages.saving'),
            allowOutsideClick: false,
            allowEscapeKey: false,
            showConfirmButton: false,
            didOpen: () => {
                Swal.showLoading();
            }
        });

        // Prepare request
        const url = isEditing ? `/api/v1/floors/${floorId}` : '/api/v1/floors';
        const method = isEditing ? 'PUT' : 'POST';

        // Make API request
        const response = await fetch(url, {
            method: method,
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCsrfToken()
            },
            body: JSON.stringify(floorData)
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || langManager.translate(
                isEditing ? 'floors.messages.updateError' : 'floors.messages.saveError'
            ));
        }

        const savedFloor = await response.json();

        // Show success message
        await Swal.fire({
            icon: 'success',
            title: langManager.translate(
                isEditing ? 'floors.messages.updateSuccess' : 'floors.messages.saveSuccess'
            ),
            timer: 1500,
            showConfirmButton: false,
            timerProgressBar: true
        });

        // Update UI
        if (isEditing) {
            updateFloorCard(savedFloor);
        } else {
            addNewFloorCard(savedFloor);
        }

        // Close modal if open
        const modal = bootstrap.Modal.getInstance(document.getElementById('addFloorModal'));
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

// Helper function to validate floor data
function validateFloorData(data) {
    // Check required fields
    if (!data.name || !data.number || !data.total_units) {
        Swal.fire({
            icon: 'error',
            title: langManager.translate('common.error'),
            text: langManager.translate('floors.validation.requiredFields'),
            confirmButtonColor: '#dc3545'
        });
        return false;
    }

    // Validate floor number
    if (data.number <= 0) {
        Swal.fire({
            icon: 'error',
            title: langManager.translate('common.error'),
            text: langManager.translate('floors.validation.invalidNumber'),
            confirmButtonColor: '#dc3545'
        });
        return false;
    }

    // Validate total units
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

async function editFloor(floorId) {
    try {
        Swal.fire({
            title: langManager.translate('common.loading'),
            text: langManager.translate('floors.messages.loading'),
            allowOutsideClick: false,
            allowEscapeKey: false,
            showConfirmButton: false,
            didOpen: () => {
                Swal.showLoading();
            }
        });

        const response = await fetch(`/api/v1/floors/${floorId}`);
        const floor = await response.json();

        const { value: formValues } = await Swal.fire({
            title: langManager.translate('floors.edit'),
            html: `
                <input id="floorName" class="swal2-input" 
                       placeholder="${langManager.translate('floors.formName')}" value="${floor.name}">
                <input id="floorNumber" type="number" class="swal2-input" 
                       placeholder="${langManager.translate('floors.formNumber')}" value="${floor.number}">
                <input id="totalUnits" type="number" class="swal2-input" 
                       placeholder="${langManager.translate('floors.formUnits')}" value="${floor.total_units}">
            `,
            focusConfirm: false,
            showCancelButton: true,
            confirmButtonText: langManager.translate('floors.formSave'),
            cancelButtonText: langManager.translate('floors.formCancel'),
            preConfirm: () => {
                return {
                    name: document.getElementById('floorName').value,
                    number: document.getElementById('floorNumber').value,
                    total_units: document.getElementById('totalUnits').value
                }
            }
        });

        if (formValues) {
            const response = await fetch(`/api/v1/floors/${floorId}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCsrfToken()
                },
                body: JSON.stringify(formValues)
            });

            if (!response.ok) {
                throw new Error(langManager.translate('floors.messages.saveError'));
            }

            await Swal.fire({
                icon: 'success',
                title: langManager.translate('floors.messages.updateSuccess'),
                showConfirmButton: false,
                timer: 1500
            });

            window.location.reload();
        }
    } catch (error) {
        console.error('Error:', error);
        Swal.fire({
            title: langManager.translate('common.error'),
            text: error.message || langManager.translate('floors.messages.editError'),
            icon: 'error',
            confirmButtonColor: '#dc3545'
        });
    }
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

// Initialize page functionality
document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('searchInput');
    const statusFilter = document.getElementById('statusFilter');
    const sortBy = document.getElementById('sortBy');

    if (searchInput) searchInput.addEventListener('input', filterFloors);
    if (statusFilter) statusFilter.addEventListener('change', filterFloors);
    if (sortBy) sortBy.addEventListener('change', filterFloors);
});

// Helper function to reset form
function resetForm() {
    const form = document.getElementById('floorForm');
    if (form) {
        form.reset();
        form.querySelectorAll('.is-valid, .is-invalid').forEach(element => {
            element.classList.remove('is-valid', 'is-invalid');
        });
    }
    const modalTitle = document.querySelector('#addFloorModal .modal-title');
    if (modalTitle) {
        modalTitle.textContent = langManager.translate('floors.add');
    }
}