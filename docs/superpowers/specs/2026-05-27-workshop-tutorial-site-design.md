# Workshop Tutorial Site — Design

**Date:** 2026-05-27
**Topic:** Docusaurus-based step-by-step tutorial for building the Runoff Depth Calculator
Tethys Component App, published to GitHub Pages.

## Goal

Produce a hosted, step-by-step workshop tutorial that teaches attendees how to build this
app (a Tethys **Component App**) from scratch. Each step introduces and illustrates one
concept with focused code additions. The finished tutorial code matches the app already in
this repo (`app.py` / `compute.py`), so the tutorial is verifiable against `main`.

Modeled on the official Tethys
[Component App Basics tutorial](https://docs.tethysplatform.org/en/latest/tutorials/component_app_basics.html)
and grounded in the
[Components SDK reference](https://docs.tethysplatform.org/en/latest/tethys_sdk/components.html).

## Decisions (settled with stakeholder)

- **Narrative arc:** Scaffold-to-finished. Attendee runs `tethys scaffold`, then builds up
  to the full app over 9 concept-named steps.
- **Checkpoints:** Code snippets in docs only — no per-step git tags or branches.
- **Site scope:** Tutorial only, plus a landing/intro page. Link out to the Tethys SDK docs
  for deep reference (no separate concepts-reference section).
- **Docusaurus root folder:** `workshop/` at the repo root.
- **Local build verification:** Required — `npm run build` must succeed before this is done.

## Architecture

### Site tooling & location

- **Docusaurus 3.x, classic preset, docs-only mode** (blog disabled; docs served at site
  root). Node 20 in CI.
- Self-contained in **`workshop/`** at the repo root (its own `package.json`, `node_modules`,
  build output). No `__init__.py`, so setuptools `packages.find` does not package it; the
  Python app build is unaffected.
- Config for project Pages:
  - `url: https://tethysplatform.github.io`
  - `baseUrl: /tethysapp-runoff_depth_calculator/`
  - `organizationName: tethysplatform`
  - `projectName: tethysapp-runoff_depth_calculator`
- Tutorial markdown lives in `workshop/docs/`. Sidebar ordered by the 9 steps.

### Tutorial content (concept-per-step)

Each step: (1) names the concept, (2) shows the additions (highlighted), (3) ends with a
"full file so far" block and a "what you should see" note.

1. **Set up & scaffold** — `tethys scaffold`, the component-app template, `pip install -e .`,
   `tethys quickstart`.
2. **The App class & page functions** — `ComponentBase`, app metadata (name, package,
   root_url, etc.), `@App.page`, the `lib` namespace.
3. **Adding a Map** — `lib.tethys.Map`, `lib.ol` layer/source, remote GeoJSON,
   props-as-kwargs / children-as-call syntax.
4. **State** — `lib.hooks.use_state`, the re-render model, storing the selected feature
   (`area_sqkm`) and deriving `area_acres`.
5. **Event handlers & the Stepper** — `onClick` / `onChange`, `lib.m.Stepper`, advancing
   `active_step`, `Slider` and `Select` inputs.
6. **The computation layer** — `compute.py` as pure, framework-free NRCS Curve Number logic
   (CN matrix, `S`, `Ia`, runoff equation); calling it from the land-use handler.
7. **Displaying results** — `lib.m.Modal` gated on `result` state, `lib.pl.Plot` (Plotly)
   chart of design-storm runoff volumes.
8. **UX polish** — feature styling via `lib.ol.style.Styler`, "Start Over" reset, making the
   map interactive only on step 0.
9. **Conclusion** — recap of concepts and links to the SDK reference / further tutorials.

In docs-only mode the **intro page is the site root** (`workshop/docs/intro.md` with
`slug: /`). It summarizes the app and what the workshop covers, and states prerequisites
(working Tethys install via Quick Start). No separate React homepage is built.

### CI/CD to GitHub Pages

- Single workflow `.github/workflows/docs.yml`:
  - **Triggers:** push to `main` filtered to `workshop/**` (and the workflow file itself);
    plus `workflow_dispatch`.
  - **Build job:** checkout → setup-node@20 (npm cache) → `npm ci` → `npm run build` in
    `workshop/` → `upload-pages-artifact` pointing at `workshop/build`.
  - **Deploy job:** `deploy-pages` with `pages: write` + `id-token: write` permissions,
    `github-pages` environment.
  - Uses the **official GitHub Pages Actions** (`configure-pages`, `upload-pages-artifact`,
    `deploy-pages`) — no `gh-pages` branch.
  - *Alternative considered:* `docusaurus deploy` pushing a `gh-pages` branch — older,
    needs branch management; rejected.
- **Manual one-time step (stakeholder):** set repo Pages source to "GitHub Actions"
  (Settings → Pages). Documented in the spec/plan; cannot be automated here.

### Repo integration

- `README.md`: add a "Workshop / Tutorial" link to the published site
  (`https://tethysplatform.github.io/tethysapp-runoff_depth_calculator/`).
- `.gitignore`: add `workshop/node_modules`, `workshop/build`, `workshop/.docusaurus`.

## Out of scope

- Per-step solution branches/tags.
- A separate SDK concepts-reference section (link out instead).
- Versioned docs, i18n, search backends beyond Docusaurus defaults.
- Changes to the application code itself (`app.py` / `compute.py`).

## Success criteria

- `cd workshop && npm ci && npm run build` succeeds locally with no broken-link errors.
- Site renders the 9-step tutorial with correct ordering and the landing page.
- `baseUrl` is correct for project Pages (links work under
  `/tethysapp-runoff_depth_calculator/`).
- Workflow file is valid and configured to deploy on push to `main`.
- README links to the site; gitignore excludes build artifacts.
- Tutorial's final code matches the committed `app.py` / `compute.py`.
