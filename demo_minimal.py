#!/usr/bin/env python3
"""
Minimal AI Streaming Demo - PyCon ID 2025

A clean, focused demo showing LLM-style streaming in the terminal.
Perfect for live presentations.
"""

import asyncio
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Container, Horizontal, VerticalScroll
from textual.widgets import Header, Footer, Static, Button, TextArea, Markdown
from rich.text import Text

from llm.ollama import ollama_stream


class StreamingOutput(VerticalScroll):
    """Scrollable output widget for AI responses."""
    
    BORDER_TITLE = "💬 AI Response"
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.content_widget = Markdown("")
        self.is_showing_generating = False
        self.accumulated_text = ""
    
    def compose(self):
        yield self.content_widget
    
    def append_token(self, token: str):
        """Append a token and auto-scroll."""
        # If we're showing the generating message, clear it first
        if self.is_showing_generating:
            self.accumulated_text = ""
            self.is_showing_generating = False
        
        # Accumulate the markdown text
        self.accumulated_text += token
        
        # Update the markdown widget with the full accumulated text
        self.content_widget.update(self.accumulated_text)
        self.scroll_end(animate=False)
    
    def show_generating(self):
        """Show generating message."""
        self.is_showing_generating = True
        self.accumulated_text = ""
        self.content_widget.update("🔄 **Generating response...**\n\nPlease wait while the AI thinks...")
    
    def clear_output(self):
        """Clear all output."""
        self.is_showing_generating = False
        self.accumulated_text = ""
        self.content_widget.update(
            "*AI response will appear here...*\n\n"
            "Enter a prompt and click Generate."
        )


class MinimalAIDemo(App):
    """
    Minimal AI Streaming Demo
    
    Shows the core concept: prompt → streaming response
    """
    
    CSS = """
    Screen {
        background: $surface;
    }
    
    #header {
        height: 3;
        background: $primary;
        color: $text;
        content-align: center middle;
        text-style: bold;
    }
    
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
        margin: 0 0 1 0;
    }
    
    #buttons {
        height: auto;
        align: center middle;
    }
    
    Button {
        margin: 1;
        min-width: 20;
    }
    
    StreamingOutput {
        height: 1fr;
        border: solid $primary;
        background: $surface;
        margin: 1 0 0 0;
    }
    
    StreamingOutput > Static {
        padding: 1;
    }
    """
    
    TITLE = "🤖 AI Streaming Demo - PyCon ID 2025"
    
    BINDINGS = [
        Binding("escape", "cancel", "Cancel", show=True),
        Binding("ctrl+c", "quit", "Quit", show=False),
    ]
    
    def __init__(self):
        super().__init__()
        self.is_generating = False
        self.cancel_flag = False
    
    def compose(self) -> ComposeResult:
        """Compose the minimal UI."""
        yield Header(show_clock=True)
        
        with Container(id="main"):
            yield Static("💭 Enter your prompt:", id="prompt-label")
            yield TextArea(
                id="prompt-input",
                language="markdown",
                show_line_numbers=False,
            )
            
            with Horizontal(id="buttons"):
                yield Button("🚀 Generate", id="generate-btn", variant="primary")
                yield Button("🗑️  Clear", id="clear-btn", variant="default")
            
            yield StreamingOutput(id="output")
        
        yield Footer()
    
    def on_mount(self):
        """Initialize on mount."""
        self.output = self.query_one("#output", StreamingOutput)
        self.prompt_input = self.query_one("#prompt-input", TextArea)
        self.output.clear_output()
    
    async def on_button_pressed(self, event: Button.Pressed):
        """Handle button clicks."""
        if event.button.id == "generate-btn":
            await self.generate()
        elif event.button.id == "clear-btn":
            self.clear()
    
    async def generate(self):
        """Generate AI response with streaming."""
        # Get prompt
        prompt = self.prompt_input.text.strip()
        if not prompt:
            return
        
        if self.is_generating:
            return
        
        # Start generation
        self.is_generating = True
        self.cancel_flag = False
        self.prompt_input.disabled = True
        
        # Update button
        btn = self.query_one("#generate-btn", Button)
        btn.label = "⏳ Generating..."
        btn.disabled = True
        
        # Clear previous output first, then show generating message
        self.output.clear_output()
        self.output.show_generating()
        
        # Small delay to ensure UI updates before Ollama call
        await asyncio.sleep(0.1)
        
        try:
            # Stream tokens from Ollama
            async for token in ollama_stream(prompt, model="llama3.2"):
                if self.cancel_flag:
                    raise asyncio.CancelledError()
                
                self.output.append_token(token)
            
        except asyncio.CancelledError:
            self.output.append_token("\n\n[Cancelled]")
            
        except Exception as e:
            self.output.append_token(f"\n\n[Error: {e}]")
            
        finally:
            # Reset state
            self.is_generating = False
            self.prompt_input.disabled = False
            btn.label = "🚀 Generate"
            btn.disabled = False
    
    def clear(self):
        """Clear output and input."""
        self.output.clear_output()
        self.prompt_input.text = ""
    
    def action_cancel(self):
        """Cancel generation."""
        if self.is_generating:
            self.cancel_flag = True


def main():
    """Run the minimal demo."""
    app = MinimalAIDemo()
    app.run()


if __name__ == "__main__":
    main()
