"""
LLM Client Interface and Real Google Gemini Implementation.
No Mock LLM exists in production code; unit/integration tests inject test doubles from tests/.
"""

from abc import ABC, abstractmethod
from typing import Optional

from smart_gst.common.logging import logger
from smart_gst.config import settings


class LlmClient(ABC):
    """Abstract interface for LLM reasoning and explainability providers."""

    @abstractmethod
    def explain_classification(
        self, product: str, hsn: str, rate: float, evidence: list[dict]
    ) -> str:
        """Generate chain-of-thought statutory explanation for HSN match."""
        pass


class GeminiLlmClient(LlmClient):
    """Production implementation using Google Gemini Generative AI SDK."""

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or settings.GEMINI_API_KEY
        self._model = None
        if self.api_key:
            try:
                import google.generativeai as genai

                genai.configure(api_key=self.api_key)
                self._model = genai.GenerativeModel("gemini-1.5-flash")
            except Exception as e:
                logger.warning(f"Could not initialize Gemini LLM client: {e}")

    def explain_classification(
        self, product: str, hsn: str, rate: float, evidence: list[dict]
    ) -> str:
        if not self._model:
            return (
                f"Statutory classification for '{product}' mapped to HSN {hsn} "
                f"at {rate}% GST based on CBIC Rate Schedule."
            )

        prompt = (
            f"As a statutory Indian GST Tax Counsel, explain why product '{product}' "
            f"classifies under HSN {hsn} at {rate}% GST based on evidence: {evidence}. "
            f"Provide concise, audit-defensible 2-sentence legal reasoning."
        )
        try:
            response = self._model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            logger.error(f"Gemini API error during explanation: {e}")
            return (
                f"Statutory classification for '{product}' mapped to HSN {hsn} "
                f"at {rate}% GST based on CBIC Rate Schedule."
            )
