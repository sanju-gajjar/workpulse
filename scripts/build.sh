#!/usr/bin/env bash
# ============================================================================
# WORKPULSE BUILD SCRIPT
# ============================================================================
# Creates distributable packages:
#   1. Self-extracting installer bundle
#   2. Tarball archive
#   3. (Optional) .deb package
# ============================================================================

set -euo pipefail

# Colors
readonly RED='\033[0;31m'
readonly GREEN='\033[0;32m'
readonly YELLOW='\033[0;33m'
readonly BLUE='\033[0;34m'
readonly BOLD='\033[1m'
readonly NC='\033[0m'

# Version (should match common.sh)
readonly VERSION="1.0.0"
readonly PACKAGE_NAME="workpulse"

# Directories
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
DIST_DIR="$PROJECT_DIR/dist"
BUILD_DIR="$PROJECT_DIR/build"

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

log_info() {
    echo -e "${BLUE}[INFO]${NC} $*"
}

log_success() {
    echo -e "${GREEN}[OK]${NC} $*"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $*"
}

clean_build() {
    log_info "Cleaning build directory..."
    rm -rf "$BUILD_DIR"
    mkdir -p "$BUILD_DIR"
    mkdir -p "$DIST_DIR"
}

# ============================================================================
# BUILD TARBALL
# ============================================================================

build_tarball() {
    local tarball="$DIST_DIR/${PACKAGE_NAME}-${VERSION}.tar.gz"
    local staging="$BUILD_DIR/staging"
    
    echo "[INFO] Building tarball..." >&2
    
    mkdir -p "$staging/${PACKAGE_NAME}-${VERSION}"
    
    # Copy source files, including mascot_lib and ui
    cp -r "$PROJECT_DIR/src" "$staging/${PACKAGE_NAME}-${VERSION}/"
    cp -r "$PROJECT_DIR/config" "$staging/${PACKAGE_NAME}-${VERSION}/"
    cp -r "$PROJECT_DIR/systemd" "$staging/${PACKAGE_NAME}-${VERSION}/"
    cp -r "$PROJECT_DIR/scripts" "$staging/${PACKAGE_NAME}-${VERSION}/"
    cp -r "$PROJECT_DIR/src/mascot_lib" "$staging/${PACKAGE_NAME}-${VERSION}/src/"
    cp "$PROJECT_DIR/README.md" "$staging/${PACKAGE_NAME}-${VERSION}/" 2>/dev/null || true
    cp "$PROJECT_DIR/LICENSE" "$staging/${PACKAGE_NAME}-${VERSION}/" 2>/dev/null || true
    
    # Make scripts executable
    chmod +x "$staging/${PACKAGE_NAME}-${VERSION}/src/workpulse"
    chmod +x "$staging/${PACKAGE_NAME}-${VERSION}/src/workpulsed"
    chmod +x "$staging/${PACKAGE_NAME}-${VERSION}/src/workpulse-widget"
    chmod +x "$staging/${PACKAGE_NAME}-${VERSION}/src/workpulse-mascot"
    chmod +x "$staging/${PACKAGE_NAME}-${VERSION}/scripts/"*.sh
    
    # Create tarball
    tar -czf "$tarball" -C "$staging" "${PACKAGE_NAME}-${VERSION}"
    
    echo "[OK] Created: $tarball" >&2
    echo "$tarball"
}

# ============================================================================
# BUILD SELF-EXTRACTING INSTALLER
# ============================================================================

