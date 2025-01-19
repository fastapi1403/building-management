// app/static/js/lang/fa.js
const fa = {
    base: {
        description: "سیستم مدیریت ساختمان حرفه ای - املاک خود را به صورت کارآمد مدیریت کنید",
        title: "سیستم مدیریت ساختمان",
        language: "زبان",
        english: "انگلیسی",
        persian: "فارسی",
        building_management: "مدیریت ساختمان",
        home: "خانه",
        dashboard: "داشبورد",
        user_profile: "حسن",
        profile: "پروفایل",
        settings: "تنظیمات",
        logout: "خروج",
        buildings: "ساختمان‌ها",
        tenants: "مستاجران",
        maintenance: "نگهداری",
        reports: "گزارش‌ها",
        footer_text: "© 2025 سیستم مدیریت ساختمان. کلیه حقوق محفوظ است.",
        current_utc_time: "زمان فعلی:",
        floors: "طبقات"
    },
    common: {
        add: "افزودن",
        edit: "ویرایش",
        delete: "حذف",
        save: "ذخیره",
        cancel: "انصراف",
        loading: "در حال بارگذاری...",
        success: "موفق!",
        error: "خطا!",
        confirm: "تایید",
        yes: "بله",
        no: "خیر",
        warning: "اخطار",
        ok: "تایید"
    },
    buildings: {
        title: "مدیریت ساختمان‌ها",
        subtitle: "مدیریت و نظارت بر تمام ساختمان‌ها",
        addNew: "افزودن ساختمان جدید",
        editBuilding: "ویرایش ساختمان",
        name: "نام ساختمان",
        floors: "طبقه",
        description: "توضیحات",
        search: "جستجوی ساختمان‌ها...",
        statusActive: "فعال",
        statusDeleted: "حذف شده",
        sortName: "مرتب‌سازی بر اساس نام",
        sortFloors: "مرتب‌سازی بر اساس طبقات",
        edit: "ویرایش ساختمان",
        delete: "حذف ساختمان",
        formName: "نام ساختمان",
        formFloors: "تعداد طبقات",
        formDescription: "توضیحات",
        formCancel: "لغو",
        formSave: "ذخیره ساختمان",
        validationError: "خطای اعتبارسنجی",
        required: "الزامی است!",
        validationFloors: "تعداد طبقات باید حداقل 1 باشد",
        loading: "در حال بارگذاری...",
        fetchingDetails: "در حال دریافت جزئیات ساختمان",
        error: "خطا!",
        loadError: "بارگیری جزئیات ساختمان با شکست مواجه شد. لطفا دوباره تلاش کنید.",
        unexpectedError: "خطای غیرمنتظره‌ای رخ داد. لطفاً دوباره تلاش کنید.",
        deleteConfirmation: "آیا مطمئن هستید که می‌خواهید این ساختمان را حذف کنید؟ این عمل قابل بازگشت نیست.",
        deleteConfirmButton: "بله، آن را حذف کن!",
        deleting: "در حال حذف...",
        deleteWait: "لطفاً صبر کنید تا ساختمان حذف شود.",
        deleteSuccess: "ساختمان با موفقیت حذف شد.",
        deleteError: "در حذف ساختمان خطایی رخ داد. لطفاً دوباره تلاش کنید.",
        deleteFail: "حذف ساختمان ناموفق بود",
        errorDeletingBuilding: "خطا در حذف ساختمان",
        status: {
            active: "فعال",
            deleted: "حذف شده"
        },
        units: "واحد",
        occupied: "اشغال شده",
        since: "از سال",
        validation: {
            nameRequired: "نام ساختمان الزامی است!",
            floorsRequired: "تعداد طبقات الزامی است!",
            minFloors: "تعداد طبقات باید حداقل 1 باشد"
        },
        messages: {
            deleteConfirm: "آیا از حذف این ساختمان اطمینان دارید؟ این عمل قابل بازگشت نیست.",
            deleteSuccess: "ساختمان با موفقیت حذف شد.",
            createSuccess: "ساختمان با موفقیت ایجاد شد!",
            updateSuccess: "ساختمان با موفقیت به‌روزرسانی شد!",
            loadError: "خطا در بارگذاری اطلاعات ساختمان. لطفا دوباره تلاش کنید.",
            saveError: "خطا در ذخیره‌سازی ساختمان. لطفا دوباره تلاش کنید.",
            loading: "در حال بارگذاری داده‌های ساختمان. لطفاً منتظر بمانید!",
        },
        detailTitle: "جزئیات ساختمان",
        details: {
            details: "جزئیات",
            basicInfo: "اطلاعات پایه",
            quickStats: "آمار سریع",
            financialSummary: "خلاصه مالی",
            maintenanceStatus: "وضعیت نگهداری",
            createdAt: "تاریخ ایجاد",
            lastUpdated: "آخرین بروزرسانی",
            totalIncome: "درآمد کل",
            totalExpenses: "هزینه‌های کل"
        },
        backToList: "بازگشت به لیست ساختمان‌ها",
        maintenanceHistory: "تاریخچه نگهداری",
        restore: "بازگردانی ساختمان",
        restoreConfirmation: "آیا از بازگردانی این ساختمان اطمینان دارید؟",
        restoreConfirmButton: "بله، بازگردانی شود!",
        restoreSuccess: "ساختمان با موفقیت بازگردانی شد.",
        restoreFail: "بازگردانی ساختمان ناموفق بود",
        cannotEditDeleted: "ویرایش ساختمان حذف شده امکان‌پذیر نیست",
        alreadyDeleted: "ساختمان قبلاً حذف شده است",
        confirmHardDeleteTitle: 'آیا مطمئن هستید؟',
        confirmHardDeleteText: 'آیا مطمئن هستید که می‌خواهید این ساختمان را به طور دائمی حذف کنید؟ این عمل قابل بازگشت نیست.',
        successHardDelete: 'ساختمان با موفقیت حذف شد',
        errorHardDelete: 'حذف ساختمان ناموفق بود. لطفاً دوباره تلاش کنید.',
        networkErrorHardDelete: 'شبکه پاسخ مناسبی نداشت.',
        hardDelete: 'حذف دائم'
    },
    floors: {
        // General
        title: "طبقات",
        addNew: "افزودن طبقه جدید",
        generalDetails: "جزئیات طبقه",
        searchPlaceholder: "جستجوی طبقات...",
        backToList: "بازگشت به لیست طبقات",

        // Form Labels
        formName: "نام طبقه",
        formNumber: "شماره طبقه",
        formUnits: "تعداد کل واحدها",
        formDescription: "توضیحات",
        formBuilding: "ساختمان",
        formCancel: "انصراف",
        formSave: "ذخیره طبقه",

        // Status
        status: {
            active: "فعال",
            deleted: "حذف شده",
            maintenance: "در حال تعمیر"
        },

        // Statistics
        units: "واحدها",
        occupied: "اشغال شده",
        vacant: "خالی",
        occupancyRate: "نرخ اشغال",
        maintenance: "وظایف نگهداری",

        // Actions
        edit: "ویرایش طبقه",
        delete: "حذف طبقه",
        restore: "بازیابی طبقه",
        hardDelete: "حذف دائمی",
        view: "مشاهده جزئیات",
        addUnit: "افزودن واحد",
        addMaintenance: "افزودن وظیفه نگهداری",

        // Confirmations
        deleteConfirmation: "آیا از حذف این طبقه اطمینان دارید؟",
        restoreConfirmation: "آیا از بازیابی این طبقه اطمینان دارید؟",
        hardDeleteConfirmation: "این عمل قابل بازگشت نیست. آیا اطمینان دارید؟",

        // Messages
        messages: {
            creating: "در حال ایجاد طبقه جدید...",
            updating: "در حال به‌روزرسانی طبقه...",
            deleting: "در حال حذف طبقه...",
            loading: "در حال بارگذاری اطلاعات طبقه...",
            saving: "در حال ذخیره طبقه...",
            createSuccess: "طبقه با موفقیت ایجاد شد",
            updateSuccess: "طبقه با موفقیت به‌روزرسانی شد",
            deleteSuccess: "طبقه با موفقیت حذف شد",
            restoreSuccess: "طبقه با موفقیت بازیابی شد",
            saveError: "خطا در ذخیره طبقه",
            deleteError: "خطا در حذف طبقه",
            fetchError: "خطا در دریافت اطلاعات طبقه",
            editError: "خطا در ویرایش طبقه",
            validationError: "لطفاً خطاهای فرم را بررسی کنید"
        },

        // Validation
        required: "این فیلد الزامی است",
        validationFloorNumber: "شماره طبقه باید بزرگتر از ۰ باشد",
        validationUnits: "تعداد کل واحدها باید ۰ یا بیشتر باشد",
        validationName: "نام طبقه الزامی است",

        // Details
        details: {
            basicInfo: "اطلاعات پایه",
            quickStats: "آمار سریع",
            maintenance: "تاریخچه نگهداری",
            units: "واحدها",
            createdAt: "تاریخ ایجاد",
            lastUpdated: "آخرین به‌روزرسانی",
            noMaintenanceHistory: "تاریخچه نگهداری موجود نیست"
        }
    }
};