# Chokkar Gurusamy — Resume Project

Professional resume built in LaTeX, compiled to PDF, and deployed as a live web page with inline PDF rendering.

**Live URL:** https://kvginnovate.github.io/old-resume/

---

## Project Structure

```
OLD_Resume/
├── main.tex                  # Primary resume (2 pages, full version)
├── main_v2.tex               # Compact alternative (1 page)
├── main_recruiter.tex        # Short recruiter-focused version
├── main_v3.tex               # Latest version with improved content
├── main_v3.pdf               # Compiled PDF (served by GitHub Pages)
├── docs/
│   ├── index.html            # Web viewer (PDF.js inline renderer)
│   └── main_v3.pdf           # PDF copy served by GitHub Pages
├── company_reqq/             # Job requirement screenshots
├── setup-docs/               # Setup instructions
├── deploy_netlify.py         # Netlify deploy script (alternative hosting)
├── preview.html              # Local live-reload preview
├── .gitignore                # Excludes PDFs (except docs/), credentials, build artifacts
└── README.md                 # This file
```

---

## How It Was Built

### 1. LaTeX Resume

- **Template:** Custom resume template using `article` class with `fontawesome5`, `enumitem`, `hyperref`, `fancyhdr`
- **Custom commands:** `\resumeItem`, `\resumeSubheading`, `\resumeProjectHeading` for consistent formatting
- **Compilation:** `pdflatex -interaction=nonstopmode main_v3.tex`

### 2. Local Preview Server

Python HTTP server with live reload:

```bash
cd E:\1_Resume_Prepreation\OLD_Resume
python -m http.server 8888
```

Open **http://localhost:8888/preview.html** — refresh after each compilation to see changes.

### 3. GitHub Pages Deployment

#### Step 1: Make Repo Public

```bash
gh repo edit kvginnovate/old-resume --visibility public --accept-visibility-change-consequences
```

> **Note:** GitHub Pages requires the repo to be public on free plans. The resume contains no secrets (credentials.json is gitignored).

#### Step 2: Enable GitHub Pages

```bash
gh api -X POST repos/kvginnovate/old-resume/pages --input - <<EOF
{"build_type":"legacy","source":{"branch":"main","path":"/docs"}}
EOF
```

This serves the `docs/` folder from the `main` branch.

#### Step 3: Push Updates

After any change to `docs/`:

```bash
git add docs/
git commit -m "update: resume content"
git push origin main
```

GitHub auto-deploys in ~30 seconds.

### 4. PDF.js Inline Rendering (Mobile-Friendly)

The `<embed>` tag doesn't render PDFs on mobile browsers. Solution: **PDF.js** (Mozilla's PDF renderer).

**`docs/index.html`** key implementation:

```javascript
// Load PDF.js from CDN
pdfjsLib.GlobalWorkerOptions.workerSrc = 
  'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.worker.min.js';

async function renderPDF() {
  const pdf = await pdfjsLib.getDocument('main_v3.pdf').promise;
  for (let i = 1; i <= pdf.numPages; i++) {
    const page = await pdf.getPage(i);
    const scale = 2;  // 2x for crisp text on mobile
    const viewport = page.getViewport({scale});
    const canvas = document.createElement('canvas');
    canvas.width = viewport.width;
    canvas.height = viewport.height;
    // CSS constrains display: width: 100%; height: auto;
    await page.render({canvasContext: canvas.getContext('2d'), viewport}).promise;
  }
}
```

**Why `scale = 2`?**
- `Math.min(window.innerWidth / pageWidth, 2)` gives ~0.6x on mobile → unreadable
- Fixed 2x + CSS `width: 100%; height: auto;` → crisp text on all devices

---

## MiKTeX Setup (Windows)

MiKTeX is installed at user level (not system-wide):

```
%LOCALAPPDATA%\Programs\MiKTeX\miktex\bin\x64\pdflatex.exe
```

**Not in PATH** — use full path:

```bash
"%LOCALAPPDATA%/Programs/MiKTeX/miktex/bin/x64/pdflatex.exe" -interaction=nonstopmode main_v3.tex
```

---

## Resume Versions

| File | Pages | Purpose |
|---|---|---|
| `main.tex` | 2 | Primary full resume |
| `main_v2.tex` | 1 | Compact version (trimmed bullets) |
| `main_recruiter.tex` | 1 | Short recruiter-focused |
| `main_v3.tex` | 2 | Latest — improved content, placeholders for metrics |

### main_v3 Improvements Over main.tex

- Added GitHub link to heading
- Platform scale numbers (`[X]+ microservices`, `[X]M+ subscribers`)
- Rewrote promotion line (full scope, not just Spring Boot 3)
- Removed corporate fluff ("foster engineering culture")
- Consolidated personal AI tools (cut Paseo/Orca/OMP)
- Merged MCP into "AI & Automation" section
- Moved certifications to own section
- Added `[X]` placeholders for real metrics
- Fixed In-Home App "measurable increase" → `[X%]` placeholder
- Added 2nd bullets to 1-bullet projects
- Outcome-focused Pivot3 bullets

---

## Alternative Hosting: Netlify

A deploy script is included for Netlify (if you prefer private repo + public link):

```bash
python deploy_netlify.py
```

Or drag-drop the `docs/` folder at **https://app.netlify.com/drop** while logged in.

---

## Environment

- **OS:** Windows 11
- **LaTeX:** MiKTeX 25.12 (user install)
- **PDF viewer:** PDF.js 3.11.174 (CDN)
- **Hosting:** GitHub Pages (free, public repo)
- **Repo:** https://github.com/kvginnovate/old-resume
