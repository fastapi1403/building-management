/**
 * floors.js
 * Floor management functionality for Building Management System
 * Author: fastapi1403
 * Last Updated: 2025-01-19
 */

// Function to update existing floor card
function updateFloorCard(floor) {
    const floorCard = document.querySelector(`[data-floor-id="${floor.id}"]`);
    if (!floorCard) {
        window.location.reload();
        return;
    }

    const elements = {
        title: floorCard.querySelector('.card-title'),
        status: floorCard.querySelector('.status-badge'),
        units: floorCard.querySelector('[data-stat="units"]'),
        occupancyRate: floorCard.querySelector('[data-stat="occupancy"]'),
        floorNumber: floorCard.querySelector('[data-stat="floor-number"]'),
        maintenanceCount: floorCard.querySelector('[data-stat="maintenance"]'),
        progressBar: floorCard.querySelector('.progress-bar')
    };

    // Update basic info
    elements.title.textContent = floor.name;
    elements.status.className = `status-badge ${floor.is_deleted ? 'status-inactive' : 'status-active'}`;
    elements.status.textContent = floor.is_deleted ? 'Deleted' : 'Active';

    // Update statistics
    if (elements.units) elements.units.textContent = `${floor.total_units} Units`;
    if (elements.occupancyRate) elements.occupancyRate.textContent = `${floor.occupancy_rate}%`;
    if (elements.floorNumber) elements.floorNumber.textContent = `Floor ${floor.number}`;
    if (elements.maintenanceCount) {
        elements.maintenanceCount.textContent = `${floor.maintenance_count || 0} Tasks`;
    }

    // Update progress bar
    if (elements.progressBar) {
        elements.progressBar.style.width = `${floor.occupancy_rate}%`;
        elements.progressBar.setAttribute('aria-valuenow', floor.occupancy_rate);
    }

    // Visual feedback for update
    floorCard.style.transition = 'background-color 0.5s ease';
    floorCard.style.backgroundColor = '#e8f5e9';
    setTimeout(() => {
        floorCard.style.backgroundColor = '';
    }, 1500);
}

// Save or update floor
async function saveFloor(event) {
    event?.preventDefault();

    const floorId = document.getElementById('floorId')?.value;
    const isEditing = !!floorId;

    const floorData = {
        name: document.getElementById('floorName').value,
        number: parseInt(document.getElementById('floorNumber').value),
        building_id: parseInt(document.getElementById('buildingId').value),
        total_units: parseInt(document.getElementById('totalUnits').value),
        description: document.getElementById('floorDescription').value,
        updated_by: 'fastapi1403',
        updated_at: new Date().toISOString()
    };

    if (!validateFloorData(floorData)) return;

    try {
        showLoadingIndicator(isEditing ? 'Updating...' : 'Creating...');

        const url = `/api/v1/floors${isEditing ? `/${floorId}` : ''}`;
        const response = await fetch(url, {
            method: isEditing ? 'PUT' : 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCsrfToken()
            },
            body: JSON.stringify(floorData)
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Operation failed');
        }

        const savedFloor = await response.json();

        await showSuccessMessage(
            isEditing ? 'Floor Updated' : 'Floor Created',
            isEditing ? 'Floor has been updated successfully.' : 'New floor has been created successfully.'
        );

        if (isEditing) {
            updateFloorCard(savedFloor);
        } else {
            addNewFloorCard(savedFloor);
        }

        closeModal('floorModal');

    } catch (error) {
        showErrorMessage('Operation Failed', error.message);
    }
}

// Delete floor
async function deleteFloor(floorId) {
    const result = await showConfirmDialog(
        'Delete Floor?',
        'Are you sure you want to delete this floor? This action can be undone later.',
        'warning'
    );

    if (!result.isConfirmed) return;

    try {
        showLoadingIndicator('Deleting...');

        const response = await fetch(`/api/v1/floors/${floorId}`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCsrfToken()
            }
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Failed to delete floor');
        }

        await showSuccessMessage('Floor Deleted', 'Floor has been deleted successfully.');
        document.querySelector(`[data-floor-id="${floorId}"]`)?.remove();

    } catch (error) {
        showErrorMessage('Delete Failed', error.message);
    }
}

