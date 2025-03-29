from typing import Any
import httpx
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("send")


async def make_send_message(message: str) -> str:
    """Call Discord webhook to send message"""
    webhook_url = "https://discord.com/api/webhooks/1245209817497468930/F-aJPglLSTrr4QRid4CZqNG5LHZUiZrIv1KUepAlGz2XYEKa9QpW3Zq1h45cGmi5-BSi"

    payload = {
        "content": message
    }

    headers = {
        "Content-Type": "application/json"
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                webhook_url,
                json=payload,
                headers=headers,
                timeout=10.0
            )
            response.raise_for_status()
            return f"✅ Message sent successfully (Status code: {response.status_code})"

    except httpx.RequestError as e:
        return f"❌ Request error: {str(e)}"
    except httpx.HTTPStatusError as e:
        return f"❌ HTTP error: {e.response.status_code} - {e.response.text}"
    except Exception as e:
        return f"❌ Unexpected error: {str(e)}"


@mcp.tool()
async def send_message(message: Any) -> str:
    """
    Send text message to Discord

    Args:
        message: The message text to be sent
    """
    return await make_send_message(str(message))


if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport="stdio")
