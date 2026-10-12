"""
Script to generate OpenAPI schema into packages/contracts/openapi.json.
"""
import json
import os
import sys

# Ensure src is on path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "apps", "api", "src"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "backend"))

try:
    from smart_gst.main import app  # type: ignore[import-not-found,import-untyped]
except Exception:
    from app.main import app  # type: ignore[import-not-found,import-untyped]

def generate_openapi():
    out_dir = os.path.join(os.path.dirname(__file__), "..", "packages", "contracts")
    os.makedirs(out_dir, exist_ok=True)
    out_file = os.path.join(out_dir, "openapi.json")

    openapi_schema = app.openapi()
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(openapi_schema, f, indent=2)
    print(f"✅ Generated OpenAPI schema at {out_file}")

if __name__ == "__main__":
    generate_openapi()
