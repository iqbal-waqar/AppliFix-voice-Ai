from typing import Dict, Any, Optional
import httpx
import json
from config import settings

class VapiService:
    VAPI_BASE_URL = "https://api.vapi.ai"

    def get_headers(self) -> Dict[str, str]:
        return {
            "Authorization": f"Bearer {settings.vapi_api_key}",
            "Content-Type": "application/json",
        }

    def parse_webhook(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        event_type = payload.get("message", {}).get("type") or payload.get("type", "unknown")

        call_data = payload.get("message", {}).get("call") or payload.get("call", {})
        call_id = call_data.get("id", "")
        caller_phone = call_data.get("customer", {}).get("number", "")

        result = {
            "event_type": event_type,
            "call_id": call_id,
            "caller_phone": caller_phone,
            "raw": payload,
        }

        tool_calls = payload.get("message", {}).get("toolCalls", [])
        if tool_calls:
            result["tool_calls"] = tool_calls

        transcript = payload.get("message", {}).get("transcript", "")
        if transcript:
            result["transcript"] = transcript

        summary = payload.get("message", {}).get("summary", "")
        if summary:
            result["summary"] = summary

        return result

    def build_tool_result_response(self, tool_call_id: str, result: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "results": [
                {
                    "toolCallId": tool_call_id,
                    "result": json.dumps(result),
                }
            ]
        }

        return []
