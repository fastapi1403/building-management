// app/static/js/lang/en.js
const en = {
    base: {
        description: "Professional Building Management System - Efficiently manage your properties",
        title: "Building Management System",
        language: "Language",
        english: "English",
        persian: "Persian",
        building_management: "Building Management",
        home: "Home",
        dashboard: "Dashboard",
        user_profile: "Hassan",
        profile: "Profile",
        settings: "Settings",
        logout: "Logout",
        buildings: "Buildings",
        tenants: "Tenants",
        maintenance: "Maintenance",
        reports: "Reports",
        footer_text: "© 2025 Building Management System. All rights reserved.",
        current_utc_time: "Current Time:",
        floors: "Floors"
    },
    common: {
        add: "Add",
        edit: "Edit",
        delete: "Delete",
        save: "Save",
        cancel: "Cancel",
        loading: "Loading...",
        success: "Success!",
        error: "Error!",
        confirm: "Confirm",
        yes: "Yes",
        no: "No",
        warning: "Warning",
        ok: "OK"
    },
    buildings: {
        title: "Buildings Management",
        subtitle: "Manage and monitor all your buildings",
        addNew: "Add New Building",
        editBuilding: "Edit Building",
        name: "Building Name",
        floors: "Total Floors",
        description: "Description",
        search: "Search buildings...",
        statusActive: "Active",
        statusDeleted: "Deleted",
        sortName: "Sort by Name",
        sortFloors: "Sort by Floors",
        edit: "Edit Building",
        delete: "Delete Building",
        formName: "Building Name",
        formFloors: "Total Floors",
        formDescription: "Description",
        formCancel: "Cancel",
        formSave: "Save Building",
        validationError: "Validation Error",
        required: "is required!",
        validationFloors: "Number of floors must be at least 1",
        loading: "Loading...",
        fetchingDetails: "Fetching building details",
        error: "Error!",
        loadError: "Failed to load building details. Please try again.",
        unexpectedError: "An unexpected error occurred. Please try again.",
        deleteConfirmation: "Are you sure you want to delete this building? This action cannot be undone.",
        deleteConfirmButton: "Yes, delete it!",
        deleting: "Deleting...",
        deleteWait: "Please wait while we delete the building.",
        deleteSuccess: "The building has been successfully deleted.",
        deleteError: "There was an error deleting the building. Please try again.",
        deleteFail: "Failed to delete building",
        errorDeletingBuilding: "Error deleting building",
        status: {
            active: "Active",
            deleted: "Deleted"
        },
        units: "Units",
        occupied: "Occupied",
        since: "Since",
        validation: {
            nameRequired: "Building name is required!",
            floorsRequired: "Number of floors is required!",
            minFloors: "Number of floors must be at least 1"
        },
        messages: {
            deleteConfirm: "Are you sure you want to delete this building? This action cannot be undone.",
            deleteSuccess: "The building has been successfully deleted.",
            createSuccess: "Building created successfully!",
            updateSuccess: "Building updated successfully!",
            loadError: "Failed to load building details. Please try again.",
            saveError: "There was an error saving the building. Please try again.",
            loading: "Loading building data. Please wait!",
        },
        detailTitle: "Building Details",
        details: {
            details: "Details",
            basicInfo: "Basic Information",
            quickStats: "Quick Statistics",
            financialSummary: "Financial Summary",
            maintenanceStatus: "Maintenance Status",
            createdAt: "Created At",
            lastUpdated: "Last Updated",
            totalIncome: "Total Income",
            totalExpenses: "Total Expenses"
        },
        backToList: "Back to Buildings",
        maintenanceHistory: "Maintenance History",
        restore: "Restore Building",
        restoreConfirmation: "Are you sure you want to restore this building?",
        restoreConfirmButton: "Yes, restore it!",
        restoreSuccess: "The building has been successfully restored.",
        restoreFail: "Failed to restore building",
        cannotEditDeleted: "Cannot edit deleted building",
        alreadyDeleted: "Building already deleted",
        confirmHardDeleteTitle: 'Are you sure?',
        confirmHardDeleteText: 'Are you sure you want to permanently delete this building? This action cannot be undone.',
        successHardDelete: 'Building deleted successfully',
        errorHardDelete: 'Failed to delete the building. Please try again.',
        networkErrorHardDelete: 'Network response was not ok',
        hardDelete: 'Permanent delete'
    },
    floors: {
        // General
        title: "Floors",
        addNew: "Add New Floor",
        generalDetails: "Floor Details",
        searchPlaceholder: "Search floors...",
        backToList: "Back to Floors List",

        // Form Labels
        formName: "Floor Name",
        formNumber: "Floor Number",
        formUnits: "Total Units",
        formDescription: "Description",
        formBuilding: "Building",
        formCancel: "Cancel",
        formSave: "Save Floor",

        // Status
        status: {
            active: "Active",
            deleted: "Deleted",
            maintenance: "Under Maintenance"
        },

        // Statistics
        units: "Units",
        occupied: "Occupied",
        vacant: "Vacant",
        occupancyRate: "Occupancy Rate",
        maintenance: "Maintenance Tasks",

        // Actions
        edit: "Edit Floor",
        delete: "Delete Floor",
        restore: "Restore Floor",
        hardDelete: "Permanently Delete",
        view: "View Details",
        addUnit: "Add Unit",
        addMaintenance: "Add Maintenance Task",

        // Confirmations
        deleteConfirmation: "Are you sure you want to delete this floor?",
        restoreConfirmation: "Are you sure you want to restore this floor?",
        hardDeleteConfirmation: "This action cannot be undone. Are you sure?",

        // Messages
        messages: {
            creating: "Creating new floor...",
            updating: "Updating floor...",
            deleting: "Deleting floor...",
            loading: "Loading floor data...",
            saving: "Saving floor...",
            createSuccess: "Floor created successfully",
            updateSuccess: "Floor updated successfully",
            deleteSuccess: "Floor deleted successfully",
            restoreSuccess: "Floor restored successfully",
            saveError: "Failed to save floor",
            deleteError: "Failed to delete floor",
            fetchError: "Failed to fetch floor data",
            editError: "Failed to edit floor",
            validationError: "Please check the form for errors"
        },

        // Validation
        required: "This field is required",
        validationFloorNumber: "Floor number must be greater than 0",
        validationUnits: "Total units must be 0 or greater",
        validationName: "Floor name is required",

        // Details
        details: {
            basicInfo: "Basic Information",
            quickStats: "Quick Statistics",
            maintenance: "Maintenance History",
            units: "Units",
            createdAt: "Created At",
            lastUpdated: "Last Updated",
            noMaintenanceHistory: "No maintenance history available"
        }
    }
};
