import asyncio
import requests
from typing import Dict

from common.utils.logging import setup_logger

logger = setup_logger(__name__)

async def send_message(chat_id: str, text: str, token: str) -> Dict[str, str]:
    """Send a text message via the Telegram Bot API."""
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    loop = asyncio.get_running_loop()
    try:
        response = await loop.run_in_executor(None, lambda: requests.post(url, data=payload, timeout=10))
        data = response.json()
        if data.get("ok"):
            return {"status": True, "message_id": data["result"]["message_id"]}
        logger.error(f"Telegram API error: {data}")
        return {"status": False, "message": data.get("description", "error")}
    except Exception as e:
        logger.error(f"Failed to send message: {e}")
        return {"status": False, "message": str(e)}

async def send_photo(chat_id: str, photo_url: str, caption: str, token: str) -> Dict[str, str]:
    """Send a photo with optional caption via the Telegram Bot API."""
    url = f"https://api.telegram.org/bot{token}/sendPhoto"
    payload = {"chat_id": chat_id, "photo": photo_url, "caption": caption}
    loop = asyncio.get_running_loop()
    try:
        response = await loop.run_in_executor(None, lambda: requests.post(url, data=payload, timeout=10))
        data = response.json()
        if data.get("ok"):
            return {"status": True, "message_id": data["result"]["message_id"]}
        logger.error(f"Telegram API error: {data}")
        return {"status": False, "message": data.get("description", "error")}
    except Exception as e:
        logger.error(f"Failed to send photo: {e}")
        return {"status": False, "message": str(e)}
