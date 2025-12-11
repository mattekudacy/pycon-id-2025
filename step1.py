#!/usr/bin/env python3
"""
Step 1: Basic App Canvas
PyCon ID 2025 - Building Modern Terminal UIs with Textual

Learn:
- Basic Textual app structure
- App class and compose() method
- Built-in Header and Footer widgets
- Running a minimal TUI application

Run: python step1.py
"""

from textual.app import App, ComposeResult
from textual.widgets import Header, Footer

class MinimalAIDemo(App):
    """Our minimal AI demo application."""
    
    TITLE = "🤖 AI Streaming Demo - PyCon ID 2025"
    
    def compose(self) -> ComposeResult:
        """Build the UI layout."""
        yield Header(show_clock=True)
        # We'll add widgets here
        yield Footer()

def main():
    app = MinimalAIDemo()
    app.run()

if __name__ == "__main__":
    main()