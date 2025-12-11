#!/usr/bin/env python3
"""
Textual AI Streaming Observability Dashboard

A live demo showcasing:
- LLM-style token streaming in the terminal
- Real-time observability metrics
- Reactive state management with Textual
- Clean separation of concerns

Press Enter to submit prompts, Esc to cancel, 'l' to toggle logs.
"""

import asyncio
from pathlib import Path

from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Container, Horizontal, VerticalScroll
from textual.widgets import Header, Footer, Static, Button, TextArea
from textual.reactive import reactive

from state import AppState, Status
from ui.widgets import MetricsPanel, LifecyclePanel, StreamingOutput, ActivityLog

# Choose your backend:
USE_OLLAMA = True  # Set to False to use simulator

if USE_OLLAMA:
    from llm.ollama import ollama_stream, is_ollama_available
    from llm.simulator import (
        simulate_analysis_step,
        simulate_context_step,
        simulate_postprocess_step,
    )
else:
    from llm.simulator import (
        simulate_llm_stream,
        simulate_analysis_step,
        simulate_context_step,
        simulate_postprocess_step,
    )


class AIStreamingDashboard(App):
    """
    Main application for AI streaming observability.
    
    Demonstrates:
    - Reactive state management
    - Async background workers
    - Non-blocking UI updates
    - Custom widget composition
    """
    
    CSS_PATH = "styles.tcss"
    
    TITLE = "🤖 AI Streaming Observability Dashboard"
    SUB_TITLE = "Real-time LLM monitoring in the terminal"
    
    BINDINGS = [
        Binding("escape", "cancel", "Cancel", show=True),
        Binding("l", "toggle_logs", "Toggle Logs", show=True),
        Binding("c", "clear_output", "Clear", show=True),
        Binding("t", "toggle_theme", "Theme", show=True),
        Binding("q", "quit", "Quit", show=True),
    ]
    
    # Reactive state
    show_logs = reactive(True)
    is_generating = reactive(False)
    
    def __init__(self):
        super().__init__()
        self.state = AppState()
        self.cancel_flag = False
        self.update_timer = None
    
    def compose(self) -> ComposeResult:
        """Compose the UI layout."""
        yield Header(show_clock=True)
        
        with Horizontal(id="main-container"):
            # Left panel - Prompt input
            with Container(id="left-panel"):
                yield Static("💭 Enter your prompt:", id="prompt-label")
                yield TextArea(
                    id="prompt-input",
                    language="markdown",
                    theme="monokai",
                    show_line_numbers=False,
                )
                
                with Container(id="submit-container"):
                    yield Button("🚀 Generate", id="submit-btn", variant="primary")
                    yield Button("🗑️  Clear", id="clear-btn", variant="default")
            
            # Center panel - Streaming output
            with Container(id="center-panel"):
                yield StreamingOutput(id="output")
            
            # Right panel - Metrics and lifecycle
            with Container(id="right-panel"):
                yield MetricsPanel(id="metrics")
                yield LifecyclePanel(id="lifecycle")
        
        # Bottom panel - Activity log
        with Container(id="log-container"):
            yield ActivityLog(id="activity-log", highlight=True, markup=True)
        
        yield Footer()
    
    def on_mount(self):
        """Initialize the app on mount."""
        # Get widgets
        self.metrics_panel = self.query_one("#metrics", MetricsPanel)
        self.lifecycle_panel = self.query_one("#lifecycle", LifecyclePanel)
        self.output_widget = self.query_one("#output", StreamingOutput)
        self.activity_log = self.query_one("#activity-log", ActivityLog)
        self.prompt_input = self.query_one("#prompt-input", TextArea)
        
        # Initial state
        self.lifecycle_panel.update_steps(self.state.lifecycle_steps)
        self.activity_log.log_info("Dashboard initialized")
        self.activity_log.log_info("Ready to generate AI responses")
        
        # Start metrics update timer
        self.set_interval(0.1, self.update_metrics_display)
    
    def update_metrics_display(self):
        """Update metrics display (called every 100ms)."""
        if self.state.is_generating:
            self.state.metrics.update_elapsed()
            self.metrics_panel.update_from_metrics(self.state.metrics)
    
    def watch_show_logs(self, show: bool):
        """React to show_logs changes."""
        log_container = self.query_one("#log-container")
        if show:
            log_container.remove_class("hidden")
        else:
            log_container.add_class("hidden")
    
    def watch_is_generating(self, generating: bool):
        """React to generation state changes."""
        # Enable/disable input
        self.prompt_input.disabled = generating
        
        # Update button
        submit_btn = self.query_one("#submit-btn", Button)
        if generating:
            submit_btn.label = "⏳ Generating..."
            submit_btn.disabled = True
        else:
            submit_btn.label = "🚀 Generate"
            submit_btn.disabled = False
    
    async def on_button_pressed(self, event: Button.Pressed):
        """Handle button presses."""
        if event.button.id == "submit-btn":
            await self.action_submit()
        elif event.button.id == "clear-btn":
            self.action_clear_output()
    
    async def action_submit(self):
        """Submit prompt and start generation."""
        # Get prompt
        prompt = self.prompt_input.text.strip()
        if not prompt:
            self.activity_log.log_warning("Empty prompt - nothing to generate")
            return
        
        if self.is_generating:
            self.activity_log.log_warning("Already generating - please wait")
            return
        
        # Start generation
        self.activity_log.log_info(f"Prompt submitted: {prompt[:50]}...")
        await self.generate_response(prompt)
    
    async def generate_response(self, prompt: str):
        """
        Main generation workflow.
        
        Demonstrates:
        - Multi-step async workflow
        - State management
        - UI updates during long-running operations
        """
        self.is_generating = True
        self.cancel_flag = False
        self.state.current_prompt = prompt
        self.state.metrics.reset()
        self.state.reset_steps()
        
        # Clear previous output first, then show generating message
        self.output_widget.clear_output()
        self.output_widget.show_generating()
        
        # Small delay to ensure UI updates
        await asyncio.sleep(0.1)
        
        try:
            # Step 1: Analyze prompt
            self.activity_log.log_info("Step 1/4: Analyzing prompt...")
            self.state.advance_step()
            self.lifecycle_panel.update_steps(self.state.lifecycle_steps)
            self.state.metrics.start()
            
            await simulate_analysis_step()
            
            if self.cancel_flag:
                raise asyncio.CancelledError()
            
            # Step 2: Prepare context
            self.activity_log.log_info("Step 2/4: Preparing context...")
            self.state.advance_step()
            self.lifecycle_panel.update_steps(self.state.lifecycle_steps)
            
            await simulate_context_step()
            
            if self.cancel_flag:
                raise asyncio.CancelledError()
            
            # Step 3: Generate response (streaming)
            self.activity_log.log_info("Step 3/4: Generating response...")
            self.state.advance_step()
            self.lifecycle_panel.update_steps(self.state.lifecycle_steps)
            
            token_count = 0
            first_token = True
            
            # Use Ollama or simulator based on configuration
            if USE_OLLAMA:
                stream = ollama_stream(prompt, model="llama3.2")
            else:
                stream = simulate_llm_stream(prompt)
            
            async for token in stream:
                if self.cancel_flag:
                    raise asyncio.CancelledError()
                
                # Record first token
                if first_token:
                    self.state.metrics.record_first_token()
                    self.activity_log.log_success("First token received!")
                    first_token = False
                
                # Update output
                self.output_widget.append_token(token)
                token_count += 1
                self.state.metrics.tokens_generated = token_count
                
                # Update metrics every 10 tokens
                if token_count % 10 == 0:
                    self.state.metrics.update_elapsed()
                    self.metrics_panel.update_from_metrics(self.state.metrics)
            
            if self.cancel_flag:
                raise asyncio.CancelledError()
            
            # Step 4: Post-process
            self.activity_log.log_info("Step 4/4: Post-processing...")
            self.state.advance_step()
            self.lifecycle_panel.update_steps(self.state.lifecycle_steps)
            
            await simulate_postprocess_step()
            
            # Complete
            self.state.metrics.complete()
            self.metrics_panel.update_from_metrics(self.state.metrics)
            
            # Mark final step as complete
            self.state.lifecycle_steps[-1].mark_completed()
            self.lifecycle_panel.update_steps(self.state.lifecycle_steps)
            
            self.activity_log.log_success(
                f"Generation complete! {token_count} tokens in "
                f"{self.state.metrics.elapsed_time:.2f}s "
                f"({self.state.metrics.tokens_per_second:.1f} tok/s)"
            )
            
        except asyncio.CancelledError:
            self.state.metrics.cancel()
            self.metrics_panel.update_from_metrics(self.state.metrics)
            self.activity_log.log_warning("Generation cancelled by user")
            
        except Exception as e:
            self.state.metrics.error()
            self.metrics_panel.update_from_metrics(self.state.metrics)
            self.activity_log.log_error(f"Generation failed: {e}")
            
        finally:
            self.is_generating = False
    
    def action_cancel(self):
        """Cancel ongoing generation."""
        if self.is_generating:
            self.cancel_flag = True
            self.activity_log.log_warning("Cancellation requested...")
    
    def action_toggle_logs(self):
        """Toggle activity log visibility."""
        self.show_logs = not self.show_logs
    
    def action_clear_output(self):
        """Clear output, input, and reset state."""
        self.output_widget.clear_output()
        self.prompt_input.text = ""
        self.state.metrics.reset()
        self.state.reset_steps()
        self.metrics_panel.update_from_metrics(self.state.metrics)
        self.lifecycle_panel.update_steps(self.state.lifecycle_steps)
        self.activity_log.log_info("Output and input cleared")
    
    def action_toggle_theme(self):
        """Toggle between light and dark theme."""
        self.theme = "textual-light" if self.theme == "textual-dark" else "textual-dark"
        self.activity_log.log_info(f"Theme switched to {self.theme}")


def main():
    """Run the dashboard."""
    app = AIStreamingDashboard()
    app.run()


if __name__ == "__main__":
    main()
