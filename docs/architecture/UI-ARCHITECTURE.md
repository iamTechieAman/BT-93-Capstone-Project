# UI/UX System Architecture & Design System Specification

## 1. Executive Summary & Design Philosophy

The **Smart GST Verification System** frontend interface is built as an production-grade AI compliance platform. The UI design system combines a dark glassmorphic palette (`#07090e`, `#0e131f`), vibrant emerald/cyan accents (`#10b981`, `#06b6d4`), typography hierarchy using *Plus Jakarta Sans* for body UI and *JetBrains Mono* for codes/rates, and responsive component adaptations across 320px small mobile phones to 1920px+ desktop displays.

---

## 2. Reusable Design System Tokens

### 2.1 Color Token System
```css
:root {
  --bg-dark: #07090e;
  --bg-card: #0e131f;
  --bg-card-hover: #141b2b;
  --border-color: rgba(255, 255, 255, 0.08);
  --border-glow: rgba(16, 185, 129, 0.3);
  
  --emerald-primary: #10b981;
  --emerald-glow: rgba(16, 185, 129, 0.15);
  --cyan-accent: #06b6d4;
  --purple-accent: #a855f7;
  --amber-accent: #f59e0b;
  --rose-accent: #f43f5e;
  
  --text-main: #f8fafc;
  --text-muted: #94a3b8;
  --text-dim: #64748b;
}
```

### 2.2 Typography Scale
- **Headings**: `Plus Jakarta Sans` (800 / 700 / 600 weight)
  - H1: 1.5rem (24px) / Line height 1.2
  - H2: 1.25rem (20px) / Line height 1.3
  - H3: 1.1rem (17.6px) / Line height 1.4
- **Body & Controls**: `Plus Jakarta Sans` (500 / 400 weight)
  - Body Regular: 0.9rem (14.4px)
  - Small / Micro: 0.75rem (12px)
- **Monospace (HSN, SAC, Rates, GSTIN)**: `JetBrains Mono`
  - Code Bold: 1.25rem - 1.5rem (20px - 24px)
  - Code Label: 0.8rem (12.8px)

### 2.3 Spacing & Radius System
- **Border Radius**:
  - `rounded-2xl` (16px) for main cards and search banners.
  - `rounded-xl` (12px) for input containers and modal dialogs.
  - `rounded-lg` (8px) for buttons, chips, and table cells.
- **Spacing Scale**: 4px / 8px / 12px / 16px / 24px / 32px padding and margin steps.

---

## 3. UI Component Standards

1. **Button System**: `.btn-emerald` (primary action), `.btn-secondary` (outline/surface action), `.btn-sm`, `.btn-lg`. Includes hover states and disabled states.
2. **Form Controls**: Glassmorphic search inputs (`.search-input-wrapper`), clear focus rings, and validation helper text.
3. **Card & Metric Grid**: Metric boxes with highlighted primary values (e.g. HSN 42031010 in emerald, 18% GST in cyan).
4. **Badges & Status Pills**: `.status-pill.green` (Active/Verified), `.status-pill.blue` (Inter-State IGST), `.status-pill.amber` (Review Flagged).
5. **Modal & Confirmation Dialogs**: Centered backdrop-blur overlay modals with explicit confirm/cancel buttons.
6. **Toast & Notifications**: Floating feedback toasts for copy, export, and system notifications.
7. **Empty, Skeleton & Error States**:
   - Empty Audit Log: Clear illustration icon with prompt action.
   - Loading State: Spinning `Cpu` icon with active pipeline step progress.
   - Error Banner: `AlertCircle` warning with descriptive next steps.

---

## 4. Terminology Standard

> **Mandatory UI Rule**: *Internal technical jargon such as "Explainable CoT Rationale" MUST NOT be shown to end users. The user interface uses user-facing "Evidence-Backed Explanation".*
