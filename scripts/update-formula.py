#!/usr/bin/env python3
"""Render the formula from a verified release checksum file."""
import argparse
import re
from pathlib import Path

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("version")
parser.add_argument("checksums", type=Path)
parser.add_argument("--output", type=Path, default=Path("Formula/gitforge-mcp.rb"))
args = parser.parse_args()
if not re.fullmatch(r"[0-9]+\.[0-9]+\.[0-9]+", args.version):
    parser.error("expected a stable MAJOR.MINOR.PATCH version")
sums = {}
for line in args.checksums.read_text().splitlines():
    match = re.fullmatch(r"([a-f0-9]{64})  ([A-Za-z0-9_.-]+)", line)
    if not match or match[2] in sums:
        parser.error("invalid or duplicate checksum entry")
    sums[match[2]] = match[1]
lines = [
    'class GitforgeMcp < Formula',
    '  desc "Forge-aware MCP tools for CI, pull requests and repository settings"',
    '  homepage "https://github.com/paceydev/gitforge-mcp"',
    f'  version "{args.version}"',
    '  license any_of: ["MIT", "Apache-2.0"]',
    '',
]
for os_name, suffix, extension in [("macos", "apple-darwin", "zip"), ("linux", "unknown-linux-gnu", "tar.gz")]:
    lines.append(f"  on_{os_name} do")
    for arch, target in [("arm", "aarch64"), ("intel", "x86_64")]:
        name = f"gitforge-mcp-{args.version}-{target}-{suffix}.{extension}"
        if name not in sums:
            parser.error(f"missing checksum for {name}")
        lines += [f"    on_{arch} do", f'      url "https://github.com/paceydev/gitforge-mcp/releases/download/v{args.version}/{name}"', f'      sha256 "{sums[name]}"', '    end']
    lines += ['  end', '']
lines += [
    '  def install',
    '    bin.install "gitforge-mcp"',
    '    doc.install "README.md" if File.exist?("README.md")',
    '  end',
    '',
    '  test do',
    '    assert_equal "gitforge-mcp #{version}", shell_output("#{bin}/gitforge-mcp --version").strip',
    '    assert_match "stdio", shell_output("#{bin}/gitforge-mcp --help")',
    '  end',
    'end',
]
args.output.write_text("\n".join(lines) + "\n")
