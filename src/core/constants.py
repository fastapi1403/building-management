from enum import Enum

class ChargeType(str, Enum):
    OWNER = "owner"
    TENANT = "tenant"

class TransactionType(str, Enum):
    INCOME = "income"
    EXPENSE = "expense"

class ExpenseCategory(str, Enum):
    UTILITIES = "utilities"
    MAINTENANCE = "maintenance"
    CLEANING = "cleaning"
    REPAIRS = "repairs"
    OTHER = "other"

class UnitStatus(str, Enum):
    OCCUPIED = "occupied"
    VACANT = "vacant"
    MAINTENANCE = "maintenance"

class PaymentStatus(str, Enum):
    PAID = "paid"
    UNPAID = "unpaid"
    PARTIAL = "partial"
    OVERDUE = "overdue"
