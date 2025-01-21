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

// Save tenant function to handle the save/update process
async function saveTenant() {
    let loadingSwal;
    try {
        const tenantId = document.getElementById('tenantId')?.value
        const isEditing = tenantId !== '';

        // Get the form element
        const form = document.getElementById('tenantForm');
        if (!form) {
            throw new Error(langManager.translate('tenants.formNotFound'));
        }

            console.log('tenantData');
        // Collect data from form fields with null coalescing and trimming
        const tenantData = {
            name: document.getElementById('tenantName')?.value?.trim() || '',
            phone: document.getElementById('tenantPhone')?.value?.trim() || '',
            // Optional fields
            national_id: document.getElementById('tenantIdentificationID')?.value?.trim() || '',
            // phone_alt: document.getElementById('tenantPhoneAlt')?.value?.trim() || '',
            phone_emergency: document.getElementById('tenantPhoneEmergency')?.value?.trim() || '',
            phone_emergency_name: document.getElementById('tenantPhoneEmergencyName')?.value?.trim() || '',
            phone_emergency_relation: document.getElementById('tenantPhoneEmergencyRelation')?.value?.trim() || '',
            email: document.getElementById('tenantEmail')?.value?.trim() || '',
            whatsapp: document.getElementById('tenantWhatsapp')?.value?.trim() || '',
            telegram: document.getElementById('tenantTelegram')?.value?.trim() || '',
            notes: document.getElementById('tenantNotes')?.value?.trim() || ''
        };

            console.log(tenantData);


        // Remove empty optional fields
        Object.keys(tenantData).forEach(key => {
            if (!tenantData[key] && key !== 'name' && key !== 'phone') {
                delete tenantData[key];
            }
        });

        // Validate tenant data
        if (!validateTenantData(tenantData)) {
            return false;
        }

        // Show loading state
        loadingSwal = Swal.fire({
            title: langManager.translate('common.loading'),
            text: langManager.translate(isEditing ? 'tenants.messages.updating' : 'tenants.messages.saving'),
            allowOutsideClick: false,
            allowEscapeKey: false,
            showConfirmButton: false,
            didOpen: () => {
                Swal.showLoading();
            }
        });

        // Prepare request URL and method
        const url = isEditing ? `/api/v1/tenants/${tenantId}` : '/api/v1/tenants';
        const method = isEditing ? 'PUT' : 'POST';

        // Make API request
        const response = await fetch(url, {
            method: method,
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCsrfToken(),
                'Accept': 'application/json'
            },
            body: JSON.stringify(tenantData)
        });

        // Parse response
        const data = await response.json();

        // Handle non-successful responses
        if (!response.ok) {
            throw new Error(
                data.detail?.[0]?.msg ||
                data.detail ||
                langManager.translate('tenants.messages.saveError')
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
                'tenants.messages.updateSuccess' :
                'tenants.messages.createSuccess'
            ),
            icon: 'success',
            confirmButtonColor: '#198754',
            timer: 2000,
            timerProgressBar: true
        });

        // Close the modal if it exists
        const modal = bootstrap.Modal.getInstance(document.getElementById('addTenantModal'));
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
        console.error('Save Tenant Error:', error);

        // Close loading state if it exists
        if (loadingSwal) {
            loadingSwal.close();
        }

        // Show error message
        await Swal.fire({
            title: langManager.translate('common.error'),
            text: error.message || langManager.translate('tenants.messages.saveError'),
            icon: 'error',
            confirmButtonColor: '#dc3545'
        });
    }
}

async function editTenant(tenantId) {
    let loadingSwal;
    try {
        // Show loading state
        loadingSwal = Swal.fire({
            title: langManager.translate('common.loading'),
            text: langManager.translate('tenants.messages.loading'),
            allowOutsideClick: false,
            allowEscapeKey: false,
            showConfirmButton: false,
            didOpen: () => {
                Swal.showLoading();
            }
        });

        const response = await fetch(`/api/v1/tenants/${tenantId}`);

        // Close loading state
        if (loadingSwal) {
            Swal.close();
        }

        if (!response.ok) {
            throw new Error(langManager.translate('tenants.messages.fetchError'));
        }

        const tenant = await response.json();

        // Fill form fields with proper field IDs
        document.getElementById('tenantName').value = tenant.name || '';
        document.getElementById('tenantIdentificationID').value = tenant.national_id || '';
        document.getElementById('tenantPhone').value = tenant.phone || '';
        // document.getElementById('tenantPhoneAlt').value = tenant.phone_alt || '';
        document.getElementById('tenantPhoneEmergency').value = tenant.phone_emergency || '';
        document.getElementById('tenantPhoneEmergencyName').value = tenant.phone_emergency_name || '';
        document.getElementById('tenantPhoneEmergencyRelation').value = tenant.phone_emergency_relation || '';
        document.getElementById('tenantEmail').value = tenant.email || '';
        document.getElementById('tenantWhatsapp').value = tenant.whatsapp || '';
        document.getElementById('tenantTelegram').value = tenant.telegram || '';
        document.getElementById('tenantNotes').value = tenant.notes || '';
        console.log('tenantId = ', tenantId)
        document.getElementById('tenantId').value = tenantId;

        // Update modal title to indicate creating new tenant
        const modalTitle = document.querySelector('#addTenantModalLabel span');
        if (modalTitle) {
            modalTitle.textContent = langManager.translate('tenants.createNew');
        }

        // Show modal
        const modal = new bootstrap.Modal(document.getElementById('addTenantModal'));
        modal.show();

        // Add event listener for form submission
        // const form = document.getElementById('tenantForm');
        // form.onsubmit = async (e) => {
        //     e.preventDefault();
        //     await saveTenant(true); // Pass false to indicate creating new tenant
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
            text: error.message || langManager.translate('tenants.messages.editError'),
            icon: 'error',
            confirmButtonColor: '#dc3545'
        });
    }
}

