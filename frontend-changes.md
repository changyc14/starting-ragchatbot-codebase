# Frontend Changes

## Code Quality Tooling

Added frontend code quality tooling (Prettier + ESLint) to enforce consistent formatting and catch common JavaScript issues.

### New Files

**`frontend/package.json`**
- Defines the frontend as an npm package with `prettier` and `eslint` as dev dependencies.
- Provides npm scripts:
  - `npm run format` — auto-format all JS/CSS/HTML with Prettier
  - `npm run format:check` — check formatting without writing changes (CI-safe)
  - `npm run lint` — lint JavaScript with ESLint
  - `npm run lint:fix` — auto-fix ESLint issues
  - `npm run quality` — run format check + lint together

**`frontend/.prettierrc`**
- Prettier configuration: 2-space indentation, single quotes, trailing commas (`es5`), semicolons, 80-char print width, LF line endings.
- Note: Prettier is the frontend equivalent of Python's `black` — it enforces a single, non-negotiable style so formatting is never debated.

**`frontend/eslint.config.js`**
- ESLint flat config targeting `*.js` files.
- Sets browser globals (`document`, `window`, `fetch`, `marked`, etc.).
- Rules: `no-unused-vars` (warn), `eqeqeq` (error), `no-var` (error), `prefer-const` (warn).

**`scripts/check-frontend.sh`**
- Dev script to run all frontend quality checks (Prettier check + ESLint).
- Automatically installs npm deps if `node_modules` is missing.
- Exits non-zero on any failure, suitable for CI.

**`scripts/format-frontend.sh`**
- Dev script to auto-format all frontend files with Prettier in one command.
- Automatically installs npm deps if `node_modules` is missing.

### Modified Files

**`frontend/script.js`**
- Reformatted to match Prettier config: 2-space indentation, single quotes, trailing commas, 80-char line wrapping.
- Removed extra blank lines between function declarations.

**`frontend/style.css`**
- Reformatted to match Prettier config: 2-space indentation, each selector on its own line for multi-selector rules, consistent `@keyframes` brace style.

### Usage

```bash
# Check formatting and lint (read-only, good for CI)
./scripts/check-frontend.sh

# Auto-format frontend files
./scripts/format-frontend.sh

# Or use npm scripts directly from frontend/
cd frontend
npm install
npm run quality      # check only
npm run format       # write formatting
```

## Dark / Light Theme Toggle

### Summary
Added a toggle button in the top-right corner that lets users switch between the existing dark theme and a new light theme. The chosen theme persists across page reloads via `localStorage`.

---

### Files Modified

#### `frontend/index.html`
- Added `<button id="themeToggle">` just inside `<body>`, before `.container`.
- The button contains two inline SVG icons:
  - **Sun icon** — displayed in dark mode; clicking switches to light.
  - **Moon icon** — displayed in light mode; clicking switches to dark.
- Includes `aria-label="Toggle light/dark theme"` and `title` for accessibility. Keyboard events (`Enter`/`Space`) are wired up in JS.

#### `frontend/style.css`

**CSS Variables**
- Removed unused `--assistant-message` variable.
- Added new semantic variables to `:root` (dark defaults):
  - `--code-bg` — background for inline code and code blocks.
  - `--error-color`, `--error-bg`, `--error-border` — error message palette.
  - `--success-color`, `--success-bg`, `--success-border` — success message palette.

**Light theme** (`html[data-theme="light"]`)
- Overrides all color variables for a clean light appearance:
  - `--background: #f8fafc` / `--surface: #ffffff` / `--surface-hover: #f1f5f9`
  - `--text-primary: #0f172a` / `--text-secondary: #64748b` (both WCAG AA compliant)
  - `--border-color: #e2e8f0`, lighter `--shadow`
  - `--welcome-bg: #eff6ff`
  - `--code-bg: rgba(0,0,0,0.06)` — subtle on white backgrounds
  - `--error-color: #b91c1c` / `--success-color: #15803d` — accessible on light backgrounds (WCAG AA contrast ≥ 4.5:1)

**Hardcoded color fixes** — replaced all hardcoded values with variables so they adapt automatically:
- `rgba(0,0,0,0.2)` on `.message-content code` and `pre` → `var(--code-bg)`
- `rgba(0,0,0,0.2)` on `.message.welcome-message` box-shadow → `var(--shadow)`
- Hardcoded hex colors in `.error-message` / `.success-message` → `var(--error-*)` / `var(--success-*)`

**Smooth transitions**
- Added `transition` (background-color, color, border-color, box-shadow at 0.3s ease) to key elements: `body`, `.main-content`, `.sidebar`, `.chat-*`, `.message-content`, `.stat-item`, `.suggested-item`, `.loading span`, `#chatInput`, `#themeToggle`.
- `#themeToggle` also includes `transform 0.2s ease` so the scale-up on hover is smooth.

**`#themeToggle` styles**
- Fixed position (`top: 1rem; right: 1rem; z-index: 200`), 40 × 40 px circle.
- All colors (`background`, `border`, `color`) use CSS variables — adapts automatically to both themes.
- CSS rules show/hide `.icon-sun` / `.icon-moon` based on `html[data-theme]` attribute.
- `@keyframes iconSpin` — short rotate + fade-in animation plays on the SVG each time the icon changes.

#### `frontend/script.js`
- **`initTheme()`** — reads `localStorage.getItem('theme')` on load; if `'light'`, sets `data-theme="light"` on `<html>`. Attaches `click` and `keydown` (`Enter`/`Space`) listeners to `#themeToggle`.
- **`toggleTheme()`** — reads current `data-theme`, toggles it, and persists to `localStorage`.
- `initTheme()` is called at the top of the `DOMContentLoaded` handler (before other setup).
