from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from database.session import get_db
from interactors.conversation_interactor import ConversationInteractor
import logging

router = APIRouter(prefix="/vapi", tags=["vapi"])
logger = logging.getLogger(__name__)

@router.post("/webhook")
async def vapi_webhook(request: Request, db: Session = Depends(get_db)):

    try:
        payload = await request.json()
        return ConversationInteractor().process_webhook(db, payload)
    except Exception as e:
        logger.error(f"Vapi webhook error: {e}", exc_info=True)
        return {"status": "error", "detail": str(e)}