build_self_installer() {
    log_info "Building self-extracting installer..."
    
    local output="$DIST_DIR/${PACKAGE_NAME}-${VERSION}-installer.run"
    local tarball
    tarball=$(build_tarball)
    
    # Create self-extracting header
    cat > "$BUILD_DIR/header.sh" << 'HEADER_EOF'
#!/usr/bin/env bash
# ============================================================================
# WORKPULSE SELF-EXTRACTING INSTALLER
# ============================================================================
# This is a self-extracting archive. Run with:
#   chmod +x workpulse-*-installer.run
#   ./workpulse-*-installer.run
# ============================================================================

set -euo pipefail

readonly MARKER="__ARCHIVE_BELOW__"
readonly TEMP_DIR=$(mktemp -d)

cleanup() {
    rm -rf "$TEMP_DIR"
}

trap cleanup EXIT

echo ""
echo "  ╦ ╦╔═╗╦═╗╦╔═╔═╗╦ ╦╦  ╔═╗╔═╗"
echo "  ║║║║ ║╠╦╝╠╩╗╠═╝║ ║║  ╚═╗║╣ "
echo "  ╚╩╝╚═╝╩╚═╩ ╩╩  ╚═╝╩═╝╚═╝╚═╝"
echo ""
echo "  Professional Time Tracking for Linux"
echo ""

# Find the line number where the archive starts
ARCHIVE_LINE=$(awk "/^${MARKER}$/{print NR + 1; exit 0;}" "$0")

if [[ -z "$ARCHIVE_LINE" ]]; then
    echo "Error: Could not find archive marker"
    exit 1
fi

echo "Extracting..."

# Extract the archive
tail -n +"$ARCHIVE_LINE" "$0" | tar -xzf - -C "$TEMP_DIR"

# Find the extracted directory
EXTRACTED_DIR=$(find "$TEMP_DIR" -maxdepth 1 -type d -name "workpulse-*" | head -1)

if [[ -z "$EXTRACTED_DIR" ]]; then
    echo "Error: Could not find extracted directory"
    exit 1
fi

# Run the installer
chmod +x "$EXTRACTED_DIR/scripts/install.sh"
"$EXTRACTED_DIR/scripts/install.sh" "$@"

exit 0
__ARCHIVE_BELOW__
HEADER_EOF

    # Combine header and tarball
    cat "$BUILD_DIR/header.sh" "$tarball" > "$output"
    chmod +x "$output"
    
    log_success "Created: $output"
    echo ""
    echo "To install, run:"
    echo "  chmod +x $(basename "$output")"
    echo "  ./$(basename "$output")"
}

# ============================================================================
# BUILD .DEB PACKAGE
# ============================================================================

