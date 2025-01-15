You are a professional Python and FastAPI developer. 
Write a professional-grade application for the following description, with optimized file structures, advanced design, and excellent user experience. 
The application should be well-documented and include tests.
The front page must be visually appealing and user-friendly, with a responsive design. and pretty URLs. and nice design.
Url should be like this:
- /buildings
- /floors
- /units
- /owners
- /tenants
- /funds
- /transactions
- /charges
- /costs
- /reports
- /settings
- site main page is static web page to introduce the application and its features.
- site portal url is /dashboard

---

**Building Management Web Application - Version 1**

---

### **Web Application Features**
- **User Access**: In the first version, only the building manager has access to the application; residents cannot use it.
- **User Management**: There is no need for user management.
- **Login and Registration**: User registration and login are not required.

---

### **Programming Specifications**
- **Programming Language**: Python 3.12 or above.
- **Framework**: Async FastAPI with ModelSQL.
- **Frontend**: FastAPI with Jinja2, HTML, CSS, and JavaScript.
- **Database**: Async PostgreSQL with Alembic.
- **Virtual Environment**: Poetry.

---

### **Building Structure**
- **Building**: Composed of several floors, and each floor includes multiple units.
- **Parking**: The number of parking spaces is fewer than the number of units.
- **Additional Facilities**: Includes an elevator and a boiler room.

---

### **Unit Features**
1. **Ownership and Residency**:  
   - Each unit has one owner and one resident.  
   - The owner may also be the resident.  
   - Units may be unoccupied.
2. **Facilities**:  
   - Units may or may not have parking.

---

### **Building Fund**
1. **Income**: Deposited into the fund.  
2. **Expenses**: Withdrawn from the fund.

---

### **Unit Charges**
- **Owner Charges**:  
  - Includes repair and related costs.  
  - Ability to create and assign repair costs.
- **Tenant Charges**:
  1. **Fixed Charge**: If the unit is vacant, this charge is added to the owner (configurable).  
  2. **Management Fee**: If the unit is vacant, this fee is added to the owner (configurable).  
  3. **Gas Consumption**:  
     - Cold Months: Total gas cost is divided by the number of people in occupied units.  
     - Warm Months: Total gas cost is divided by the number of occupied units.  
  4. **Water Consumption**: Total water cost is divided by the number of people in occupied units.  
  5. **Electricity Consumption**: Total electricity cost is divided by the number of people in occupied units.  
  6. **Cleaning**: Cleaning costs are divided among occupied units.  
  7. **Miscellaneous Costs**: Can be defined for division among units.  
  8. **Monthly Fixed Charge**.  
  9. **Ability to add specific charges for owners or residents of particular units**.
  10. Each unit has a separate account for charges.
  10. **Constant extra charge**: Variable for each unit.
  11. **Charge Payment**: Residents pay charges monthly.
  12. **Charge Payment Status**: Paid/Unpaid.
  13. **Charge Payment Details**: Payment date, amount, and method.
  14. **Charge Payment Reminder**: Automatic reminders for unpaid charges.
  15. **Charge Payment Report**: Monthly report on charge payments.
  16. **Charge Payment History**: Payment history for each unit.
  17. **Charge Payment Receipt**: Receipt generation for each payment.
  18. **Charge Payment Confirmation**: Confirmation of payment receipt.
  19. **Charge Payment Notification**: Notification of payment receipt.


---

### **Cost Structure**
- Costs must be editable and linked to either the owner or resident.  
- Methods of cost division should be specified.  
- Ability to define differences for warm and cold months.

---

### **Administrative Panel Features**
1. Add, edit, and delete units.  
2. Add, edit, and delete owners and residents.  
3. Manage costs and calculate monthly charges.  
4. Enter charge payment details and generate reports.  
5. Send automatic monthly charges.  
6. Generate pre- and post-payment invoices.  
7. Send invoices via WhatsApp and Telegram.

---

### **Reporting**
1. **Income and Expenses**: Show detailed breakdown by category.  
2. **Charge Payment Status**: Display payment status for each unit (Paid/Unpaid).  
3. **Resource Usage**: Provide details on water, electricity, and gas consumption.  
4. **Unit Accounts**: Show debts and payments for each unit.  
5. **Parking Status**: Report allocated and vacant parking spaces.  
6. **Repairs and Maintenance**: Show incurred costs.  
7. **Debtors**: List indebted units.  
8. **Resident Count**: Show the total number of residents.  
9. **Unit Occupancy Status**: Show the number of occupied and vacant units.  

**Additional Report Features**:
- Export reports in PDF and Excel formats.  
- Add visual charts for data representation.  
- Display bar, pie, or line charts.  
- Schedule automatic report delivery.  
- Intelligent messaging: Automatically send payment reminders and updates.

---

### **Suggested Ledger System**
**Key Features**:
1. Transaction Logging: Includes income and expense entries.  
2. Data Structure: Includes date, transaction type, amount, description, and status.  
3. Transaction Categories: Based on income or expense types.  
4. Account Balance: Display building fund balance.  
5. Advanced Reporting: Cash flow, transactions, debts.  
6. Integration with Charge System: Automatically log charge payments.  
7. Bank File Import: Import bank Excel files, match them with expenses, and complete cost fields.  

**User Interface**:
- Transaction Entry Page.  
- Transaction Review Page.  
- Financial Reports Page.  

---

create with this structure
---
building_management/
│
├── alembic/
│   ├── versions/
│   ├── env.py
│   ├── script.py.mako
│   └── README
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── building.py
│   │   ├── floor.py
│   │   ├── unit.py
│   │   ├── owner.py
│   │   ├── tenant.py
│   │   ├── fund.py
│   │   ├── transaction.py
│   │   ├── charge.py
│   │   └── cost.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── building.py
│   │   ├── floor.py
│   │   ├── unit.py
│   │   ├── owner.py
│   │   ├── tenant.py
│   │   ├── fund.py
│   │   ├── transaction.py
│   │   ├── charge.py
│   │   └── cost.py
│   ├── crud/
│   │   ├── __init__.py
│   │   ├── building.py
│   │   ├── floor.py
│   │   ├── unit.py
│   │   ├── owner.py
│   │   ├── tenant.py
│   │   ├── fund.py
│   │   ├── transaction.py
│   │   ├── charge.py
│   │   └── cost.py
│   ├── api/
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── buildings.py
│   │       ├── floors.py
│   │       ├── units.py
│   │       ├── owners.py
│   │       ├── tenants.py
│   │       ├── funds.py
│   │       ├── transactions.py
│   │       ├── charges.py
│   │       └── costs.py
│   ├── db/
│   │   ├── __init__.py
│   │   └── session.py
│   ├── templates/
│   │   ├── index.html
│   │   ├── buildings.html
│   │   ├── units.html
│   │   └── reports.html
│   ├── static/
│   │   ├── css/
│   │   │   └── styles.css
│   │   └── js/
│   │       └── scripts.js
│   └── config.pyWould you like the Python/FastAPI code written for this specification?
│
├── tests/
│   └── __init__.py
│
├── poetry.lock
├── pyproject.toml
├── alembic.ini
├── README.md
└── requirements.txt