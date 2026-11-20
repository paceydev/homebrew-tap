class GitforgeMcp < Formula
  desc "Forge-aware MCP tools for CI, pull requests and repository settings"
  homepage "https://github.com/paceydev/gitforge-mcp"
  version "0.2.0"
  license any_of: ["MIT", "Apache-2.0"]

  on_macos do
    on_arm do
      url "https://github.com/paceydev/gitforge-mcp/releases/download/v0.2.0/gitforge-mcp-0.2.0-aarch64-apple-darwin.zip"
      sha256 "d54925069dc6b942ce53ff1b12587e6fe2579de2ff44f4e9611de3d094a3a7a0"
    end
    on_intel do
      url "https://github.com/paceydev/gitforge-mcp/releases/download/v0.2.0/gitforge-mcp-0.2.0-x86_64-apple-darwin.zip"
      sha256 "3cf215cf31f9dec86d1e016a7a880dc976874d2ca514bd0ae186ee013de1890e"
    end
  end

  on_linux do
    on_arm do
      url "https://github.com/paceydev/gitforge-mcp/releases/download/v0.2.0/gitforge-mcp-0.2.0-aarch64-unknown-linux-gnu.tar.gz"
      sha256 "3b16740c2af568a176cf476f27fcdc75253306a536df5eefc59cb0e94ac22d82"
    end
    on_intel do
      url "https://github.com/paceydev/gitforge-mcp/releases/download/v0.2.0/gitforge-mcp-0.2.0-x86_64-unknown-linux-gnu.tar.gz"
      sha256 "a0bbe653c234525a4374d39dd6c09b633a3bbf1dadb8d4cbcb3e193093d3d534"
    end
  end

  def install
    bin.install "gitforge-mcp"
    doc.install "README.md" if File.exist?("README.md")
  end

  test do
    assert_equal "gitforge-mcp #{version}", shell_output("#{bin}/gitforge-mcp --version").strip
    assert_match "stdio", shell_output("#{bin}/gitforge-mcp --help")
  end
end
