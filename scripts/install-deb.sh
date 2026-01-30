#!/bin/bash
#
# WorkPulse .deb Installer with Dependency Handling
# Run this instead of dpkg -i to get automatic dependency installation
#
# Usage: sudo ./install-deb.sh [workpulse.deb]
#

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m'

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Find .deb file
DEB_FILE="${1:-}"
if [ -z "$DEB_FILE" ]; then
    # Try to find .deb in common locations
    for loc in "$SCRIPT_DIR" "$SCRIPT_DIR/../dist" "." "./dist"; do
        found=$(find "$loc" -maxdepth 1 -name "workpulse*.deb" 2>/dev/null | head -1)
        if [ -n "$found" ]; then
            DEB_FILE="$found"
            break
        fi
    done
fi

print_banner() {
    clear 2>/dev/null || true
    echo ""
    echo -e "${GREEN}╔══════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║${NC}${BOLD}          WorkPulse - Time Tracking for Linux                ${NC}${GREEN}║${NC}"
    echo -e "${GREEN}║${NC}              Professional Daily Time Tracker                 ${GREEN}║${NC}"
    echo -e "${GREEN}╚══════════════════════════════════════════════════════════════╝${NC}"
    echo ""
}

check_root() {
    if [ "$EUID" -ne 0 ]; then
        echo -e "${YELLOW}This installer needs sudo privileges.${NC}"
        echo ""
        exec sudo bash "$0" "$@"
    fi
}

# Check if apt/dpkg is locked
is_apt_locked() {
    if flock -n /var/lib/dpkg/lock-frontend -c true 2>/dev/null; then
        return 1  # Not locked
    else
        return 0  # Locked
    fi
}

wait_for_apt() {
    if is_apt_locked; then
        echo -e "${YELLOW}⏳ Waiting for package manager to be available...${NC}"
        local count=0
        while is_apt_locked && [ $count -lt 30 ]; do
            sleep 2
            ((count++))
            echo -n "."
        done
        echo ""
        
        if is_apt_locked; then
            echo -e "${RED}Package manager is still busy after 60 seconds.${NC}"
            echo "Please wait for other installations to finish and try again."
            exit 1
        fi
        echo -e "${GREEN}✓ Package manager is now available${NC}"
    fi
}

check_package() {
    dpkg -l "$1" 2>/dev/null | grep -q "^ii"
}

