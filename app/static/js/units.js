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

// Save unit function to handle the save/update process
async function saveUnit() {
    let loadingSwal;
    try {
        const unitId = document.getElementById('unitId')?.value
        const isEditing = unitId !== '';

        // Get the form element
        const form = document.getElementById('unitForm');
        if (!form) {
            throw new Error(langManager.translate('units.formNotFound'));
        }

        // Collect data from form fields with null coalescing and trimming
        const unitData = {
            name: document.getElementById('unitName')?.value?.trim() || '',
            phone: document.getElementById('unitPhone')?.value?.trim() || '',
            // Optional fields
            national_id: document.getElementById('unitIdentificationID')?.value?.trim() || '',
            phone_alt: document.getElementById('unitPhoneAlt')?.value?.trim() || '',
            phone_emergency: document.getElementById('unitPhoneEmergency')?.value?.trim() || '',
            phone_emergency_name: document.getElementById('unitPhoneEmergencyName')?.value?.trim() || '',
            email: document.getElementById('unitEmail')?.value?.trim() || '',
            whatsapp: document.getElementById('unitWhatsapp')?.value?.trim() || '',
            telegram: document.getElementById('unitTelegram')?.value?.trim() || '',
            notes: document.getElementById('unitNotes')?.value?.trim() || ''
        };



        // Remove empty optional fields
        Object.keys(unitData).forEach(key => {
            if (!unitData[key] && key !== 'name' && key !== 'phone') {
                delete unitData[key];
            }
        });

        // Validate unit data
        if (!validateUnitData(unitData)) {
            return false;
        }

        // Show loading state
        loadingSwal = Swal.fire({
            title: langManager.translate('common.loading'),
            text: langManager.translate(isEditing ? 'units.messages.updating' : 'units.messages.saving'),
            allowOutsideClick: false,
            allowEscapeKey: false,
            showConfirmButton: false,
            didOpen: () => {
                Swal.showLoading();
            }
        });

        // Prepare request URL and method
        const url = isEditing ? `/api/v1/units/${unitId}` : '/api/v1/units';
        const method = isEditing ? 'PUT' : 'POST';

        // Make API request
        const response = await fetch(url, {
            method: method,
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCsrfToken(),
                'Accept': 'application/json'
            },
            body: JSON.stringify(unitData)
        });

        // Parse response
        const data = await response.json();

        // Handle non-successful responses
        if (!response.ok) {
            throw new Error(
                data.detail?.[0]?.msg ||
                data.detail ||
                langManager.translate('units.messages.saveError')
            );
        }

        // Close loading dialog
        if (loadingSwal) {
            loadingSwal.close();
        }

        // Show success message
        Swal.fire({
            title: langManager.translate('common.success'),
            text: langManager.translate(
                isEditing ?
                'units.messages.updateSuccess' :
                'units.messages.createSuccess'
            ),
            icon: 'success',
            confirmButtonColor: '#198754',
            timer: 2000,
            timerProgressBar: true
        });

        // Close the modal if it exists
        const modal = bootstrap.Modal.getInstance(document.getElementById('addUnitModal'));
        if (modal) {
            modal.hide();
        }

        // Clear form validation states
        form.querySelectorAll('.is-valid, .is-invalid').forEach(element => {
            element.classList.remove('is-valid', 'is-invalid');
        });

        // Reset form
        form.reset();

        // Refresh the page to show updated data
        window.location.reload();

    } catch (error) {
        console.error('Save Unit Error:', error);

        // Close loading state if it exists
        if (loadingSwal) {
            loadingSwal.close();
        }

        // Show error message
        await Swal.fire({
            title: langManager.translate('common.error'),
            text: error.message || langManager.translate('units.messages.saveError'),
            icon: 'error',
            confirmButtonColor: '#dc3545'
        });
    }
}

async function editUnit(unitId) {
    let loadingSwal;
    try {
        // Show loading state
        loadingSwal = Swal.fire({
            title: langManager.translate('common.loading'),
            text: langManager.translate('units.messages.loading'),
            allowOutsideClick: false,
            allowEscapeKey: false,
            showConfirmButton: false,
            didOpen: () => {
                Swal.showLoading();
            }
        });

        const response = await fetch(`/api/v1/units/${unitId}`);

        // Close loading state
        if (loadingSwal) {
            Swal.close();
        }

        if (!response.ok) {
            throw new Error(langManager.translate('units.messages.fetchError'));
        }

        const unit = await response.json();

        // Fill form fields with proper field IDs
        document.getElementById('unitName').value = unit.name || '';
        document.getElementById('unitIdentificationID').value = unit.national_id || '';
        document.getElementById('unitPhone').value = unit.phone || '';
        document.getElementById('unitPhoneAlt').value = unit.phone_alt || '';
        document.getElementById('unitPhoneEmergency').value = unit.phone_emergency || '';
        document.getElementById('unitPhoneEmergencyName').value = unit.phone_emergency_name || '';
        document.getElementById('unitEmail').value = unit.email || '';
        document.getElementById('unitWhatsapp').value = unit.whatsapp || '';
        document.getElementById('unitTelegram').value = unit.telegram || '';
        document.getElementById('unitNotes').value = unit.notes || '';
        console.log('unitId = ', unitId)
        document.getElementById('unitId').value = unitId;

        // Update modal title to indicate creating new unit
        const modalTitle = document.querySelector('#addUnitModalLabel span');
        if (modalTitle) {
            modalTitle.textContent = langManager.translate('units.createNew');
        }

        // Show modal
        const modal = new bootstrap.Modal(document.getElementById('addUnitModal'));
        modal.show();

        // Add event listener for form submission
        // const form = document.getElementById('unitForm');
        // form.onsubmit = async (e) => {
        //     e.preventDefault();
        //     await saveUnit(true); // Pass false to indicate creating new unit
        // };

    } catch (error) {
        console.error('Error:', error);

        // Make sure loading state is closed
        if (loadingSwal) {
            Swal.close();
        }

        // Show error message
        Swal.fire({
            title: langManager.translate('common.error'),
            text: error.message || langManager.translate('units.messages.editError'),
            icon: 'error',
            confirmButtonColor: '#dc3545'
        });
    }
}

