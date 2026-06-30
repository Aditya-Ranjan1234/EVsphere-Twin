---
name: Engineering Intelligence
colors:
  surface: '#0e141a'
  surface-dim: '#0e141a'
  surface-bright: '#343a41'
  surface-container-lowest: '#090f15'
  surface-container-low: '#161c22'
  surface-container: '#1a2027'
  surface-container-high: '#252b31'
  surface-container-highest: '#2f353c'
  on-surface: '#dde3ec'
  on-surface-variant: '#c1c7d2'
  inverse-surface: '#dde3ec'
  inverse-on-surface: '#2b3138'
  outline: '#8b919b'
  outline-variant: '#414750'
  surface-tint: '#a1c9ff'
  primary: '#a1c9ff'
  on-primary: '#00325a'
  primary-container: '#005a9c'
  on-primary-container: '#afd1ff'
  inverse-primary: '#1261a3'
  secondary: '#fff9ef'
  on-secondary: '#3a3000'
  secondary-container: '#ffdb3c'
  on-secondary-container: '#725f00'
  tertiary: '#00dbe7'
  on-tertiary: '#00363a'
  tertiary-container: '#006268'
  on-tertiary-container: '#00e4f1'
  error: '#ffb4ab'
  on-error: '#690005'
  error-container: '#93000a'
  on-error-container: '#ffdad6'
  primary-fixed: '#d2e4ff'
  primary-fixed-dim: '#a1c9ff'
  on-primary-fixed: '#001c37'
  on-primary-fixed-variant: '#00487f'
  secondary-fixed: '#ffe16d'
  secondary-fixed-dim: '#e9c400'
  on-secondary-fixed: '#221b00'
  on-secondary-fixed-variant: '#544600'
  tertiary-fixed: '#74f5ff'
  tertiary-fixed-dim: '#00dbe7'
  on-tertiary-fixed: '#002022'
  on-tertiary-fixed-variant: '#004f54'
  background: '#0e141a'
  on-background: '#dde3ec'
  surface-variant: '#2f353c'
typography:
  display-lg:
    fontFamily: Inter
    fontSize: 48px
    fontWeight: '700'
    lineHeight: 56px
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: Inter
    fontSize: 32px
    fontWeight: '600'
    lineHeight: 40px
  headline-md:
    fontFamily: Inter
    fontSize: 24px
    fontWeight: '600'
    lineHeight: 32px
  body-lg:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
  body-sm:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '400'
    lineHeight: 20px
  label-mono:
    fontFamily: JetBrains Mono
    fontSize: 13px
    fontWeight: '500'
    lineHeight: 16px
    letterSpacing: 0.05em
  headline-lg-mobile:
    fontFamily: Inter
    fontSize: 28px
    fontWeight: '600'
    lineHeight: 36px
rounded:
  sm: 0.125rem
  DEFAULT: 0.25rem
  md: 0.375rem
  lg: 0.5rem
  xl: 0.75rem
  full: 9999px
spacing:
  unit: 4px
  gutter: 16px
  margin-mobile: 16px
  margin-desktop: 32px
  container-max: 1440px
---

## Brand & Style
The design system is engineered for high-stakes industrial environments, specifically tailored for the Tata InnoVent hackathon. The brand personality is rooted in **Engineering Intelligence**: a marriage of deep-seated industrial reliability with cutting-edge computational power. It targets technical stakeholders, engineers, and decision-makers who require rapid data synthesis.

The aesthetic follows a **Modern Industrial / Digital Twin** approach. It prioritizes data density and functional clarity over decorative elements. The UI should evoke the feeling of a sophisticated control center—precise, authoritative, and real-time. By utilizing a "Dark Mode" foundation, the system reduces eye strain in low-light industrial settings while allowing neon data indicators to pop with maximum signal-to-noise ratio.

## Colors
The palette is dominated by **Tata Blue** (#005A9C), used for primary actions and structural branding to establish trust. **Innovation Gold** (#FFD700) is used sparingly as a "high-intelligence" accent—highlighting AI insights, novel breakthroughs, or critical path items.

The background uses a deep **Neutral** (#0B1117) to create a "void" effect, allowing for layered surfaces. **Cyan** (#00F2FF) is reserved specifically for "Digital Twin" elements: active telemetry, graph lines, and LLM agent activity. Success, warning, and critical states follow standard industrial conventions but are rendered in high-saturation "Neon" variants to ensure visibility against the dark backdrop.

## Typography
This design system utilizes **Inter** for all UI and body text to maintain a professional, neutral, and highly legible tone. To emphasize the "Engineering" aspect, **JetBrains Mono** is introduced for all data labels, timestamps, and terminal logs. This monospaced contrast signals "Raw Data" vs. "Human Insight."

Headlines should be tight and bold, while labels use slightly increased letter spacing and uppercase styling to denote metadata or system statuses.

## Layout & Spacing
The layout employs a **12-column Fixed Grid** for desktop dashboards, ensuring data containers align with mathematical precision. Spacing follows a strict 4px base unit to allow for high-density information architecture without feeling cluttered.

- **Desktop:** 12 columns, 16px gutters, 32px side margins.
- **Mobile:** 4 columns, 12px gutters, 16px side margins. 

Layouts should prioritize "Above the Fold" data visibility. Dashboard widgets should use a modular "Bento" style where each unit can scale based on its data importance.

## Elevation & Depth
Depth is conveyed through **Tonal Layering** rather than traditional shadows. This maintains the "Digital Twin" screen aesthetic.

1.  **Level 0 (Base):** #0B1117 (The deep background).
2.  **Level 1 (Card/Surface):** #161E27 (Subtle lift, used for main content containers).
3.  **Level 2 (Active/Hover):** #1F2937 (Used for interactive elements).

Instead of drop shadows, use **Low-contrast outlines** (1px border in #2D3748) to define edges. For critical alerts or AI focus states, use a "Glow" effect—a subtle 0.5px border using the accent color (Gold or Cyan) with a faint outer blur of the same hue.

## Shapes
Shapes are **Soft** (0.25rem / 4px). This minimal radius offers a modern feel while retaining the rigid, structural integrity of industrial hardware. 

- **Buttons/Inputs:** 4px radius.
- **Large Data Containers:** 8px (rounded-lg).
- **Status Indicators:** Perfect circles or sharp 0px for "Terminal" feel.

Avoid pill shapes unless used for specialized toggle switches. The geometry should feel "constructed" rather than "organic."

## Components
- **Data Cards:** Dark background (#161E27), 1px border (#2D3748). Top-right corner often contains a "Mono Label" for sensor IDs.
- **Graph Containers:** Use the Cyan accent for line charts. Fill areas with a low-opacity (10%) Cyan gradient. Grid lines within charts should be ultra-faint.
- **Risk Indicators:** Use a "Gauge" or "Step" visual. High risk is Neon Red, Nominal is Cyan.
- **Terminal Logs:** A dedicated container with a #05070A background. Text is JetBrains Mono. Use Cyan for the "Agent Name" and White/Grey for the log body. A "blinking cursor" underscore (_) adds to the real-time feel.
- **Buttons:**
    - *Primary:* Solid Tata Blue with White text.
    - *Secondary:* Ghost style with 1px Blue border.
    - *Insight:* Solid Gold with Dark text (reserved for AI actions).
- **Inputs:** Darker than the card surface. 1px border that turns Cyan on focus. Labels sit above the field in JetBrains Mono.