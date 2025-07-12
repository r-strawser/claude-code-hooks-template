# Claude Code Hooks Template

A comprehensive hooks system for Claude Code that provides logging, safety features, and session management.

## Features

- 📝 **Session Logging** - All tool usage logged to `logs/sessions/{session-id}/`
- 🛡️ **Safety Guards** - Blocks dangerous commands (rm -rf, .env access)
- 🔊 **Audio Feedback** - Optional TTS notifications (requires API keys)
- 🚀 **Parallel Sessions** - Multiple Claude Code sessions without conflicts
- 📍 **Works Everywhere** - Edit files anywhere, logs stay in project directory

## Prerequisites

Before using this template, ensure you have:

- **Claude Code** - The official Claude CLI tool ([installation guide](https://docs.anthropic.com/en/docs/claude-code/quickstart))
- **Python 3.8+** - Required for running hook scripts
- **uv** - Fast Python package installer (installed during setup)
- **Git** - For version control and cloning the template
- **Unix-like environment** - macOS, Linux, or WSL on Windows

## Quick Start

1. **Clone this template**:
   ```bash
   git clone https://github.com/yourusername/claude-code-hooks-template.git my-project
   cd my-project
   ```

2. **Set up the hooks**:
   ```bash
   # Install uv (if not already installed)
   curl -LsSf https://astral.sh/uv/install.sh | sh
   
   # Make hooks executable
   chmod +x .claude/hooks/*.py
   
   # Create logs directory
   mkdir -p logs/sessions
   
   # Test hooks are working (optional)
   echo '{}' | uv run .claude/hooks/pre_tool_use.py && echo "✅ Hooks working!"
   ```

3. **Test the hooks**:
   ```bash
   # The hooks will activate automatically when using Claude Code
   # Check logs were created:
   ls -la logs/sessions/
   ```

4. **(Optional) Create CLAUDE.md**:
   ```bash
   cp CLAUDE.md.example CLAUDE.md
   # Edit CLAUDE.md with your project-specific instructions
   ```

## What's Included

### Understanding Claude Code Hooks

Hooks are Python scripts that run at specific points during Claude Code's execution. They enable you to extend Claude Code's functionality without modifying its core behavior. Each hook receives event data as JSON via stdin and can perform custom actions.

### Available Hooks

#### 1. **PreToolUse** (`pre_tool_use.py`)
- **Trigger**: Before any tool (Bash, Edit, Write, etc.) is executed
- **Purpose**: Validate and potentially block dangerous operations
- **Features**:
  - Blocks destructive commands (e.g., `rm -rf /`, `dd if=/dev/zero`)
  - Prevents access to sensitive files (`.env`, private keys)
  - Logs all attempted tool usage
  - Can modify or reject tool parameters
- **Use Cases**: Security enforcement, command validation, audit logging

#### 2. **PostToolUse** (`post_tool_use.py`)
- **Trigger**: After a tool completes execution
- **Purpose**: Log results and perform post-processing
- **Features**:
  - Records tool outputs and execution results
  - Captures error messages and exit codes
  - Maintains activity timestamps
  - Can trigger notifications on specific outcomes
- **Use Cases**: Debugging, audit trails, error monitoring

#### 3. **Stop** (`stop.py`)
- **Trigger**: When a Claude Code session ends
- **Purpose**: Cleanup and session finalization
- **Features**:
  - Creates complete session transcript
  - Plays completion sound (optional)
  - Generates session summary
  - Archives logs for future reference
- **Use Cases**: Session archival, time tracking, notifications

#### 4. **Notification** (`notification.py`)
- **Trigger**: When Claude needs user input or attention
- **Purpose**: Alert users to required actions
- **Features**:
  - Desktop notifications (system-dependent)
  - Audio alerts via TTS APIs
  - Custom notification messages
  - Priority-based alerting
- **Use Cases**: Long-running tasks, error alerts, completion notices

#### 5. **SubagentStop** (`subagent_stop.py`)
- **Trigger**: When a subagent completes its task
- **Purpose**: Track nested agent operations
- **Features**:
  - Logs subagent results
  - Tracks execution hierarchy
  - Maintains parent-child relationships
  - Performance metrics
- **Use Cases**: Complex workflows, performance analysis, debugging

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
export ENGINEER_NAME="Your Name"          # Personalized messages
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

## Examples

### Example: Dangerous Command Blocked
```
User: Delete all files in the system
Claude: I'll help you delete files. Let me...
[BLOCKED: Dangerous rm command detected and prevented]
```

### Example: Session Logs
```json
// logs/sessions/{id}/chat.json
{
  "conversation": [
    {
      "role": "user", 
      "content": "Help me refactor this function"
    },
    {
      "role": "assistant",
      "content": "I'll help you refactor...",
      "tool_calls": [...]
    }
  ]
}
```

## Troubleshooting

### Logs not appearing
- Check `uv` is installed: `which uv`
- Verify `.claude/settings.json` exists
- Look for errors in Claude Code output

### Permission errors
- Ensure hooks are executable: `chmod +x .claude/hooks/*.py`
- Check write permissions for logs directory: `ls -la logs/`

### Hook errors
- Hooks output errors to stderr, visible in Claude Code
- Check Python syntax in hook files
- Verify JSON format in settings.json

### "Hook test failed" during setup
- Ensure Python 3.8+ is available
- Try running a hook directly: `uv run .claude/hooks/pre_tool_use.py --version`

## Contributing

Please see our [Contributing Guidelines](CONTRIBUTING.md) for details on how to contribute to this project.

## Resources

### Official Documentation
- [Claude Code Documentation](https://docs.anthropic.com/en/docs/claude-code) - Official Claude Code docs
- [Claude Code Hooks](https://docs.anthropic.com/en/docs/claude-code/hooks) - Detailed hooks documentation
- [Claude Code Settings](https://docs.anthropic.com/en/docs/claude-code/settings) - Configuration and settings reference

### Related Projects
- [Original claude-code-hooks-mastery](https://github.com/disler/claude-code-hooks-mastery) - The original template this project builds upon
- [Claude Code GitHub](https://github.com/anthropics/claude-code) - Official Claude Code repository

### Community Resources
- [Claude Code Issues](https://github.com/anthropics/claude-code/issues) - Report bugs and request features
- [Anthropic Discord](https://discord.gg/anthropic) - Community support and discussions

### Learning Resources
- [Python subprocess documentation](https://docs.python.org/3/library/subprocess.html) - For understanding hook execution
- [JSON Schema](https://json-schema.org/) - For understanding settings.json structure
- [uv Documentation](https://github.com/astral-sh/uv) - Fast Python package installer used by hooks

## Credits

This project is based on the original [claude-code-hooks-mastery](https://github.com/disler/claude-code-hooks-mastery) template by disler, with enhancements added for improved session management, safety features, and logging capabilities.

## License

MIT License - feel free to use this template for any project.