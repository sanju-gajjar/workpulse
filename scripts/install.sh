#!/usr/bin/env bash
# ============================================================================
# WORKPULSE INSTALLER
# ============================================================================
# Installs WorkPulse system-wide or per-user
# Usage: ./install.sh [--system|--user]
# ============================================================================

set -euo pipefail

# Colors
readonly RED='\033[0;31m'
readonly GREEN='\033[0;32m'
readonly YELLOW='\033[0;33m'
readonly BLUE='\033[0;34m'
readonly CYAN='\033[0;36m'
readonly BOLD='\033[1m'
readonly NC='\033[0m'

# Version
readonly VERSION="1.0.0"

# Installation directories
USER_BIN_DIR="$HOME/.local/bin"
USER_SHARE_DIR="$HOME/.local/share/workpulse"
USER_CONFIG_DIR="$HOME/.config/workpulse"
USER_SYSTEMD_DIR="$HOME/.config/systemd/user"

SYSTEM_BIN_DIR="/usr/local/bin"
SYSTEM_SHARE_DIR="/usr/share/workpulse"
SYSTEM_SYSTEMD_DIR="/etc/systemd/user"

# Default to user installation
INSTALL_MODE="user"

# Source directory (where install.sh is located)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SOURCE_DIR="$(dirname "$SCRIPT_DIR")"

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

log_info() {
    echo -e "${BLUE}[INFO]${NC} $*"
}

log_success() {
    echo -e "${GREEN}[OK]${NC} $*"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $*"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $*"
}

header() {
    echo ""
    echo -e "${BOLD}========================================${NC}"
    echo -e "${BOLD}  WorkPulse Installer v$VERSION${NC}"
    echo -e "${BOLD}========================================${NC}"
    echo ""
}

# Check if running as root
is_root() {
    [[ $EUID -eq 0 ]]
}

# Check if command exists
has_command() {
    command -v "$1" &>/dev/null
}

# ============================================================================
# CLEANUP EXISTING INSTALLATION
# ============================================================================

