# ?? KALKI AI — .is-a.dev Domain Registration Guide

This guide walks you through claiming and activating your free **kalki-1.5.is-a.dev** (or **kalki-1-5.is-a.dev**) domain from [is-a.dev](https://is-a.dev/).

---

## ?? Domain Registration Steps

### Step 1: Fork the is-a-dev/register Repository
1. Go to: **[https://github.com/is-a-dev/register](https://github.com/is-a-dev/register)**
2. Click **Fork** in the top-right corner to fork it to your account (KGupta171025/register).

### Step 2: Add your Domain JSON File
1. In your forked repository, navigate to the domains/ folder.
2. Click **Add file** -> **Create new file**.
3. Name the file **kalki-1.5.json** (or **kalki-1-5.json**).
4. Paste the following JSON configuration:

\\\json
{
  "description": "KALKI AI — Krishna Artificial Lattice Keystone Intelligence Operating System",
  "repo": "https://github.com/KGupta171025/KALKI-1.5",
  "owner": {
    "username": "KGupta171025",
    "email": "kgupta171025@gmail.com"
  },
  "record": {
    "CNAME": "kgupta171025.github.io"
  }
}
\\\

*(Note: Replace \email\ with your personal or preferred contact email if different).*

### Step 3: Open a Pull Request
1. Commit the file to your fork.
2. Click **Contribute** -> **Open pull request** against \is-a-dev/register:main\.
3. Give it a title like: \Add kalki-1.5.is-a.dev\
4. The automated CI bot will test your record and approve/merge it.

---

## ?? Repository & GitHub Pages Setup (Already Prepared!)

The KALKI 1.5 repository is already configured for this custom domain:
1. **CNAME file**: Contains \kalki-1.5.is-a.dev\ at the repository root.
2. **GitHub Actions Workflow** (\.github/workflows/deploy-pages.yml\): Automatically bundles and preserves the \CNAME\ file in the GitHub Pages artifact on every commit.
3. **Next.js Config** (\rontend/next.config.js\): Configured with \asePath: ''\ for custom root domain serving.

### Step 4: Enable Custom Domain in GitHub Repository Settings
Once your PR is merged on \is-a-dev/register\:
1. Go to your repository settings: **[https://github.com/KGupta171025/KALKI-1.5/settings/pages](https://github.com/KGupta171025/KALKI-1.5/settings/pages)**
2. Under **Custom domain**, ensure **kalki-1.5.is-a.dev** (or \kalki-1-5.is-a.dev\) is entered.
3. Wait a few minutes for DNS propagation, then check **Enforce HTTPS**.

Your site will now be live at **https://kalki-1.5.is-a.dev**!