// Validate unit data
function validateUnitData(data) {
    // Check required fields
    if (!data.name || !data.phone) {
        Swal.fire({
            title: langManager.translate('units.validationError'),
            text: langManager.translate('units.requiredFields'),
            icon: 'error',
            confirmButtonText: langManager.translate('common.ok')
        });
        return false;
    }

    // Validate email only if it exists
    if (data.email && !validateEmail(data.email)) {
        Swal.fire({
            title: langManager.translate('units.validationError'),
            text: langManager.translate('units.invalidEmail'),
            icon: 'error',
            confirmButtonText: langManager.translate('common.ok')
        });
        return false;
    }

    // Validate phone
    if (!validatePhone(data.phone)) {
        Swal.fire({
            title: langManager.translate('units.validationError'),
            text: langManager.translate('units.invalidPhone'),
            icon: 'error',
            confirmButtonText: langManager.translate('common.ok')
        });
        return false;
    }

    return true;
}

// Delete unit function
async function deleteUnit(unitId) {
    try {
        const result = await Swal.fire({
            title: langManager.translate('units.delete'),
            text: langManager.translate('units.deleteConfirmation'),
            icon: 'warning',
            showCancelButton: true,
            confirmButtonColor: '#dc3545',
            cancelButtonColor: '#6c757d',
            confirmButtonText: langManager.translate('units.deleteConfirmButton'),
            cancelButtonText: langManager.translate('common.cancel'),
            reverseButtons: true
        });

        if (result.isConfirmed) {
            Swal.fire({
                title: langManager.translate('units.deleting'),
                allowOutsideClick: false,
                allowEscapeKey: false,
                showConfirmButton: false,
                didOpen: () => {
                    Swal.showLoading();
                }
            });

            const response = await fetch(`/api/v1/units/${unitId}`, {
                method: 'DELETE',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCsrfToken(),
                    'Accept': 'application/json'
                }
            });

            if (!response.ok) {
                throw new Error(langManager.translate('units.deleteFail'));
            }

            Swal.fire({
                title: langManager.translate('common.success'),
                text: langManager.translate('units.deleteSuccess'),
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
            text: error.message || langManager.translate('units.deleteError'),
            icon: 'error',
            confirmButtonColor: '#dc3545'
        });
    }
}

// Reset form function
function resetForm() {
    const form = document.getElementById('unitForm');
    if (form) {
        form.reset();
        document.getElementById('unitId').value = '';

        // Reset validation states
        form.querySelectorAll('.is-valid, .is-invalid').forEach(element => {
            element.classList.remove('is-valid', 'is-invalid');
        });

        // Reset modal title
        const modalTitle = document.querySelector('#addUnitModalLabel span');
        if (modalTitle) {
            modalTitle.textContent = langManager.translate('units.addNew');
        }
    }
}

// Initialize page when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    // Modal reset on close
    const addUnitModal = document.getElementById('addUnitModal');
    if (addUnitModal) {
        addUnitModal.addEventListener('hidden.bs.modal', resetForm);
    }

    // Real-time validation for form fields
    const unitForm = document.getElementById('unitForm');
    if (unitForm) {
        unitForm.querySelectorAll('input, textarea').forEach(element => {
            element.addEventListener('input', function() {
                this.classList.remove('is-invalid', 'is-valid');
                if (this.value.trim()) {
                    if (this.id === 'unitEmail' && this.value) {
                        this.classList.add(validateEmail(this.value) ? 'is-valid' : 'is-invalid');
                    } else if (['unitPhone', 'unitPhoneAlt', 'unitPhoneEmergency'].includes(this.id)) {
                        this.classList.add(validatePhone(this.value) ? 'is-valid' : 'is-invalid');
                    } else {
                        this.classList.add('is-valid');
                    }
                }
            });
        });
    }

    // Search functionality
    const searchInput = document.getElementById('searchUnit');
    if (searchInput) {
        searchInput.addEventListener('input', function(e) {
            const searchTerm = e.target.value.toLowerCase();
            document.querySelectorAll('.unit-card').forEach(card => {
                const unitName = card.querySelector('.card-title').textContent.toLowerCase();
                card.closest('.col-md-6').style.display =
                    unitName.includes(searchTerm) ? '' : 'none';
            });
        });
    }

    // Status filter
    const statusFilter = document.getElementById('statusFilter');
    if (statusFilter) {
        statusFilter.addEventListener('change', function(e) {
            const selectedStatus = e.target.value === '1' ? 'active' : 'inactive';
            document.querySelectorAll('.unit-card').forEach(card => {
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