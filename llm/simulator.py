"""
Simulated LLM backend for safe, deterministic demos.
"""

import asyncio
import random
from typing import AsyncGenerator


# Sample responses for different prompt types
SAMPLE_RESPONSES = {
    "default": """The future of AI is incredibly exciting. We're seeing breakthroughs in natural language processing, computer vision, and reinforcement learning. These technologies are transforming industries from healthcare to finance, enabling new possibilities that were once science fiction.

However, with great power comes great responsibility. We must ensure AI systems are developed ethically, with proper safeguards against bias and misuse. The goal should be augmenting human intelligence, not replacing it entirely.

Terminal-based interfaces like this one show that powerful AI tools don't need complex GUIs. Sometimes the simplest interface is the most effective.""",
    
    "code": """Here's a simple Python function to calculate Fibonacci numbers:

```python
def fibonacci(n: int) -> int:
    \"\"\"Calculate the nth Fibonacci number.\"\"\"
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

# More efficient iterative version
def fibonacci_iter(n: int) -> int:
    \"\"\"Calculate the nth Fibonacci number iteratively.\"\"\"
    if n <= 1:
        return n
    
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b
```

The recursive version is elegant but inefficient for large n. The iterative version is O(n) time and O(1) space.""",
    
    "explain": """Let me break this down step by step:

1. **First**, we need to understand the problem domain. What exactly are we trying to solve?

2. **Second**, we analyze the constraints and requirements. This helps us choose the right approach.

3. **Third**, we design a solution that balances simplicity with effectiveness. Over-engineering is a common pitfall.

4. **Finally**, we implement and test iteratively, refining as we go.

The key insight here is that great solutions often come from deeply understanding the problem, not just jumping to implementation.""",
    
    "short": "That's a great question! In essence, it comes down to finding the right balance between complexity and usability. The best tools are often the simplest ones.",
}


def get_response_for_prompt(prompt: str) -> str:
    """Select appropriate response based on prompt content."""
    prompt_lower = prompt.lower()
    
    if any(word in prompt_lower for word in ["code", "python", "function", "program"]):
        return SAMPLE_RESPONSES["code"]
    elif any(word in prompt_lower for word in ["explain", "how", "why", "what"]):
        return SAMPLE_RESPONSES["explain"]
    elif len(prompt) < 20:
        return SAMPLE_RESPONSES["short"]
    else:
        return SAMPLE_RESPONSES["default"]


async def simulate_llm_stream(
    prompt: str,
    delay_range: tuple[float, float] = (0.02, 0.08)
) -> AsyncGenerator[str, None]:
    """
    Simulate LLM token streaming with realistic delays.
    
    Args:
        prompt: The user's input prompt
        delay_range: Min/max delay between tokens (seconds)
    
    Yields:
        Individual tokens (words or characters)
    """
    # Get appropriate response
    response = get_response_for_prompt(prompt)
    
    # Split into tokens (words + punctuation)
    words = response.split()
    
    for i, word in enumerate(words):
        # Add space before word (except first)
        if i > 0:
            yield " "
            await asyncio.sleep(random.uniform(*delay_range) / 2)
        
        # Stream word character by character (occasionally)
        # This makes it feel more like real streaming
        if len(word) > 8 and random.random() > 0.7:
            for char in word:
                yield char
                await asyncio.sleep(random.uniform(*delay_range) / 3)
        else:
            yield word
            await asyncio.sleep(random.uniform(*delay_range))


async def simulate_analysis_step(duration: float = 0.5):
    """Simulate the 'analyze prompt' step."""
    await asyncio.sleep(duration)


async def simulate_context_step(duration: float = 0.3):
    """Simulate the 'prepare context' step."""
    await asyncio.sleep(duration)


async def simulate_postprocess_step(duration: float = 0.2):
    """Simulate the 'post-process' step."""
    await asyncio.sleep(duration)
