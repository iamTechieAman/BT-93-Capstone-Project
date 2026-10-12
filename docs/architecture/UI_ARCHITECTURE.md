# UI_ARCHITECTURE.md — Frontend Design System & UI Architecture

**Project**: Smart GST Verification and Manufacturing Sales Automation System  
**Document Version**: 2.4.0  
**Authors**: Aman Kumar (Frontend Lead) & Aryan Singh  

---

## 1. Design System Principles

1. **Professional B2B ERP Aesthetic**:
   - Clean dark-mode canvas (`#07090e`), elevated glassmorphic card containers (`#0e131f`), and glowing emerald/cyan/purple accents.
2. **Design Tokens & Typography**:
   - Primary Sans Font: `Plus Jakarta Sans` for clean enterprise UI elements.
   - Monospace Font: `JetBrains Mono` for HSN codes, GSTIN numbers, and tax figures.
3. **Information Hierarchy**:
   - High-contrast visual cards for HSN matches, GST rates, and evidence checklists.
   - Clear distinction between Intra-State (`CGST 9% + SGST 9%`) and Inter-State (`IGST 18%`) supply modes.

---

## 2. Reusable Component Hierarchy

```
frontend/src/
├── components/
│   ├── ui/                    # Reusable Design System Primitives
│   │   ├── Button.tsx         # Primary, Secondary, Outline, Emerald, Danger
│   │   ├── Card.tsx           # Card, CardHeader, CardContent
│   │   ├── Badge.tsx          # Status Badges (Emerald, Cyan, Purple, Amber, Rose)
│   │   ├── Input.tsx          # Accessible Input with Label & Error states
│   │   └── Modal.tsx          # Accessible Dialog Overlay
│   ├── Sidebar.tsx            # Navigation Shell Sidebar
│   ├── Header.tsx             # Sticky Header Bar
│   ├── GstStudio.tsx          # Natural Language Search Studio
│   ├── PipelineVisualizer.tsx # 8-Stage Architecture Flow visualizer
│   ├── KnowledgeGraphCanvas.tsx # Neo4j Graph visualizer
│   ├── RagExplorer.tsx        # Searchable Notification Library
│   ├── InvoiceBuilder.tsx     # B2B Tax Invoice Generator
│   ├── AnalyticsCharts.tsx    # Recharts Tax Analytics
│   └── AuditLogs.tsx          # Decision Trace Audit Logger
└── pages/                     # Full Page Views
    ├── DashboardPage.tsx      # Overview & Stats Dashboard
    ├── ProductMasterPage.tsx  # Product Catalogue
    ├── SalesPage.tsx          # Sales Orders & History
    ├── InvoiceValidationPage.tsx # GSTIN & Rate Compliance Validator
    ├── ReportsPage.tsx        # GSTR-1 HSN Summary Reports
    └── SettingsPage.tsx       # AI Provider & Database Settings
```

---

## 3. Service Interface Abstraction

To ensure clean separation of concerns, UI components interact with service interfaces (`frontend/src/lib/api.ts` and `frontend/src/services/mockGstService.ts`) rather than hardcoding data or business logic directly inside components.
