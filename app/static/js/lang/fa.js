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
    "floors": {
    "title": "طبقات",
    "add": "افزودن طبقه جدید",
    "addNew": "افزودن طبقه جدید",
    "edit": "ویرایش طبقه",
    "delete": "حذف طبقه",
    "view": "مشاهده طبقه",
    "formName": "نام طبقه",
    "formNumber": "شماره طبقه",
    "formUnits": "تعداد کل واحدها",
    "formDescription": "توضیحات",
    "formSave": "ذخیره",
    "formCancel": "انصراف",
    "required": "الزامی است",
    "validationError": "خطای اعتبارسنجی",
    "validationNumber": "شماره طبقه باید بزرگتر از 0 باشد",
    "validationUnits": "تعداد واحدها باید بزرگتر از 0 باشد",
    "deleteConfirmation": "آیا از حذف این طبقه مطمئن هستید؟",
    "deleteConfirmButton": "بله، حذف شود!",
    "restore": "بازیابی طبقه",
    "restoreConfirmation": "آیا می‌خواهید این طبقه را بازیابی کنید؟",
    "restoreConfirmButton": "بله، بازیابی شود!",
    "units": "واحدها",
    "occupied": "اشغال شده",
    "maintenance": "تعمیر و نگهداری",
    "messages": {
      "loading": "در حال بارگذاری اطلاعات طبقه...",
      "saving": "در حال ذخیره طبقه...",
      "updating": "در حال به‌روزرسانی طبقه...",
      "deleting": "در حال حذف طبقه...",
      "deleteWait": "لطفاً صبر کنید در حال حذف طبقه...",
      "saveError": "خطا در ذخیره طبقه",
      "updateSuccess": "طبقه با موفقیت به‌روزرسانی شد",
      "createSuccess": "طبقه با موفقیت ایجاد شد",
      "deleteSuccess": "طبقه با موفقیت حذف شد",
      "editError": "خطا در ویرایش طبقه",
      "fetchError": "خطا در دریافت اطلاعات طبقه",
      "deleteFail": "خطا در حذف طبقه",
      "deleteError": "خطا در حذف طبقه",
      "restoreSuccess": "طبقه با موفقیت بازیابی شد",
      "restoreFail": "خطا در بازیابی طبقه",
        "saveSuccess": "طبقه با موفقیت ذخیره شد",
        "updateError": "خطا در به‌روزرسانی طبقه"
    }
  }
};