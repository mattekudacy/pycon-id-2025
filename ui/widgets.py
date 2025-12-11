"""
Custom Textual widgets for the AI dashboard.
"""

from datetime import datetime
from rich.text import Text
from rich.panel import Panel
from rich.table import Table as RichTable
from textual.widgets import Static, RichLog, Markdown
from textual.reactive import reactive
from textual.containers import VerticalScroll

from state import Metrics, LifecycleStep, Status, StepState


class MetricsPanel(Static):
    """
    Live-updating metrics display.
    
    Demonstrates: Reactive state updates, Rich rendering
    """
    
    # Reactive properties - automatically trigger re-render
    elapsed_time = reactive(0.0)
    time_to_first_token = reactive(None)
    tokens_generated = reactive(0)
    tokens_per_second = reactive(0.0)
    status = reactive(Status.IDLE)
    
    def update_from_metrics(self, metrics: Metrics):
        """Update all reactive properties from Metrics object."""
        self.elapsed_time = metrics.elapsed_time
        self.time_to_first_token = metrics.time_to_first_token
        self.tokens_generated = metrics.tokens_generated
        self.tokens_per_second = metrics.tokens_per_second
        self.status = metrics.status
    
    def render(self) -> Panel:
        """Render the metrics panel."""
        table = RichTable.grid(padding=(0, 2))
        table.add_column(style="cyan", justify="left")
        table.add_column(style="white", justify="right")
        
        # Status with color coding
        status_color = {
            Status.IDLE: "dim",
            Status.RUNNING: "yellow",
            Status.COMPLETED: "green",
            Status.ERROR: "red",
            Status.CANCELLED: "orange1",
        }.get(self.status, "white")
        
        table.add_row("Status:", f"[{status_color}]{self.status.value}[/{status_color}]")
        table.add_row("", "")
        
        # Timing metrics
        table.add_row(
            "Elapsed:",
            f"{self.elapsed_time:.2f}s" if self.elapsed_time else "0.00s"
        )
        
        if self.time_to_first_token is not None:
            table.add_row(
                "First Token:",
                f"{self.time_to_first_token:.2f}s"
            )
        else:
            table.add_row("First Token:", "[dim]waiting...[/dim]")
        
        table.add_row("", "")
        
        # Token metrics
        table.add_row("Tokens:", str(self.tokens_generated))
        table.add_row(
            "Tokens/sec:",
            f"{self.tokens_per_second:.1f}" if self.tokens_per_second else "0.0"
        )
        
        return Panel(
            table,
            title="📊 Metrics",
            border_style="cyan",
            padding=(1, 2)
        )


class LifecyclePanel(Static):
    """
    Displays AI generation lifecycle steps.
    
    Demonstrates: Dynamic state visualization
    """
    
    steps = reactive([])
    
    def update_steps(self, steps: list[LifecycleStep]):
        """Update the lifecycle steps."""
        self.steps = steps.copy()
        self.refresh()
    
    def render(self) -> Panel:
        """Render the lifecycle steps."""
        text = Text()
        
        if not self.steps:
            text.append("No active workflow", style="dim")
        else:
            for step in self.steps:
                icon = step.icon()
                
                # Style based on state
                if step.state == StepState.COMPLETED:
                    style = "green"
                elif step.state == StepState.ACTIVE:
                    style = "yellow bold"
                else:
                    style = "dim"
                
                text.append(f"[{icon}] ", style=style)
                text.append(f"{step.description}\n", style=style)
        
        return Panel(
            text,
            title="🔄 Lifecycle",
            border_style="magenta",
            padding=(1, 2)
        )


class StreamingOutput(VerticalScroll):
    """
    Displays streaming LLM output with auto-scroll.
    
    Demonstrates: Incremental rendering, scrolling, markdown rendering
    """
    
    BORDER_TITLE = "💬 AI Response"
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.content_widget = Markdown("")
        self.is_showing_generating = False
        self.accumulated_text = ""
    
    def compose(self):
        """Compose the scrollable output."""
        yield self.content_widget
    
    def append_token(self, token: str):
        """Append a token to the output."""
        # If we're showing the generating message, clear it first
        if self.is_showing_generating:
            self.accumulated_text = ""
            self.is_showing_generating = False
        
        # Accumulate the markdown text
        self.accumulated_text += token
        
        # Update the markdown widget with the full accumulated text
        self.content_widget.update(self.accumulated_text)
        # Auto-scroll to bottom
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
            "*Output will appear here...*\n\n"
            "Enter a prompt and press Enter to start generating."
        )


class ActivityLog(RichLog):
    """
    Scrollable activity log for system events.
    
    Demonstrates: Rich logging, auto-scroll
    """
    
    def log_info(self, message: str):
        """Log an info message."""
        timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        self.write(f"[dim]{timestamp}[/dim] [cyan]INFO[/cyan]  {message}")
    
    def log_warning(self, message: str):
        """Log a warning message."""
        timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        self.write(f"[dim]{timestamp}[/dim] [yellow]WARN[/yellow]  {message}")
    
    def log_error(self, message: str):
        """Log an error message."""
        timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        self.write(f"[dim]{timestamp}[/dim] [red]ERROR[/red] {message}")
    
    def log_success(self, message: str):
        """Log a success message."""
        timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        self.write(f"[dim]{timestamp}[/dim] [green]✓[/green]     {message}")
