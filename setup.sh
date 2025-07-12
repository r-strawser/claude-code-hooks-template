#!/bin/bash
# Claude Code Hooks Setup Script

echo "🚀 Setting up Claude Code Hooks..."

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    echo "📦 Installing uv..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    
    # Add to PATH for current session
    export PATH="$HOME/.cargo/bin:$PATH"
    
    echo "✅ uv installed successfully"
else
    echo "✅ uv is already installed"
fi

# Ensure hooks are executable
echo "🔧 Making hooks executable..."
chmod +x .claude/hooks/*.py

# Create logs directory structure
echo "📁 Creating logs directory..."
mkdir -p logs/sessions

# Test hook execution
echo "🧪 Testing hook setup..."
if uv run .claude/hooks/pre_tool_use.py --version &> /dev/null; then
    echo "✅ Hooks are working correctly"
else
    echo "⚠️  Warning: Hook test failed. Please check your Python installation."
fi

echo ""
echo "✨ Setup complete! Claude Code hooks are ready to use."
echo ""
echo "Optional: Set environment variables for enhanced features:"
echo "  export ELEVENLABS_API_KEY='your-key'     # For premium TTS"
echo "  export OPENAI_API_KEY='your-key'         # For OpenAI TTS"
echo "  export ANTHROPIC_API_KEY='your-key'      # For completion messages"
echo "  export CLAUDE_ENGINEER_NAME='Your Name'  # For personalized messages"
echo ""
echo "To test: Use Claude Code normally - hooks will activate automatically"