cleanup_existing_installation() {
    log_info "Checking for existing installation..."
    
    local found_installation=false
    
    # Check for existing binaries
    if [[ -f "$USER_BIN_DIR/workpulse" ]] || [[ -f "$USER_BIN_DIR/workpulsed" ]] || \
       [[ -f "$USER_BIN_DIR/workpulse-gui" ]] || [[ -f "$USER_BIN_DIR/workpulse-mascot" ]] || \
       [[ -f "$USER_BIN_DIR/workpulse-widget" ]] || [[ -f "$USER_BIN_DIR/workpulse-tray" ]] || \
       [[ -f "$SYSTEM_BIN_DIR/workpulse" ]] || [[ -f "$SYSTEM_BIN_DIR/workpulsed" ]] || \
       [[ -f "$SYSTEM_BIN_DIR/workpulse-gui" ]] || [[ -f "$SYSTEM_BIN_DIR/workpulse-mascot" ]] || \
       [[ -f "$SYSTEM_BIN_DIR/workpulse-widget" ]] || [[ -f "$SYSTEM_BIN_DIR/workpulse-tray" ]]; then
        found_installation=true
    fi
    
    # Check for share directories
    if [[ -d "$USER_SHARE_DIR" ]] || [[ -d "$SYSTEM_SHARE_DIR" ]]; then
        found_installation=true
    fi
    
    # Check for systemd service
    if [[ -f "$USER_SYSTEMD_DIR/workpulse.service" ]] || [[ -f "$SYSTEM_SYSTEMD_DIR/workpulse.service" ]]; then
        found_installation=true
    fi
    
    # Check for config
    if [[ -d "$USER_CONFIG_DIR" ]]; then
        found_installation=true
    fi
    
    # Check for autostart desktop files
    if [[ -f "$HOME/.config/autostart/workpulse-mascot.desktop" ]] || \
       [[ -f "$HOME/.config/autostart/workpulse-tray.desktop" ]] || \
       [[ -f "/etc/xdg/autostart/workpulse-mascot.desktop" ]]; then
        found_installation=true
    fi
    
    if [[ "$found_installation" == "false" ]]; then
        log_success "No existing installation found"
        return 0
    fi
    
    log_warn "Found existing WorkPulse installation"
    log_warn "Performing complete cleanup for fresh installation..."
    echo ""
    
    # Stop all running processes
    log_info "Stopping all WorkPulse processes..."
    pkill -f workpulsed 2>/dev/null || true
    pkill -f workpulse-mascot 2>/dev/null || true
    pkill -f workpulse-widget 2>/dev/null || true
    pkill -f workpulse-tray 2>/dev/null || true
    pkill -f workpulse-gui 2>/dev/null || true
    pkill -f "workpulse.*forcelock" 2>/dev/null || true
    sleep 1
    
    # Stop and disable systemd service
    if systemctl --user is-active --quiet workpulse.service 2>/dev/null; then
        log_info "Stopping workpulse service..."
        systemctl --user stop workpulse.service || true
    fi
    
    if systemctl --user is-enabled --quiet workpulse.service 2>/dev/null; then
        log_info "Disabling workpulse service..."
        systemctl --user disable workpulse.service || true
    fi
    
    # Remove user installation files
    log_info "Removing user installation files..."
    rm -f "$USER_BIN_DIR/workpulse" 2>/dev/null || true
    rm -f "$USER_BIN_DIR/workpulsed" 2>/dev/null || true
    rm -f "$USER_BIN_DIR/workpulse-gui" 2>/dev/null || true
    rm -f "$USER_BIN_DIR/workpulse-mascot" 2>/dev/null || true
    rm -f "$USER_BIN_DIR/workpulse-widget" 2>/dev/null || true
    rm -f "$USER_BIN_DIR/workpulse-tray" 2>/dev/null || true
    
    # Remove system installation files (if we have permission)
    if is_root; then
        log_info "Removing system installation files..."
        rm -f "$SYSTEM_BIN_DIR/workpulse" 2>/dev/null || true
        rm -f "$SYSTEM_BIN_DIR/workpulsed" 2>/dev/null || true
        rm -f "$SYSTEM_BIN_DIR/workpulse-gui" 2>/dev/null || true
        rm -f "$SYSTEM_BIN_DIR/workpulse-mascot" 2>/dev/null || true
        rm -f "$SYSTEM_BIN_DIR/workpulse-widget" 2>/dev/null || true
        rm -f "$SYSTEM_BIN_DIR/workpulse-tray" 2>/dev/null || true
        rm -rf "$SYSTEM_SHARE_DIR" 2>/dev/null || true
        rm -f "$SYSTEM_SYSTEMD_DIR/workpulse.service" 2>/dev/null || true
    fi
    
    # Remove share directories and all data
    log_info "Removing data directories..."
    rm -rf "$USER_SHARE_DIR" 2>/dev/null || true
    
    # Remove config directory and all settings
    log_info "Removing configuration..."
    rm -rf "$USER_CONFIG_DIR" 2>/dev/null || true
    
    # Remove mascot settings and data
    log_info "Removing mascot/widget settings..."
    rm -f "$HOME/.local/share/workpulse/mascot_settings.json" 2>/dev/null || true
    rm -f "$HOME/.local/share/workpulse/task_history.json" 2>/dev/null || true
    rm -f "$HOME/.local/share/workpulse/git_activity.log" 2>/dev/null || true
    
    # Remove runtime files
    rm -f "$HOME/.local/share/workpulse/workpulse.pid" 2>/dev/null || true
    rm -f "$HOME/.local/share/workpulse/workpulse.sock" 2>/dev/null || true
    rm -f "$HOME/.local/share/workpulse/forcelock.pid" 2>/dev/null || true
    rm -f "$HOME/.local/share/workpulse/forcelock.active" 2>/dev/null || true
    rm -f "$HOME/.local/share/workpulse/disabled_devices" 2>/dev/null || true
    
    # Remove systemd service files
    log_info "Removing systemd service files..."
    rm -f "$USER_SYSTEMD_DIR/workpulse.service" 2>/dev/null || true
    
    # Remove autostart entries
    log_info "Removing autostart entries..."
    rm -f "$HOME/.config/autostart/workpulse-mascot.desktop" 2>/dev/null || true
    rm -f "$HOME/.config/autostart/workpulse-tray.desktop" 2>/dev/null || true
    
    if is_root; then
        rm -f "/etc/xdg/autostart/workpulse-mascot.desktop" 2>/dev/null || true
    fi
    
    # Remove desktop application entries
    rm -f "$HOME/.local/share/applications/workpulse.desktop" 2>/dev/null || true
    rm -f "$HOME/.local/share/applications/workpulse-mascot.desktop" 2>/dev/null || true
    
    # Reload systemd
    systemctl --user daemon-reload 2>/dev/null || true
    
    log_success "Cleanup completed - ready for fresh installation"
    echo ""
}

# ============================================================================
# DEPENDENCY CHECKS
# ============================================================================

