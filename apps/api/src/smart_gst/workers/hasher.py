"""
Pure Content Hashing and Document SHA-256 Digest Module.
Strictly separated from prompt safety wrapping.
"""

import hashlib


def compute_sha256(content: bytes) -> str:
    """Compute SHA-256 hexadecimal digest of raw document bytes."""
    return hashlib.sha256(content).hexdigest()


def compute_text_sha256(text: str) -> str:
    """Compute SHA-256 hexadecimal digest of UTF-8 text string."""
    return hashlib.sha256(text.encode("utf-8")).hexdigest()
