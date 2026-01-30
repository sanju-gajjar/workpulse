# WorkPulse Reminder System v2.0

## Overview
WorkPulse now features a **user-controlled, customizable reminder system** that eliminates the need for systemd services. Reminders only appear when the workpulse daemon is actively running.

## Key Changes

### 1. **No More Systemd Dependency**
Previously, you needed to run:
```bash
systemctl --user daemon-reload
systemctl --user enable --now workpulse
```

**Now you simply run:**
```bash
workpulse daemon start
```

The daemon runs as a **user process** in the foreground or background. Reminders only appear when it's running.

---

### 2. **Dynamic Reminder Intervals**
Instead of hardcoded hourly reminders, **you now choose the interval after each check-in**.

#### Available Options:
- **Every 30 minutes** (Quick mode - for intense focus sessions)
- **Every 1 hour** (Standard - default)
- **Every 2 hours** (Extended - for deep work)
- **Every 4 hours** (Long - minimal interruption)
- **Custom** - Enter any interval from 5-480 minutes

#### How It Works:
1. Daemon checks if current time >= next prompt time
2. If yes, shows the prompt dialog
3. After you respond, you're asked "When should I remind you next?"
4. The daemon calculates: `next_prompt = now + your_choice_minutes`
5. Returns to regular checks

---

### 3. **Integration with Mascot Widget**
The widget now displays:
- **Next Reminder Time**: Countdown (e.g., "45m", "1h 20m")
- **Reminder Frequency**: Current interval (e.g., "Every 2h")

You can check your next reminder anytime:
```bash
workpulse reminder show
```

---

### 4. **Easy Reminder Adjustment**
Change your reminder frequency at any time (without waiting for the next prompt):
```bash
workpulse reminder set
```

This opens the frequency selection dialog immediately.

---

## Technical Implementation

### Files Modified:

1. **`src/lib/prompt.sh`**
   - Added `show_frequency_dialog()` - Interactive frequency picker
   - Modified `do_prompt()` - Asks for next interval after response
   - Stores `next_prompt_timestamp` and `prompt_frequency_minutes` in state

2. **`src/workpulsed`**
   - Changed `check_prompt_due()` - Dynamic timestamp-based checking instead of hourly cron
   - Added `check_long_running_task()` - Reminds users about tasks >1 hour old
   - Added `do_long_running_prompt()` - Dialog for long-running tasks

3. **`src/lib/common.sh`**
   - Added `get_next_prompt_countdown()` - Human-readable time until next prompt
   - Added `get_prompt_frequency_readable()` - Format frequency for display

4. **`src/workpulse`** (CLI)
   - Added `cmd_reminder()` - Command to show/set reminder frequency
   - New commands: `workpulse reminder show` and `workpulse reminder set`
   - Updated help text to document systemd-free workflow

---

## Usage Examples

### Start/Stop Daemon (No Systemd Needed)
```bash
# Start daemon
workpulse daemon start

# Stop daemon
workpulse daemon stop

# Check if running
workpulse daemon status
```

### Manage Reminders
```bash
# Show next reminder and frequency
workpulse reminder show

# Change reminder frequency (interactive dialog)
workpulse reminder set
```

### State Information
Internally stored in `~/.local/share/workpulse/state.json`:
```json
{
  "next_prompt_timestamp": "1705426800",
  "prompt_frequency_minutes": "60",
  "last_prompt_timestamp": "1705423200"
}
```

---

## Configuration

### Config File
`~/.config/workpulse/config` - Define default working hours, notifications, etc.

### Daemon Behavior
The daemon:
- Runs every 60 seconds (configurable loop interval)
- Checks if current time >= next prompt time
- If yes and in working hours → shows prompt
- After response → calculates next reminder based on user choice
- Runs indefinitely until `workpulse daemon stop` is called

---

## Automatic Long-Running Task Prompt

If a task runs >1 hour without check-in, the daemon will ask:
**"Your task 'X' has been running for 1h 30m. Continue or stop?"**

- **Continue**: Task keeps running, no prompt until next interval
- **Stop & Log**: Stops task and opens logging dialog immediately

This prevents forgotten long-running tasks.

---

## Migration from Old System

If you were using systemd:

**Before:**
```bash
systemctl --user daemon-reload
systemctl --user enable --now workpulse
# Running as systemd service
```

**After:**
```bash
workpulse daemon start
# Running as user daemon (can be killed/stopped easily)
```

You can disable the systemd service:
```bash
systemctl --user disable workpulse
```

---

## Mascot Widget Integration

The mascot widget (if running) will show:
- 🔔 Next reminder countdown in tooltip
- 📊 Current task and time spent
- Synced frequency with daemon

Example widget display:
```
[WIDGET: 45m to next check-in]
Task: "API Development"
Time: 1h 30m
Frequency: Every 1h (next in 45m)
```

---

## Troubleshooting

### Reminders not appearing?
1. Check if daemon is running: `workpulse daemon status`
2. Check logs: `workpulse logs`
3. Verify it's within working hours (default 9-17)

### Want to change frequency?
```bash
workpulse reminder set
```

### Reset to defaults?
```bash
rm ~/.local/share/workpulse/state.json
workpulse daemon restart
```

---

## Benefits

✅ **No systemd required** - Run anytime, stop anytime  
✅ **User control** - Choose frequency after each check-in  
✅ **Flexible** - 5-480 minute intervals supported  
✅ **Visual feedback** - See countdown in widget  
✅ **Prevents task abandonment** - Long-running task checks  
✅ **Simple setup** - Just `workpulse daemon start`  

---

## Future Enhancements

- [ ] Save preferred frequencies for specific tasks
- [ ] Dynamic frequency based on context (time of day, task type)
- [ ] Weekend/holiday exemptions
- [ ] Reminder snooze (15m postpone)
- [ ] Custom notification sounds per frequency
- [ ] Frequency trends visualization

