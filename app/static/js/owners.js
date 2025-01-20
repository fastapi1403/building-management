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
    let loadingSwal;
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
            phone: document.getElementById('ownerPhone')?.value?.trim() || '',
        };

        // Add optional fields only if they have values
        const national_id = document.getElementById('ownerPhoneNumber')?.value?.trim();
        if (national_id) {
            ownerData.national_id = national_id;
        }

        const phone_alt = document.getElementById('ownerPhoneAlt')?.value?.trim();
        if (phone_alt) {
            ownerData.phone_alt = phone_alt;
        }

        const phone_emergency = document.getElementById('ownerPhoneEmergency')?.value?.trim();
        if (phone_emergency) {
            ownerData.phone_emergency = phone_emergency;
        }

        const phone_emergency_name = document.getElementById('ownerPhoneEmergencyName')?.value?.trim();
        if (phone_emergency_name) {
            ownerData.phone_emergency_name = phone_emergency_name;
        }

        const email = document.getElementById('ownerEmail')?.value?.trim();
        if (email) {
            ownerData.email = email;
        }

        const whatsapp = document.getElementById('ownerWhatsapp')?.value?.trim();
        if (whatsapp) {
            ownerData.whatsapp = whatsapp;
        }

        const telegram = document.getElementById('ownerTelegram')?.value?.trim();
        if (telegram) {
            ownerData.telegram = telegram;
        }

        const note = document.getElementById('ownerNotes')?.value?.trim();
        if (note) {
            ownerData.note = note;
        }

        // Validate required fields
        if (!validateOwnerData(ownerData)) {
            return false;
        }

        // Show loading state
        loadingSwal = Swal.fire({
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

        // Close loading state
        if (loadingSwal) {
            loadingSwal;
            Swal.close();
        }

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail?.[0]?.msg || data.detail || langManager.translate('owners.messages.saveError'));
        }

        // Show success message
        await Swal.fire({
            title: langManager.translate('common.success'),
            text: langManager.translate(isEditing ? 'owners.messages.updateSuccess' : 'owners.messages.createSuccess'),
            icon: 'success',
            confirmButtonColor: '#198754',
            timer: 2000,
            timerProgressBar: true
        });

        // Close modal
        const modal = bootstrap.Modal.getInstance(document.getElementById('addOwnerModal'));
        if (modal) {
            modal.hide();
        }

        // Refresh page
        window.location.reload();

    } catch (error) {
        console.error('Error:', error);

        // Make sure loading state is closed
        if (loadingSwal) {
            await loadingSwal;
            Swal.close();
        }

        // Show error message
        await Swal.fire({
            title: langManager.translate('common.error'),
            text: error.message || langManager.translate('owners.messages.saveError'),
            icon: 'error',
            confirmButtonColor: '#dc3545'
        });
    }
}

async function editOwner(ownerId) {
    let loadingSwal;
    try {
        // Show loading state
        loadingSwal = Swal.fire({
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

        // Close loading state
        if (loadingSwal) {
            loadingSwal;
            Swal.close();
        }

        if (!response.ok) {
            throw new Error(langManager.translate('owners.messages.fetchError'));
        }

        const owner = await response.json();

        // Set hidden owner ID field for form submission
        const ownerIdInput = document.getElementById('ownerId');
        if (ownerIdInput) {
            ownerIdInput.value = ownerId; // Use the actual owner ID, not national_id
        }

        // Update modal title
        const modalTitle = document.querySelector('#addOwnerModalLabel span');
        if (modalTitle) {
            modalTitle.textContent = langManager.translate('owners.edit');
        }

        // Fill form fields with proper field IDs
        document.getElementById('ownerName').value = owner.name || '';
        document.getElementById('ownerId').value = owner.national_id || '';
        document.getElementById('ownerPhone').value = owner.phone || '';
        document.getElementById('ownerPhoneAlt').value = owner.phone_alt || '';
        document.getElementById('ownerPhoneEmergency').value = owner.phone_emergency || '';
        document.getElementById('ownerPhoneEmergencyName').value = owner.phone_emergency_name || '';
        document.getElementById('ownerEmail').value = owner.email || '';
        document.getElementById('ownerWhatsapp').value = owner.whatsapp || '';
        document.getElementById('ownerTelegram').value = owner.telegram || '';
        document.getElementById('ownerNotes').value = owner.note || '';

        // Show modal
        const modal = new bootstrap.Modal(document.getElementById('addOwnerModal'));
        modal.show();

    } catch (error) {
        console.error('Error:', error);

        // Make sure loading state is closed
        if (loadingSwal) {
            await loadingSwal;
            Swal.close();
        }

        // Show error message
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
    // Check required fields
    if (!data.name || !data.phone) {
        Swal.fire({
            title: langManager.translate('owners.validationError'),
            text: langManager.translate('owners.requiredFields'),
            icon: 'error',
            confirmButtonText: langManager.translate('common.ok')
        });
        return false;
    }

    // Validate email only if it exists
    if (data.email && !validateEmail(data.email)) {
        Swal.fire({
            title: langManager.translate('owners.validationError'),
            text: langManager.translate('owners.invalidEmail'),
            icon: 'error',
            confirmButtonText: langManager.translate('common.ok')
        });
        return false;
    }

    // Validate phone
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