check_dependencies() {
    log_info "Checking dependencies..."
    
    local missing=()
    local optional_missing=()
    
    # Required dependencies
    has_command bash || missing+=("bash (>= 4.0)")
    has_command zenity || missing+=("zenity")
    has_command notify-send || missing+=("libnotify-bin / libnotify")
    has_command sqlite3 || missing+=("sqlite3")
    has_command nc || missing+=("netcat / nc")
    
    # Optional dependencies
    has_command timew || optional_missing+=("timewarrior (for time tracking)")
    has_command xdotool || optional_missing+=("xdotool (for X11 window management)")
    has_command wmctrl || optional_missing+=("wmctrl (for window control)")
    has_command xinput || optional_missing+=("xinput (for force mode input blocking)")
    
    if [[ ${#missing[@]} -gt 0 ]]; then
        log_error "Missing required dependencies:"
        for dep in "${missing[@]}"; do
            echo "  - $dep"
        done
        echo ""
        echo "Please install them using your package manager:"
        echo ""
        echo "  Ubuntu/Debian:"
        echo "    sudo apt install zenity libnotify-bin sqlite3 netcat-openbsd"
        echo ""
        echo "  Fedora:"
        echo "    sudo dnf install zenity libnotify sqlite netcat"
        echo ""
        echo "  Arch Linux:"
        echo "    sudo pacman -S zenity libnotify sqlite gnu-netcat"
        echo ""
        return 1
    fi
    
    log_success "All required dependencies found"
    
    if [[ ${#optional_missing[@]} -gt 0 ]]; then
        log_warn "Optional dependencies not found (some features may be limited):"
        for dep in "${optional_missing[@]}"; do
            echo "  - $dep"
        done
        echo ""
    fi
    
    return 0
}

# ============================================================================
# INSTALLATION
# ============================================================================

create_directories() {
    log_info "Creating directories..."
    
    if [[ "$INSTALL_MODE" == "user" ]]; then
        mkdir -p "$USER_BIN_DIR"
        mkdir -p "$USER_SHARE_DIR"
        mkdir -p "$USER_CONFIG_DIR"
        mkdir -p "$USER_SYSTEMD_DIR"
        mkdir -p "$USER_SHARE_DIR/lib"
    else
        mkdir -p "$SYSTEM_BIN_DIR"
        mkdir -p "$SYSTEM_SHARE_DIR"
        mkdir -p "$SYSTEM_SHARE_DIR/lib"
        mkdir -p "$SYSTEM_SYSTEMD_DIR"
    fi
    
    log_success "Directories created"
}

install_files() {
    log_info "Installing files..."
    
    local bin_dir share_dir systemd_dir
    
    if [[ "$INSTALL_MODE" == "user" ]]; then
        bin_dir="$USER_BIN_DIR"
        share_dir="$USER_SHARE_DIR"
        systemd_dir="$USER_SYSTEMD_DIR"
    else
        bin_dir="$SYSTEM_BIN_DIR"
        share_dir="$SYSTEM_SHARE_DIR"
        systemd_dir="$SYSTEM_SYSTEMD_DIR"
    fi
    
    # Install main executables
    cp "$SOURCE_DIR/src/workpulse" "$bin_dir/workpulse"
    cp "$SOURCE_DIR/src/workpulsed" "$bin_dir/workpulsed"
    chmod +x "$bin_dir/workpulse"
    chmod +x "$bin_dir/workpulsed"
    
    # Install library files
    cp "$SOURCE_DIR/src/lib/"*.sh "$share_dir/lib/"
    # Install mascot_lib and ui folders
    mkdir -p "$share_dir/mascot_lib"
    cp -r "$SOURCE_DIR/src/mascot_lib/"* "$share_dir/mascot_lib/"
    
    # Update library path in executables
    sed -i "s|LIB_DIR=\"\$INSTALL_DIR/lib\"|LIB_DIR=\"$share_dir/lib\"|" "$bin_dir/workpulse"
    sed -i "s|LIB_DIR=\"\$INSTALL_DIR/lib\"|LIB_DIR=\"$share_dir/lib\"|" "$bin_dir/workpulsed"
    
    # Install default config
    cp "$SOURCE_DIR/config/workpulse.conf.default" "$share_dir/"
    
    # Install systemd service
    if [[ "$INSTALL_MODE" == "user" ]]; then
        # User service - adjust path
        sed "s|%h/.local/bin/workpulsed|$bin_dir/workpulsed|" \
            "$SOURCE_DIR/systemd/workpulse.service" > "$systemd_dir/workpulse.service"
    else
        cp "$SOURCE_DIR/systemd/workpulse.service" "$systemd_dir/"
        # System service needs different path
        sed -i "s|%h/.local/bin/workpulsed|$bin_dir/workpulsed|" "$systemd_dir/workpulse.service"
    fi
    
    log_success "Files installed"
}

setup_user_config() {
    log_info "Setting up user configuration..."
    
    local share_dir
    if [[ "$INSTALL_MODE" == "user" ]]; then
        share_dir="$USER_SHARE_DIR"
    else
        share_dir="$SYSTEM_SHARE_DIR"
    fi
    
    # Create user config if doesn't exist
    if [[ ! -f "$USER_CONFIG_DIR/config" ]]; then
        mkdir -p "$USER_CONFIG_DIR"
        cp "$share_dir/workpulse.conf.default" "$USER_CONFIG_DIR/config"
        log_success "Created user config at $USER_CONFIG_DIR/config"
    else
        log_info "User config already exists, skipping"
    fi
    
    # Create data directories
    mkdir -p "$HOME/.local/share/workpulse/logs"
    mkdir -p "$HOME/.local/share/workpulse/exports"
    
    log_success "User configuration ready"
}

enable_systemd_service() {
    log_info "Configuring systemd service..."
    
    # Reload systemd
    systemctl --user daemon-reload
    
    # Enable service
    systemctl --user enable workpulse.service
    
    log_success "Systemd service enabled"
    log_info "The service will start automatically on next login"
    
    # Offer to start now
    echo ""
    read -p "Start WorkPulse now? (Y/n) " -n 1 -r
    echo
    
    if [[ ! $REPLY =~ ^[Nn]$ ]]; then
        systemctl --user start workpulse.service
        sleep 2
        
        if systemctl --user is-active --quiet workpulse.service; then
            log_success "WorkPulse is now running"
        else
            log_warn "Service may not have started correctly"
            log_info "Check with: systemctl --user status workpulse"
        fi
    fi
}

update_path() {
    if [[ "$INSTALL_MODE" == "user" ]]; then
        # Check if ~/.local/bin is in PATH
        if [[ ":$PATH:" != *":$USER_BIN_DIR:"* ]]; then
            log_warn "$USER_BIN_DIR is not in your PATH"
            echo ""
            echo "Add the following to your ~/.bashrc or ~/.zshrc:"
            echo ""
            echo "  export PATH=\"\$HOME/.local/bin:\$PATH\""
            echo ""
        fi
    fi
}

# ============================================================================
# MAIN INSTALLATION FLOW
# ============================================================================

install_workpulse() {
    header
    
    log_info "Installation mode: $INSTALL_MODE"
    echo ""
    
    # Check for root if system install
    if [[ "$INSTALL_MODE" == "system" ]] && ! is_root; then
        log_error "System installation requires root privileges"
        log_info "Run with: sudo ./install.sh --system"
        exit 1
    fi
    
    # Clean up any existing installation first
    cleanup_existing_installation
    
    # Check dependencies
    if ! check_dependencies; then
        exit 1
    fi
    
    echo ""
    
    # Create directories
    create_directories
    
    # Install files
    install_files
    
    # Setup user config
    setup_user_config
    
    # Enable systemd (print instruction if root)
    if ! is_root; then
        enable_systemd_service
    else
        log_info "Skipping systemd setup (running as root)"
        echo ""
        echo "To enable and start the WorkPulse user service, log in as the target user and run:"
        echo "  systemctl --user enable --now workpulse"
    fi
    
    # PATH reminder
    update_path
    
    echo ""
    echo -e "${BOLD}========================================${NC}"
    echo -e "${GREEN}  Installation Complete!${NC}"
    echo -e "${BOLD}========================================${NC}"
    echo ""
    echo "Quick Start:"
    echo "  workpulse status        - Check status"
    echo "  workpulse start 'task'  - Start tracking"
    echo "  workpulse help          - Show all commands"
    echo ""
    echo "Configuration: $USER_CONFIG_DIR/config"
    echo "Logs:          ~/.local/share/workpulse/logs/"
    echo ""
}

# ============================================================================
# ARGUMENT PARSING
# ============================================================================

print_usage() {
    cat << EOF
WorkPulse Installer v$VERSION

Usage: ./install.sh [options]

Options:
    --user      Install for current user only (default)
    --system    Install system-wide (requires root)
    --help      Show this help message

Examples:
    ./install.sh              # User installation
    sudo ./install.sh --system # System-wide installation
EOF
}

main() {
    # Parse arguments
    while [[ $# -gt 0 ]]; do
        case "$1" in
            --user)
                INSTALL_MODE="user"
                shift
                ;;
            --system)
                INSTALL_MODE="system"
                shift
                ;;
            --help|-h)
                print_usage
                exit 0
                ;;
            *)
                log_error "Unknown option: $1"
                print_usage
                exit 1
                ;;
        esac
    done
    
    install_workpulse
}

main "$@"
