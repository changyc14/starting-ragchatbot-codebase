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