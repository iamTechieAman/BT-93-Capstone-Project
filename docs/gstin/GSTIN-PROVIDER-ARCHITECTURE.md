# GSTIN Provider Architecture & Extensibility

## Overview
The GSTIN Validator utilizes an object-oriented provider pattern enabling seamless switching between local statutory format engines, external GSPs, and test mocks without changing application business logic.

```python
class GSTINVerificationProvider(ABC):
    @abstractmethod
    def get_provider_name(self) -> str: pass

    @abstractmethod
    def lookup_taxpayer(self, gstin: str) -> GSTINVerificationResult: pass
```

## Concrete Implementations

1. `LocalFormatProvider`:
   - Always available. Runs local statutory validation (15 chars, PAN structure, State Code, Modulus 36 checksum).
   - `registration_verified = False`, `taxpayer_status = "UNKNOWN"`.

2. `ExternalGSTProvider`:
   - Configured via environment variables:
     - `GST_PROVIDER_API_KEY`
     - `GST_PROVIDER_URL`
     - `GST_PROVIDER_TIMEOUT`
   - Returns `SOURCE_UNAVAILABLE` gracefully when unconfigured or unreachable.

3. `MockGSTProvider`:
   - Activated during tests or when `GST_ENABLE_MOCK_PROVIDER=1`.
   - Contains explicit test fixtures clearly tagged with `DEMO DATA`.