// Validate tenant data
function validateTenantData(data) {
    // Check required fields
    if (!data.name || !data.phone) {
        Swal.fire({
            title: langManager.translate('tenants.validationError'),
            text: langManager.translate('tenants.requiredFields'),
            icon: 'error',
            confirmButtonText: langManager.translate('common.ok')
        });
        return false;
    }

    // Validate email only if it exists
    if (data.email && !validateEmail(data.email)) {
        Swal.fire({
            title: langManager.translate('tenants.validationError'),
            text: langManager.translate('tenants.invalidEmail'),
            icon: 'error',
            confirmButtonText: langManager.translate('common.ok')
        });
        return false;
    }

    // Validate phone
    if (!validatePhone(data.phone)) {
        Swal.fire({
            title: langManager.translate('tenants.validationError'),
            text: langManager.translate('tenants.invalidPhone'),
            icon: 'error',
            confirmButtonText: langManager.translate('common.ok')
        });
        return false;
    }

    return true;
}

// Delete tenant function
async function deleteTenant(tenantId) {
    try {
        const result = await Swal.fire({
            title: langManager.translate('tenants.delete'),
            text: langManager.translate('tenants.deleteConfirmation'),
            icon: 'warning',
            showCancelButton: true,
            confirmButtonColor: '#dc3545',
            cancelButtonColor: '#6c757d',
            confirmButtonText: langManager.translate('tenants.deleteConfirmButton'),
            cancelButtonText: langManager.translate('common.cancel'),
            reverseButtons: true
        });

        if (result.isConfirmed) {
            Swal.fire({
                title: langManager.translate('tenants.deleting'),
                allowOutsideClick: false,
                allowEscapeKey: false,
                showConfirmButton: false,
                didOpen: () => {
                    Swal.showLoading();
                }
            });

            const response = await fetch(`/api/v1/tenants/${tenantId}`, {
                method: 'DELETE',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCsrfToken(),
                    'Accept': 'application/json'
                }
            });

            if (!response.ok) {
                throw new Error(langManager.translate('tenants.deleteFail'));
            }

            Swal.fire({
                title: langManager.translate('common.success'),
                text: langManager.translate('tenants.deleteSuccess'),
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
            text: error.message || langManager.translate('tenants.deleteError'),
            icon: 'error',
            confirmButtonColor: '#dc3545'
        });
    }
}

// Reset form function
function resetForm() {
    const form = document.getElementById('tenantForm');
    if (form) {
        form.reset();
        document.getElementById('tenantId').value = '';

        // Reset validation states
        form.querySelectorAll('.is-valid, .is-invalid').forEach(element => {
            element.classList.remove('is-valid', 'is-invalid');
        });

        // Reset modal title
        const modalTitle = document.querySelector('#addTenantModalLabel span');
        if (modalTitle) {
            modalTitle.textContent = langManager.translate('tenants.addNew');
        }
    }
}

// Initialize page when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    // Modal reset on close
    const addTenantModal = document.getElementById('addTenantModal');
    if (addTenantModal) {
        addTenantModal.addEventListener('hidden.bs.modal', resetForm);
    }

    // Real-time validation for form fields
    const tenantForm = document.getElementById('tenantForm');
    if (tenantForm) {
        tenantForm.querySelectorAll('input, textarea').forEach(element => {
            element.addEventListener('input', function() {
                this.classList.remove('is-invalid', 'is-valid');
                if (this.value.trim()) {
                    if (this.id === 'tenantEmail' && this.value) {
                        this.classList.add(validateEmail(this.value) ? 'is-valid' : 'is-invalid');
                    } else if (['tenantPhone', 'tenantPhoneAlt', 'tenantPhoneEmergency'].includes(this.id)) {
                        this.classList.add(validatePhone(this.value) ? 'is-valid' : 'is-invalid');
                    } else {
                        this.classList.add('is-valid');
                    }
                }
            });
        });
    }

    // Search functionality
    const searchInput = document.getElementById('searchTenant');
    if (searchInput) {
        searchInput.addEventListener('input', function(e) {
            const searchTerm = e.target.value.toLowerCase();
            document.querySelectorAll('.tenant-card').forEach(card => {
                const tenantName = card.querySelector('.card-title').textContent.toLowerCase();
                card.closest('.col-md-6').style.display =
                    tenantName.includes(searchTerm) ? '' : 'none';
            });
        });
    }

    // Status filter
    const statusFilter = document.getElementById('statusFilter');
    if (statusFilter) {
        statusFilter.addEventListener('change', function(e) {
            const selectedStatus = e.target.value === '1' ? 'active' : 'inactive';
            document.querySelectorAll('.tenant-card').forEach(card => {
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