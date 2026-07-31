from enum import Enum
from typing import List

from pydantic import BaseModel


class NotificationType(str, Enum):
    LOW_STOCK = "LOW_STOCK"
    OVERDUE_INVOICE = "OVERDUE_INVOICE"


class NotificationSeverity(str, Enum):
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"


class Notification(BaseModel):
    type: NotificationType
    severity: NotificationSeverity
    title: str
    message: str
    reference_id: str


class NotificationListResponse(BaseModel):
    total_notifications: int
    notifications: List[Notification]
