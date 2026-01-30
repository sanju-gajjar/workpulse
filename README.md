# WorkPulse

**Professional Time Tracking & Work Accountability for Linux**

```
  ╦ ╦╔═╗╦═╗╦╔═╔═╗╦ ╦╦  ╔═╗╔═╗
  ║║║║ ║╠╦╝╠╩╗╠═╝║ ║║  ╚═╗║╣ 
  ╚╩╝╚═╝╩╚═╩ ╩╩  ╚═╝╩═╝╚═╝╚═╝
```

WorkPulse is a Linux desktop application that helps professionals track their work time, maintain accountability, and generate detailed reports. It features hourly prompts, focus mode, and an innovative "force mode" that ensures check-ins happen.

## Features

### 🕐 Time Tracking
- **Timewarrior Integration**: Seamless integration with the popular time tracking tool
- **Auto-tagging**: Automatically tags tasks based on keywords (meeting, code, review, etc.)
- **Continuous tracking**: Start, stop, and switch between tasks effortlessly

### 📝 Hourly Check-ins
- **Smart prompts**: Non-intrusive notifications with follow-up dialogs
- **Working hours aware**: Only prompts during configured work hours (default: 10 AM - 7:30 PM)
- **Track progress**: Log what you're working on, what you completed, and any blockers

### 🎯 Focus Mode
- **Suppress prompts**: Temporarily disable check-ins for deep work
- **Configurable duration**: Set focus periods from 30 minutes to 3 hours
- **Automatic exit**: Focus mode ends automatically after the set duration

### ⚠️ Force Mode (Accountability Feature)
When you've been working for 3+ hours and missed 3 consecutive prompts:
- Screen becomes blocked with a mandatory input dialog
- Cannot be dismissed without providing a task update
- Ensures accountability even during the busiest days

### 📊 Reports & Exports
- **Daily summaries**: Automatic end-of-day summary at 7:30 PM
- **Multiple formats**: Export to CSV, Markdown, and JSON
- **Time by tag**: See how you spend time across different activities

## Installation

### Quick Install (Self-Extracting Installer)

```bash
# Download the installer
wget https://github.com/workpulse/workpulse/releases/download/v1.0.0/workpulse-1.0.0-installer.run

# Make it executable and run
chmod +x workpulse-1.0.0-installer.run
./workpulse-1.0.0-installer.run
```

### From Source

```bash
# Clone the repository
git clone https://github.com/workpulse/workpulse.git
cd workpulse

# Run the installer
./scripts/install.sh
```

### Debian/Ubuntu Package

```bash
# Download the .deb
wget https://github.com/workpulse/workpulse/releases/download/v1.0.0/workpulse_1.0.0_all.deb

# Install
sudo dpkg -i workpulse_1.0.0_all.deb
sudo apt-get install -f  # Install dependencies if needed

# Enable for your user
systemctl --user enable --now workpulse
```

## Dependencies

### Required
- `bash` (>= 4.0)
- `zenity` - GTK+ dialog boxes
- `libnotify-bin` - Desktop notifications
- `sqlite3` - Database storage
- `netcat` - IPC communication

### Optional (Recommended)
- `timewarrior` - Time tracking backend
- `xdotool` - X11 window management
- `wmctrl` - Window control
- `xinput` - Input device control (for force mode)

### Install Dependencies

**Ubuntu/Debian:**
```bash
sudo apt install zenity libnotify-bin sqlite3 netcat-openbsd timewarrior xdotool wmctrl xinput
```

**Fedora:**
```bash
sudo dnf install zenity libnotify sqlite netcat timewarrior xdotool wmctrl xinput
```

**Arch Linux:**
```bash
sudo pacman -S zenity libnotify sqlite gnu-netcat xdotool wmctrl xorg-xinput
yay -S timewarrior
```

## Usage

### Basic Commands

```bash
# Check status
workpulse status

# Start tracking a task
workpulse start "Working on API endpoints"

# Stop tracking
workpulse stop

# Continue previous task
workpulse continue

# Open check-in dialog
workpulse log
```

