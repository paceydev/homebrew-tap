class GitforgeMcp < Formula
  desc "Forge-aware MCP tools for CI, pull requests and repository settings"
  homepage "https://github.com/paceydev/gitforge-mcp"
  version "0.2.1"
  license any_of: ["MIT", "Apache-2.0"]

  on_macos do
    on_arm do
      url "https://github.com/paceydev/gitforge-mcp/releases/download/v0.2.1/gitforge-mcp-0.2.1-aarch64-apple-darwin.zip"
      sha256 "dc13be1a462da88343fd9b913be87f7b604795c55bf43aa4db16c19e9f2ca3d6"
    end
    on_intel do
      url "https://github.com/paceydev/gitforge-mcp/releases/download/v0.2.1/gitforge-mcp-0.2.1-x86_64-apple-darwin.zip"
      sha256 "9973639739bbce4ad4cc1a1858d63dac10b0c96a6bee929f044b1a959b4241d8"
    end
  end

  on_linux do
    depends_on "patchelf" => :build
    depends_on "gcc"

    on_arm do
      url "https://github.com/paceydev/gitforge-mcp/releases/download/v0.2.1/gitforge-mcp-0.2.1-aarch64-unknown-linux-gnu.tar.gz"
      sha256 "851f35d72d5647b5906dd24ef9e2d7a3461d431e25c1d07464d71215b2152f5b"
    end
    on_intel do
      url "https://github.com/paceydev/gitforge-mcp/releases/download/v0.2.1/gitforge-mcp-0.2.1-x86_64-unknown-linux-gnu.tar.gz"
      sha256 "5a8fb4ad890b2a4e3088689e9d923ff3355d341e34aa64bd4382ded129b33b8c"
    end
  end

  def install
    bin.install "gitforge-mcp"
    if OS.linux?
      system HOMEBREW_PREFIX/"lib/ld.so", formula_opt_bin("patchelf")/"patchelf",
             "--set-rpath", "#{formula_opt_lib("gcc")}/gcc/current:#{HOMEBREW_PREFIX}/lib",
             bin/"gitforge-mcp"
    end
    doc.install "README.md" if File.exist?("README.md")
  end

  test do
    assert_equal "gitforge-mcp #{version}", shell_output("#{bin}/gitforge-mcp --version").strip
    assert_match "stdio", shell_output("#{bin}/gitforge-mcp --help")
  end
end
