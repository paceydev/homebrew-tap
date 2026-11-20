#!/usr/bin/env python3
"""Check the installed server's real stdio initialize response."""
import json
import subprocess
import sys
import tempfile

with tempfile.TemporaryDirectory() as checkout:
    subprocess.run(["git", "init", "--quiet", checkout], check=True)
    request = {"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {
        "protocolVersion": "2025-06-18", "capabilities": {},
        "clientInfo": {"name": "tap-smoke", "version": "1.0"}}}
    result = subprocess.run([sys.argv[1], "--dir", checkout],
                            input=json.dumps(request) + "\n", capture_output=True,
                            text=True, timeout=20, check=True)
    responses = [json.loads(line) for line in result.stdout.splitlines() if line.strip()]
    response = next(item for item in responses if item.get("id") == 1)
    assert "error" not in response, response
    assert response["result"]["serverInfo"]["name"] == "gitforge-mcp", response
    print("MCP initialize passed")
