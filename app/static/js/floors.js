// Floor management functions
async function createFloor() {
    try {
        const { value: formValues } = await Swal.fire({
            title: i18next.t('floors.form.create.title'),
            html: `
                <input id="floorName" class="swal2-input" 
                       placeholder="${i18next.t('floors.form.fields.name')}">
                <input id="floorNumber" type="number" class="swal2-input" 
                       placeholder="${i18next.t('floors.form.fields.number')}">
                <input id="totalUnits" type="number" class="swal2-input" 
                       placeholder="${i18next.t('floors.form.fields.totalUnits')}">
            `,
            focusConfirm: false,
            showCancelButton: true,
            confirmButtonText: i18next.t('floors.form.create.confirmButton'),
            preConfirm: () => {
                return {
                    name: document.getElementById('floorName').value,
                    number: document.getElementById('floorNumber').value,
                    total_units: document.getElementById('totalUnits').value
                }
            }
        });

        if (formValues) {
            const response = await fetch('/api/floors/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formValues)
            });

            if (response.ok) {
                Swal.fire({
                    icon: 'success',
                    title: i18next.t('floors.form.success.create'),
                    showConfirmButton: false,
                    timer: 1500
                }).then(() => {
                    window.location.reload();
                });
            } else {
                throw new Error('Failed to create floor');
            }
        }
    } catch (error) {
        console.error('Error:', error);
        Swal.fire({
            icon: 'error',
            title: 'Error',
            text: i18next.t('floors.form.error.create')
        });
    }
}

async function editFloor(floorId) {
    try {
        // First, fetch the current floor data
        const response = await fetch(`/api/floors/${floorId}`);
        const floor = await response.json();

        const { value: formValues } = await Swal.fire({
            title: 'Edit Floor',
            html: `
                <input id="floorName" class="swal2-input" placeholder="Floor Name" value="${floor.name}">
                <input id="floorNumber" type="number" class="swal2-input" placeholder="Floor Number" value="${floor.number}">
                <input id="totalUnits" type="number" class="swal2-input" placeholder="Total Units" value="${floor.total_units}">
            `,
            focusConfirm: false,
            showCancelButton: true,
            confirmButtonText: 'Update',
            preConfirm: () => {
                return {
                    name: document.getElementById('floorName').value,
                    number: document.getElementById('floorNumber').value,
                    total_units: document.getElementById('totalUnits').value
                }
            }
        });

        if (formValues) {
            const updateResponse = await fetch(`/api/floors/${floorId}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formValues)
            });

            if (updateResponse.ok) {
                Swal.fire({
                    icon: 'success',
                    title: 'Floor Updated Successfully',
                    showConfirmButton: false,
                    timer: 1500
                }).then(() => {
                    window.location.reload();
                });
            } else {
                throw new Error('Failed to update floor');
            }
        }
    } catch (error) {
        console.error('Error:', error);
        Swal.fire({
            icon: 'error',
            title: 'Error',
            text: 'Failed to update floor. Please try again.'
        });
    }
}

async function deleteFloor(floorId) {
    try {
        const result = await Swal.fire({
            title: 'Are you sure?',
            text: "You won't be able to revert this!",
            icon: 'warning',
            showCancelButton: true,
            confirmButtonColor: '#d33',
            cancelButtonColor: '#3085d6',
            confirmButtonText: 'Yes, delete it!'
        });

        if (result.isConfirmed) {
            const response = await fetch(`/api/floors/${floorId}`, {
                method: 'DELETE'
            });

            if (response.ok) {
                Swal.fire({
                    icon: 'success',
                    title: 'Floor Deleted Successfully',
                    showConfirmButton: false,
                    timer: 1500
                }).then(() => {
                    window.location.reload();
                });
            } else {
                throw new Error('Failed to delete floor');
            }
        }
    } catch (error) {
        console.error('Error:', error);
        Swal.fire({
            icon: 'error',
            title: 'Error',
            text: 'Failed to delete floor. Please try again.'
        });
    }
}

async function restoreFloor(floorId) {
    try {
        const result = await Swal.fire({
            title: 'Restore Floor?',
            text: "This will make the floor active again.",
            icon: 'question',
            showCancelButton: true,
            confirmButtonColor: '#3085d6',
            cancelButtonColor: '#d33',
            confirmButtonText: 'Yes, restore it!'
        });

        if (result.isConfirmed) {
            const response = await fetch(`/api/floors/${floorId}/restore`, {
                method: 'POST'
            });

            if (response.ok) {
                Swal.fire({
                    icon: 'success',
                    title: 'Floor Restored Successfully',
                    showConfirmButton: false,
                    timer: 1500
                }).then(() => {
                    window.location.reload();
                });
            } else {
                throw new Error('Failed to restore floor');
            }
        }
    } catch (error) {
        console.error('Error:', error);
        Swal.fire({
            icon: 'error',
            title: 'Error',
            text: 'Failed to restore floor. Please try again.'
        });
    }
}

// Search and filter functionality
document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('searchInput');
    const statusFilter = document.getElementById('statusFilter');
    const sortBy = document.getElementById('sortBy');

    if (searchInput) {
        searchInput.addEventListener('input', filterFloors);
    }
    if (statusFilter) {
        statusFilter.addEventListener('change', filterFloors);
    }
    if (sortBy) {
        sortBy.addEventListener('change', filterFloors);
    }
});

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

    // Reorder elements
    floorArray.forEach(card => {
        floorGrid.appendChild(card.closest('.col-md-6'));
    });
}