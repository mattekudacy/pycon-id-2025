#!/usr/bin/env python3
"""
Step 2: Adding Input Box
PyCon ID 2025 - Building Modern Terminal UIs with Textual

Learn:
- Container widget for grouping
- Static widget for labels
- TextArea for multi-line input
- Basic CSS styling
- Using IDs to reference widgets

Run: python step2.py
"""

from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Static, TextArea
from textual.containers import Container

class MinimalAIDemo(App):
    """Our minimal AI demo application."""
    
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