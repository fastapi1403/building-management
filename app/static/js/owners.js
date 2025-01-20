// Function to update existing owner card
function updateOwnerCard(owner) {
    const ownerCard = document.querySelector(`[data-owner-id="${owner.id}"]`);
    if (ownerCard) {
        ownerCard.querySelector('.card-title').textContent = owner.name;

        const floorsElement = ownerCard.querySelector('.fa-owner').nextElementSibling;
        if (floorsElement) {
            floorsElement.textContent = `${owner.total_floors} Floors`;
        }

        const statusBadge = ownerCard.querySelector('.status-badge');
        if (statusBadge) {
            statusBadge.className = `status-badge ${owner.is_deleted ? 'status-inactive' : 'status-active'}`;
            statusBadge.textContent = owner.is_deleted ? 'Deleted' : 'Active';
        }

        const descriptionElement = ownerCard.querySelector('.owner-description');
        if (descriptionElement && owner.description) {
            descriptionElement.textContent = owner.description;
        }

        ownerCard.classList.add('owner-updated');
        setTimeout(() => {
            ownerCard.classList.remove('owner-updated');
        }, 1000);

        const updateInfo = ownerCard.querySelector('.update-info');
        if (updateInfo) {
            updateInfo.textContent = `Updated: ${owner.updated_at}`;
        }

        ownerCard.style.transition = 'background-color 0.5s ease';
        ownerCard.style.backgroundColor = '#e8f5e9';
        setTimeout(() => {
            ownerCard.style.backgroundColor = '';
        }, 1500);

        langManager.translatePage();
    } else {
        window.location.reload();
    }
}

