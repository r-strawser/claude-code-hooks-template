# Claude Code Hooks Template

A comprehensive hooks system for Claude Code that provides logging, safety features, and session management.

## Features

- 📝 **Session Logging** - All tool usage logged to `logs/sessions/{session-id}/`
- 🛡️ **Safety Guards** - Blocks dangerous commands (rm -rf, .env access)
- 🔊 **Audio Feedback** - Optional TTS notifications (requires API keys)
- 🚀 **Parallel Sessions** - Multiple Claude Code sessions without conflicts
- 📍 **Works Everywhere** - Edit files anywhere, logs stay in project directory

## Quick Start

1. **Clone this template**:
   ```bash
   git clone https://github.com/yourusername/claude-code-hooks-template.git my-project
   cd my-project
   ```

2. **Install uv** (if not already installed):
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

3. **Test the hooks**:
   ```bash
   # The hooks will activate automatically when using Claude Code
   # Check logs were created:
   ls -la logs/sessions/
   ```

## What's Included

### Hooks
- **PreToolUse** - Validates and blocks dangerous operations
- **PostToolUse** - Logs all tool results
- **Stop** - Creates session transcript, plays completion sound
- **Notification** - Alerts when Claude needs input
- **SubagentStop** - Tracks subagent completion

### Safety Features
- Blocks `rm -rf` and similar destructive commands
- Prevents access to `.env` files (allows `.env.sample`)
- Comprehensive command pattern matching

## Configuration

### Optional Environment Variables

For enhanced audio features, set these in your shell:

```bash
export ELEVENLABS_API_KEY="your-key"      # Premium voice synthesis
export OPENAI_API_KEY="your-key"          # OpenAI TTS
export ANTHROPIC_API_KEY="your-key"       # Anthropic API
export CLAUDE_ENGINEER_NAME="Your Name"   # Personalized messages
```

### Customizing Hooks

Edit `.claude/settings.json` to:
- Add/remove hooks
- Modify permissions
- Change hook commands

## File Structure

```
.claude/
├── hooks/
│   ├── pre_tool_use.py      # Pre-execution validation
│   ├── post_tool_use.py     # Post-execution logging
│   ├── stop.py              # Session completion
│   ├── notification.py      # User notifications
│   └── subagent_stop.py    # Subagent tracking
└── settings.json            # Hook configuration

logs/sessions/{session-id}/  # Created automatically
├── pre_tool_use.json       # Tool usage log
├── post_tool_use.json      # Tool results log
├── chat.json               # Session transcript
└── last-activity           # Timestamp file
```

## Usage

Simply use Claude Code as normal. The hooks run automatically and will:

1. Create a unique session directory for each Claude Code session
2. Log all tool usage and results
3. Block dangerous operations
4. Create a complete transcript when done

### View Logs

```bash
# See all sessions
ls -la logs/sessions/

# View recent activity
for dir in logs/sessions/*/; do 
  echo "$(basename $dir): $(cat $dir/last-activity 2>/dev/null)"
done

# Read a session transcript
cat logs/sessions/{session-id}/chat.json | jq .
```

### Disable Hooks Temporarily

```bash
# Rename settings to disable
mv .claude/settings.json .claude/settings.json.disabled

# Restore to re-enable
mv .claude/settings.json.disabled .claude/settings.json
```

## How It Works

1. **Path Resolution**: Hooks use `Path(__file__)` to find their location, ensuring logs always go to the project directory regardless of where you're editing files

2. **Session Isolation**: Each Claude Code session gets a unique ID and separate log directory

3. **Fast Execution**: Uses `uv run` for minimal overhead

4. **Graceful Failures**: Hooks fail silently to not interrupt Claude Code

## Troubleshooting

### Logs not appearing
- Check `uv` is installed: `which uv`
- Verify `.claude/settings.json` exists
- Look for errors in Claude Code output

### Permission errors
- Ensure hook scripts are executable: `chmod +x .claude/hooks/*.py`
- Check write permissions for logs directory

### Hook errors
- Hooks output errors to stderr, visible in Claude Code
- Check Python syntax in hook files
- Verify JSON format in settings.json

## Contributing

Feel free to submit issues and enhancement requests!

## License

MIT License - feel free to use this template for any project.