cleanup_existing_installation() {
    echo -e "${BLUE}━━━ Checking for Existing Installation ━━━${NC}"
    echo ""
    
    # Check if workpulse is already installed
    if ! check_package "workpulse" && ! command -v workpulse &>/dev/null; then
        echo -e "${GREEN}✓ No existing installation found${NC}"
        echo ""
        return 0
    fi
    
    echo -e "${YELLOW}⚠ Found existing WorkPulse installation${NC}"
    echo -e "${YELLOW}  Performing complete cleanup for fresh installation...${NC}"
    echo ""
    
    # Stop all running processes
    echo -e "${CYAN}→ Stopping all WorkPulse processes...${NC}"
    pkill -f workpulsed 2>/dev/null || true
    pkill -f workpulse-mascot 2>/dev/null || true
    pkill -f workpulse-widget 2>/dev/null || true
    pkill -f workpulse-tray 2>/dev/null || true
    pkill -f workpulse-gui 2>/dev/null || true
    pkill -f "workpulse.*forcelock" 2>/dev/null || true
    sleep 1
    
    # Stop and disable systemd service for all users
    echo -e "${CYAN}→ Stopping services...${NC}"
    
    # Try to stop for current user if not root
    if [ "$EUID" -ne 0 ]; then
        systemctl --user stop workpulse.service 2>/dev/null || true
        systemctl --user disable workpulse.service 2>/dev/null || true
    fi
    
    # If there's a .deb package installed, remove it
    if check_package "workpulse"; then
        echo -e "${CYAN}→ Removing installed .deb package...${NC}"
        dpkg --purge workpulse 2>/dev/null || true
        apt-get remove --purge -y workpulse 2>/dev/null || true
    fi
    
    # Clean up user directories for all potential users
    echo -e "${CYAN}→ Cleaning up user data and configs...${NC}"
    
    # Clean current user's data
    rm -rf "$HOME/.local/bin/workpulse"* 2>/dev/null || true
    rm -rf "$HOME/.local/share/workpulse" 2>/dev/null || true
    rm -rf "$HOME/.config/workpulse" 2>/dev/null || true
    rm -f "$HOME/.config/systemd/user/workpulse.service" 2>/dev/null || true
    rm -f "$HOME/.config/autostart/workpulse"*.desktop 2>/dev/null || true
    rm -f "$HOME/.local/share/applications/workpulse"*.desktop 2>/dev/null || true
    
    # If running as root, clean system-wide installations
    if [ "$EUID" -eq 0 ]; then
        echo -e "${CYAN}→ Cleaning system-wide installation...${NC}"
        rm -f /usr/bin/workpulse* 2>/dev/null || true
        rm -f /usr/local/bin/workpulse* 2>/dev/null || true
        rm -rf /usr/share/workpulse 2>/dev/null || true
        rm -rf /usr/local/share/workpulse 2>/dev/null || true
        rm -f /etc/systemd/user/workpulse.service 2>/dev/null || true
        rm -f /etc/xdg/autostart/workpulse*.desktop 2>/dev/null || true
        rm -f /usr/share/applications/workpulse*.desktop 2>/dev/null || true
        
        # Clean up for all users in /home
        for user_home in /home/*; do
            if [ -d "$user_home" ]; then
                rm -rf "$user_home/.local/bin/workpulse"* 2>/dev/null || true
                rm -rf "$user_home/.local/share/workpulse" 2>/dev/null || true
                rm -rf "$user_home/.config/workpulse" 2>/dev/null || true
                rm -f "$user_home/.config/systemd/user/workpulse.service" 2>/dev/null || true
                rm -f "$user_home/.config/autostart/workpulse"*.desktop 2>/dev/null || true
                rm -f "$user_home/.local/share/applications/workpulse"*.desktop 2>/dev/null || true
            fi
        done
        
        # Reload systemd
        systemctl daemon-reload 2>/dev/null || true
    fi
    
    # Reload user systemd
    systemctl --user daemon-reload 2>/dev/null || true
    
    echo -e "${GREEN}✓ Cleanup completed - ready for fresh installation${NC}"
    echo ""
}

install_dependencies() {
    echo -e "${BLUE}━━━ Step 1: Cleaning Existing Installation ━━━${NC}"
    echo ""
    
    # Always do a clean installation
    cleanup_existing_installation
    
    echo -e "${BLUE}━━━ Step 2: Checking Dependencies ━━━${NC}"
    echo ""
    
    # Wait for apt if it's locked
    wait_for_apt
    
    # All required packages
    REQUIRED_PKGS=(
        "bash"
        "zenity" 
        "libnotify-bin"
        "sqlite3"
        "netcat-openbsd"
        "python3"
        "python3-gi"
        "gir1.2-gtk-3.0"
    )
    
    # Optional recommended packages  
    RECOMMENDED_PKGS=(
        "timewarrior"
        "xdotool"
        "wmctrl"
        "xprintidle"
    )
    
    MISSING_REQUIRED=()
    MISSING_RECOMMENDED=()
    
    # Check required
    echo -e "${CYAN}Required packages:${NC}"
    for pkg in "${REQUIRED_PKGS[@]}"; do
        if check_package "$pkg"; then
            echo -e "  ${GREEN}✓${NC} $pkg"
        else
            echo -e "  ${RED}✗${NC} $pkg"
            MISSING_REQUIRED+=("$pkg")
        fi
    done
    
    echo ""
    echo -e "${CYAN}Recommended packages:${NC}"
    for pkg in "${RECOMMENDED_PKGS[@]}"; do
        if check_package "$pkg"; then
            echo -e "  ${GREEN}✓${NC} $pkg"
        else
            echo -e "  ${YELLOW}○${NC} $pkg (optional)"
            MISSING_RECOMMENDED+=("$pkg")
        fi
    done
    echo ""
    
    # Install required packages
    if [ ${#MISSING_REQUIRED[@]} -gt 0 ]; then
        echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
        echo -e "${RED}Missing required:${NC} ${MISSING_REQUIRED[*]}"
        echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
        echo ""
        read -p "Install required packages now? [Y/n] " -n 1 -r
        echo ""
        
        if [[ ! $REPLY =~ ^[Nn]$ ]]; then
            echo ""
            echo -e "${BLUE}Updating package lists...${NC}"
            apt-get update -qq
            
            echo -e "${BLUE}Installing: ${MISSING_REQUIRED[*]}${NC}"
            if apt-get install -y "${MISSING_REQUIRED[@]}"; then
                echo ""
                echo -e "${GREEN}✓ Required packages installed!${NC}"
            else
                echo -e "${RED}Failed to install some packages.${NC}"
                exit 1
            fi
        else
            echo -e "${RED}Cannot continue without required packages.${NC}"
            exit 1
        fi
        echo ""
    else
        echo -e "${GREEN}All required packages are installed!${NC}"
        echo ""
    fi
    
    # Offer recommended packages
    if [ ${#MISSING_RECOMMENDED[@]} -gt 0 ]; then
        read -p "Install recommended packages (${MISSING_RECOMMENDED[*]})? [y/N] " -n 1 -r
        echo ""
        
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            echo -e "${BLUE}Installing recommended packages...${NC}"
            apt-get install -y "${MISSING_RECOMMENDED[@]}" 2>/dev/null || true
            echo -e "${GREEN}✓ Done!${NC}"
            echo ""
        fi
    fi
}

install_workpulse() {
    echo -e "${BLUE}━━━ Step 3: Installing WorkPulse ━━━${NC}"
    echo ""
    
    if [ -z "$DEB_FILE" ] || [ ! -f "$DEB_FILE" ]; then
        echo -e "${RED}Error: Cannot find workpulse .deb file${NC}"
        echo ""
        echo "Usage: sudo $0 /path/to/workpulse.deb"
        echo ""
        exit 1
    fi
    
    echo "Package: $DEB_FILE"
    echo ""
    
    if dpkg -i "$DEB_FILE"; then
        echo ""
        echo -e "${GREEN}✓ WorkPulse installed successfully!${NC}"
    else
        echo ""
        echo -e "${YELLOW}Fixing dependencies...${NC}"
        apt-get install -f -y
        echo -e "${GREEN}✓ Installation complete!${NC}"
    fi
    echo ""
}

setup_user() {
    ACTUAL_USER="${SUDO_USER:-$USER}"
    ACTUAL_HOME=$(getent passwd "$ACTUAL_USER" | cut -d: -f6)
    
    # Configure timewarrior
    if command -v timew &>/dev/null; then
        TIMEW_DIR="$ACTUAL_HOME/.timewarrior"
        if [ ! -d "$TIMEW_DIR" ]; then
            mkdir -p "$TIMEW_DIR"
            echo "# Timewarrior config" > "$TIMEW_DIR/timewarrior.cfg"
            chown -R "$ACTUAL_USER:$ACTUAL_USER" "$TIMEW_DIR"
            echo -e "${GREEN}✓ Timewarrior configured${NC}"
        fi
    fi
}

print_success() {
    echo ""
    echo -e "${GREEN}══════════════════════════════════════════════════════════════${NC}"
    echo -e "${GREEN}  ✓ WorkPulse installed successfully!${NC}"
    echo -e "${GREEN}══════════════════════════════════════════════════════════════${NC}"
    echo ""
    echo -e "${BOLD}Start the mascot widget:${NC}"
    echo -e "  ${CYAN}workpulse-mascot &${NC}"
    echo ""
    echo -e "${BOLD}Enable background daemon:${NC}"
    echo -e "  ${CYAN}systemctl --user daemon-reload${NC}"
    echo -e "  ${CYAN}systemctl --user enable --now workpulse${NC}"
    echo ""
    echo -e "${BOLD}Quick commands:${NC}"
    echo -e "  ${CYAN}workpulse status${NC}         - Check status"
    echo -e "  ${CYAN}workpulse start \"task\"${NC}   - Start tracking"
    echo -e "  ${CYAN}workpulse export standup${NC} - Standup report"
    echo ""
    echo -e "${GREEN}★ Mascot will auto-start on next login!${NC}"
    echo ""
    
    # Start mascot now?
    ACTUAL_USER="${SUDO_USER:-$USER}"
    read -p "Start mascot now? [Y/n] " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Nn]$ ]]; then
        su - "$ACTUAL_USER" -c "DISPLAY=${DISPLAY:-:0} nohup /usr/bin/workpulse-mascot >/dev/null 2>&1 &" || true
        echo -e "${GREEN}✓ Mascot started!${NC}"
    fi
    echo ""
}

# Main
print_banner
check_root "$@"
install_dependencies
install_workpulse
setup_user
print_success

exit 0
