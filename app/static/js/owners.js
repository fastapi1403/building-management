// Global language manager reference (assuming it's defined elsewhere)
/* global langManager, bootstrap, Swal */

// Function to get CSRF token from cookies
function getCsrfToken() {
    const name = 'csrftoken=';
    const decodedCookie = decodeURIComponent(document.cookie);
    const ca = decodedCookie.split(';');
    for (let c of ca) {
        while (c.charAt(0) === ' ') {
            c = c.substring(1);
        }
        if (c.indexOf(name) === 0) {
            return c.substring(name.length, c.length);
        }
    }
    return '';
}

// Helper function to validate email format
function validateEmail(email) {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}

// Helper function to validate phone numbers
function validatePhone(phone) {
    return /^\+?[\d\s-]{10,}$/.test(phone);
}

// Save owner function to handle the save/update process
async function saveOwner() {
    try {
        const form = document.getElementById('ownerForm');
        if (!form) {
            throw new Error('Owner form not found');
        }

        const ownerId = document.getElementById('ownerId')?.value;
        const isEditing = !!ownerId;

        // Collect data from all form fields
        const ownerData = {
            name: document.getElementById('ownerName')?.value?.trim() || '',
            national_id: document.getElementById('ownerId')?.value?.trim() || '',
            phone: document.getElementById('ownerPhone')?.value?.trim() || '',
            phone_alt: document.getElementById('ownerPhoneAlt')?.value?.trim() || '',
            phone_emergency: document.getElementById('ownerPhoneEmergency')?.value?.trim() || '',
            phone_emergency_name: document.getElementById('ownerPhoneEmergencyName')?.value?.trim() || '',
            email: document.getElementById('ownerEmail')?.value?.trim() || '',
            whatsapp: document.getElementById('ownerWhatsapp')?.value?.trim() || '',
            telegram: document.getElementById('ownerTelegram')?.value?.trim() || '',
            note: document.getElementById('ownerNote')?.value?.trim() || ''
        };

        // Validate required fields
        if (!validateOwnerData(ownerData)) {
            return false;
        }

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

        Swal.close();

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

        const modal = bootstrap.Modal.getInstance(document.getElementById('addOwnerModal'));
        if (modal) {
            modal.hide();
        }

        // Refresh the page to show updated data
        window.location.reload();

    } catch (error) {
        console.error('Error:', error);
        await Swal.fire({
            title: langManager.translate('common.error'),
            text: error.message || langManager.translate('owners.messages.saveError'),
            icon: 'error',
            confirmButtonColor: '#dc3545'
        });
    }
}

