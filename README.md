# Flast
Flast is a *Static Site Generator* (SSG) for documentation focused on human and AI use. Used in all my projects. 

## Features
- SEO compliant (robots.txt + sitemap.xml)
- Supports all filetypes (.ico, .jpeg...)
- Image conversion to .webp for faster loading times
- Code highlighting + copy
- Nav bar positioning
- Deployment options

## Getting Started
1. Clone the code from the Github repo.   
2. (optional) Create Virtual Environment
3. Install dependencies
```Bash
#Virtual Environment
python -m venv .venv
.venv/Scripts/activate
# Dependencies
pip install -r requirements.txt
```
Then
```Bash
python main.py
```
to start the wizard. 

### Deploy to Netlify
Select `Netlify` under `Deploy` → `Netlify`. 
If the configured domain is still `http://localhost/`, Flast
first deploys a temporary one-file page, saves Netlify's production URL in the
configuration, regenerates the site (including sitemap and robots URLs), and
then deploys the real `public/` files. When a domain is already configured,
Flast deploys `public/` directly.

Before your first deployment, install the [Netlify CLI](https://docs.netlify.com/api-and-cli-guides/cli-guides/get-started-with-cli/) and authenticate it:
```Bash
npm install -g netlify-cli
netlify login
```
The first deployment will let the Netlify CLI link this project to an existing
site or create one. Flast does not store Netlify credentials. The deployment
system is provider-based so future services can add their own adapter without
changing the generation flow.

Flast stores URLs per provider in `core.urls`. An explicitly configured URL is
saved as `self` and is used for generated sitemap and robots URLs first;
otherwise Flast uses the first provider URL that was successfully saved.

### Deploy to GitHub Pages

Select `GitHub Pages` from `Deploy` → `Third Party`. Flast publishes only the
generated files to a managed `gh-pages` branch, adds `.nojekyll`, and enables
GitHub Pages from that branch when it is not already enabled. It will not
replace an existing Pages configuration that uses another branch or folder.
You can publish to the current repository, specify another `owner/repository`,
or create a new repository in your authenticated GitHub account.

Install [GitHub CLI](https://cli.github.com/) and authenticate first:

```Bash
gh auth login
```

### Deploy to Cloudflare Pages

Select `Cloudflare Pages` from `Deploy` → `Third Party`, then choose an
existing Pages project or create a new one. Flast uses Cloudflare Pages Direct
Upload and saves the returned `pages.dev` URL under `cloudflare-pages`.

Install Wrangler and authenticate first:

```Bash
npm install -g wrangler
wrangler login
```

### Deploy to Surge

Select `Surge` from `Deploy` → `Third Party`. On the first deployment, Flast
asks for a `.surge.sh` or custom domain, so Surge can publish without an
invisible CLI prompt. Flast saves the resulting production URL under `surge`,
regenerates the site with that URL, and uses it for later non-interactive
deployments.

Install the Surge CLI, then complete its interactive sign-in the first time
you deploy:

```Bash
npm install -g surge
surge
```

### Deploy to a self-hosted Linux server

Set your public URL in `Configure` → `Core`; it is stored as the `self` URL and
used in generated sitemap and robots files. Then select `Deploy` →
`Self-Hosted/VPS` and enter the Linux host, SSH user, port, and absolute web
directory. Flast saves those non-secret connection details for later deploys.

The local machine needs `ssh` and `rsync` on `PATH`; the Linux server needs
both tools and a user that can write the configured directory. On Windows,
Flast automatically falls back to `wsl rsync` when native rsync is absent. Set
up WSL with a Linux distribution, then install `rsync` and `openssh-client`
inside that distribution. Flast previews the rsync mirror, shows any
`*deleting` entries, and asks for confirmation before applying the preview.
The destination directory is created by rsync when needed. Authentication is
handled by SSH: an SSH agent/key is preferred, but password prompts also work
and are never saved.

You can easily install `rsync` on Windows by installing `WSL` and a Linux distribution.

#### .md
Should have a heading e.g: (minimum = title)
```yaml
---
title: Welcome
weight: 0
sitemap:
  lastmod: "YYYY-MM-DD"
  changefreq: "monthly"
  priority: "0.5"
---
```
Then the rest of the .md file. 

## Example
Content contains example  documentation of FlanOS. Find it here:   
[FlanOS Documentation](https://flanos.forageek.com/)
