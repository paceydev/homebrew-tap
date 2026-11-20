#!/usr/bin/env python3
"""Verify all four upstream release artifacts before proposing a formula."""
import hashlib
import json
import re
import subprocess
from pathlib import Path

repo = "paceydev/gitforge-mcp"
def gh(*args):
    return subprocess.check_output(["gh", *args], text=True)
release = json.loads(gh("api", f"repos/{repo}/releases/latest"))
tag = release["tag_name"]
if release["draft"] or release["prerelease"] or not re.fullmatch(r"v[0-9]+\.[0-9]+\.[0-9]+", tag):
    raise SystemExit("Expected a published stable release")
version = tag[1:]
current = re.search(r'  version "([^"]+)"', Path("Formula/gitforge-mcp.rb").read_text())[1]
if tuple(map(int, version.split('.'))) < tuple(map(int, current.split('.'))):
    raise SystemExit("Refusing to downgrade")
target = Path("/tmp/upstream")
target.mkdir(exist_ok=True)
names = [f"gitforge-mcp-{version}-{arch}-{system}.{ext}"
         for arch in ("aarch64", "x86_64")
         for system, ext in (("apple-darwin", "zip"), ("unknown-linux-gnu", "tar.gz"))]
args = ["release", "download", tag, "--repo", repo, "--dir", str(target), "--clobber", "--pattern", "SHA256SUMS"]
for name in names:
    args += ["--pattern", name]
gh(*args)
sums = {}
for line in (target / "SHA256SUMS").read_text().splitlines():
    match = re.fullmatch(r"([a-f0-9]{64})  ([A-Za-z0-9_.-]+)", line)
    if not match or match[2] in sums:
        raise SystemExit("Invalid checksum manifest")
    sums[match[2]] = match[1]
for name in names:
    archive = target / name
    if hashlib.sha256(archive.read_bytes()).hexdigest() != sums.get(name):
        raise SystemExit(f"Checksum mismatch: {name}")
    subprocess.run(["gh", "attestation", "verify", str(archive), "--repo", repo,
                    "--signer-workflow", f"{repo}/.github/workflows/release.yml"],
                   stdout=subprocess.DEVNULL, check=True)
print(version)
