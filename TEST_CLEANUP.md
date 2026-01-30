# Installation Cleanup Testing Guide

## What Changed

Both installation scripts now automatically clean up any existing WorkPulse installations before performing a fresh install:

### 1. `scripts/install.sh`
- Added `cleanup_existing_installation()` function
- Automatically called before dependency check
- Removes all files, configs, and data

### 2. `scripts/install-deb.sh`
- Added `cleanup_existing_installation()` function  
- Called as Step 1 before checking dependencies
- Removes .deb package if installed
- Cleans up all user and system files

## What Gets Cleaned Up

The cleanup process removes:

### Binaries
- `/usr/bin/workpulse*` (all variants)
- `/usr/local/bin/workpulse*`
- `~/.local/bin/workpulse*`

### System Files
- `/usr/share/workpulse/`
- `/usr/local/share/workpulse/`
- `/etc/systemd/user/workpulse.service`
- `/etc/xdg/autostart/workpulse-mascot.desktop`
- `/usr/share/applications/workpulse*.desktop`

### User Files
- `~/.local/share/workpulse/` (entire directory including logs, exports, database)
- `~/.config/workpulse/` (all configuration)
- `~/.config/systemd/user/workpulse.service`
- `~/.config/autostart/workpulse*.desktop`
- `~/.local/share/applications/workpulse*.desktop`

### Mascot/Widget Specific Files
- `~/.local/share/workpulse/mascot_settings.json`
- `~/.local/share/workpulse/task_history.json`
- `~/.local/share/workpulse/git_activity.log`

### Runtime Files
- `~/.local/share/workpulse/workpulse.pid`
- `~/.local/share/workpulse/workpulse.sock`
- `~/.local/share/workpulse/forcelock.pid`
- `~/.local/share/workpulse/forcelock.active`
- `~/.local/share/workpulse/disabled_devices`

### Processes
- Stops and disables systemd service
- Kills all running workpulse processes:
  - `workpulsed`
  - `workpulse-mascot`
  - `workpulse-widget`
  - `workpulse-tray`
  - `workpulse-gui`
  - `workpulse forcelock`

## Testing the Changes

### Test 1: Fresh Install (No Previous Installation)
```bash
cd /home/sigma/Gajjar/Logger/workpulsev1
./scripts/install.sh
```
Expected: Should show "No existing installation found" and proceed with installation.

### Test 2: Re-install Over Existing Installation
```bash
# First install
./scripts/install.sh

# Now re-install
./scripts/install.sh
```
Expected: 
- Should detect existing installation
- Should show cleanup messages
- Should remove all previous files
- Should install fresh

### Test 3: .deb Package Installation
```bash
# Build the .deb first
./scripts/build.sh --deb

# Install it
sudo ./scripts/install-deb.sh dist/workpulse_*.deb

# Re-install it
sudo ./scripts/install-deb.sh dist/workpulse_*.deb
```
Expected:
- First install works normally
- Second install detects and removes the .deb package
- Cleans all system-wide and user files
- Installs fresh

### Test 4: Verify Cleanup Works for All Files
```bash
# Create mock installation
mkdir -p ~/.local/bin ~/.local/share/workpulse ~/.config/workpulse
touch ~/.local/bin/workpulse
touch ~/.local/bin/workpulse-mascot
echo '{"test": "data"}' > ~/.local/share/workpulse/mascot_settings.json
echo 'TEST=1' > ~/.config/workpulse/config

# Run install
./scripts/install.sh

# Verify old files are gone and new ones exist
ls ~/.local/bin/workpulse*
ls ~/.local/share/workpulse/
ls ~/.config/workpulse/
```
Expected: All old files should be replaced with fresh installation.

## Benefits

1. **Always Fresh**: Every installation starts clean, no leftover configs or data
2. **No Conflicts**: Prevents issues from old versions interfering with new ones
3. **Mascot Settings Reset**: Ensures mascot/widget always starts with defaults
4. **Clean Migration**: Perfect for testing or upgrading from older versions
5. **Debugging**: Makes it easier to troubleshoot by eliminating "works on my machine" issues

## Manual Cleanup (if needed)

If you ever need to manually clean up without reinstalling:

```bash
# Stop all processes
pkill -f workpulse

# Remove everything
rm -rf ~/.local/bin/workpulse*
rm -rf ~/.local/share/workpulse
rm -rf ~/.config/workpulse
rm -f ~/.config/systemd/user/workpulse.service
rm -f ~/.config/autostart/workpulse*.desktop
systemctl --user daemon-reload

# For system-wide (requires sudo)
sudo rm -rf /usr/bin/workpulse*
sudo rm -rf /usr/share/workpulse
sudo rm -f /etc/systemd/user/workpulse.service
sudo rm -f /etc/xdg/autostart/workpulse*.desktop
```

## Notes

- The cleanup is **automatic** - no user confirmation required
- User data is **always removed** for truly fresh installs
- If you want to preserve data, back it up before reinstalling
- System-wide cleanup only happens when running as root/sudo