// Hard delete floor
async function hardDeleteFloor(floorId) {
    const result = await showConfirmDialog(
        'Permanently Delete Floor?',
        'This action cannot be undone. Are you sure you want to permanently delete this floor?',
        'warning'
    );

    if (!result.isConfirmed) return;

    try {
        showLoadingIndicator('Deleting permanently...');

        const response = await fetch(`/api/v1/floors/${floorId}/permanent`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCsrfToken()
            }
        });

        if (!response.ok) throw new Error('Failed to permanently delete floor');

        await showSuccessMessage('Floor Deleted Permanently', 'Floor has been permanently deleted.');
        window.location.href = '/floors';

    } catch (error) {
        showErrorMessage('Permanent Delete Failed', error.message);
    }
}

// Restore deleted floor
async function restoreFloor(floorId) {
    try {
        showLoadingIndicator('Restoring...');

        const response = await fetch(`/api/v1/floors/${floorId}/restore`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCsrfToken()
            }
        });

        if (!response.ok) throw new Error('Failed to restore floor');

        await showSuccessMessage('Floor Restored', 'Floor has been restored successfully.');
        window.location.reload();

    } catch (error) {
        showErrorMessage('Restore Failed', error.message);
    }
}

// Validate floor data
function validateFloorData(data) {
    const validations = [
        { field: 'name', message: 'Floor name is required' },
        { field: 'number', message: 'Floor number must be greater than 0', condition: n => n > 0 },
        { field: 'building_id', message: 'Building ID is required' },
        { field: 'total_units', message: 'Total units must be 0 or greater', condition: n => n >= 0 }
    ];

    for (const validation of validations) {
        const value = data[validation.field];
        if (!value || (validation.condition && !validation.condition(value))) {
            showErrorMessage('Validation Error', validation.message);
            return false;
        }
    }

    return true;
}

// UI Helper Functions
function showLoadingIndicator(message) {
    return Swal.fire({
        title: message,
        allowOutsideClick: false,
        didOpen: () => Swal.showLoading()
    });
}

function showSuccessMessage(title, message) {
    return Swal.fire({
        title,
        text: message,
        icon: 'success',
        timer: 2000,
        timerProgressBar: true
    });
}

function showErrorMessage(title, message) {
    return Swal.fire({
        title,
        text: message,
        icon: 'error'
    });
}

function showConfirmDialog(title, text, icon) {
    return Swal.fire({
        title,
        text,
        icon,
        showCancelButton: true,
        confirmButtonColor: '#dc3545',
        cancelButtonColor: '#6c757d',
        confirmButtonText: 'Yes, proceed',
        cancelButtonText: 'Cancel'
    });
}

function closeModal(modalId) {
    const modal = bootstrap.Modal.getInstance(document.getElementById(modalId));
    if (modal) modal.hide();
}

function getCsrfToken() {
    return document.querySelector('meta[name="csrf-token"]')?.getAttribute('content');
}

// Initialize floor management page
document.addEventListener('DOMContentLoaded', function() {
    // Search functionality
    const searchInput = document.getElementById('searchInput');
    if (searchInput) {
        searchInput.addEventListener('input', function(e) {
            const searchTerm = e.target.value.toLowerCase();
            document.querySelectorAll('.floor-card').forEach(card => {
                const floorName = card.querySelector('.card-title').textContent.toLowerCase();
                const floorNumber = card.querySelector('[data-stat="floor-number"]').textContent.toLowerCase();
                card.closest('.col').style.display =
                    floorName.includes(searchTerm) || floorNumber.includes(searchTerm) ? '' : 'none';
            });
        });
    }

    // Status filter
    const statusFilter = document.getElementById('statusFilter');
    if (statusFilter) {
        statusFilter.addEventListener('change', function(e) {
            const status = e.target.value;
            document.querySelectorAll('.floor-card').forEach(card => {
                const isDeleted = card.querySelector('.status-badge').classList.contains('status-inactive');
                card.closest('.col').style.display =
                    (status === '1' && !isDeleted) || (status === '0' && isDeleted) ? '' : 'none';
            });
        });
    }

    // Form validation
    const floorForm = document.getElementById('floorForm');
    if (floorForm) {
        floorForm.addEventListener('submit', saveFloor);
        floorForm.querySelectorAll('input').forEach(input => {
            input.addEventListener('input', function() {
                this.classList.toggle('is-valid', this.checkValidity());
                this.classList.toggle('is-invalid', !this.checkValidity());
            });
        });
    }
});