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
├── main_v3.tex               # Latest version with real metrics
├── main_v3.pdf               # Compiled PDF
├── docs/
│   ├── index.html            # Web viewer (PDF.js inline renderer)
│   └── main_v3.pdf           # PDF served by GitHub Pages
├── company_reqq/             # Job requirement screenshots
├── setup-docs/               # Setup instructions
├── deploy_netlify.py         # Netlify deploy script (alternative hosting)
├── server.js                 # Local preview server (Node.js)
├── preview.html              # Local live-reload preview
├── .gitignore                # Excludes PDFs (except docs/), credentials, build artifacts
└── README.md                 # This file
```

---

## Daily Workflow: Edit → Compile → Push

This is the step-by-step process for making changes and deploying them.

### Step 1: Edit the Resume

Edit `main_v3.tex` in your favorite editor (VS Code, Overleaf, etc.):

```bash
# Open in VS Code
code main_v3.tex
```

Make your changes to the content, formatting, or structure.

### Step 2: Compile to PDF

```bash
cd E:\1_Resume_Prepreation\OLD_Resume
"%LOCALAPPDATA%/Programs/MiKTeX/miktex/bin/x64/pdflatex.exe" -interaction=nonstopmode main_v3.tex
```

**Important:** Run twice if you have cross-references or TOC changes.

Check for errors:
- `Overfull \hbox` — minor, ignore (text slightly wider than line)
- `Font shape undefined` — cosmetic, ignore
- `Missing }` — syntax error, fix the tex file

### Step 3: Preview Locally

```bash
# Start the preview server (if not running)
"C:/Program Files/nodejs/node.exe" server.js
```

Open **http://localhost:8888/preview.html** — the iframe auto-loads `main_v3.pdf`.

Click **Refresh PDF** or press **Ctrl+R** to reload after recompiling.

### Step 4: Copy PDF to docs/

GitHub Pages serves from `docs/`, so the PDF must be there:

```bash
cp main_v3.pdf docs/main_v3.pdf
```

### Step 5: Push to GitHub

```bash
git add main_v3.tex main_v3.pdf docs/main_v3.pdf
git commit -m "update: [describe your changes]"
git push origin main
```

### Step 6: Live in ~30 Seconds

GitHub Pages auto-deploys on push. No manual action needed.

**Live URL:** https://kvginnovate.github.io/old-resume/

### Quick Reference (Copy-Paste)

```bash
# Full workflow in one block
cd E:\1_Resume_Prepreation\OLD_Resume
"%LOCALAPPDATA%/Programs/MiKTeX/miktex/bin/x64/pdflatex.exe" -interaction=nonstopmode main_v3.tex
cp main_v3.pdf docs/main_v3.pdf
git add main_v3.tex main_v3.pdf docs/main_v3.pdf
git commit -m "update: your changes here"
git push origin main
```

---

## How It Was Built

### 1. LaTeX Resume

- **Template:** Custom resume template using `article` class with `fontawesome5`, `enumitem`, `hyperref`, `fancyhdr`
- **Custom commands:** `\resumeItem`, `\resumeSubheading`, `\resumeProjectHeading` for consistent formatting
- **Compilation:** `pdflatex -interaction=nonstopmode main_v3.tex`

### 2. Local Preview Server

Node.js server (`server.js`) serves the project directory on port 8888:

```bash
"C:/Program Files/nodejs/node.exe" server.js
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
| `main_v3.tex` | 2 | Latest — improved content with real metrics |

### main_v3 Improvements Over main.tex

- Added GitHub link to heading
- Platform scale numbers (10M+ subscribers, 3+ teams, 50+ engineers)
- Rewrote promotion line (full scope, not just Spring Boot 3)
- Removed corporate fluff ("foster engineering culture")
- Consolidated personal AI tools (cut Paseo/Orca/OMP)
- Merged MCP into "AI & Automation" section
- Moved certifications to own section
- Added 2nd bullets to 1-bullet projects
- Outcome-focused Pivot3 bullets
- Added Kafka, RabbitMQ, GemFire, ELK, PagerDuty to skills
- Added CGPA placeholder in education

---

## Troubleshooting

| Problem | Solution |
|---|---|
| `pdflatex` not found | Use full path: `"%LOCALAPPDATA%/Programs/MiKTeX/miktex/bin/x64/pdflatex.exe"` |
| Port 8888 in use | `netstat -ano \| findstr 8888` → `taskkill -PID <pid> -F` |
| GitHub Pages not updating | Wait 30s, hard refresh (Ctrl+Shift+R), check `git log` |
| PDF blank on mobile | Ensure `docs/index.html` uses PDF.js with `scale = 2` |
| LaTeX errors | Check `main_v3.log` for details |

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
- **Repo:** old-resume
