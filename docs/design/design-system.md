# Design System & UI/UX Guidelines

This document outlines the core design tokens, typography, color palettes, and component guidelines for the **AI-Powered Business Discovery & Digital Transformation Platform** (Dashboard and PDF Reports).

## Design Philosophy
The platform should feel **Premium, Modern, and Trustworthy**.
- **Use Rich Aesthetics**: Vibrant colors, dark mode support, and glassmorphism for premium feel.
- **Dynamic & Alive**: Utilize subtle micro-animations for hover states and transitions.
- **Accessible**: Ensure high contrast ratios and clear hierarchy.

---

## Typography

We use modern, highly legible sans-serif fonts from Google Fonts to maintain a clean tech aesthetic.

- **Primary Font (Headings)**: `Outfit`
  - Weights: SemiBold (600), Bold (700)
  - Usage: H1, H2, H3, and major data callouts.
- **Secondary Font (Body)**: `Inter`
  - Weights: Regular (400), Medium (500)
  - Usage: Paragraphs, data tables, UI labels, and tooltips.

### Scale
- **H1**: 32px / 40px line-height (Outfit, Bold)
- **H2**: 24px / 32px line-height (Outfit, SemiBold)
- **H3**: 20px / 28px line-height (Outfit, Medium)
- **Body 1 (Default)**: 16px / 24px line-height (Inter, Regular)
- **Body 2 (Small)**: 14px / 20px line-height (Inter, Regular)
- **Caption**: 12px / 16px line-height (Inter, Medium)

---

## Color Palette

Avoid generic plain red/blue/green. Use carefully tailored HSL colors.

### 1. Primary Colors (Brand & Action)
- **Primary Blue**: `#2563EB` (Tailwind Blue-600) — Used for primary buttons, active states, and key highlights.
- **Primary Light**: `#DBEAFE` (Tailwind Blue-100) — Used for soft backgrounds and hover states on primary items.
- **Primary Dark**: `#1E40AF` (Tailwind Blue-800) — Used for hover states on primary buttons.

### 2. Digital Maturity Scoring Colors
Used dynamically to represent the digital score (0-100).
- **Mature (91-100)**: `#10B981` (Emerald-500) - Vibrant Green
- **Advanced (76-90)**: `#34D399` (Emerald-400) - Soft Green
- **Growing (51-75)**: `#F59E0B` (Amber-500) - Warm Yellow/Orange
- **Basic (31-50)**: `#F97316` (Orange-500) - Bright Orange
- **Offline (0-30)**: `#EF4444` (Red-500) - Alert Red

### 3. Neutral Colors (Text & Backgrounds)
**Light Mode:**
- **Background**: `#F8FAFC` (Slate-50)
- **Surface (Cards/Modals)**: `#FFFFFF` (White)
- **Text Primary**: `#0F172A` (Slate-900)
- **Text Secondary**: `#475569` (Slate-600)
- **Borders**: `#E2E8F0` (Slate-200)

**Dark Mode:**
- **Background**: `#0F172A` (Slate-900)
- **Surface (Cards/Modals)**: `#1E293B` (Slate-800)
- **Text Primary**: `#F8FAFC` (Slate-50)
- **Text Secondary**: `#94A3B8` (Slate-400)
- **Borders**: `#334155` (Slate-700)

---

## UI Components & Aesthetics

### 1. Cards & Surfaces
- **Corner Radius**: `12px` (rounded-xl) for larger containers, `8px` (rounded-lg) for smaller buttons and inputs.
- **Shadows**: Soft, diffused shadows. 
  - Light mode: `box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);`
  - Dark mode: Avoid heavy shadows; use slight border highlights (`1px solid rgba(255,255,255,0.1)`).
- **Glassmorphism**: Use backdrop-blur (`backdrop-filter: blur(8px)`) for sticky headers and modal overlays with semi-transparent backgrounds.

### 2. Buttons
- **Primary**: Solid background (`Primary Blue`), white text. Hover: `Primary Dark`.
- **Secondary**: Outline border (`Borders` color), transparent background, `Text Primary` color. Hover: `Primary Light` background.
- **Transitions**: Apply a `150ms ease-in-out` transition to `background-color`, `transform`, and `box-shadow`. Add a slight scale effect (`transform: scale(0.98)`) on `:active`.

### 3. Data Visualization (Charts & Scores)
- Use smooth gradients for score gauges (e.g., a gradient from `Red-500` to `Emerald-500` for a digital maturity arc).
- Use rounded caps on bar charts.

## PDF Report Specifics
- PDF reports should strictly use a light theme to ensure readability when printed.
- Maintain high contrast.
- Use vector-based icons (SVG) so they remain crisp at any zoom level.
