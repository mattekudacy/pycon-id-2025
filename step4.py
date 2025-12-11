#!/usr/bin/env python3
"""
Step 4: Adding Response Window
PyCon ID 2025 - Building Modern Terminal UIs with Textual

Learn:
- Custom scrollable widgets
- VerticalScroll container
- Rich Text rendering
- Auto-scrolling to bottom
- Widget composition

Run: python step4.py
"""

from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Static, TextArea, Button
from textual.containers import Container, Horizontal

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
        #buttons {
            height: auto;
            align: center middle;
        }

        Button {
            margin: 1;
            min-width: 20;
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
            # Button container (horizontal layout)
            with Horizontal(id="buttons"):
                yield Button("🚀 Generate", id="generate-btn", variant="primary")
                yield Button("🗑️  Clear", id="clear-btn", variant="default")

        yield Footer()

def main():
    app = MinimalAIDemo()
    app.run()

if __name__ == "__main__":
    main()