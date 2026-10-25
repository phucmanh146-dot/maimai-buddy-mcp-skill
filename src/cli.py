"""CLI for inspecting and calling the configured McDonald's MCP server."""
from __future__ import annotations

import argparse
import json
import sys

from .mcp_client import MCPError, McdMCPClient


def main() -> int:
    parser = argparse.ArgumentParser(description="麦麦搭子·省着吃 MCP utility")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("tools", help="list server tools and input schemas")
    call_parser = sub.add_parser("call", help="call one tool after checking its input schema")
    call_parser.add_argument("name", help="exact tool name returned by tools/list")
    call_parser.add_argument("--args-json", default="{}", help="JSON object matching the tool input schema")
    args = parser.parse_args()

    try:
        client = McdMCPClient()
        client.initialize()
        if args.command == "tools":
            for tool in client.list_tools():
                print(f"\n{tool.get('name', '(unnamed)')}\n{tool.get('description', '')}")
                schema = tool.get("inputSchema")
                if schema:
                    print(json.dumps(schema, ensure_ascii=False, indent=2))
            return 0
        try:
            arguments = json.loads(args.args_json)
        except json.JSONDecodeError as exc:
            raise MCPError(f"--args-json must be valid JSON: {exc.msg}") from None
        if not isinstance(arguments, dict):
            raise MCPError("--args-json must be a JSON object")
        result = client.call_tool(args.name, arguments)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except MCPError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
