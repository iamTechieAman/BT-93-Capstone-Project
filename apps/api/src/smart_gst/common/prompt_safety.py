"""
Prompt Safety and Prompt Injection Mitigation Sanitizer.
Strictly separated from hashing.
"""

import re


def sanitize_for_prompt(text: str) -> str:
    """Strip malicious prompt injection markers and wrap untrusted text safely."""
    if not text:
        return ""
    # Strip markdown code fencing escapes and system prompt overrides
    sanitized = re.sub(r"```", "", text)
    sanitized = re.sub(r"<\/?system_instruction>", "", sanitized, flags=re.IGNORECASE)
    sanitized = re.sub(r"<\/?prompt>", "", sanitized, flags=re.IGNORECASE)
    return sanitized.strip()


def wrap_untrusted_xml(text: str, tag: str = "untrusted_input") -> str:
    """Encapsulate untrusted input inside XML delimiters for safe LLM evaluation."""
    clean = sanitize_for_prompt(text)
    return f"<{tag}>\n{clean}\n</{tag}>"