// Validate owner data
function validateOwnerData(data) {
    const requiredFields = [
        { field: 'name', label: 'Name' },
        { field: 'phone', label: 'Phone' }
    ];

    for (const { field, label } of requiredFields) {
        if (!data[field]) {
            Swal.fire({
                title: langManager.translate('owners.validationError'),
                text: `${label} ${langManager.translate('owners.required')}`,
                icon: 'error',
                confirmButtonText: langManager.translate('common.ok')
            });
            return false;
        }
    }

    if (data.email && !validateEmail(data.email)) {
        Swal.fire({
            title: langManager.translate('owners.validationError'),
            text: langManager.translate('owners.invalidEmail'),
            icon: 'error',
            confirmButtonText: langManager.translate('common.ok')
        });
        return false;
    }

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

// Edit owner function
async function editOwner(ownerId) {
    try {
        await Swal.fire({
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

        // Update modal title and set owner ID
        document.getElementById('ownerId').value = ownerId;
        const modalTitle = document.querySelector('#addOwnerModalLabel span');
        if (modalTitle) {
            modalTitle.textContent = langManager.translate('owners.edit');
        }

        // Fill form fields
        document.getElementById('ownerName').value = owner.name || '';
        document.getElementById('ownerId').value = owner.national_id || '';
        document.getElementById('ownerPhone').value = owner.phone || '';
        document.getElementById('ownerPhoneAlt').value = owner.phone_alt || '';
        document.getElementById('ownerPhoneEmergency').value = owner.phone_emergency || '';
        document.getElementById('ownerPhoneEmergencyName').value = owner.phone_emergency_name || '';
        document.getElementById('ownerEmail').value = owner.email || '';
        document.getElementById('ownerWhatsapp').value = owner.whatsapp || '';
        document.getElementById('ownerTelegram').value = owner.telegram || '';
        document.getElementById('ownerNote').value = owner.note || '';

        await Swal.close();

        // Show modal
        const modal = new bootstrap.Modal(document.getElementById('addOwnerModal'));
        modal.show();

    } catch (error) {
        console.error('Error:', error);
        await Swal.fire({
            title: langManager.translate('common.error'),
            text: error.message || langManager.translate('owners.messages.editError'),
            icon: 'error',
            confirmButtonColor: '#dc3545'
        });
    }
}

// Delete owner function
async function deleteOwner(ownerId) {
    try {
        const result = await Swal.fire({
            title: langManager.translate('owners.delete'),
            text: langManager.translate('owners.deleteConfirmation'),
            icon: 'warning',
            showCancelButton: true,
            confirmButtonColor: '#dc3545',
            cancelButtonColor: '#6c757d',
            confirmButtonText: langManager.translate('owners.deleteConfirmButton'),
            cancelButtonText: langManager.translate('common.cancel'),
            reverseButtons: true
        });

        if (result.isConfirmed) {
            await Swal.fire({
                title: langManager.translate('owners.deleting'),
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
                throw new Error(langManager.translate('owners.deleteFail'));
            }

            await Swal.fire({
                title: langManager.translate('common.success'),
                text: langManager.translate('owners.deleteSuccess'),
                icon: 'success',
                confirmButtonColor: '#198754',
                timer: 2000,
                timerProgressBar: true
            });

            window.location.reload();
        }
    } catch (error) {
        console.error('Error:', error);
        await Swal.fire({
            title: langManager.translate('common.error'),
            text: error.message || langManager.translate('owners.deleteError'),
            icon: 'error',
            confirmButtonColor: '#dc3545'
        });
    }
}

// Reset form function
function resetForm() {
    const form = document.getElementById('ownerForm');
    if (form) {
        form.reset();
        document.getElementById('ownerId').value = '';

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

// Initialize page when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    // Modal reset on close
    const addOwnerModal = document.getElementById('addOwnerModal');
    if (addOwnerModal) {
        addOwnerModal.addEventListener('hidden.bs.modal', resetForm);
    }

    // Real-time validation for form fields
    const ownerForm = document.getElementById('ownerForm');
    if (ownerForm) {
        ownerForm.querySelectorAll('input, textarea').forEach(element => {
            element.addEventListener('input', function() {
                this.classList.remove('is-invalid', 'is-valid');
                if (this.value.trim()) {
                    if (this.id === 'ownerEmail' && this.value) {
                        this.classList.add(validateEmail(this.value) ? 'is-valid' : 'is-invalid');
                    } else if (['ownerPhone', 'ownerPhoneAlt', 'ownerPhoneEmergency'].includes(this.id)) {
                        this.classList.add(validatePhone(this.value) ? 'is-valid' : 'is-invalid');
                    } else {
                        this.classList.add('is-valid');
                    }
                }
            });
        });
    }

    // Search functionality
    const searchInput = document.getElementById('searchOwner');
    if (searchInput) {
        searchInput.addEventListener('input', function(e) {
            const searchTerm = e.target.value.toLowerCase();
            document.querySelectorAll('.owner-card').forEach(card => {
                const ownerName = card.querySelector('.card-title').textContent.toLowerCase();
                card.closest('.col-md-6').style.display =
                    ownerName.includes(searchTerm) ? '' : 'none';
            });
        });
    }

    // Status filter
    const statusFilter = document.getElementById('statusFilter');
    if (statusFilter) {
        statusFilter.addEventListener('change', function(e) {
            const selectedStatus = e.target.value === '1' ? 'active' : 'inactive';
            document.querySelectorAll('.owner-card').forEach(card => {
                const statusBadge = card.querySelector('.status-badge');
                if (statusBadge) {
                    const isActive = statusBadge.classList.contains('status-active');
                    card.closest('.col-md-6').style.display =
                        (selectedStatus === 'active' && isActive) ||
                        (selectedStatus === 'inactive' && !isActive) ? '' : 'none';
                }
            });
        });
    }
});