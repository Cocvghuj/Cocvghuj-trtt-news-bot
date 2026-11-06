# Vercel Production Deployment Lock

TRTT builds are fail-closed for Vercel Production.

## Default behavior

When `VERCEL_ENV=production`, `build.js` exits before generating the static output unless:

```text
TRTT_PRODUCTION_DEPLOY_APPROVED=true
```

The variable must be configured in the Vercel **Production** environment only, and only after the repository owner explicitly authorizes a production release. Do not add it to Preview or Development environments.

## What remains available

- GitHub CI can run the normal build without Vercel environment variables.
- Vercel Preview deployments are not blocked by this production-only guard.
- The Blogger workflow remains manual and DRAFT-only.
- The Blogger workflow has read-only repository permissions and does not push commits to `main`.

## Verification

CI runs `VERCEL_ENV=production node build.js` without the approval variable and requires the build to fail with the TRTT Production Lock message.

This is a build-time safety barrier. It does not replace GitHub branch protection or Vercel team access controls; those must be configured separately by the repository owner.
