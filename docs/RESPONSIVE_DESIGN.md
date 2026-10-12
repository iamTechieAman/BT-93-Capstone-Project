# Responsive Design & Multi-Viewport Specification

## 1. Overview & Breakpoint Grid

The Smart GST System UI is engineered for seamless responsiveness across all screen sizes from 320px small mobile displays to 1920px+ ultra-wide desktop monitors.

| Viewport Range | Target Device Category | Layout Strategy |
| :--- | :--- | :--- |
| **320px - 480px** | Small & Large Mobile Phones | 1-Column vertical stacking, mobile navigation menu drawer, touch targets $\ge$ 44px, horizontal preset scrolling |
| **768px - 1024px** | Tablet Portrait & Landscape | 2-Column flexible grid, collapsible sidebar, responsive header wrapping |
| **1280px - 1920px+** | Laptops & Desktops | Full multi-column dashboard, side-by-side RAG & Knowledge Graph explorer panels |

---

## 2. Component Adaptation Rules

- **Header (`Header.jsx`)**: Navigation items collapse into a clean hamburger/drawer menu on mobile screens without horizontal overflow or clipped text.
- **Verification Studio (`GstVerificationStudio.jsx`)**: Result cards transition from side-by-side desktop grids to single-column mobile cards.
- **Sales & Invoice (`InvoiceModule.jsx`)**: Line item tables support smooth horizontal scrolling on mobile viewports while preserving critical description and total columns.
- **Knowledge Graph Explorer (`KnowledgeGraphExplorer.jsx`)**: Node canvas adapts with touch pan/zoom and compact relationship list view on mobile.
