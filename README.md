# Coursework Archive Source

This folder is the source tree behind the public coursework archive on `vmoor.com`.

## Layout

- `NAU/NAU/<semester>/<course>/...`
- reports, labs, briefs, and writeups stay in the course folders
- code projects stay alongside the class material they came from

## What belongs here

- final reports and polished writeups
- screenshots and supporting visuals
- code that backs the coursework
- curated project data and results when you want them public

## What stays out

The root `.gitignore` keeps local-only clutter out of the repo by default:

- virtual environments and caches
- compiled binaries
- local secrets and auth material
- password wordlists
- editor and OS noise

## Site connection

The site repo at `../vmoor` rebuilds its public archive from this folder.

When this folder is published to GitHub, update:

- `C:\Users\tyler\Desktop\vmoor\vmoor\scripts\coursework-project-links.json`

Set `__defaults.githubBaseUrl` to the repo tree URL ending at `NAU/NAU`, then rebuild the site archive. After that, the coursework code cards on the site will link straight back to the matching folders in this repo.
