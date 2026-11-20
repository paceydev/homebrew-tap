# paceydev Homebrew tap

Install [gitforge-mcp](https://github.com/paceydev/gitforge-mcp):

```sh
brew install paceydev/tap/gitforge-mcp
```

Update:

```sh
brew update
brew upgrade paceydev/tap/gitforge-mcp
```

Check the installed version:

```sh
"$(brew --prefix)/bin/gitforge-mcp" --version
```

If you previously installed with Cargo, `~/.cargo/bin` may appear first on
PATH. Use `type -a gitforge-mcp` to check which installation your client uses.
Restart your MCP client after upgrading.

## Platforms

Prebuilt macOS and Linux binaries for ARM64 and x86-64. No Rust compiler
required. Linux requires glibc 2.35 or newer; Alpine/musl is unsupported.
The upstream macOS binaries are currently unsigned by a publisher; Developer
ID signing and notarization are planned. Homebrew verifies the pinned archive
checksum. Upstream also publishes GitHub build attestations.

## Maintenance

CI installs and tests the formula on all four platforms. The daily and manual
update workflow verifies upstream archive checksums and GitHub attestations,
then proposes a formula update as a pull request. It explicitly dispatches
formula CI on that branch because a pull request made with GITHUB_TOKEN does
not trigger pull-request workflows. Updates require review and merge.

Repository setup: allow GitHub Actions to create pull requests; allow pinned
`actions/checkout` and `Homebrew/actions/setup-homebrew`; protect main with
required `gate` and block force pushes/deletion. Workflow tokens are read-only
except the update job, which can write contents, open PRs and dispatch tests.
No cross-repository write credential is required.

Manual formula regeneration, after verifying the upstream release:

```sh
python3 scripts/update-formula.py 0.2.0 /path/to/SHA256SUMS
```

Formula definitions and maintenance scripts use the MIT license in LICENSE.
The distributed gitforge-mcp executable retains its upstream MIT OR Apache-2.0
license.