build_deb() {
    log_info "Building .deb package..."
    
    if ! command -v dpkg-deb &>/dev/null; then
        log_error "dpkg-deb not found. Install dpkg on your system."
        return 1
    fi
    
    local deb_root="$BUILD_DIR/deb"
    local deb_name="${PACKAGE_NAME}_${VERSION}_all.deb"
    
    mkdir -p "$deb_root/DEBIAN"
    mkdir -p "$deb_root/usr/bin"
    mkdir -p "$deb_root/usr/share/workpulse/lib"
    mkdir -p "$deb_root/usr/share/applications"
    mkdir -p "$deb_root/usr/share/icons/hicolor/scalable/apps"
    mkdir -p "$deb_root/usr/share/icons/hicolor/48x48/apps"
    mkdir -p "$deb_root/etc/systemd/user"
    mkdir -p "$deb_root/etc/xdg/autostart"
    
    # Copy files
    cp "$PROJECT_DIR/src/workpulse" "$deb_root/usr/bin/"
    cp "$PROJECT_DIR/src/workpulsed" "$deb_root/usr/bin/"
    cp "$PROJECT_DIR/src/workpulse-gui" "$deb_root/usr/bin/"
    cp "$PROJECT_DIR/src/workpulse-tray" "$deb_root/usr/bin/"
    cp "$PROJECT_DIR/src/workpulse-widget" "$deb_root/usr/bin/"
    cp "$PROJECT_DIR/src/workpulse-mascot" "$deb_root/usr/bin/"
    cp "$PROJECT_DIR/src/lib/"*.sh "$deb_root/usr/share/workpulse/lib/"
    # Copy mascot_lib and ui folders
    mkdir -p "$deb_root/usr/share/workpulse/mascot_lib"
    cp -r "$PROJECT_DIR/src/mascot_lib/"* "$deb_root/usr/share/workpulse/mascot_lib/"
    cp "$PROJECT_DIR/config/workpulse.conf.default" "$deb_root/usr/share/workpulse/"
    
    # Desktop file and icon
    cp "$PROJECT_DIR/desktop/workpulse.desktop" "$deb_root/usr/share/applications/"
    cp "$PROJECT_DIR/desktop/workpulse.svg" "$deb_root/usr/share/icons/hicolor/scalable/apps/"
    
    # Also create a symlink for 48x48 (most launchers look here)
    ln -sf "../../../scalable/apps/workpulse.svg" "$deb_root/usr/share/icons/hicolor/48x48/apps/workpulse.svg"
    
    # Autostart for mascot (replaces tray)
    cp "$PROJECT_DIR/desktop/workpulse-mascot.desktop" "$deb_root/etc/xdg/autostart/"
    
    # Update library paths in executables for system-wide installation
    # For workpulse: Replace the if/else lib detection with system path
    sed -i '/# Source libraries (check both possible locations)/,/^fi$/{
        /# Source libraries (check both possible locations)/c\
# Source libraries from system installation\
LIB_DIR="/usr/share/workpulse/lib"
        /^if \[\[/d
        /LIB_DIR=/d
        /else$/d
        /Fallback for installed version/d
        /^fi$/d
    }' "$deb_root/usr/bin/workpulse"
    
    # For workpulsed: Simple string replacement
    sed -i 's|LIB_DIR="\$INSTALL_DIR/lib"|LIB_DIR="/usr/share/workpulse/lib"|' \
        "$deb_root/usr/bin/workpulsed"
    
    # workpulse-clickup already has correct paths - no modification needed
    
    chmod +x "$deb_root/usr/bin/workpulse"
    chmod +x "$deb_root/usr/bin/workpulsed"
    chmod +x "$deb_root/usr/bin/workpulse-gui"
    chmod +x "$deb_root/usr/bin/workpulse-tray"
    chmod +x "$deb_root/usr/bin/workpulse-widget"
    chmod +x "$deb_root/usr/bin/workpulse-mascot"
    
    # Systemd service
    cat > "$deb_root/etc/systemd/user/workpulse.service" << 'EOF'
[Unit]
Description=WorkPulse Time Tracking Daemon
Documentation=https://github.com/workpulse/workpulse
After=graphical-session.target
Wants=graphical-session.target

[Service]
Type=simple
ExecStart=/usr/bin/workpulsed foreground
ExecStop=/bin/kill -TERM $MAINPID
ExecReload=/bin/kill -HUP $MAINPID
Restart=on-failure
RestartSec=5
TimeoutStopSec=30

# Pass through user's graphical session environment
PassEnvironment=DISPLAY WAYLAND_DISPLAY XAUTHORITY

# Fallback environment
Environment=DISPLAY=:0

StandardOutput=journal
StandardError=journal
SyslogIdentifier=workpulse

[Install]
WantedBy=graphical-session.target
EOF
    
    # Control file - minimal dependencies to allow dpkg install
    # Full dependency check is done by install-deb.sh or postinst
    cat > "$deb_root/DEBIAN/control" << EOF
Package: workpulse
Version: $VERSION
Section: utils
Priority: optional
Architecture: all
Depends: bash (>= 4.0)
Recommends: zenity, libnotify-bin, sqlite3, python3, python3-gi, timewarrior
Suggests: xdotool, wmctrl, xprintidle
Maintainer: WorkPulse Team <workpulse@example.com>
Description: Professional Time Tracking for Linux
 WorkPulse is a desktop application for tracking work time,
 with hourly prompts, focus mode, and animated mascot widget.
 Features include standup report generation for ClickUp/Jira.
 .
 For best experience, run install-deb.sh which will install
 all required dependencies automatically.
EOF

    # Post-install script with dependency check
    cat > "$deb_root/DEBIAN/postinst" << 'POSTINST'
#!/bin/bash
set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo ""
echo -e "${GREEN}╔══════════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║          WorkPulse - Time Tracking for Linux                 ║${NC}"
echo -e "${GREEN}╚══════════════════════════════════════════════════════════════╝${NC}"
echo ""

PROJECT_DIR="/usr/share/workpulse"

# Check for missing dependencies
check_dependency() {
    local pkg="$1"
    local cmd="$2"
    
    if command -v "$cmd" &>/dev/null || dpkg -l "$pkg" 2>/dev/null | grep -q "^ii"; then
        return 0
    else
        return 1
    fi
}

# Required dependencies
MISSING_REQUIRED=()
MISSING_RECOMMENDED=()

echo -e "${BLUE}Checking dependencies...${NC}"
echo ""

# Required packages
declare -A REQUIRED_DEPS=(
    ["zenity"]="zenity"
    ["notify-send"]="libnotify-bin"
    ["sqlite3"]="sqlite3"
    ["python3"]="python3"
    ["nc"]="netcat-openbsd"
)

# Check required
for cmd in "${!REQUIRED_DEPS[@]}"; do
    pkg="${REQUIRED_DEPS[$cmd]}"
    if check_dependency "$pkg" "$cmd"; then
        echo -e "  ${GREEN}✓${NC} $pkg"
    else
        echo -e "  ${RED}✗${NC} $pkg (required)"
        MISSING_REQUIRED+=("$pkg")
    fi
done

# Check Python GTK bindings
if python3 -c "import gi; gi.require_version('Gtk', '3.0')" 2>/dev/null; then
    echo -e "  ${GREEN}✓${NC} python3-gi (GTK bindings)"
else
    echo -e "  ${RED}✗${NC} python3-gi (required for mascot widget)"
    MISSING_REQUIRED+=("python3-gi")
    MISSING_REQUIRED+=("gir1.2-gtk-3.0")
fi

# Recommended packages
declare -A RECOMMENDED_DEPS=(
    ["timew"]="timewarrior"
    ["xdotool"]="xdotool"
    ["wmctrl"]="wmctrl"
    ["xprintidle"]="xprintidle"
)

echo ""
echo -e "${BLUE}Checking recommended packages...${NC}"
echo ""

for cmd in "${!RECOMMENDED_DEPS[@]}"; do
    pkg="${RECOMMENDED_DEPS[$cmd]}"
    if check_dependency "$pkg" "$cmd"; then
        echo -e "  ${GREEN}✓${NC} $pkg"
    else
        echo -e "  ${YELLOW}○${NC} $pkg (recommended)"
        MISSING_RECOMMENDED+=("$pkg")
    fi
done

echo ""

# Function to check if apt is locked
is_apt_locked() {
    if flock -n /var/lib/dpkg/lock-frontend -c true 2>/dev/null; then
        return 1  # Not locked
    else
        return 0  # Locked
    fi
}

# Function to safely install packages
safe_apt_install() {
    local packages=("$@")
    
    # Check if apt is locked
    if is_apt_locked; then
        echo -e "${YELLOW}⚠ Package manager is busy (another installation in progress)${NC}"
        echo -e "${YELLOW}  Skipping automatic installation. Please run manually later:${NC}"
        echo "  sudo apt-get install ${packages[*]}"
        return 1
    fi
    
    # Try to install
    if apt-get install -y "${packages[@]}" 2>/dev/null; then
        return 0
    else
        return 1
    fi
}

# Install missing required dependencies
if [ ${#MISSING_REQUIRED[@]} -gt 0 ]; then
    echo -e "${YELLOW}═══════════════════════════════════════════════════════════════${NC}"
    echo -e "${RED}Missing required dependencies:${NC} ${MISSING_REQUIRED[*]}"
    echo -e "${YELLOW}═══════════════════════════════════════════════════════════════${NC}"
    echo ""
    
    # Check if apt is locked first
    if is_apt_locked; then
        echo -e "${YELLOW}⚠ Package manager is busy. Please install manually:${NC}"
        echo "  sudo apt-get install ${MISSING_REQUIRED[*]}"
    elif [ -t 0 ]; then
        read -p "Would you like to install them now? [Y/n] " -n 1 -r
        echo ""
        if [[ ! $REPLY =~ ^[Nn]$ ]]; then
            echo -e "${BLUE}Installing required dependencies...${NC}"
            if safe_apt_install "${MISSING_REQUIRED[@]}"; then
                echo -e "${GREEN}✓ Required dependencies installed successfully!${NC}"
            else
                echo -e "${RED}Failed to install some dependencies. Please install manually:${NC}"
                echo "  sudo apt-get install ${MISSING_REQUIRED[*]}"
            fi
        else
            echo -e "${YELLOW}Please install required dependencies manually:${NC}"
            echo "  sudo apt-get install ${MISSING_REQUIRED[*]}"
        fi
    else
        echo -e "${YELLOW}Please install required dependencies:${NC}"
        echo "  sudo apt-get install ${MISSING_REQUIRED[*]}"
    fi
    echo ""
fi

# Offer to install recommended dependencies
if [ ${#MISSING_RECOMMENDED[@]} -gt 0 ]; then
    echo -e "${YELLOW}Optional recommended packages:${NC} ${MISSING_RECOMMENDED[*]}"
    echo ""
    
    # Check if apt is locked first
    if is_apt_locked; then
        echo -e "${YELLOW}⚠ Package manager is busy. To install later:${NC}"
        echo "  sudo apt-get install ${MISSING_RECOMMENDED[*]}"
    elif [ -t 0 ]; then
        read -p "Would you like to install recommended packages? [y/N] " -n 1 -r
        echo ""
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            echo -e "${BLUE}Installing recommended packages...${NC}"
            if safe_apt_install "${MISSING_RECOMMENDED[@]}"; then
                echo -e "${GREEN}✓ Recommended packages installed!${NC}"
            else
                echo -e "${YELLOW}Some packages may not be available. Continuing anyway.${NC}"
            fi
        fi
    else
        echo "To install recommended packages:"
        echo "  sudo apt-get install ${MISSING_RECOMMENDED[*]}"
    fi
    echo ""
fi

# Configure timewarrior if installed
if command -v timew &>/dev/null; then
    TIMEW_CONFIG_DIR="${HOME}/.timewarrior"
    if [ ! -d "$TIMEW_CONFIG_DIR" ]; then
        mkdir -p "$TIMEW_CONFIG_DIR"
        echo "# Timewarrior configuration for WorkPulse" > "$TIMEW_CONFIG_DIR/timewarrior.cfg"
        echo -e "${GREEN}✓ Timewarrior configured${NC}"
    fi
fi

# =============================================================================
# PERSONALIZATION WIZARD
# =============================================================================
personalize_mascot() {
    local REAL_USER="${SUDO_USER:-$USER}"
    local REAL_HOME=$(getent passwd "$REAL_USER" | cut -d: -f6)
    local SETTINGS_DIR="$REAL_HOME/.local/share/workpulse"
    local SETTINGS_FILE="$SETTINGS_DIR/mascot_settings.json"
    
    # Skip if settings already exist (re-install)
    if [ -f "$SETTINGS_FILE" ]; then
        echo ""
        echo -e "${BLUE}Found existing settings. Keep current personalization? [Y/n]${NC} "
        read -r keep_settings
        if [[ ! "$keep_settings" =~ ^[Nn] ]]; then
            echo -e "${GREEN}✓ Keeping existing settings${NC}"
            return
        fi
    fi
    
    echo ""
    echo -e "${YELLOW}╔══════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${YELLOW}║              🎨 Let's personalize your mascot! 🎨            ║${NC}"
    echo -e "${YELLOW}╚══════════════════════════════════════════════════════════════╝${NC}"
    echo ""
    
    # Ask for user's name
    echo -e "${BLUE}What's your name?${NC} (for personalized greetings)"
    echo -n "Your name [$(whoami)]: "
    read -r user_name
    user_name="${user_name:-$(whoami)}"
    
    echo ""
    
    # Ask for mascot name
    echo -e "${BLUE}What would you like to call your mascot?${NC}"
    echo -n "Mascot name [Pulsy]: "
    read -r mascot_name
    mascot_name="${mascot_name:-Pulsy}"
    
    echo ""
    
    # Theme selection (dynamic from mascot_lib/character.py)
    echo -e "${BLUE}Choose a mascot theme:${NC}"
    THEME_LIST=()
    THEME_NAMES=()
    THEME_ICONS=()
    theme_index=1
    while IFS= read -r line; do
        # Parse lines like: '    'theme_key': { ... 'name': 'Name', 'icon': 'Icon', ... },'
        if [[ $line =~ "^[[:space:]]*'([a-zA-Z0-9_]+)':[[:space:]]*\{" ]]; then
            key=${BASH_REMATCH[1]}
            THEME_LIST+=("$key")
        fi
        if [[ $line =~ "'name': '([^']+)'" ]]; then
            THEME_NAMES+=("${BASH_REMATCH[1]}")
        fi
        if [[ $line =~ "'icon': '([^']+)'" ]]; then
            THEME_ICONS+=("${BASH_REMATCH[1]}")
        fi
    done < "$PROJECT_DIR/mascot_lib/character.py"

    for i in "${!THEME_LIST[@]}"; do
        icon="${THEME_ICONS[$i]:-}"
        name="${THEME_NAMES[$i]:-}"
        printf "  %2d) %s %s\n" "$((i+1))" "$icon" "$name"
    done
    echo ""
    echo -n "Theme [1-${#THEME_LIST[@]}, default 1]: "
    read -r theme_choice
    if [[ "$theme_choice" =~ ^[0-9]+$ ]] && (( theme_choice >= 1 && theme_choice <= ${#THEME_LIST[@]} )); then
        theme="${THEME_LIST[$((theme_choice-1))]}"
    else
        theme="blob"
    fi
    
    echo ""
    
    # Mascot size
    echo -e "${BLUE}Choose mascot size:${NC}"
    echo "  1) 🔹 Small  - Compact, less distracting"
    echo "  2) 🔸 Medium - Normal size (default)"
    echo "  3) 🔶 Large  - Big and visible"
    echo ""
    echo -n "Size [1-3, default 2]: "
    read -r size_choice
    
    case "$size_choice" in
        1) size="small" ;;
        3) size="large" ;;
        *) size="medium" ;;
    esac
    
    echo ""
    
    # End-of-day reminder time
    echo -e "${BLUE}When should I remind you to export your standup?${NC}"
    echo -n "Time (HH:MM, 24h format) [17:30]: "
    read -r eod_time
    eod_time="${eod_time:-17:30}"
    
    # Parse hour and minute
    eod_hour=$(echo "$eod_time" | cut -d: -f1)
    eod_minute=$(echo "$eod_time" | cut -d: -f2)
    
    # Validate
    if ! [[ "$eod_hour" =~ ^[0-9]+$ ]] || [ "$eod_hour" -lt 0 ] || [ "$eod_hour" -gt 23 ]; then
        eod_hour=17
    fi
    if ! [[ "$eod_minute" =~ ^[0-9]+$ ]] || [ "$eod_minute" -lt 0 ] || [ "$eod_minute" -gt 59 ]; then
        eod_minute=30
    fi
    
    echo ""
    
    # Create settings directory
    mkdir -p "$SETTINGS_DIR" 2>/dev/null || true
    
    # Write settings file
    cat > "$SETTINGS_FILE" << SETTINGS_EOF
{
  "user_name": "$user_name",
  "mascot_name": "$mascot_name",
  "mascot_theme": "$theme",
  "size": "$size",
  "eod_reminder_hour": $eod_hour,
  "eod_reminder_minute": $eod_minute,
  "show_system_notifications": true,
  "show_all_notifications": false,
  "scheduled_reminders": []
}
SETTINGS_EOF
    
    # Set correct ownership
    chown -R "$REAL_USER:$REAL_USER" "$SETTINGS_DIR" 2>/dev/null || true
    
    echo -e "${GREEN}╔══════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║                    ✨ All set! ✨                            ║${NC}"
    echo -e "${GREEN}╚══════════════════════════════════════════════════════════════╝${NC}"
    echo ""
    echo -e "  👤 Your name: ${BLUE}$user_name${NC}"
    echo -e "  🎭 Mascot name: ${BLUE}$mascot_name${NC}"
    echo -e "  🎨 Theme: ${BLUE}$theme${NC}"
    echo -e "  📐 Size: ${BLUE}$size${NC}"
    echo -e "  ⏰ EOD reminder: ${BLUE}$eod_hour:$(printf '%02d' $eod_minute)${NC}"
    echo ""
    echo -e "  💡 Tip: Add custom reminders from mascot menu!"
    echo ""
}

# Run personalization
personalize_mascot

# Setup mascot autostart for the current user
setup_mascot_autostart() {
    # Get the real user (not root when using sudo)
    local REAL_USER="${SUDO_USER:-$USER}"
    local REAL_HOME=$(getent passwd "$REAL_USER" | cut -d: -f6)
    
    if [ -n "$REAL_HOME" ] && [ -d "$REAL_HOME" ]; then
        local AUTOSTART_DIR="$REAL_HOME/.config/autostart"
        
        # Create autostart directory if needed
        mkdir -p "$AUTOSTART_DIR" 2>/dev/null || true
        
        # Create autostart entry for mascot
        cat > "$AUTOSTART_DIR/workpulse-mascot.desktop" << 'AUTOSTART_EOF'
[Desktop Entry]
Type=Application
Name=WorkPulse Mascot
Comment=Animated time tracking assistant
Exec=/usr/bin/workpulse-mascot
Icon=preferences-system-time
Terminal=false
StartupNotify=false
X-GNOME-Autostart-enabled=true
X-GNOME-Autostart-Delay=3
Categories=Utility;
AUTOSTART_EOF
        
        # Set correct ownership
        chown "$REAL_USER:$REAL_USER" "$AUTOSTART_DIR/workpulse-mascot.desktop" 2>/dev/null || true
        chmod 644 "$AUTOSTART_DIR/workpulse-mascot.desktop"
        
        echo -e "${GREEN}✓ Mascot auto-start configured for $REAL_USER${NC}"
        
        # Don't try to start mascot during dpkg install - it won't have display access
        # The mascot will start automatically on next login via autostart
        echo -e "${GREEN}✓ Mascot will start automatically on login${NC}"
    fi
}

# Run autostart setup
setup_mascot_autostart

echo ""
echo -e "${GREEN}═══════════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}  WorkPulse installed successfully!${NC}"
echo -e "${GREEN}═══════════════════════════════════════════════════════════════${NC}"
echo ""

# Update icon cache and desktop database
if command -v gtk-update-icon-cache &> /dev/null; then
    gtk-update-icon-cache -f -t /usr/share/icons/hicolor 2>/dev/null || true
fi
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database /usr/share/applications 2>/dev/null || true
fi

echo "🎉 Search for 'WorkPulse' in your app launcher to start!"
echo ""
echo "Or run manually:"
echo -e "  ${BLUE}workpulse-mascot &${NC}"
echo ""
echo "To enable the background daemon:"
echo -e "  ${BLUE}systemctl --user daemon-reload${NC}"
echo -e "  ${BLUE}systemctl --user enable --now workpulse${NC}"
echo ""
echo "Quick commands:"
echo -e "  ${BLUE}workpulse status${NC}        - Check status"
echo -e "  ${BLUE}workpulse start \"task\"${NC}  - Start tracking"
echo -e "  ${BLUE}workpulse export standup${NC} - Generate standup report"
echo -e "  ${BLUE}workpulse help${NC}          - Show all commands"
echo ""
echo -e "The mascot will auto-start on your next login!"
echo ""

exit 0
POSTINST
    chmod +x "$deb_root/DEBIAN/postinst"

    # Pre-remove script
    cat > "$deb_root/DEBIAN/prerm" << 'EOF'
#!/bin/bash
set -e

# Stop user service if running
if systemctl --user is-active workpulse 2>/dev/null; then
    systemctl --user stop workpulse || true
fi

exit 0
EOF
    chmod +x "$deb_root/DEBIAN/prerm"
    
    # Fix permissions for apt install (avoid _apt user permission denied)
    chmod -R 755 "$deb_root"
    find "$deb_root" -type f -exec chmod 644 {} \;
    chmod 755 "$deb_root/DEBIAN"
    chmod 755 "$deb_root/DEBIAN/postinst" "$deb_root/DEBIAN/prerm"
    chmod 755 "$deb_root/usr/bin/"*
    
    # Build .deb with root ownership
    dpkg-deb --root-owner-group --build "$deb_root" "$DIST_DIR/$deb_name"
    
    # Make the .deb readable by all
    chmod 644 "$DIST_DIR/$deb_name"
    
    log_success "Created: $DIST_DIR/$deb_name"
}

# ============================================================================
# MAIN
# ============================================================================

print_usage() {
    cat << EOF
WorkPulse Build Script

Usage: ./build.sh [target]

Targets:
    all         Build all packages (default)
    tarball     Build tarball archive
    installer   Build self-extracting installer
    deb         Build .deb package (requires dpkg-deb)
    clean       Clean build artifacts

Output: dist/
EOF
}

main() {
    local target="${1:-all}"
    
    echo ""
    echo -e "${BOLD}WorkPulse Build System${NC}"
    echo "======================"
    echo "Version: $VERSION"
    echo ""
    
    case "$target" in
        all)
            clean_build
            build_self_installer
            echo ""
            
            if command -v dpkg-deb &>/dev/null; then
                build_deb
            else
                log_info "Skipping .deb (dpkg-deb not available)"
            fi
            ;;
        tarball)
            clean_build
            build_tarball
            ;;
        installer)
            clean_build
            build_self_installer
            ;;
        deb)
            clean_build
            build_deb
            ;;
        clean)
            clean_build
            rm -f "$DIST_DIR"/*
            log_success "Build cleaned"
            ;;
        -h|--help|help)
            print_usage
            ;;
        *)
            log_error "Unknown target: $target"
            print_usage
            exit 1
            ;;
    esac
    
    echo ""
    echo -e "${GREEN}Build complete!${NC}"
    echo ""
    echo "Output files in: $DIST_DIR/"
    ls -la "$DIST_DIR/" 2>/dev/null || true
}

main "$@"
