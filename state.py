"""
Shared application state using Textual's reactive system.
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional


class Status(Enum):
    """Application status states."""
    IDLE = "Idle"
    RUNNING = "Running"
    COMPLETED = "Completed"
    ERROR = "Error"
    CANCELLED = "Cancelled"


class StepState(Enum):
    """Lifecycle step states."""
    PENDING = "pending"
    ACTIVE = "active"
    COMPLETED = "completed"


@dataclass
class LifecycleStep:
    """Represents a single step in the AI generation lifecycle."""
    name: str
    description: str
    state: StepState = StepState.PENDING
    
    def mark_active(self):
        """Mark this step as currently active."""
        self.state = StepState.ACTIVE
    
    def mark_completed(self):
        """Mark this step as completed."""
        self.state = StepState.COMPLETED
    
    def icon(self) -> str:
        """Return icon based on state."""
        if self.state == StepState.COMPLETED:
            return "✓"
        elif self.state == StepState.ACTIVE:
            return "→"
        else:
            return " "


@dataclass
class Metrics:
    """Observability metrics for AI generation."""
    status: Status = Status.IDLE
    elapsed_time: float = 0.0
    time_to_first_token: Optional[float] = None
    tokens_generated: int = 0
    tokens_per_second: float = 0.0
    start_time: Optional[datetime] = None
    first_token_time: Optional[datetime] = None
    current_step: int = 0
    
    def reset(self):
        """Reset all metrics."""
        self.status = Status.IDLE
        self.elapsed_time = 0.0
        self.time_to_first_token = None
        self.tokens_generated = 0
        self.tokens_per_second = 0.0
        self.start_time = None
        self.first_token_time = None
        self.current_step = 0
    
    def start(self):
        """Mark generation start."""
        self.status = Status.RUNNING
        self.start_time = datetime.now()
    
    def record_first_token(self):
        """Record first token timestamp."""
        if self.first_token_time is None and self.start_time:
            self.first_token_time = datetime.now()
            self.time_to_first_token = (
                self.first_token_time - self.start_time
            ).total_seconds()
    
    def update_elapsed(self):
        """Update elapsed time."""
        if self.start_time:
            self.elapsed_time = (datetime.now() - self.start_time).total_seconds()
            
            # Calculate tokens per second
            if self.elapsed_time > 0:
                self.tokens_per_second = self.tokens_generated / self.elapsed_time
    
    def complete(self):
        """Mark generation as completed."""
        self.status = Status.COMPLETED
        self.update_elapsed()
    
    def error(self):
        """Mark generation as errored."""
        self.status = Status.ERROR
        self.update_elapsed()
    
    def cancel(self):
        """Mark generation as cancelled."""
        self.status = Status.CANCELLED
        self.update_elapsed()


@dataclass
class AppState:
    """Central application state."""
    metrics: Metrics = field(default_factory=Metrics)
    lifecycle_steps: list[LifecycleStep] = field(default_factory=list)
    output_text: str = ""
    current_prompt: str = ""
    is_generating: bool = False
    
    def __post_init__(self):
        """Initialize lifecycle steps."""
        self.lifecycle_steps = [
            LifecycleStep("analyze", "Analyze prompt"),
            LifecycleStep("context", "Prepare context"),
            LifecycleStep("generate", "Generate response"),
            LifecycleStep("postprocess", "Post-process"),
        ]
    
    def reset_steps(self):
        """Reset all steps to pending."""
        for step in self.lifecycle_steps:
            step.state = StepState.PENDING
    
    def advance_step(self):
        """Move to next step in lifecycle."""
        current_idx = self.metrics.current_step
        
        # Mark current step as completed
        if current_idx > 0:
            self.lifecycle_steps[current_idx - 1].mark_completed()
        
        # Mark next step as active
        if current_idx < len(self.lifecycle_steps):
            self.lifecycle_steps[current_idx].mark_active()
            self.metrics.current_step += 1
