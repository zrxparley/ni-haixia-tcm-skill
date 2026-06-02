#!/usr/bin/env bash
set -euo pipefail

REPO_URL="https://github.com/zrxparley/ni-haixia-tcm-skill.git"
SKILL_DIR="ni-haixia-tcm"
TMP_DIR=""
CLEANUP=true

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m'

detect_platform() {
	case "$(uname -s)" in
		Darwin) echo "macos" ;;
		Linux)  echo "linux" ;;
		*)      die "Unsupported OS: $(uname -s). Requires macOS or Linux." ;;
	esac
}

die() { echo -e "${RED}ERROR: $*${NC}" >&2; exit 1; }
info() { echo -e "${CYAN}[INFO]${NC} $*"; }
ok() { echo -e "${GREEN}[OK]${NC} $*"; }
warn() { echo -e "${YELLOW}[WARN]${NC} $*"; }

cleanup() {
	if [ "$CLEANUP" = true ] && [ -n "$TMP_DIR" ] && [ -d "$TMP_DIR" ]; then
		rm -rf "$TMP_DIR"
	fi
}
trap cleanup EXIT

usage() {
	cat <<EOF
Ni Haixia TCM Skill Installer v3.0

USAGE:
  ./install.sh [OPTIONS]

OPTIONS:
  --path <DIR>     Custom install directory (overrides auto-detection)
  --platform <P>   Target platform: opencode | workbuddy (default: auto-detect)
  --local <DIR>    Install from local directory instead of cloning from GitHub
  --no-verify      Skip post-install verification
  -h, --help       Show this help

INSTALL TARGETS (auto-detected):
  OpenCode:   ~/.config/opencode/skills/ni-haixia-tcm/
  Workbuddy:  ~/.workbuddy/skills/ni-haixia-tcm/

EXAMPLES:
  ./install.sh                                    # Auto-detect and install
  ./install.sh --platform opencode                # Install for OpenCode only
  ./install.sh --path /custom/dir                 # Custom directory
  ./install.sh --local ./ni-haixia-tcm-skill      # From local copy
EOF
	exit 0
}

verify_skill() {
	local target="$1"
	local errors=0

	if [ ! -f "$target/SKILL.md" ]; then
		die "SKILL.md not found in $target"
	fi

	local ref_count
	ref_count=$(find "$target/references" -name "*.md" 2>/dev/null | wc -l | tr -d ' ')
	local tpl_count
	tpl_count=$(find "$target/templates" -name "*.md" 2>/dev/null | wc -l | tr -d ' ')

	if [ "$ref_count" -lt 20 ]; then
		warn "Expected 25+ references, found $ref_count"
		((errors++))
	fi
	if [ "$tpl_count" -lt 4 ]; then
		warn "Expected 5 templates, found $tpl_count"
		((errors++))
	fi

	[ "$errors" -eq 0 ] && ok "Verification passed: $ref_count references, $tpl_count templates"
	return "$errors"
}

install_opencode() {
	local target="$HOME/.config/opencode/skills/$SKILL_DIR"
	info "Installing for OpenCode: $target"
	mkdir -p "$target"
	cp -r "$SOURCE_DIR"/* "$target"/
	ok "Installed to $target"
	if [ "$NO_VERIFY" = false ]; then verify_skill "$target"; fi
}

install_workbuddy() {
	local target="$HOME/.workbuddy/skills/$SKILL_DIR"
	info "Installing for Workbuddy: $target"
	mkdir -p "$target"
	cp -r "$SOURCE_DIR"/* "$target"/
	ok "Installed to $target"
	if [ "$NO_VERIFY" = false ]; then verify_skill "$target"; fi
}

install_custom() {
	local custom_path="$1"
	info "Installing to custom path: $custom_path"
	mkdir -p "$custom_path"
	cp -r "$SOURCE_DIR"/* "$custom_path"/
	ok "Installed to $custom_path"
	if [ "$NO_VERIFY" = false ]; then verify_skill "$custom_path"; fi
}

CUSTOM_PATH=""
PLATFORM=""
LOCAL_DIR=""
NO_VERIFY=false

while [[ $# -gt 0 ]]; do
	case "$1" in
		--path)     CUSTOM_PATH="$2"; shift 2 ;;
		--platform) PLATFORM="$2"; shift 2 ;;
		--local)    LOCAL_DIR="$2"; shift 2 ;;
		--no-verify) NO_VERIFY=true; shift ;;
		-h|--help)  usage ;;
		*)          die "Unknown option: $1" ;;
	esac
done

echo ""
echo -e "${BOLD}=== Ni Haixia TCM Skill Installer v3.0 ===${NC}"
echo ""

detected_os=$(detect_platform)
info "Detected platform: $detected_os"

if [ -n "$LOCAL_DIR" ]; then
	SOURCE_DIR="$(cd "$LOCAL_DIR" && pwd)"
	info "Using local source: $SOURCE_DIR"
else
	TMP_DIR="$(mktemp -d)"
	info "Downloading from: $REPO_URL"
	git clone --depth 1 "$REPO_URL" "$TMP_DIR/clone"
	SOURCE_DIR="$TMP_DIR/clone"
	ok "Download complete"
fi

if [ -n "$CUSTOM_PATH" ]; then
	install_custom "$CUSTOM_PATH"
elif [ -n "$PLATFORM" ]; then
	case "$PLATFORM" in
		opencode) install_opencode ;;
		workbuddy) install_workbuddy ;;
		*) die "Unknown platform: $PLATFORM. Use 'opencode' or 'workbuddy'." ;;
	esac
else
	installed=false
	if [ -d "$HOME/.config/opencode" ]; then
		install_opencode
		installed=true
	fi
	if [ -d "$HOME/.workbuddy" ]; then
		install_workbuddy
		installed=true
	fi
	if [ "$installed" = false ]; then
		warn "Neither OpenCode nor Workbuddy directory detected."
		echo ""
		read -p "Enter custom install path: " custom_input
		if [ -n "$custom_input" ]; then
			install_custom "$custom_input"
		else
			die "No install target found. Use --path to specify a directory."
		fi
	fi
fi

echo ""
echo -e "${BOLD}${GREEN}Installation complete!${NC}"
echo ""
echo -e "Start using the skill by saying:"
echo -e "  ${CYAN}倪师${NC}           — Enter study mode"
echo -e "  ${CYAN}我要学中医${NC}     — Get a study plan"
echo -e "  ${CYAN}中医诊断${NC}       — TCM diagnosis assistant"
echo -e "  ${CYAN}/学习模式${NC}      — Force study mode"
echo -e "  ${CYAN}/诊断模式${NC}      — Force diagnosis mode"
echo ""
echo -e "Documentation: ${BOLD}https://github.com/zrxparley/ni-haixia-tcm-skill${NC}"
