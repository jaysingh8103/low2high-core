# Background Design Guidelines (bg.md)

This document provides specifications for the background aesthetics of the **AI-Powered Business Discovery & Digital Transformation Platform**. To achieve a truly premium and state-of-the-art feel, we avoid flat, generic backgrounds and instead use dynamic, textured, and rich background elements.

## 1. Mesh Gradients (Primary Dashboard Backgrounds)
Mesh gradients provide a soft, dynamic, and modern look that pairs perfectly with glassmorphism UI elements.

- **Light Mode Mesh**:
  - Base: `#F8FAFC` (Slate-50)
  - Accent Orbs: `#DBEAFE` (Blue-100) and `#E0E7FF` (Indigo-100)
  - Application: Place large, highly blurred circular gradients (blur: 120px) in the background corners (e.g., top-right and bottom-left) to break up flat spaces without distracting from content.
  
- **Dark Mode Mesh**:
  - Base: `#0F172A` (Slate-900)
  - Accent Orbs: `#1E3A8A` (Blue-900 with 30% opacity) and `#312E81` (Indigo-900 with 30% opacity)
  - Application: Subtle, deep atmospheric glows to prevent the background from feeling like a harsh black void.

## 2. Animated Micro-Backgrounds
To make the platform feel alive:
- **Subtle Drift**: Apply a very slow, infinite CSS keyframe animation to the mesh gradient orbs so they drift organically (e.g., drifting 3-5% over 20 seconds).
- **Interactive Hover States**: For feature cards or pricing tiers, use a radial gradient mask that follows the user's cursor (`background: radial-gradient(circle at var(--mouse-x) var(--mouse-y), ...)`), giving a premium "flashlight" effect.

## 3. Patterns & Textures
For areas needing more structure (e.g., empty states, login screens, or report covers):
- **Dot Matrix**: 
  - A subtle 1px dot grid with `24px` spacing.
  - Opacity: `5%` in light mode, `10%` in dark mode.
- **Topographic Lines**:
  - Extremely faint, contoured SVG lines to signify "discovery" and "mapping" (fitting for a Business Discovery platform).

## 4. Glassmorphism Layering
The backgrounds are designed to work in tandem with our UI surface components:
- Cards and sidebars should use a slightly translucent background (e.g., `rgba(255, 255, 255, 0.7)` in light mode).
- Apply a `backdrop-filter: blur(16px)` and `-webkit-backdrop-filter: blur(16px)` to ensure the rich mesh gradients bleed softly through the UI components.
- Add a 1px solid border (`rgba(255, 255, 255, 0.2)`) to glassmorphic elements to define their edges against the complex backgrounds.

## 5. CSS Implementation Example

```css
/* Example of an animated mesh background */
.bg-mesh-container {
  background-color: #F8FAFC;
  position: relative;
  overflow: hidden;
}

.bg-orb {
  position: absolute;
  border-radius: 50%;
  filter: blur(100px);
  animation: drift 20s infinite alternate ease-in-out;
}

.orb-primary {
  width: 500px;
  height: 500px;
  background-color: #DBEAFE;
  top: -10%;
  right: -5%;
}

.orb-secondary {
  width: 400px;
  height: 400px;
  background-color: #E0E7FF;
  bottom: 10%;
  left: -10%;
  animation-delay: -10s;
}

@keyframes drift {
  0% { transform: translate(0, 0) scale(1); }
  100% { transform: translate(50px, 30px) scale(1.05); }
}
```
