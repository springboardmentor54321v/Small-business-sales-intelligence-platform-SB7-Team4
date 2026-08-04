from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.notification import NotificationListResponse
from app.services.notification_service import NotificationService

router = APIRouter(
    prefix="/notifications",
    tags=["Notifications"],
)


@router.get( 
    "",
    response_model=NotificationListResponse,
)
def get_notifications(db: Session = Depends(get_db)):
    return NotificationService.get_notifications(db)
