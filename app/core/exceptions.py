from typing import Any, Dict, Optional
from fastapi import HTTPException, status
from pydantic import BaseModel

class ErrorResponseModel(BaseModel):
    """Standardized error response model"""
    detail: str
    code: str
    metadata: Optional[Dict[str, Any]] = None

class BuildingManagementException(HTTPException):
    """Base exception for Building Management System"""
    def __init__(
        self,
        detail: str,
        code: str,
        status_code: int = status.HTTP_400_BAD_REQUEST,
        metadata: Optional[Dict[str, Any]] = None
    ):
        super().__init__(
            status_code=status_code,
            detail=ErrorResponseModel(
                detail=detail,
                code=code,
                metadata=metadata
            ).dict()
        )

# Resource Exceptions
class ResourceNotFoundException(BuildingManagementException):
    """Exception raised when a requested resource is not found"""
    def __init__(
        self,
        resource_type: str,
        resource_id: Any,
        metadata: Optional[Dict[str, Any]] = None
    ):
        super().__init__(
            detail=f"{resource_type} with id {resource_id} not found",
            code="RESOURCE_NOT_FOUND",
            status_code=status.HTTP_404_NOT_FOUND,
            metadata=metadata
        )

class ResourceAlreadyExistsException(BuildingManagementException):
    """Exception raised when attempting to create a resource that already exists"""
    def __init__(
        self,
        resource_type: str,
        identifier: str,
        value: Any,
        metadata: Optional[Dict[str, Any]] = None
    ):
        super().__init__(
            detail=f"{resource_type} with {identifier} '{value}' already exists",
            code="RESOURCE_ALREADY_EXISTS",
            status_code=status.HTTP_409_CONFLICT,
            metadata=metadata
        )

# Validation Exceptions
class ValidationException(BuildingManagementException):
    """Exception raised when validation fails"""
    def __init__(
        self,
        detail: str,
        metadata: Optional[Dict[str, Any]] = None
    ):
        super().__init__(
            detail=detail,
            code="VALIDATION_ERROR",
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            metadata=metadata
        )

# Business Logic Exceptions
class BusinessLogicException(BuildingManagementException):
    """Exception raised when a business rule is violated"""
    def __init__(
        self,
        detail: str,
        code: str = "BUSINESS_RULE_VIOLATION",
        metadata: Optional[Dict[str, Any]] = None
    ):
        super().__init__(
            detail=detail,
            code=code,
            status_code=status.HTTP_400_BAD_REQUEST,
            metadata=metadata
        )

# Specific Business Exceptions
class UnitOccupancyException(BusinessLogicException):
    """Exception raised for unit occupancy related issues"""
    def __init__(self, detail: str, metadata: Optional[Dict[str, Any]] = None):
        super().__init__(
            detail=detail,
            code="UNIT_OCCUPANCY_ERROR",
            metadata=metadata
        )

class MaintenanceException(BusinessLogicException):
    """Exception raised for maintenance related issues"""
    def __init__(self, detail: str, metadata: Optional[Dict[str, Any]] = None):
        super().__init__(
            detail=detail,
            code="MAINTENANCE_ERROR",
            metadata=metadata
        )

# Permission Exceptions
class PermissionDeniedException(BuildingManagementException):
    """Exception raised when user doesn't have required permissions"""
    def __init__(
        self,
        detail: str = "You don't have permission to perform this action",
        metadata: Optional[Dict[str, Any]] = None
    ):
        super().__init__(
            detail=detail,
            code="PERMISSION_DENIED",
            status_code=status.HTTP_403_FORBIDDEN,
            metadata=metadata
        )

# Database Exceptions
class DatabaseOperationException(BuildingManagementException):
    """Exception raised when a database operation fails"""
    def __init__(
        self,
        operation: str,
        detail: str,
        metadata: Optional[Dict[str, Any]] = None
    ):
        super().__init__(
            detail=f"Database {operation} failed: {detail}",
            code="DATABASE_ERROR",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            metadata=metadata
        )

# Utility function for exception handling
def handle_exceptions(func):
    """Decorator to handle common exceptions"""
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except BuildingManagementException:
            raise
        except Exception as e:
            raise DatabaseOperationException(
                operation="operation",
                detail=str(e),
                metadata={"original_error": str(e)}
            )
    return wrapper