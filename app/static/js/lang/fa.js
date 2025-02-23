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
        units: "واحدها",
        tenants: "مستاجران",
        owners: "مالکین",
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
        },
        "form": {
          "building": "ساختمان",
          "description": "توضیحات",
          "selectBuilding": "ساختمان را انتخاب کنید",
          "buildingRequired": "لطفاً یک ساختمان انتخاب کنید",
          "descriptionPlaceholder": "توضیحات طبقه را وارد کنید (اختیاری)"
        }
    },
    owners: {
     title: "مدیریت مالکین",
        subtitle: "مدیریت و نظارت بر تمام مالکین",
        addNew: "افزودن مالک جدید",
        editBuilding: "ویرایش مالک",
        name: "نام مالک",
        floors: "طبقه",
        description: "توضیحات",
        search: "جستجوی مالکین...",
        statusActive: "فعال",
        statusDeleted: "حذف شده",
        sortName: "مرتب‌سازی بر اساس نام",
        sortFloors: "مرتب‌سازی بر اساس طبقات",
        edit: "ویرایش مالک",
        delete: "حذف مالک",
        formName: "نام مالک",
        formFloors: "تعداد طبقات",
        formDescription: "توضیحات",
        formCancel: "لغو",
        formSave: "ذخیره مالک",
        validationError: "خطای اعتبارسنجی",
        required: "الزامی است!",
        validationFloors: "تعداد طبقات باید حداقل 1 باشد",
        loading: "در حال بارگذاری...",
        fetchingDetails: "در حال دریافت جزئیات مالک",
        error: "خطا!",
        loadError: "بارگیری جزئیات مالک با شکست مواجه شد. لطفا دوباره تلاش کنید.",
        unexpectedError: "خطای غیرمنتظره‌ای رخ داد. لطفاً دوباره تلاش کنید.",
        deleteConfirmation: "آیا مطمئن هستید که می‌خواهید این مالک را حذف کنید؟ این عمل قابل بازگشت نیست.",
        deleteConfirmButton: "بله، آن را حذف کن!",
        deleting: "در حال حذف...",
        deleteWait: "لطفاً صبر کنید تا مالک حذف شود.",
        deleteSuccess: "مالک با موفقیت حذف شد.",
        deleteError: "در حذف مالک خطایی رخ داد. لطفاً دوباره تلاش کنید.",
        deleteFail: "حذف مالک ناموفق بود",
        errorDeletingBuilding: "خطا در حذف مالک",
        status: {
            active: "فعال",
            deleted: "حذف شده"
        },
        units: "واحد",
        occupied: "اشغال شده",
        since: "از سال",
        validation: {
            nameRequired: "نام مالک الزامی است!",
            floorsRequired: "تعداد طبقات الزامی است!",
            minFloors: "تعداد طبقات باید حداقل 1 باشد"
        },
        messages: {
            deleteConfirm: "آیا از حذف این مالک اطمینان دارید؟ این عمل قابل بازگشت نیست.",
            deleteSuccess: "مالک با موفقیت حذف شد.",
            createSuccess: "مالک با موفقیت ایجاد شد!",
            updateSuccess: "مالک با موفقیت به‌روزرسانی شد!",
            loadError: "خطا در بارگذاری اطلاعات مالک. لطفا دوباره تلاش کنید.",
            saveError: "خطا در ذخیره‌سازی مالک. لطفا دوباره تلاش کنید.",
            loading: "در حال بارگذاری داده‌های مالک. لطفاً منتظر بمانید!",
        },
        detailTitle: "جزئیات مالک",
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
        form: {
            name: "نام مالک",
            id: "کد ملی",
            phone: "تلفن",
            phoneAlt: "تلفن جایگزین",
            phoneEmergency: "تلفن اضطراری",
            phoneEmergencyName: "نام تلفن اضطراری",
            email: "ایمیل",
            whatsapp: "واتس‌اپ",
            telegram: "تلگرام",
            note: "یادداشت",
            cancel: "لغو",
            save: "ذخیره مالک"
        },
        backToList: "بازگشت به لیست مالکین",
        maintenanceHistory: "تاریخچه نگهداری",
        restore: "بازگردانی مالک",
        restoreConfirmation: "آیا از بازگردانی این مالک اطمینان دارید؟",
        restoreConfirmButton: "بله، بازگردانی شود!",
        restoreSuccess: "مالک با موفقیت بازگردانی شد.",
        restoreFail: "بازگردانی مالک ناموفق بود",
        cannotEditDeleted: "ویرایش مالک حذف شده امکان‌پذیر نیست",
        alreadyDeleted: "مالک قبلاً حذف شده است",
        confirmHardDeleteTitle: 'آیا مطمئن هستید؟',
        confirmHardDeleteText: 'آیا مطمئن هستید که می‌خواهید این مالک را به طور دائمی حذف کنید؟ این عمل قابل بازگشت نیست.',
        successHardDelete: 'مالک با موفقیت حذف شد',
        errorHardDelete: 'حذف مالک ناموفق بود. لطفاً دوباره تلاش کنید.',
        networkErrorHardDelete: 'شبکه پاسخ مناسبی نداشت.',
        hardDelete: 'حذف دائم'
    },
    tenants: {
        title: "مدیریت مستاجران",
        subtitle: "مدیریت و نظارت بر تمام مستاجران",
        addNew: "افزودن مستاجر جدید",
        editBuilding: "ویرایش مستاجر",
        name: "نام مستاجر",
        floors: "طبقه",
        description: "توضیحات",
        search: "جستجوی مستاجران...",
        statusActive: "فعال",
        statusDeleted: "حذف شده",
        sortName: "مرتب‌سازی بر اساس نام",
        sortFloors: "مرتب‌سازی بر اساس طبقات",
        edit: "ویرایش مستاجر",
        delete: "حذف مستاجر",
        formName: "نام مستاجر",
        formFloors: "تعداد طبقات",
        formDescription: "توضیحات",
        formCancel: "لغو",
        formSave: "ذخیره مستاجر",
        validationError: "خطای اعتبارسنجی",
        required: "الزامی است!",
        validationFloors: "تعداد طبقات باید حداقل 1 باشد",
        loading: "در حال بارگذاری...",
        fetchingDetails: "در حال دریافت جزئیات مستاجر",
        error: "خطا!",
        loadError: "بارگیری جزئیات مستاجر با شکست مواجه شد. لطفا دوباره تلاش کنید.",
        unexpectedError: "خطای غیرمنتظره‌ای رخ داد. لطفاً دوباره تلاش کنید.",
        deleteConfirmation: "آیا مطمئن هستید که می‌خواهید این مستاجر را حذف کنید؟ این عمل قابل بازگشت نیست.",
        deleteConfirmButton: "بله، آن را حذف کن!",
        deleting: "در حال حذف...",
        deleteWait: "لطفاً صبر کنید تا مستاجر حذف شود.",
        deleteSuccess: "مستاجر با موفقیت حذف شد.",
        deleteError: "در حذف مستاجر خطایی رخ داد. لطفاً دوباره تلاش کنید.",
        deleteFail: "حذف مستاجر ناموفق بود",
        errorDeletingBuilding: "خطا در حذف مستاجر",
        status: {
            active: "فعال",
            deleted: "حذف شده"
        },
        units: "واحد",
        occupied: "اشغال شده",
        since: "از سال",
        validation: {
            nameRequired: "نام مستاجر الزامی است!",
            floorsRequired: "تعداد طبقات الزامی است!",
            minFloors: "تعداد طبقات باید حداقل 1 باشد"
        },
        messages: {
            deleteConfirm: "آیا از حذف این مستاجر اطمینان دارید؟ این عمل قابل بازگشت نیست.",
            deleteSuccess: "مستاجر با موفقیت حذف شد.",
            createSuccess: "مستاجر با موفقیت ایجاد شد!",
            updateSuccess: "مستاجر با موفقیت به‌روزرسانی شد!",
            loadError: "خطا در بارگذاری اطلاعات مستاجر. لطفا دوباره تلاش کنید.",
            saveError: "خطا در ذخیره‌سازی مستاجر. لطفا دوباره تلاش کنید.",
            loading: "در حال بارگذاری داده‌های مستاجر. لطفاً منتظر بمانید!",
        },
        detailTitle: "جزئیات مستاجر",
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
        form: {
            name: "نام مستاجر",
            id: "کد ملی",
            phone: "تلفن",
            phoneAlt: "تلفن جایگزین",
            phoneEmergency: "تلفن اضطراری",
            phoneEmergencyName: "نام تلفن اضطراری",
            phoneEmergencyRelation: "نسبت با مستاجر",
            email: "ایمیل",
            whatsapp: "واتس‌اپ",
            telegram: "تلگرام",
            note: "یادداشت",
            cancel: "لغو",
            save: "ذخیره مستاجر"
        },
        backToList: "بازگشت به لیست مستاجران",
        maintenanceHistory: "تاریخچه نگهداری",
        restore: "بازگردانی مستاجر",
        restoreConfirmation: "آیا از بازگردانی این مستاجر اطمینان دارید؟",
        restoreConfirmButton: "بله، بازگردانی شود!",
        restoreSuccess: "مستاجر با موفقیت بازگردانی شد.",
        restoreFail: "بازگردانی مستاجر ناموفق بود",
        cannotEditDeleted: "ویرایش مستاجر حذف شده امکان‌پذیر نیست",
        alreadyDeleted: "مستاجر قبلاً حذف شده است",
        confirmHardDeleteTitle: 'آیا مطمئن هستید؟',
        confirmHardDeleteText: 'آیا مطمئن هستید که می‌خواهید این مستاجر را به طور دائمی حذف کنید؟ این عمل قابل بازگشت نیست.',
        successHardDelete: 'مستاجر با موفقیت حذف شد',
        errorHardDelete: 'حذف مستاجر ناموفق بود. لطفاً دوباره تلاش کنید.',
        networkErrorHardDelete: 'شبکه پاسخ مناسبی نداشت.',
        hardDelete: 'حذف دائم'
    },
    units: {
        title: "مدیریت واحدها",
        subtitle: "مدیریت و نظارت بر تمام واحدها",
        addNew: "افزودن واحد جدید",
        editBuilding: "ویرایش واحد",
        name: "نام واحد",
        floors: "طبقه",
        description: "توضیحات",
        search: "جستجوی واحدها...",
        statusActive: "فعال",
        statusDeleted: "حذف شده",
        sortName: "مرتب‌سازی بر اساس نام",
        sortFloors: "مرتب‌سازی بر اساس طبقات",
        edit: "ویرایش واحد",
        delete: "حذف واحد",
        formName: "نام واحد",
        formFloors: "تعداد طبقات",
        formDescription: "توضیحات",
        formCancel: "لغو",
        formSave: "ذخیره واحد",
        validationError: "خطای اعتبارسنجی",
        required: "الزامی است!",
        validationFloors: "تعداد طبقات باید حداقل 1 باشد",
        loading: "در حال بارگذاری...",
        fetchingDetails: "در حال دریافت جزئیات واحد",
        error: "خطا!",
        loadError: "بارگیری جزئیات واحد با شکست مواجه شد. لطفا دوباره تلاش کنید.",
        unexpectedError: "خطای غیرمنتظره‌ای رخ داد. لطفاً دوباره تلاش کنید.",
        deleteConfirmation: "آیا مطمئن هستید که می‌خواهید این واحد را حذف کنید؟ این عمل قابل بازگشت نیست.",
        deleteConfirmButton: "بله، آن را حذف کن!",
        deleting: "در حال حذف...",
        deleteWait: "لطفاً صبر کنید تا واحد حذف شود.",
        deleteSuccess: "واحد با موفقیت حذف شد.",
        deleteError: "در حذف واحد خطایی رخ داد. لطفاً دوباره تلاش کنید.",
        deleteFail: "حذف واحد ناموفق بود",
        errorDeletingBuilding: "خطا در حذف واحد",
        status: {
            active: "فعال",
            deleted: "حذف شده"
        },
        units: "واحد",
        occupied: "اشغال شده",
        since: "از سال",
        validation: {
            nameRequired: "نام واحد الزامی است!",
            floorsRequired: "تعداد طبقات الزامی است!",
            minFloors: "تعداد طبقات باید حداقل 1 باشد"
        },
        messages: {
            deleteConfirm: "آیا از حذف این واحد اطمینان دارید؟ این عمل قابل بازگشت نیست.",
            deleteSuccess: "واحد با موفقیت حذف شد.",
            createSuccess: "واحد با موفقیت ایجاد شد!",
            updateSuccess: "واحد با موفقیت به‌روزرسانی شد!",
            loadError: "خطا در بارگذاری اطلاعات واحد. لطفا دوباره تلاش کنید.",
            saveError: "خطا در ذخیره‌سازی واحد. لطفا دوباره تلاش کنید.",
            loading: "در حال بارگذاری داده‌های واحد. لطفاً منتظر بمانید!",
        },
        detailTitle: "جزئیات واحد",
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
        form: {
            building: "نام ساختمان",
            selectBuilding: "انتخاب ساختمان",
            floor: "طبقه",
            selectFloor: "انتخاب طبقه",
            owner: "مالک",
            selectOwner: "انتخاب مالک",
            unitNumber: "شماره واحد",
            unitArea: "مساحت واحد",
            unitHasParking: "واحد دارای پارکینگ",
            unitParkingNumber: "شماره پارکینگ واحد",
            unitConstantExtraCharge: "هزینه اضافی ثابت واحد",
            notes: "یادداشت",
            no: "خیر",
            yes: "بله",
            name: "نام واحد",
            id: "کد ملی",
            phone: "تلفن",
            phoneAlt: "تلفن جایگزین",
            phoneEmergency: "تلفن اضطراری",
            phoneEmergencyName: "نام تلفن اضطراری",
            email: "ایمیل",
            whatsapp: "واتس‌اپ",
            telegram: "تلگرام",
            note: "یادداشت",
            cancel: "لغو",
            save: "ذخیره واحد"
        },
        backToList: "بازگشت به لیست واحدها",
        maintenanceHistory: "تاریخچه نگهداری",
        restore: "بازگردانی واحد",
        restoreConfirmation: "آیا از بازگردانی این واحد اطمینان دارید؟",
        restoreConfirmButton: "بله، بازگردانی شود!",
        restoreSuccess: "واحد با موفقیت بازگردانی شد.",
        restoreFail: "بازگردانی واحد ناموفق بود",
        cannotEditDeleted: "ویرایش واحد حذف شده امکان‌پذیر نیست",
        alreadyDeleted: "واحد قبلاً حذف شده است",
        confirmHardDeleteTitle: 'آیا مطمئن هستید؟',
        confirmHardDeleteText: 'آیا مطمئن هستید که می‌خواهید این واحد را به طور دائمی حذف کنید؟ این عمل قابل بازگشت نیست.',
        successHardDelete: 'واحد با موفقیت حذف شد',
        errorHardDelete: 'حذف واحد ناموفق بود. لطفاً دوباره تلاش کنید.',
        networkErrorHardDelete: 'شبکه پاسخ مناسبی نداشت.',
        hardDelete: 'حذف دائم'
    }
};