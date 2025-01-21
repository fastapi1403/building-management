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
        units: "Units",
        tenants: "Tenants",
        owners: "Owners",
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
    "floors": {
        "title": "Floors",
        "add": "Add New Floor",
        "addNew": "Add New Floor",
        "edit": "Edit Floor",
        "delete": "Delete Floor",
        "view": "View Floor",
        "formName": "Floor Name",
        "formNumber": "Floor Number",
        "formUnits": "Total Units",
        "formDescription": "Description",
        "formSave": "Save",
        "formCancel": "Cancel",
        "required": "is required",
        "validationError": "Validation Error",
        "validationNumber": "Floor number must be greater than 0",
        "validationUnits": "Total units must be greater than 0",
        "deleteConfirmation": "Are you sure you want to delete this floor?",
        "deleteConfirmButton": "Yes, delete it!",
        "restore": "Restore Floor",
        "restoreConfirmation": "Do you want to restore this floor?",
        "restoreConfirmButton": "Yes, restore it!",
        "units": "Units",
        "occupied": "Occupied",
        "maintenance": "Maintenance",
        "messages": {
          "loading": "Loading floor data...",
          "saving": "Saving floor...",
          "updating": "Updating floor...",
          "deleting": "Deleting floor...",
          "deleteWait": "Please wait while we delete the floor...",
          "saveError": "Failed to save floor",
          "updateSuccess": "Floor updated successfully",
          "createSuccess": "Floor created successfully",
          "deleteSuccess": "Floor deleted successfully",
          "editError": "Error editing floor",
          "fetchError": "Error fetching floor data",
          "deleteFail": "Failed to delete floor",
          "deleteError": "Error deleting floor",
          "restoreSuccess": "Floor restored successfully",
          "restoreFail": "Failed to restore floor",
            "saveSuccess": "Floor saved successfully",
            "updateError": "Error updating floor"
        },
        "form": {
          "building": "Building",
          "description": "Description",
          "selectBuilding": "Select Building",
          "buildingRequired": "Please select a building",
          "descriptionPlaceholder": "Enter floor description (optional)"
        }
    },
    owners: {
        title: "Owners Management",
        subtitle: "Manage and monitor all your owners",
        addNew: "Add New Owner",
        editOwner: "Edit Owner",
        name: "Owner Name",
        floors: "Total Floors",
        description: "Description",
        search: "Search owners...",
        statusActive: "Active",
        statusDeleted: "Deleted",
        sortName: "Sort by Name",
        sortFloors: "Sort by Floors",
        edit: "Edit Owner",
        delete: "Delete Owner",
        formName: "Owner Name",
        formFloors: "Total Floors",
        formDescription: "Description",
        formCancel: "Cancel",
        formSave: "Save Owner",
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
        errorDeletingOwner: "Error deleting building",
        status: {
            active: "Active",
            deleted: "Deleted"
        },
        units: "Units",
        occupied: "Occupied",
        since: "Since",
        validation: {
            nameRequired: "Owner name is required!",
            floorsRequired: "Number of floors is required!",
            minFloors: "Number of floors must be at least 1"
        },
        messages: {
            deleteConfirm: "Are you sure you want to delete this building? This action cannot be undone.",
            deleteSuccess: "The building has been successfully deleted.",
            createSuccess: "Owner created successfully!",
            updateSuccess: "Owner updated successfully!",
            loadError: "Failed to load building details. Please try again.",
            saveError: "There was an error saving the building. Please try again.",
            loading: "Loading building data. Please wait!",
        },
        detailTitle: "Owner Details",
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
        form: {
            name: "Owner Name",
            id: "Identification No.",
            phone: "Phone",
            phoneAlt: "Alternative phone",
            phoneEmergency: "Emergency phone",
            phoneEmergencyName: "Emergency phone name",
            email: "Email",
            whatsapp: "Whatsapp",
            telegram: "Telegram",
            note: "Note",
            cancel: "Cancel",
            save: "Save Owner"
        },
        backToList: "Back to Owners",
        maintenanceHistory: "Maintenance History",
        restore: "Restore Owner",
        restoreConfirmation: "Are you sure you want to restore this building?",
        restoreConfirmButton: "Yes, restore it!",
        restoreSuccess: "The building has been successfully restored.",
        restoreFail: "Failed to restore building",
        cannotEditDeleted: "Cannot edit deleted building",
        alreadyDeleted: "Owner already deleted",
        confirmHardDeleteTitle: 'Are you sure?',
        confirmHardDeleteText: 'Are you sure you want to permanently delete this building? This action cannot be undone.',
        successHardDelete: 'Owner deleted successfully',
        errorHardDelete: 'Failed to delete the building. Please try again.',
        networkErrorHardDelete: 'Network response was not ok',
        hardDelete: 'Permanent delete',
    },
    tenants: {
        title: "Tenants Management",
        subtitle: "Manage and monitor all your tenants",
        addNew: "Add New Tenant",
        editTenant: "Edit Tenant",
        name: "Tenant Name",
        floors: "Total Floors",
        description: "Description",
        search: "Search tenants...",
        statusActive: "Active",
        statusDeleted: "Deleted",
        sortName: "Sort by Name",
        sortFloors: "Sort by Floors",
        edit: "Edit Tenant",
        delete: "Delete Tenant",
        formName: "Tenant Name",
        formFloors: "Total Floors",
        formDescription: "Description",
        formCancel: "Cancel",
        formSave: "Save Tenant",
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
        errorDeletingTenant: "Error deleting building",
        status: {
            active: "Active",
            deleted: "Deleted"
        },
        units: "Units",
        occupied: "Occupied",
        since: "Since",
        validation: {
            nameRequired: "Tenant name is required!",
            floorsRequired: "Number of floors is required!",
            minFloors: "Number of floors must be at least 1"
        },
        messages: {
            deleteConfirm: "Are you sure you want to delete this building? This action cannot be undone.",
            deleteSuccess: "The building has been successfully deleted.",
            createSuccess: "Tenant created successfully!",
            updateSuccess: "Tenant updated successfully!",
            loadError: "Failed to load building details. Please try again.",
            saveError: "There was an error saving the building. Please try again.",
            loading: "Loading building data. Please wait!",
        },
        detailTitle: "Tenant Details",
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
        form: {
            name: "Tenant Name",
            id: "Identification No.",
            phone: "Phone",
            phoneAlt: "Alternative phone",
            phoneEmergency: "Emergency phone",
            phoneEmergencyName: "Emergency phone name",
            phoneEmergencyRelation: "Relation with tenant",
            email: "Email",
            whatsapp: "Whatsapp",
            telegram: "Telegram",
            note: "Note",
            cancel: "Cancel",
            save: "Save Tenant"
        },
        backToList: "Back to Tenants",
        maintenanceHistory: "Maintenance History",
        restore: "Restore Tenant",
        restoreConfirmation: "Are you sure you want to restore this building?",
        restoreConfirmButton: "Yes, restore it!",
        restoreSuccess: "The building has been successfully restored.",
        restoreFail: "Failed to restore building",
        cannotEditDeleted: "Cannot edit deleted building",
        alreadyDeleted: "Tenant already deleted",
        confirmHardDeleteTitle: 'Are you sure?',
        confirmHardDeleteText: 'Are you sure you want to permanently delete this building? This action cannot be undone.',
        successHardDelete: 'Tenant deleted successfully',
        errorHardDelete: 'Failed to delete the building. Please try again.',
        networkErrorHardDelete: 'Network response was not ok',
        hardDelete: 'Permanent delete',
    },
    units: {
        title: "Units Management",
        subtitle: "Manage and monitor all your units",
        addNew: "Add New Unit",
        editUnit: "Edit Unit",
        name: "Unit Name",
        floors: "Total Floors",
        description: "Description",
        search: "Search units...",
        statusActive: "Active",
        statusDeleted: "Deleted",
        sortName: "Sort by Name",
        sortFloors: "Sort by Floors",
        edit: "Edit Unit",
        delete: "Delete Unit",
        formName: "Unit Name",
        formFloors: "Total Floors",
        formDescription: "Description",
        formCancel: "Cancel",
        formSave: "Save Unit",
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
        errorDeletingUnit: "Error deleting building",
        status: {
            active: "Active",
            deleted: "Deleted"
        },
        units: "Units",
        occupied: "Occupied",
        since: "Since",
        validation: {
            nameRequired: "Unit name is required!",
            floorsRequired: "Number of floors is required!",
            minFloors: "Number of floors must be at least 1"
        },
        messages: {
            deleteConfirm: "Are you sure you want to delete this building? This action cannot be undone.",
            deleteSuccess: "The building has been successfully deleted.",
            createSuccess: "Unit created successfully!",
            updateSuccess: "Unit updated successfully!",
            loadError: "Failed to load building details. Please try again.",
            saveError: "There was an error saving the building. Please try again.",
            loading: "Loading building data. Please wait!",
        },
        detailTitle: "Unit Details",
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
        form: {
            name: "Unit Name",
            id: "Identification No.",
            phone: "Phone",
            phoneAlt: "Alternative phone",
            phoneEmergency: "Emergency phone",
            phoneEmergencyName: "Emergency phone name",
            email: "Email",
            whatsapp: "Whatsapp",
            telegram: "Telegram",
            note: "Note",
            cancel: "Cancel",
            save: "Save Unit"
        },
        backToList: "Back to Units",
        maintenanceHistory: "Maintenance History",
        restore: "Restore Unit",
        restoreConfirmation: "Are you sure you want to restore this building?",
        restoreConfirmButton: "Yes, restore it!",
        restoreSuccess: "The building has been successfully restored.",
        restoreFail: "Failed to restore building",
        cannotEditDeleted: "Cannot edit deleted building",
        alreadyDeleted: "Unit already deleted",
        confirmHardDeleteTitle: 'Are you sure?',
        confirmHardDeleteText: 'Are you sure you want to permanently delete this building? This action cannot be undone.',
        successHardDelete: 'Unit deleted successfully',
        errorHardDelete: 'Failed to delete the building. Please try again.',
        networkErrorHardDelete: 'Network response was not ok',
        hardDelete: 'Permanent delete',
    },
};
