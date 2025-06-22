import asyncio
import requests
from typing import Dict

from common.utils.logging import setup_logger

logger = setup_logger(__name__)

async def post_to_page(page_id: str, message: str, access_token: str) -> Dict[str, str]:
    """Post a text update to a Facebook Page."""
    url = f"https://graph.facebook.com/{page_id}/feed"
    payload = {"message": message, "access_token": access_token}
    loop = asyncio.get_running_loop()
    try:
        response = await loop.run_in_executor(None, lambda: requests.post(url, data=payload, timeout=10))
        data = response.json()
        if data.get("id"):
            return {"status": True, "post_id": data["id"]}
        logger.error(f"Facebook API error: {data}")
        return {"status": False, "message": str(data)}
    except Exception as e:
        logger.error(f"Failed to post to page: {e}")
        return {"status": False, "message": str(e)}

async def send_message(recipient_id: str, message: str, access_token: str) -> Dict[str, str]:
    """Send a direct message from a Page."""
    url = "https://graph.facebook.com/v17.0/me/messages"
    payload = {
        "recipient": f"{{\"id\":\"{recipient_id}\"}}",
        "message": f"{{\"text\":\"{message}\"}}",
        "access_token": access_token
    }
    loop = asyncio.get_running_loop()
    try:
        response = await loop.run_in_executor(None, lambda: requests.post(url, data=payload, timeout=10))
        data = response.json()
        if data.get("recipient_id"):
            return {"status": True, "recipient_id": data.get("recipient_id"), "message_id": data.get("message_id")}
        logger.error(f"Facebook API error: {data}")
        return {"status": False, "message": str(data)}
    except Exception as e:
        logger.error(f"Failed to send message: {e}")
        return {"status": False, "message": str(e)}
