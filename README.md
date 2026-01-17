# 🎯 Building Modern Terminal UIs with Textual
## PyCon ID 2025 - Workshop Materials

A step-by-step guide to building beautiful, modern terminal user interfaces (TUIs) with [Textual](https://textual.textualize.io/). Learn how to create a professional AI streaming interface from scratch in under 100 lines of Python.

**From this talk, you'll learn:**
- Modern TUI development patterns
- Reactive programming in the terminal
- Real-time streaming interfaces
- AI/LLM integration with local models

---

## 🎬 What's Included

This repository contains:

- **📖 TALK_GUIDE.md** - Complete presentation guide with talking points
- **🎨 Demo Application** - Full-featured AI streaming interface (`demo_minimal.py`)
- **📚 Step-by-Step Examples** - Progressive builds from basic to advanced (`step1.py` → `step5.py`)
- **🏗️ Modular Components** - Reusable widgets and LLM backends
- **🎯 Production App** - Advanced version with full observability (`app.py`)

---

## 🚀 Quick Start

### Prerequisites

- Python 3.10 or higher
- Terminal with 256 color support (most modern terminals)
- [Ollama](https://ollama.ai/) (optional - for real LLM integration)

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/pycon-id-2025.git
cd pycon-id-2025

# Install dependencies
pip install -e .

# Or with uv (recommended)
uv pip install -e .
```

### Running the Demos

**Minimal AI Streaming Demo:**
```bash
python demo_minimal.py
```

**Step-by-Step Examples:**
```bash
python step1.py  # Basic app structure
python step2.py  # Add input box
python step3.py  # Add buttons
python step4.py  # Add response window
python step5.py  # Complete with interactions
```

**Full Production App:**
```bash
python app.py
```

---

## 📁 Project Structure

```
pycon-id-2025/
├── README.md                 # This file
├── TALK_GUIDE.md            # Complete presentation guide
├── pyproject.toml           # Dependencies and project config
│
├── demo_minimal.py          # Main demo - AI streaming interface
├── step1.py                 # Step 1: Basic app canvas
├── step2.py                 # Step 2: Add input box
├── step3.py                 # Step 3: Add buttons
├── step4.py                 # Step 4: Add response window
├── step5.py                 # Step 5: Wire up interactions
│
├── app.py                   # Advanced: Full observability dashboard
├── state.py                 # State management for advanced app
├── styles.tcss              # CSS styling for advanced app
│
├── llm/
│   ├── __init__.py
│   ├── ollama.py           # Ollama integration (real LLM)
│   └── simulator.py        # Simulated LLM (for demos)
│
└── ui/
    ├── __init__.py
    └── widgets.py          # Custom widgets (metrics, lifecycle, etc.)
```

---

## � Learning Path

### For First-Time Learners

Follow the step-by-step examples in order:

**1. `step1.py` - The Canvas**
- Basic Textual app structure
- Header and Footer widgets
- Understanding `compose()` method

**2. `step2.py` - Input Box**
- Containers and layout
- TextArea widget
- CSS styling basics

**3. `step3.py` - Buttons**
- Horizontal layouts
- Button widgets and variants
- Event handlers

**4. `step4.py` - Response Window**
- Custom scrollable widgets
- Rich Text rendering
- Auto-scrolling

**5. `step5.py` - Complete Interactions**
- Connecting all pieces
- Notifications and feedback
- Full working demo

**6. `demo_minimal.py` - AI Streaming**
- Async generators
- Real-time token streaming
- Markdown rendering
- Ollama integration

**7. `app.py` - Production Features**
- Advanced state management
- Metrics and observability
- Lifecycle visualization
- Activity logging

---

## 🎮 Demo Features

### Minimal Demo (`demo_minimal.py`)

**Interface:**
- Multi-line prompt input with markdown support
- Generate and Clear buttons
- Streaming markdown output window
- Real-time token-by-token rendering

**Keyboard Shortcuts:**
- `Escape` - Cancel ongoing generation
- `Ctrl+C` - Quit application

### Advanced Demo (`app.py`)

**Additional Features:**
- 📊 Real-time metrics (latency, throughput, token count)
- 🔄 Lifecycle step visualization
- 📝 Activity log with timestamps
- ⌨️ Rich keyboard shortcuts
- 🎨 Theme toggling
- 🎯 Full observability dashboard

**Keyboard Shortcuts:**
- `Enter` - Submit and generate
- `Escape` - Cancel generation
- `l` - Toggle activity log
- `c` - Clear output
- `t` - Toggle theme
- `q` - Quit application

---

## 🧠 Using Real LLMs with Ollama

The demos work with a built-in simulator by default, but you can easily switch to real LLMs.

### Setup Ollama

**1. Install Ollama:**
- Visit [ollama.ai](https://ollama.ai/)
- Download and install for your platform

**2. Pull a model:**
```bash
ollama pull llama3.2
# or
ollama pull mistral
ollama pull codellama
```

**3. Verify it's running:**
```bash
ollama list  # Should show your models
```

### Switch to Ollama

The `demo_minimal.py` is already configured to use Ollama! Just make sure:
- Ollama is installed
- A model is pulled
- Ollama service is running

If you encounter issues, the app will show an error message with instructions.

---

## 🎯 For Presenters

### Giving This Talk

Check out **[TALK_GUIDE.md](TALK_GUIDE.md)** for:
- Complete 40-minute presentation outline
- Slide content and talking points
- Live demo script with timing
- Technical setup checklist
- Q&A preparation
- Backup plans

### Tips for Live Coding

1. **Increase terminal font size** (18-24pt)
2. **Use a dark theme** with good contrast
3. **Disable notifications** during presentation
4. **Test Ollama** before the talk
5. **Have screenshots** as backup
6. **Practice the flow** 3+ times

### Suggested Flow

```
1. Show working demo first (wow factor)        - 2 min
2. Explain Textual concepts                    - 8 min
3. Build step-by-step (step1 → step5)          - 15 min
4. Show AI integration (demo_minimal.py)       - 10 min
5. Advanced features (app.py)                  - 3 min
6. Q&A                                         - 2 min
```

---

## 💡 Key Concepts Demonstrated

### 1. Declarative UI Composition
```python
def compose(self) -> ComposeResult:
    """Build UI like React components"""
    yield Header(show_clock=True)
    with Container(id="main"):
        yield TextArea(id="prompt-input")
        yield Button("Generate", variant="primary")
    yield Footer()
```

### 2. Reactive Programming
```python
class MetricsPanel(Static):
    elapsed_time = reactive(0.0)  # Auto-updates UI!
    
    def watch_elapsed_time(self, time: float):
        """Called automatically when elapsed_time changes"""
        self.update(f"Time: {time:.2f}s")
```

### 3. Async Event Handling
```python
async def on_button_pressed(self, event: Button.Pressed):
    """Non-blocking async handlers"""
    async for token in ollama_stream(prompt):
        self.output.append_token(token)
        # UI stays responsive during streaming!
```

### 4. CSS-Like Styling
```css
Button {
    background: $primary;
    margin: 1;
    min-width: 20;
}

Button:hover {
    background: $accent;
}
```

---

## 🛠️ Customization

### Adjust Streaming Speed

Edit `llm/simulator.py`:
```python
async def simulate_llm_stream(prompt, delay_range=(0.01, 0.05)):
    # Increase delay for slower streaming
    # Decrease for faster streaming
```

### Change Models

Edit `demo_minimal.py`:
```python
async for token in ollama_stream(
    prompt, 
    model="mistral"  # Change model here
):
```

### Modify Responses

Edit `llm/simulator.py` to add custom responses:
```python
SAMPLE_RESPONSES = {
    "your keyword": "Your custom response here...",
}
```

---

## 🔧 Troubleshooting

**Problem: Buttons don't work**
- Check you're using `self.notify()` instead of `print()`
- Textual captures stdout, so print won't show

**Problem: Streaming doesn't work**
- Verify Ollama is running: `ollama serve`
- Check model is pulled: `ollama list`
- Review error messages in the app

**Problem: UI doesn't update during generation**
- Ensure you're using `await asyncio.sleep(0)` in loops
- Check reactive properties are properly defined

**Problem: Markdown not rendering**
- Make sure you're using `Markdown` widget, not `Static`
- Verify accumulated text is being updated correctly

**Problem: Terminal looks weird**
- Try a terminal with 256 color support
- Use Windows Terminal on Windows
- iTerm2 or Terminal.app on macOS work great

---

## 📚 Learn More

### Textual Resources
- [Official Documentation](https://textual.textualize.io/)
- [Widget Gallery](https://textual.textualize.io/widget_gallery/)
- [Textual Examples](https://github.com/Textualize/textual/tree/main/examples)
- [Discord Community](https://discord.gg/Enf6Z3qhVr)

### Example Projects Using Textual
- **Posting** - API client like Postman
- **Dolphie** - MySQL monitoring tool
- **Trogon** - Auto-generate TUIs from Click CLIs
- **textual-paint** - MS Paint clone in the terminal

### Python Async Resources
- [Real Python - Async IO](https://realpython.com/async-io-python/)
- [Python AsyncIO Docs](https://docs.python.org/3/library/asyncio.html)

---

## 📞 Questions?

If you have questions about the code or Textual:
- Check out the [Textual Documentation](https://textual.textualize.io/)
- Join the [Textual Discord Community](https://discord.gg/Enf6Z3qhVr)
- Review the [TALK_GUIDE.md](TALK_GUIDE.md) for detailed explanations

---

**Built with ❤️ for PyCon ID 2025**

*Happy building! 🚀*

---

This line was added by an AI via Pull Request.
