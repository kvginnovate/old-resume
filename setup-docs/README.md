# LaTeX Resume — Live Preview Setup

Render and preview LaTeX resumes locally with live-edit support.

## Prerequisites

| Tool | Version | Purpose |
|------|---------|---------|
| MiKTeX | Latest | LaTeX compiler (`pdflatex`) |
| `latexmk` | Any | Auto-recompile on save (via MiKTeX Console) |
| Python | 3.x | HTTP server for browser preview |
| Browser | Any | PDF viewer |

### Install MiKTeX (Windows)
1. Download from https://miktex.org/download
2. Run installer → select **Install for anyone who uses this computer**
3. MiKTeX auto-installs missing packages (e.g., `fontawesome5`) on first compile

### Install latexmk
`latexmk` is **not included by default** in MiKTeX. Install it via:
- Open **MiKTeX Console** → **Packages** → search `latexmk` → Install
- Or run: `mpm --install=latexmk`

### Install Python (Windows)
1. Download from https://www.python.org/downloads/
2. During install, check **"Add Python to PATH"**
3. Verify: `python --version`

## Quick Start

```bash
# 1. Navigate to your resume folder
cd E:\1_Resume_Prepreation\OLD_Resume

# 2. Compile LaTeX to PDF (first time or manual recompile)
pdflatex -interaction=nonstopmode main.tex

# 3. Start HTTP server (background)
python -m http.server 8888

# 4. Open in browser
# http://localhost:8888/main.pdf        ← direct PDF
# http://localhost:8888/preview.html    ← preview with refresh button
```

Or run the one-click script: `start-preview.bat`

## Live Edit Workflow

For automatic recompile on save, run in a **separate terminal**:

```bash
cd E:\1_Resume_Prepreation\OLD_Resume
latexmk -pvc -pdf main.tex
```

This watches `main.tex` and recompiles automatically when you save.

### Full loop:
1. Edit `main.tex` in your editor
2. **Save** the file
3. `latexmk` detects change → recompiles PDF automatically
4. In browser: click **Refresh PDF** button (or press F5)
5. Updated resume appears (note: scroll resets to page 1 on refresh)

## Files

| File | Purpose |
|------|---------|
| `main.tex` | Resume source (LaTeX) |
| `main.pdf` | Compiled output |
| `preview.html` | Browser preview page with refresh button |
| `setup-docs/` | This documentation |
| `start-preview.bat` | One-click Windows launch script |

## Troubleshooting

### Port 8000 blocked (PermissionError)
Windows blocks port 8000. Use port 8888 or any other port:
```bash
python -m http.server 8888
```

### Missing packages
MiKTeX auto-installs on first compile. If prompted, click "Install" or run:
```bash
mpm --install=package-name
```

### latexmk not found
Install via MiKTeX Console → Packages → search `latexmk` → Install.
Or run: `mpm --install=latexmk`

### PDF not updating
- Ensure `latexmk -pvc` is running in a separate terminal
- Hard-refresh browser: **Ctrl+Shift+R**
- Check `main.log` for compilation errors

### Two-page PDF scroll reset
Browser PDF viewers reset scroll on reload. Use the **Refresh PDF** button
in `preview.html` instead of browser refresh to minimize disruption.

## Reuse on Another Machine

1. Copy `main.tex` and `preview.html` to the new machine (both are in this folder)
2. Install MiKTeX from https://miktex.org/download
3. Install `latexmk` via MiKTeX Console → Packages → search `latexmk`
4. Install Python 3 with "Add to PATH" checked
5. Copy `start-preview.bat` for one-click launch, or run the Quick Start commands
6. Optionally copy `main.pdf` to skip initial compilation
