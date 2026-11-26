# TRTT MAGIC AI Tool Builder — Free Automated Test Setup

**Branch:** `feature/trtt-magic-ai-tool-builder-mvp-v1`  
**Test type:** Python standard-library source-contract tests  
**Cost:** Free; no third-party package, API key, paid browser, or external service.

## What is checked

The test suite checks the fixed HTML source for:
- HTML document and mobile viewport metadata
- Required form controls and required-field validation hooks
- SEO, Blog Outline, and FAQ template hooks
- Prompt construction and safe text rendering
- Clipboard action and its manual-copy fallback
- JSON Blob/download implementation
- Responsive breakpoints, keyboard focus, and reduced-motion support
- No external scripts/stylesheets or network request APIs
- No eval/dynamic Function or browser storage
- Only the approved TRTT palette hex values

## Run locally (Android Termux or desktop)

From the repository root, run:

```sh
python --version
python -m unittest discover -s products/trtt-magic-ai-tool-builder/tests -v
```

No `pip install` is needed. The tests use Python's built-in `unittest`, `html.parser`, `pathlib`, and `re` modules.

If Termux does not have Python yet, the optional free install command is:

```sh
pkg install python -y
```

Installing Python is optional and has not been performed by this setup.

## Reading the result

- `OK`: all source-contract checks passed.
- `FAIL`: at least one assertion found a source mismatch; inspect the named test.
- `ERROR`: test setup/runtime issue, such as a missing HTML file or Python environment problem.

## Important limitation

These are automated **source-level** tests. They do not launch Chromium, click the UI, test real clipboard permissions, confirm a downloaded file, or measure visual layout on a physical phone. Browser runtime and mobile/desktop visual checks remain **NOT TESTED** until a real browser run is performed.

## Preservation and deployment

The test suite is additive. It does not replace or edit `index.html`, `index-v2-fixed.html`, or `trttmagic.html`. It does not create a GitHub Actions workflow, merge a branch, publish to Blogger, or deploy the product.


## Real browser end-to-end tests (GitHub Actions)

A separate Chromium/Playwright workflow is defined in
`.github/workflows/trtt-ai-tool-builder-e2e.yml`. It runs only on the MVP feature
branch or when manually dispatched. It starts a temporary local HTTP server in the
GitHub-hosted runner and checks page load, all starter templates, required-field
validation, prompt generation, clipboard writing, JSON download/parsing, reset,
and mobile layout overflow/panel stacking.

The browser test dependency is installed temporarily on the runner with npm; no
package manifest, lockfile, API key, repository secret, or paid browser service is
required. GitHub-hosted runner usage may still be subject to the account's Actions
minutes/usage limits.

These tests exercise Chromium in a hosted Linux runner. They are not a physical
Android device test and do not certify every mobile browser.
