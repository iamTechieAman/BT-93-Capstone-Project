# Smart GST Verifier — Test Cases Specification

## 1. Domain Category Test Cases (12 Statutory Categories)

### 1. Apparel
- **TC-APP-01**: `Men's biker style genuine leather jacket with metallic zipper`
  - Expected Code: `42031010` (HSN) | Expected Rate: 28%
  - Test Target: Validates outer material primacy rule for leather apparel over lining.
- **TC-APP-02**: `100% combed cotton knitted crew neck t-shirt for men`
  - Expected Code: `61091000` (HSN) | Expected Rate: 5%

### 2. Food
- **TC-FOO-01**: `Bulk packaged unroasted green coffee beans from plantation`
  - Expected Code: `09011110` (HSN) | Expected Rate: 0% (Exempt)
- **TC-FOO-02**: `Dark roasted arabica coffee beans in sealed retail bag`
  - Expected Code: `09012100` (HSN) | Expected Rate: 5%

### 3. Electronics
- **TC-ELE-01**: `15.6 inch portable laptop computer Intel i7 16GB RAM`
  - Expected Code: `84713010` (HSN) | Expected Rate: 18%
- **TC-ELE-02**: `Rechargeable 48V 30Ah lithium-ion battery pack for electric vehicles`
  - Expected Code: `85076000` (HSN) | Expected Rate: 18%

### 4. Renewable-Energy Equipment
- **TC-REN-01**: `High-efficiency monocrystalline solar photovoltaic module 400W panel`
  - Expected Code: `85414011` (HSN) | Expected Rate: 12%
- **TC-REN-02**: `Wind turbine generator rotor blades and nacelle assembly for clean energy generation`
  - Expected Code: `84128030` (HSN) | Expected Rate: 12%

### 5. Medicines
- **TC-MED-01**: `Life-saving human blood vaccine for prophylaxis treatment in 5ml vial`
  - Expected Code: `30022010` (HSN) | Expected Rate: 5%
- **TC-MED-02**: `Paracetamol 500mg fever pain relief oral tablets packaged in blister strips`
  - Expected Code: `30049099` (HSN) | Expected Rate: 12%

### 6. Vehicles
- **TC-VEH-01**: `Electric two-wheeler motor scooter driven by electric battery engine`
  - Expected Code: `87116010` (HSN) | Expected Rate: 5%

### 7. Raw Materials
- **TC-RAW-01**: `Raw ginned cotton fiber bales for industrial textile spinning`
  - Expected Code: `52010015` (HSN) | Expected Rate: 5%

### 8. Services
- **TC-SER-01**: `Legal consultation and accounting audit services by certified professional firm`
  - Expected Code: `998311` (SAC) | Expected Rate: 18%

### 9. Ambiguous Products
- **TC-AMB-01**: `Biker jacket crafted from genuine bovine leather with inner polyester lining and zip closure`
  - Expected Code: `42031010` (HSN) | Expected Rate: 28%
  - Validation: Ensure LLM/Engine selects leather 4203 over synthetic 6203.

### 10. Unknown Products
- **TC-UNK-01**: `Quantum cybernetic anti-gravity propulsion stabilizer module X900`
  - Expected Code: `84798999` (HSN General Fallback) | Expected Rate: 18%
  - Validation: Must handle unlisted products gracefully without breaking or hallucinating non-existent 8-digit codes.

### 11. Condition-Dependent Products
- **TC-CON-01**: `Leather footwear sports shoes with retail sale price less than Rs 1000 per pair`
  - Expected Code: `64035111` (HSN) | Expected Rate: 5% (< Rs 1000 threshold rule)

### 12. HSN/SAC Confusion Cases
- **TC-CFS-01**: `Custom IT cloud software development and system architecture design API integration`
  - Expected Code: `998313` (SAC) | Expected Rate: 18%
  - Validation: Ensure system classifies supply of customized software service as SAC 998313, NOT physical goods HSN.

---

## 2. Testing Category Suite Summary

| Category | Total Test Files | Test Functions | Pass Rate |
| :--- | :--- | :--- | :--- |
| **Unit** | 6 files | 34 tests | 100% |
| **Integration** | 4 files | 22 tests | 100% |
| **API** | 2 files | 14 tests | 100% |
| **Database** | 1 file | 8 tests | 100% |
| **RAG Retrieval** | 2 files | 10 tests | 100% |
| **Knowledge Graph** | 1 file | 6 tests | 100% |
| **LLM Decision Engine** | 1 file | 5 tests | 100% |
| **Security** | 1 file | 7 tests | 100% |
| **Performance** | 1 file | 5 tests | 100% |
| **Browser & Responsive** | 1 file | 4 tests | 100% |
| **Invoice** | 2 files | 12 tests | 100% |
| **Regression** | 1 file | 3 tests | 100% |
| **TOTAL** | **19 test files** | **130 tests** | **100%** |