### Focus Mode

```bash
# Start focus mode (60 minutes)
workpulse focus start 60

# Check focus status
workpulse focus status

# End focus mode early
workpulse focus stop
```

### Reports & Exports

```bash
# Show today's time report
workpulse report today

# Show weekly report
workpulse report week

# Export to CSV
workpulse export csv

# Export all formats
workpulse export all
```

### Daemon Control

```bash
# Start daemon
workpulse daemon start

# Stop daemon
workpulse daemon stop

# Check daemon status
workpulse daemon status

# Restart daemon
workpulse daemon restart
```

### Configuration

```bash
# Show current config
workpulse config show

# Edit config file
workpulse config edit

# Reload configuration
workpulse config reload
```

### Emergency Commands

```bash
# Emergency unlock (if force mode gets stuck)
workpulse unlock

# View logs
workpulse logs 100
```

## Configuration

Configuration file: `~/.config/workpulse/config`

```bash
# Working hours
WORK_START="10:00"
WORK_END="19:30"

# Prompt interval (minutes)
PROMPT_INTERVAL=60

# Force mode triggers
FORCE_MODE_MISSED_THRESHOLD=3
FORCE_MODE_MIN_HOURS=3

# Focus mode limits
FOCUS_MODE_DEFAULT_DURATION=60
FOCUS_MODE_MAX_DURATION=180

# Auto-tagging rules
AUTO_TAGS="meeting:+meeting,code:+dev,review:+review,ops:+ops"

# Export formats
EXPORT_FORMATS="csv,md"

# Logging
LOG_LEVEL="INFO"
```

## File Locations

| Type | Location |
|------|----------|
| Configuration | `~/.config/workpulse/config` |
| Data | `~/.local/share/workpulse/` |
| Logs | `~/.local/share/workpulse/logs/` |
| Exports | `~/.local/share/workpulse/exports/` |
| Database | `~/.local/share/workpulse/prompts.db` |

## Systemd Service

WorkPulse runs as a systemd user service:

```bash
# Enable auto-start
systemctl --user enable workpulse

# Start now
systemctl --user start workpulse

# Check status
systemctl --user status workpulse

# View logs
journalctl --user -u workpulse -f
```

## Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   workpulse     │───▶│   workpulsed     │───▶│   Timewarrior   │
│   (CLI)         │    │   (Daemon)       │    │   (Backend)     │
└─────────────────┘    └────────┬─────────┘    └─────────────────┘
                                │
                    ┌───────────┼───────────┐
                    ▼           ▼           ▼
              ┌──────────┐ ┌──────────┐ ┌──────────┐
              │ Prompter │ │ Reporter │ │ ForceLock│
              └──────────┘ └──────────┘ └──────────┘
```

## Uninstallation

```bash
# Keep configuration and data
./scripts/uninstall.sh

# Remove everything
./scripts/uninstall.sh --purge
```

## Troubleshooting

### Daemon won't start
```bash
# Check for existing process
pgrep -f workpulsed

# Check logs
journalctl --user -u workpulse --no-pager -n 50

# Try running in foreground
workpulsed foreground
```

### Force mode stuck
```bash
# Emergency unlock
workpulse unlock

# Or manually
pkill -f workpulse
rm -f ~/.local/share/workpulse/forcelock.active
```

### Prompts not showing
1. Check if daemon is running: `workpulse daemon status`
2. Verify working hours in config
3. Check if focus mode is active: `workpulse focus status`
4. Ensure DISPLAY is set: `echo $DISPLAY`

## Contributing

Contributions are welcome! Please read our contributing guidelines before submitting PRs.

## License

MIT License - see [LICENSE](LICENSE) for details.

## Acknowledgments

- [Timewarrior](https://timewarrior.net/) - Time tracking backend
- [Zenity](https://wiki.gnome.org/Projects/Zenity) - GTK+ dialogs
- The Linux desktop community

---

Made with ❤️ for professionals who value their time.
