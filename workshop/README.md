# Runoff Depth Calculator Workshop Website

This is the source for the workshop tutorial site, built with
[Docusaurus](https://docusaurus.io/), a modern static website generator. The published site
lives at <https://tethysplatform.github.io/tethysapp-runoff_depth_calculator/>.

## Prerequisites

### Node.js and npm

Docusaurus 3 requires **Node.js 20 or newer** (this project pins `>=20.0`). npm is bundled
with Node.js, so installing Node gives you both.

- Install from <https://nodejs.org/> (choose the LTS release), or use a version manager such
  as [nvm](https://github.com/nvm-sh/nvm):

  ```bash
  nvm install 20
  nvm use 20
  ```

- Verify:

  ```bash
  node --version   # should be >= 20
  npm --version
  ```

### Yarn (optional)

npm works out of the box, so Yarn is optional. If you prefer Yarn, the easiest way is
[Corepack](https://nodejs.org/api/corepack.html), which ships with Node 20:

```bash
corepack enable
corepack prepare yarn@stable --activate
yarn --version
```

Alternatively, install it globally with npm: `npm install -g yarn`.

### Docusaurus

You do **not** need to install Docusaurus globally — it is a dependency of this project and
is installed by the commands below. (This site was originally generated with
`npx create-docusaurus@latest workshop classic`.)

## Installation

From this `workshop/` directory, install the project dependencies:

```bash
npm install
# or
yarn
```

## Local development

```bash
npm start
# or
yarn start
```

This starts a local development server and opens a browser window. Most changes are
reflected live without restarting the server.

## Build

```bash
npm run build
# or
yarn build
```

This generates static content into the `build` directory, which can be served by any static
hosting service.

## Deployment

Deployment is **automatic**. The GitHub Actions workflow at
[`.github/workflows/docs.yml`](../.github/workflows/docs.yml) builds this site and publishes
it to GitHub Pages whenever changes under `workshop/` are pushed to the `main` branch — there
is no manual deploy command to run.

> One-time setup: in the repository on GitHub, go to **Settings → Pages → Build and
> deployment** and set **Source** to **"GitHub Actions"**. Until this is set, the first
> deployment run will fail.