// Save owner function to handle the save/update process
async function saveOwner() {
    console.log('saveOwner')
    const ownerId = document.getElementById('ownerId')?.value;
    const isEditing = !!ownerId;

    const ownerData = {
        name: document.getElementById('ownerName').value,
        total_floors: parseInt(document.getElementById('ownerFloors').value),
        description: document.getElementById('ownerDescription').value,
    };

    if (!validateOwnerData(ownerData)) {
        return false;
    }

    try {
        Swal.fire({
            title: langManager.translate('common.loading'),
            text: langManager.translate(isEditing ? 'owners.messages.updating' : 'owners.messages.saving'),
            allowOutsideClick: false,
            allowEscapeKey: false,
            showConfirmButton: false,
            didOpen: () => {
                Swal.showLoading();
            }
        });

        const url = isEditing ? `/api/v1/owners/${ownerId}` : '/api/v1/owners';
        const response = await fetch(url, {
            method: isEditing ? 'PUT' : 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCsrfToken(),
                'Accept': 'application/json'
            },
            body: JSON.stringify(ownerData)
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || langManager.translate('owners.messages.saveError'));
        }

        const savedOwner = await response.json();

        await Swal.fire({
            title: langManager.translate('common.success'),
            text: langManager.translate(isEditing ? 'owners.messages.updateSuccess' : 'owners.messages.createSuccess'),
            icon: 'success',
            confirmButtonColor: '#198754',
            timer: 2000,
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

    } catch (error) {
        console.error('Error:', error);
        Swal.fire({
            title: langManager.translate('common.error'),
            text: error.message || langManager.translate('owners.messages.saveError'),
            icon: 'error',
            confirmButtonColor: '#dc3545'
        });
    }
}

// Function to add a new owner card to the UI
function addNewOwnerCard(owner) {
    const ownersContainer = document.querySelector('.row.g-4');
    const newOwnerHtml = `
        <div class="col-md-6 col-lg-4" data-owner-id="${owner.id}">
            <div class="card owner-card">
                <div class="card-body">
                    <div class="d-flex justify-content-between align-items-center mb-3">
                        <h5 class="card-title mb-0">${owner.name}</h5>
                        <span class="status-badge ${owner.is_deleted ? 'status-inactive' : 'status-active'}">
                            ${owner.is_deleted ? 'Deleted' : 'Active'}
                        </span>
                    </div>

                    <div class="owner-stats mb-3">
                        <div class="row g-2">
                            <div class="col-6">
                                <div class="d-flex align-items-center">
                                    <i class="fas fa-owner me-2"></i>
                                    <span>${owner.total_floors} <span data-i18n="owners.floors"></span>
                                </div>
                            </div>
                            <div class="col-6">
                                <div class="d-flex align-items-center">
                                    <i class="fas fa-door-open me-2"></i>
                                    <span>28 <span data-i18n="owners.units"></span></span>
                                </div>
                            </div>
                            <div class="col-6">
                                <div class="d-flex align-items-center">
                                    <i class="fas fa-user-check me-2"></i>
                                    <span>100% <span data-i18n="owners.occupied"></span></span>
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
                                    onclick="editOwner('${owner.id}')">
                                <i class="fas fa-edit"></i>
                            </button>
                            <button type="button"
                                    class="btn btn-outline-danger"
                                    onclick="deleteOwner('${owner.id}')">
                                <i class="fas fa-trash"></i>
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `;

    ownersContainer.insertAdjacentHTML('afterbegin', newOwnerHtml);
}

// Helper function to reset form and validation states
function resetForm() {
    const form = document.getElementById('ownerForm');
    form.reset();

    const ownerIdInput = document.getElementById('ownerId');
    if (ownerIdInput) {
        ownerIdInput.value = '';
    }

    form.querySelectorAll('.is-valid, .is-invalid').forEach(element => {
        element.classList.remove('is-valid', 'is-invalid');
    });

    const modalTitle = document.querySelector('#addOwnerModal .modal-title');
    if (modalTitle) {
        modalTitle.textContent = 'Add New Owner';
    }
}

// Edit owner function to prepare the form for editing
async function editOwner(ownerId) {
    try {
        Swal.fire({
            title: langManager.translate('common.loading'),
            text: langManager.translate('owners.messages.loading'),
            allowOutsideClick: false,
            allowEscapeKey: false,
            showConfirmButton: false,
            didOpen: () => {
                Swal.showLoading();
            }
        });

        const response = await fetch(`/api/v1/owners/${ownerId}`);
        Swal.close();

        if (!response.ok) {
            throw new Error(langManager.translate('owners.messages.fetchError'));
        }

        const owner = await response.json();

        let modal = document.getElementById('addOwnerModal');
        if (!modal) {
            const modalHTML = `
                <div class="modal fade" id="addOwnerModal" tabindex="-1" aria-labelledby="addOwnerModalLabel" aria-hidden="true">
                    <div class="modal-dialog">
                        <div class="modal-content">
                            <div class="modal-header">
                                <h5 class="modal-title" id="addOwnerModalLabel">${langManager.translate('owners.edit')}</h5>
                                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                            </div>
                            <div class="modal-body">
                                <form id="ownerForm">
                                    <input type="hidden" id="ownerId">
                                    <div class="mb-3">
                                        <label for="ownerName" class="form-label" data-i18n="owners.formName"></label>
                                        <input type="text" class="form-control" id="ownerName" required>
                                    </div>
                                    <div class="mb-3">
                                        <label for="ownerFloors" class="form-label" data-i18n="owners.formFloors"></label>
                                        <input type="number" class="form-control" id="ownerFloors" required min="1">
                                    </div>
                                    <div class="mb-3">
                                        <label for="ownerDescription" class="form-label" data-i18n="owners.formDescription"></label>
                                        <textarea class="form-control" id="ownerDescription" rows="3"></textarea>
                                    </div>
                                </form>
                            </div>
                            <div class="modal-footer">
                                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal" data-i18n="owners.formCancel"></button>
                                <button type="button" class="btn btn-primary" onclick="saveOwner()" data-i18n="owners.formSave"></button>
                            </div>
                        </div>
                    </div>
                </div>
            `;
            document.body.insertAdjacentHTML('beforeend', modalHTML);
            modal = document.getElementById('addOwnerModal');
        }

        const modalTitle = modal.querySelector('.modal-title');
        if (modalTitle) {
            modalTitle.textContent = langManager.translate('owners.edit');
        }

        const ownerIdInput = document.getElementById('ownerId');
        if (!ownerIdInput) {
            const input = document.createElement('input');
            input.type = 'hidden';
            input.id = 'ownerId';
            document.getElementById('ownerForm').appendChild(input);
        }
        document.getElementById('ownerId').value = ownerId;
        document.getElementById('ownerName').value = owner.name || '';
        document.getElementById('ownerFloors').value = owner.total_floors || '';
        document.getElementById('ownerDescription').value = owner.description || '';

        await Swal.close();

        const bsModal = new bootstrap.Modal(modal);
        bsModal.show();

        langManager.translatePage();

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

// Delete owner function
async function deleteOwner(ownerId) {
    const result = await Swal.fire({
        title: langManager.translate('owners.delete'),
        text: langManager.translate('owners.deleteConfirmation'),
        icon: langManager.translate('common.warning'),
        showCancelButton: true,
        confirmButtonColor: '#dc3545',
        cancelButtonColor: '#6c757d',
        confirmButtonText: langManager.translate('owners.deleteConfirmButton'),
        cancelButtonText: langManager.translate('common.cancel'),
        reverseButtons: true
    });

    if (result.isConfirmed) {
        try {
            Swal.fire({
                title: langManager.translate('owners.deleting'),
                text: langManager.translate('owners.deleteWait'),
                allowOutsideClick: false,
                allowEscapeKey: false,
                showConfirmButton: false,
                didOpen: () => {
                    Swal.showLoading();
                }
            });

            const response = await fetch(`/api/v1/owners/${ownerId}`, {
                method: 'DELETE',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCsrfToken(),
                    'Accept': 'application/json'
                }
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || langManager.translate('owners.deleteFail'));
            }

            await Swal.fire({
                title: langManager.translate('owners.statusDeleted') + '!',
                text: langManager.translate('owners.deleteSuccess'),
                icon: langManager.translate('common.success'),
                confirmButtonColor: '#198754',
                timer: 2000,
                timerProgressBar: true
            });

            const ownerElement = document.querySelector(`[data-owner-id="${ownerId}"]`);
            if (ownerElement) {
                ownerElement.remove();
            } else {
                window.location.reload();
            }

        } catch (error) {
            console.error(langManager.translate('owners.errorDeletingOwner'), error);
            Swal.fire({
                title: langManager.translate('common.error'),
                text: error.message || langManager.translate('owners.deleteError'),
                icon: 'error',
                confirmButtonColor: '#dc3545'
            });
        }
    }
}

function hardDeleteOwner(ownerId) {
    // Confirm the deletion action with the user using Swal
    Swal.fire({
        title: langManager.translate('owners.confirmHardDeleteTitle'),
        text: langManager.translate('owners.confirmHardDeleteText'),
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#dc3545',
        cancelButtonColor: '#6c757d',
        confirmButtonText: langManager.translate('common.confirm'),
        cancelButtonText: langManager.translate('common.cancel')
    }).then((result) => {
        if (result.isConfirmed) {
            // Perform an AJAX request to delete the owner
            fetch(`/api/v1/owners/${ownerId}/permanent`, {
                method: 'DELETE',
                headers: {
                    'Content-Type': 'application/json'
                }
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error(langManager.translate('owners.networkErrorHardDelete'));
                }
                return response.json();
            })
            .then(data => {
                // Handle success response
                Swal.fire({
                    title: langManager.translate('common.success'),
                    text: langManager.translate('owners.successHardDelete'),
                    icon: 'success',
                    confirmButtonColor: '#198754',
                    timer: 2000,
                    timerProgressBar: true
                }).then(() => {
                    // Redirect to the owners list page
                    window.location.href = '/dashboard/owners';
                });
            })
            .catch(error => {
                // Handle error response
                Swal.fire({
                    title: langManager.translate('common.error'),
                    text: langManager.translate('owners.errorHardDelete'),
                    icon: 'error',
                    confirmButtonColor: '#dc3545'
                });
            });
        }
    });
}

// Validation function
function validateOwnerData(data) {
    const requiredFields = ['name', 'total_floors'];

    for (const field of requiredFields) {
        if (!data[field]) {
            Swal.fire({
                title: langManager.translate('owners.validationError'),
                text: `${field.replace('_', ' ').toUpperCase()} ${langManager.translate('owners.required')}`,
                icon: 'error',
                confirmButtonText: 'OK'
            });
            return false;
        }
    }

    if (data.total_floors < 1) {
        Swal.fire({
            title: langManager.translate('owners.validationError'),
            text: langManager.translate('owners.validationFloors'),
            icon: langManager.translate('common.error'),
            confirmButtonText: langManager.translate('common.ok')
        });
        return false;
    }

    return true;
}

// Restore owner function
function restoreOwner(ownerId) {
    return Swal.fire({
        title: langManager.translate('owners.restore'),
        text: langManager.translate('owners.restoreConfirmation'),
        icon: 'question',
        showCancelButton: true,
        confirmButtonColor: '#198754',
        cancelButtonColor: '#6c757d',
        confirmButtonText: langManager.translate('owners.restoreConfirmButton'),
        cancelButtonText: langManager.translate('common.cancel')
    }).then(async (result) => {
        if (result.isConfirmed) {
            try {
                const response = await fetch(`/api/v1/owners/${ownerId}/restore`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCsrfToken()
                    }
                });

                if (!response.ok) throw new Error(langManager.translate('owners.restoreFail'));

                await Swal.fire({
                    title: langManager.translate('common.success'),
                    text: langManager.translate('owners.restoreSuccess'),
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
    });
}

// Edit owner detail page function
function editOwnerDetail(ownerId) {
    window.location.href = `/owners#edit-${ownerId}`;
}

// Initialize the page functionality
function initializePage() {
    const isOwnersListPage = !!document.querySelector('.owners-container');

    if (isOwnersListPage) {
        const searchOwner = document.getElementById('searchOwner');
        if (searchOwner) {
            searchOwner.addEventListener('keyup', function(e) {
                const searchTerm = e.target.value.toLowerCase();
                const ownerCards = document.querySelectorAll('.owner-card');

                ownerCards.forEach(card => {
                    const ownerName = card.querySelector('.card-title').textContent.toLowerCase();
                    if (ownerName.includes(searchTerm)) {
                        card.closest('.col-md-6').style.display = '';
                    } else {
                        card.closest('.col-md-6').style.display = 'none';
                    }
                });
            });
        }

        const statusFilter = document.getElementById('statusFilter');
        if (statusFilter) {
            statusFilter.addEventListener('change', function(e) {
                const status = e.target.value.toLowerCase();
                const ownerCards = document.querySelectorAll('.owner-card');

                ownerCards.forEach(card => {
                    const ownerStatus = card.querySelector('.status-badge').textContent.trim().toLowerCase();
                    if (status === '' || ownerStatus === status) {
                        card.closest('.col-md-6').style.display = '';
                    } else {
                        card.closest('.col-md-6').style.display = 'none';
                    }
                });
            });
        }

        const ownerForm = document.getElementById('ownerForm');
        if (ownerForm) {
            ownerForm.addEventListener('submit', function(e) {
                e.preventDefault();
                saveOwner();
            });

            ownerForm.querySelectorAll('input, select').forEach(element => {
                element.addEventListener('input', function() {
                    this.classList.remove('is-invalid', 'is-valid');
                    this.classList.add(this.checkValidity() ? 'is-valid' : 'is-invalid');
                });
            });
        }

        const addOwnerModal = document.getElementById('addOwnerModal');
        if (addOwnerModal) {
            addOwnerModal.addEventListener('hidden.bs.modal', function() {
                resetForm();
            });
        }
    }
}

// Initialize page when DOM is ready
// document.addEventListener('DOMContentLoaded', initializePage);

// Save owner function to handle the save/update process
async function saveOwner() {
    const ownerId = document.getElementById('ownerId')?.value;
    const isEditing = !!ownerId;

    // Collect data from all form fields
    const ownerData = {
        name: document.getElementById('ownerName').value,
        national_id: document.getElementById('ownerPhoneNumber').value,
        phone: document.getElementById('ownerPhone').value,
        phone_alt: document.getElementById('ownerPhoneAlt').value,
        phone_emergency: document.getElementById('ownerPhoneEmergency').value,
        phone_emergency_name: document.getElementById('ownerPhoneEmergencyName').value,
        email: document.getElementById('ownerEmail').value,
        whatsapp: document.getElementById('ownerWhatsapp').value,
        telegram: document.getElementById('ownerTelegram').value,
        notes: document.getElementById('ownerNotes').value
    };

    // Validate required fields
    if (!validateOwnerData(ownerData)) {
        return false;
    }

    try {
        Swal.fire({
            title: langManager.translate('common.loading'),
            text: langManager.translate(isEditing ? 'owners.messages.updating' : 'owners.messages.saving'),
            allowOutsideClick: false,
            allowEscapeKey: false,
            showConfirmButton: false,
            didOpen: () => {
                Swal.showLoading();
            }
        });

        const url = isEditing ? `/api/v1/owners/${ownerId}` : '/api/v1/owners';
        const response = await fetch(url, {
            method: isEditing ? 'PUT' : 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCsrfToken(),
                'Accept': 'application/json'
            },
            body: JSON.stringify(ownerData)
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || langManager.translate('owners.messages.saveError'));
        }

        const savedOwner = await response.json();

        await Swal.fire({
            title: langManager.translate('common.success'),
            text: langManager.translate(isEditing ? 'owners.messages.updateSuccess' : 'owners.messages.createSuccess'),
            icon: 'success',
            confirmButtonColor: '#198754',
            timer: 2000,
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

    } catch (error) {
        console.error('Error:', error);
        Swal.fire({
            title: langManager.translate('common.error'),
            text: error.message || langManager.translate('owners.messages.saveError'),
            icon: 'error',
            confirmButtonColor: '#dc3545'
        });
    }
}

// Edit owner function to load data into the modal
async function editOwner(ownerId) {
    try {
        Swal.fire({
            title: langManager.translate('common.loading'),
            text: langManager.translate('owners.messages.loading'),
            allowOutsideClick: false,
            allowEscapeKey: false,
            showConfirmButton: false,
            didOpen: () => {
                Swal.showLoading();
            }
        });

        const response = await fetch(`/api/v1/owners/${ownerId}`);

        if (!response.ok) {
            throw new Error(langManager.translate('owners.messages.fetchError'));
        }

        const owner = await response.json();

        // Update modal title
        const modalTitle = document.querySelector('#addOwnerModalLabel span');
        if (modalTitle) {
            modalTitle.textContent = langManager.translate('owners.edit');
        }

        // Set form values
        document.getElementById('ownerId').value = owner.id;
        document.getElementById('ownerName').value = owner.name || '';
        document.getElementById('ownerPhoneNumber').value = owner.national_id || '';
        document.getElementById('ownerPhone').value = owner.phone || '';
        document.getElementById('ownerPhoneAlt').value = owner.phone_alt || '';
        document.getElementById('ownerPhoneEmergency').value = owner.phone_emergency || '';
        document.getElementById('ownerPhoneEmergencyName').value = owner.phone_emergency_name || '';
        document.getElementById('ownerEmail').value = owner.email || '';
        document.getElementById('ownerWhatsapp').value = owner.whatsapp || '';
        document.getElementById('ownerTelegram').value = owner.telegram || '';
        document.getElementById('ownerNotes').value = owner.notes || '';

        await Swal.close();

        // Show modal
        const modal = new bootstrap.Modal(document.getElementById('addOwnerModal'));
        modal.show();

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

// Validate owner data
function validateOwnerData(data) {
    // Required fields
    const requiredFields = ['name', 'national_id', 'phone'];

    for (const field of requiredFields) {
        if (!data[field]) {
            Swal.fire({
                title: langManager.translate('owners.validationError'),
                text: langManager.translate(`owners.${field}Required`),
                icon: 'error',
                confirmButtonText: langManager.translate('common.ok')
            });
            return false;
        }
    }

    // Validate email format if provided
    if (data.email && !validateEmail(data.email)) {
        Swal.fire({
            title: langManager.translate('owners.validationError'),
            text: langManager.translate('owners.invalidEmail'),
            icon: 'error',
            confirmButtonText: langManager.translate('common.ok')
        });
        return false;
    }

    // Validate phone numbers
    if (!validatePhone(data.phone)) {
        Swal.fire({
            title: langManager.translate('owners.validationError'),
            text: langManager.translate('owners.invalidPhone'),
            icon: 'error',
            confirmButtonText: langManager.translate('common.ok')
        });
        return false;
    }

    return true;
}

// Helper function to validate email format
function validateEmail(email) {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}

// Helper function to validate phone numbers
function validatePhone(phone) {
    // Adjust the regex pattern according to your phone number format requirements
    return /^\+?[\d\s-]{10,}$/.test(phone);
}

// Reset form helper
function resetForm() {
    const form = document.getElementById('ownerForm');
    if (form) {
        form.reset();

        // Reset hidden owner ID
        const ownerIdInput = document.getElementById('ownerId');
        if (ownerIdInput) {
            ownerIdInput.value = '';
        }

        // Reset validation states
        form.querySelectorAll('.is-valid, .is-invalid').forEach(element => {
            element.classList.remove('is-valid', 'is-invalid');
        });

        // Reset modal title
        const modalTitle = document.querySelector('#addOwnerModalLabel span');
        if (modalTitle) {
            modalTitle.textContent = langManager.translate('owners.addNew');
        }
    }
}

// Initialize page when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    // Initialize modal
    const addOwnerModal = document.getElementById('addOwnerModal');
    if (addOwnerModal) {
        // Reset form when modal is hidden
        addOwnerModal.addEventListener('hidden.bs.modal', resetForm);
    }

    // Initialize form validation
    const ownerForm = document.getElementById('ownerForm');
    if (ownerForm) {
        ownerForm.addEventListener('submit', function(e) {
            e.preventDefault();
            saveOwner();
        });

        // Add real-time validation feedback
        ownerForm.querySelectorAll('input, select, textarea').forEach(element => {
            element.addEventListener('input', function() {
                this.classList.remove('is-invalid', 'is-valid');
                if (this.value) {
                    if (this.id === 'ownerEmail' && this.value) {
                        this.classList.add(validateEmail(this.value) ? 'is-valid' : 'is-invalid');
                    } else if (this.id === 'ownerPhone' || this.id === 'ownerPhoneAlt' || this.id === 'ownerPhoneEmergency') {
                        this.classList.add(validatePhone(this.value) ? 'is-valid' : 'is-invalid');
                    } else {
                        this.classList.add('is-valid');
                    }
                }
            });
        });
    }
});