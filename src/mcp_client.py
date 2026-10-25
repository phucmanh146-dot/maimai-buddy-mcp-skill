"""Minimal stdlib-only client for the McDonald's Streamable HTTP MCP server."""
from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from typing import Any

DEFAULT_URL = "https://mcp.mcd.cn"
PROTOCOL_VERSION = "2025-06-18"


class MCPError(RuntimeError):
    """Raised when the remote MCP server returns an error."""


class McdMCPClient:
    def __init__(self, token: str | None = None, url: str | None = None, timeout: int = 30):
        raw_token = (token or os.getenv("MCD_MCP_TOKEN", "")).strip()
        if raw_token.startswith("Bearer "):
            raw_token = raw_token[7:].strip()
        if not raw_token:
            raise MCPError("MCD_MCP_TOKEN is not set. Configure it locally; never commit it.")
        self._token = raw_token
        self.url = (url or os.getenv("MCD_MCP_URL") or DEFAULT_URL).strip()
        self.timeout = timeout
        self._next_id = 0
        self._session_id: str | None = None
        self._initialized = False

    def _send(self, method: str, params: dict[str, Any] | None = None, *, notification: bool = False) -> dict[str, Any]:
        payload: dict[str, Any] = {"jsonrpc": "2.0", "method": method, "params": params or {}}
        if not notification:
            self._next_id += 1
            payload["id"] = self._next_id

        headers = {
            "Authorization": f"Bearer {self._token}",
            "Accept": "application/json, text/event-stream",
            "Content-Type": "application/json",
        }
        if self._initialized:
            headers["MCP-Protocol-Version"] = PROTOCOL_VERSION
        if self._session_id:
            headers["Mcp-Session-Id"] = self._session_id

        request = urllib.request.Request(
            self.url,
            data=json.dumps(payload).encode("utf-8"),
            headers=headers,
            method="POST",
        )
        try:
            with urllib.request.urlopen(request, timeout=self.timeout) as response:
                self._session_id = response.headers.get("Mcp-Session-Id", self._session_id)
                raw = response.read().decode("utf-8", errors="replace")
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")[:300]
            raise MCPError(f"MCP HTTP {exc.code}: {detail or 'no response body'}") from None
        except (urllib.error.URLError, TimeoutError) as exc:
            raise MCPError(f"MCP connection failed: {exc}") from None

        if notification and not raw:
            return {}
        if not raw.strip():
            return {}
        if "text/event-stream" in response.headers.get("Content-Type", ""):
            data_lines = [line[5:].strip() for line in raw.splitlines() if line.startswith("data:")]
            raw = data_lines[-1] if data_lines else "{}"
        try:
            result = json.loads(raw)
        except json.JSONDecodeError:
            raise MCPError("MCP server returned an unreadable response.") from None
        if "error" in result:
            err = result["error"]
            raise MCPError(f"MCP JSON-RPC error {err.get('code')}: {err.get('message', 'unknown error')}")
        return result

    def initialize(self) -> dict[str, Any]:
        result = self._send(
            "initialize",
            {
                "protocolVersion": PROTOCOL_VERSION,
                "capabilities": {},
                "clientInfo": {"name": "maimai-saver", "version": "1.0.0"},
            },
        )
        self._initialized = True
        try:
            self._send("notifications/initialized", notification=True)
        except MCPError:
            # Some hosted servers do not require or acknowledge this notification.
            pass
        return result.get("result", result)

    def list_tools(self) -> list[dict[str, Any]]:
        if not self._initialized:
            self.initialize()
        result = self._send("tools/list", {})
        return result.get("result", {}).get("tools", [])

    def call_tool(self, name: str, arguments: dict[str, Any] | None = None) -> dict[str, Any]:
        if not self._initialized:
            self.initialize()
        result = self._send("tools/call", {"name": name, "arguments": arguments or {}})
        return result.get("result", result)
