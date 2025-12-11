"""
Ollama backend for real LLM streaming (optional).
"""

import asyncio
from typing import AsyncGenerator, Optional

try:
    import ollama
    OLLAMA_AVAILABLE = True
except ImportError:
    OLLAMA_AVAILABLE = False


async def ollama_stream(
    prompt: str,
    model: str = "llama2",
    system_prompt: Optional[str] = None
) -> AsyncGenerator[str, None]:
    """
    Stream tokens from Ollama local LLM.
    
    Args:
        prompt: User's input prompt
        model: Ollama model name (e.g., 'llama2', 'mistral', 'codellama')
        system_prompt: Optional system prompt for context
    
    Yields:
        Individual tokens from the model
    
    Raises:
        RuntimeError: If Ollama is not installed or not running
    """
    if not OLLAMA_AVAILABLE:
        raise RuntimeError(
            "Ollama not installed. Install with: pip install ollama"
        )
    
    try:
        # Build messages
        messages = []
        if system_prompt:
            messages.append({
                "role": "system",
                "content": system_prompt
            })
        messages.append({
            "role": "user",
            "content": prompt
        })
        
        # Stream from Ollama
        # Ollama's chat is synchronous, so we need to handle it properly
        stream = ollama.chat(
            model=model,
            messages=messages,
            stream=True
        )
        
        for chunk in stream:
            if "message" in chunk and "content" in chunk["message"]:
                token = chunk["message"]["content"]
                if token:
                    yield token
                    # Give Textual a chance to update the UI
                    await asyncio.sleep(0)
                    
    except Exception as e:
        raise RuntimeError(f"Ollama error: {e}")


def is_ollama_available() -> bool:
    """Check if Ollama is installed and running."""
    if not OLLAMA_AVAILABLE:
        return False
    
    try:
        # Try to list models as a health check
        ollama.list()
        return True
    except Exception:
        return False


def list_ollama_models() -> list[str]:
    """Get list of available Ollama models."""
    if not is_ollama_available():
        return []
    
    try:
        models = ollama.list()
        return [m["name"] for m in models.get("models", [])]
    except Exception:
        return []
