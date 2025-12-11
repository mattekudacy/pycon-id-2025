#!/usr/bin/env python3
"""
Step 5: Complete Interactions
PyCon ID 2025 - Building Modern Terminal UIs with Textual

Learn:
- Event handlers (on_button_pressed)
- Using self.notify() for user feedback
- Querying widgets by ID
- Complete button interactions

Run: python step5.py
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

    async def on_button_pressed(self, event: Button.Pressed):
        """Handle button clicks."""
        if event.button.id == "generate-btn":
            await self.generate()
        elif event.button.id == "clear-btn":
            self.clear()

    async def generate(self):
        """Generate AI response (placeholder for now)."""
        self.notify("Generate clicked!", severity="information")

    def clear(self):
        """Clear output (placeholder for now)."""
        self.notify("Clear clicked!", severity="information")

def main():
    app = MinimalAIDemo()
    app.run()

if __name__ == "__main__":
    main()