# Knowledge Garden

A Quarto-based monorepo for **ever-evolving notes** and **chronological blog posts**, with per-note Python virtual environments, per-post alias stability, and Zsh auto-completion for managing content.

---

## 📂 Repository Layout

```
knowledge-garden/
  _quarto.yml
  styles/
    notes-style.css
    blog-style.css
  notes/
    <slug>/
      index.qmd
      _metadata.yml
      .venv/            # optional per-note venv
      pyproject.toml    # optional Python project
      deps.edn          # optional Clojure project
  blog/
    YYYY/
      YYYY-mm-dd-slug.qmd
  templates/
    blog-post.qmd
    note-index.qmd
  scripts/
    blog.sh
    notes.sh
```

---

## 🚀 Blog Workflow

### Create a new blog post

```bash
blog new "Post Title"
```

- Slugified filename: `blog/<year>/YYYY-mm-dd-slug.qmd`
- Alias baked in: `/blog/<year>/slug.html`
- Auto-completion suggests **only current year** posts for `blog open`.

### Open existing blog post

```bash
blog open my-pos<TAB>
```

### List blog slugs

```bash
blog list           # current year
blog list --all     # all years
blog list --year 2024
```

---

## 📝 Notes Workflow

### Create a new note

```bash
notes <slug> --title "Long Descriptive Title"
```

- Creates `notes/<slug>/index.qmd` from `templates/note-index.qmd`
- Slug = short kebab-case name (matches directory)
- Title = long descriptive (front matter)

### Optional: Python-backed note

```bash
notes <slug> --title "..." --py
```

- Creates `.venv` (uses `uv` if available, else `python -m venv`)
- Installs and registers an **ipykernel**: `kg-<slug>`
- Writes `_metadata.yml` to force Quarto to use that kernel
- Adds `.gitignore` for `.venv`, `__pycache__`, etc.

### Optional: Clojure-backed note

```bash
notes <slug> --title "..." --clj
```

- Creates `deps.edn` and `src/`
- Adds `.gitignore` for `target/`, `.cpcache/`

### Open an existing note

```bash
notes <slug>
```

- `cd`s into `notes/<slug>/`
- Activates `.venv` if present
- Opens `index.qmd` in `$EDITOR`

### List all notes

```bash
notes list
```

---

## 🔄 Scripts & PATH

1. **Put scripts in PATH**:

   ```bash
   mkdir -p ~/bin
   ln -sf "$(pwd)/scripts/blog.sh" ~/bin/blog
   ln -sf "$(pwd)/scripts/notes.sh" ~/bin/notes
   export PATH="$HOME/bin:$PATH"
   ```

2. **Zsh completion**:

   **Blog**: `$HOME/.config/zsh/completions/_blog`

   ```zsh
   #compdef blog
   _blog_complete() {
     if (( CURRENT == 2 )); then _arguments '1: :->cmds'; return; fi
     case $words[2] in
       open)
         local -a slugs; slugs=("${(@f)$(blog list)}")
         _describe 'slug' slugs
         ;;
     esac
   }
   _blog_complete "$@"
   ```

   **Notes**: `$HOME/.config/zsh/completions/_notes`

   ```zsh
   #compdef notes
   _notes_complete() {
     if (( CURRENT == 2 )); then
       local -a slugs; slugs=("${(@f)$(notes list)}")
       _describe 'slug' slugs; return
     fi
     if (( CURRENT > 2 )); then
       _arguments '*: :->args' \
         '(-)--title[Set note title]' \
         '(-)--py[Scaffold Python files]' \
         '(-)--clj[Scaffold Clojure files]'
     fi
   }
   _notes_complete "$@"
   ```

   In `.zshrc`:

   ```zsh
   fpath=($HOME/.config/zsh/completions $fpath)
   autoload -Uz compinit
   compinit
   ```

---

## 🐍 Per-Note Python Kernels

Each Python note with `--py`:

- Gets its own `.venv`
- Registers an **ipykernel** named `kg-<slug>`
- `_metadata.yml` in that note forces Quarto to use the kernel:
  ```yaml
  engine: jupyter
  jupyter: kg-<slug>
  execute:
    daemon: false
    cache: true
    freeze: auto
  ```

---

## ✅ Checking Kernel Use

1. Clean & render:

   ```bash
   quarto clean notes/<slug>
   QUARTO_LOG_LEVEL=DEBUG quarto render notes/<slug>/index.qmd
   ```

   Look for:

   ```
   Using Jupyter kernel 'kg-<slug>'
   ```

2. Debug cell:
   ````qmd
   ```{python}
   import sys
   print("python:", sys.executable)
   print("prefix:", sys.prefix)
   ```
   ````

## ♻️ Initializing Kernels for Existing Notes

For a note with .venv but no kernel:

```bash
cd notes/<slug>
source .venv/bin/activate
python -m pip install -U pip ipykernel
python -m ipykernel install --user --name "kg-<slug>" --display-name "Python (kg-<slug>)"
echo "engine: jupyter" > _metadata.yml
echo "jupyter: kg-<slug>" >> _metadata.yml

```

## 🛡 CI / Pre-commit Checks

Prevent accidental jupyter: in index.qmd (must be in \_metadata.yml):

```yaml
repos:
- repo: local
  hooks:
    - id: block-jupyter-in-note-docs
      name: Block 'jupyter:' in notes docs (use _metadata.yml)
      entry: bash -c 'if git grep -n "^[[:space:]]*jupyter:" -- notes | grep -v "_metadata.yml"; then echo "Remove jupyter: from notes docs (use _metadata.yml)"; exit 1; fi'
      language: system
      pass_filenames: false
```

Install:

```yaml
pre-commit install
```

CI check:

```bash
if git grep -n '^[[:space:]]*jupyter:' -- notes | grep -v '_metadata.yml'; then
  echo "Error: use jupyter: only in notes/*/_metadata.yml"; exit 1
fi
```

## 📌 Tips

- freeze: auto is great for large projects; flip to false when testing kernel/env changes.
- Clean stale results with quarto clean notes/<slug>.
- Use daemon: false in \_metadata.yml to prevent cross-note kernel reuse during preview.
- Per-note venvs keep dependencies isolated; avoids polluting global Python.
