#!/usr/bin/env bash
# ============================================================================
# WORKPULSE UNINSTALLER
# ============================================================================
# Removes WorkPulse from the system
# Usage: ./uninstall.sh [--purge]
# ============================================================================

set -euo pipefail

# Colors
readonly RED='\033[0;31m'
readonly GREEN='\033[0;32m'
readonly YELLOW='\033[0;33m'
readonly BLUE='\033[0;34m'
readonly BOLD='\033[1m'
readonly NC='\033[0m'

# Installation directories
USER_BIN_DIR="$HOME/.local/bin"
USER_SHARE_DIR="$HOME/.local/share/workpulse"
USER_CONFIG_DIR="$HOME/.config/workpulse"
USER_SYSTEMD_DIR="$HOME/.config/systemd/user"

SYSTEM_BIN_DIR="/usr/local/bin"
SYSTEM_SHARE_DIR="/usr/share/workpulse"
SYSTEM_SYSTEMD_DIR="/etc/systemd/user"

# Purge mode (remove config and data)
PURGE=false

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

is_root() {
    [[ $EUID -eq 0 ]]
}

# ============================================================================
# UNINSTALLATION
# ============================================================================

stop_service() {
    log_info "Stopping WorkPulse service..."
    
    # Stop user service
    if systemctl --user is-active --quiet workpulse.service 2>/dev/null; then
        systemctl --user stop workpulse.service
        log_success "Service stopped"
    fi
    
    # Disable user service
    if systemctl --user is-enabled --quiet workpulse.service 2>/dev/null; then
        systemctl --user disable workpulse.service
        log_success "Service disabled"
    fi
    
    # Kill any running processes
    pkill -f workpulsed 2>/dev/null || true
    pkill -f "workpulse.*forcelock" 2>/dev/null || true
}

remove_user_install() {
    log_info "Removing user installation..."
    
    # Remove executables
    rm -f "$USER_BIN_DIR/workpulse"
    rm -f "$USER_BIN_DIR/workpulsed"
    
    # Remove share directory (but keep user data by default)
    rm -rf "$USER_SHARE_DIR/lib"
    rm -f "$USER_SHARE_DIR/workpulse.conf.default"
    
    # Remove systemd service
    rm -f "$USER_SYSTEMD_DIR/workpulse.service"
    systemctl --user daemon-reload 2>/dev/null || true
    
    log_success "User installation removed"
}

remove_system_install() {
    if ! is_root; then
        log_warn "System installation removal requires root"
        log_info "Run with: sudo ./uninstall.sh"
        return
    fi
    
    log_info "Removing system installation..."
    
    # Remove executables
    rm -f "$SYSTEM_BIN_DIR/workpulse"
    rm -f "$SYSTEM_BIN_DIR/workpulsed"
    
    # Remove share directory
    rm -rf "$SYSTEM_SHARE_DIR"
    
    # Remove systemd service
    rm -f "$SYSTEM_SYSTEMD_DIR/workpulse.service"
    
    log_success "System installation removed"
}

remove_user_data() {
    if [[ "$PURGE" == "true" ]]; then
        log_warn "Purging user data and configuration..."
        
        # Remove config
        rm -rf "$USER_CONFIG_DIR"
        log_success "Configuration removed"
        
        # Remove data directory
        rm -rf "$USER_SHARE_DIR"
        log_success "Data directory removed"
        
        # Remove any runtime files
        rm -f "$HOME/.local/share/workpulse/workpulse.pid"
        rm -f "$HOME/.local/share/workpulse/workpulse.sock"
        rm -f "$HOME/.local/share/workpulse/forcelock.pid"
        rm -f "$HOME/.local/share/workpulse/forcelock.active"
        rm -f "$HOME/.local/share/workpulse/disabled_devices"
    else
        log_info "Keeping user data and configuration"
        log_info "Use --purge to remove all data"
        
        # Only remove empty share directory
        rmdir "$USER_SHARE_DIR" 2>/dev/null || true
    fi
}

# ============================================================================
# MAIN
# ============================================================================

print_usage() {
    cat << EOF
WorkPulse Uninstaller

Usage: ./uninstall.sh [options]

Options:
    --purge     Remove all data and configuration
    --help      Show this help message

Examples:
    ./uninstall.sh          # Keep config and data
    ./uninstall.sh --purge  # Remove everything
EOF
}

main() {
    # Parse arguments
    while [[ $# -gt 0 ]]; do
        case "$1" in
            --purge)
                PURGE=true
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
    
    echo ""
    echo -e "${BOLD}WorkPulse Uninstaller${NC}"
    echo "====================="
    echo ""
    
    # Confirmation
    if [[ "$PURGE" == "true" ]]; then
        echo -e "${YELLOW}WARNING: This will remove all WorkPulse data and configuration!${NC}"
    fi
    
    read -p "Are you sure you want to uninstall WorkPulse? (y/N) " -n 1 -r
    echo
    
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        log_info "Uninstallation cancelled"
        exit 0
    fi
    
    echo ""
    
    # Stop service
    stop_service
    
    # Remove user installation
    remove_user_install
    
    # Remove system installation (if root)
    if is_root; then
        remove_system_install
    fi
    
    # Handle user data
    remove_user_data
    
    echo ""
    echo -e "${GREEN}WorkPulse has been uninstalled${NC}"
    echo ""
    
    if [[ "$PURGE" != "true" ]]; then
        echo "Your configuration and data were preserved at:"
        echo "  Config: $USER_CONFIG_DIR"
        echo "  Data:   $USER_SHARE_DIR"
        echo ""
        echo "Run with --purge to remove them."
    fi
}

main "$@"
