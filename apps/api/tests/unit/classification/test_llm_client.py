"""
Unit tests for LlmClient Interface and Gemini client fallback behavior.
"""

from smart_gst.classification.llm_client import GeminiLlmClient


def test_gemini_client_graceful_offline_fallback():
    # Test fallback behavior when no API key is provided
    client = GeminiLlmClient(api_key="")
    explanation = client.explain_classification(
        product="Solar panel", hsn="85414011", rate=12.0, evidence=[]
    )
    assert "85414011" in explanation
    assert "12.0%" in explanation or "12%" in explanation
