#!/usr/bin/env python3
"""
Step 3: Adding Buttons
PyCon ID 2025 - Building Modern Terminal UIs with Textual

Learn:
- Horizontal container for layouts
- Button widgets and variants
- CSS styling for buttons
- Basic event handling structure

Run: python step3.py
"""

from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Static, TextArea
from textual.containers import Container

class MinimalAIDemo(App):
    """Our minimal AI demo application."""

    CSS = """
        #main {
            height: 1fr;
            padding: 1;
        }
        
        #prompt-label {
            height: 1;
            padding: 0 0 1 0;
            color: $text-muted;
        }
        
        #prompt-input {
            height: 6;
            border: solid $primary;
        }
    """
    
    TITLE = "🤖 AI Streaming Demo - PyCon ID 2025"
    
    def compose(self) -> ComposeResult:
        """Build the UI layout."""
        yield Header(show_clock=True)
        # Main container for our content
        with Container(id="main"):
            # Label for the input
            yield Static("💭 Enter your prompt:", id="prompt-label")
            
            # Multi-line text input
            yield TextArea(
                id="prompt-input",
                language="markdown",
                show_line_numbers=False,
            )
        yield Footer()

def main():
    app = MinimalAIDemo()
    app.run()

if __name__ == "__main__":
    main()