# How this is published

Written down so none of it has to be worked out twice.

## Layout

The local working folder is `~/teaching-interactive`. The git repository is the
`github/` subfolder inside it, so drafts, data preparation, and scratch work can sit
beside the repository without being pushed.

```
~/teaching-interactive/          local working folder, not a repository
└── github/                      the repository
    ├── README.md
    ├── CLAUDE.md
    ├── LICENSE                  MIT, for code
    ├── LICENSE-CC-BY-4.0        CC BY 4.0, for text and figures
    ├── .github/workflows/
    │   └── pages.yml            publishes web/ to GitHub Pages
    ├── docs/                    documentation for us, not published
    └── web/                     the published site
        ├── index.html
        ├── shared/              stylesheets and scripts used by several widgets
        └── <widget>/            one folder per widget
```

Remote: `git@github-teaching:FoldingSpace/interactive.git`
Live site: https://foldingspace.github.io/interactive/

## Credentials

Pushes use a **deploy key**, not an account credential. The key is an ed25519 pair at
`~/.ssh/interactive_deploy`, registered on the repository under Settings → Deploy keys
with write access.

This was deliberate. A deploy key is scoped to one repository and cannot reach anything
else in the account. It also stays clear of the two pieces of shared credential storage
on this machine — the `gh` CLI keyring login and the `github.com` entry in the macOS
keychain — either of which would have been disturbed by `gh auth login` or by an HTTPS
remote, breaking unrelated work.

A host alias in `~/.ssh/config` keeps the key from being offered to anything else:

```
Host github-teaching
  HostName github.com
  User git
  IdentityFile ~/.ssh/interactive_deploy
  IdentitiesOnly yes
```

`IdentitiesOnly yes` matters. Without it, ssh offers the other keys in `~/.ssh` first and
authenticates as the account by accident.

Check it with `ssh -T git@github-teaching`, which should answer
`Hi FoldingSpace/interactive!` — the repository name, not a username.

To revoke: delete the deploy key in the repository settings. That is immediate, complete,
and affects nothing else.

**A deploy key does git only.** No `gh` commands, so no issues, pull requests, or API
calls. If those are ever needed, the non-disruptive route is a fine-grained personal
access token scoped to this repository alone, kept in a gitignored file and passed per
command as `GH_TOKEN=$(cat …)`, which overrides the keyring for that one invocation
without writing to it. Never `gh auth login` with it.

## Publishing

Pages is set to **Source: GitHub Actions**, and `.github/workflows/pages.yml` uploads
`web/` as the artifact.

The workflow exists because GitHub Pages, when serving from a branch, can only be pointed
at the repository root or at a folder named `docs/`. Neither suited us: the root would
publish the documentation and licence files along with the site, and `docs/` was already
taken by our own documentation. Publishing through Actions takes any folder, so `web/`
stays exactly what is public and `docs/` stays private to the repository.

Verified: `https://foldingspace.github.io/interactive/docs/principles.md` returns 404,
so only `web/` is being served.

Deploys run on every push to `main`, and can be run by hand from the Actions tab.

## Working on it locally

The widgets are static files, so any local server will do:

```
python3 -m http.server 8791 --directory ~/teaching-interactive/github/web
```

Then open `http://localhost:8791/<widget>/`. Do not use `file://`: `history.replaceState`,
which is how the configuration lives in the URL, is unreliable there, and Blob workers are
blocked in some browsers.

`template/` sits outside `web/`, so it is not published and the server above cannot reach
it. To look at it, serve the repository root instead:

```
python3 -m http.server 8792 --directory ~/teaching-interactive/github
```

and open `http://localhost:8792/template/`.

If Claude Code is driving the browser, both servers are configured in
`.claude/launch.json` as `widgets` and `repo` — note that the file is read from the
**primary** working directory the session was launched in, not from this repository.

## Things that bit us

**GitHub Pages cannot serve an arbitrary subfolder from a branch.** Root or `docs/` only.
Hence the Actions workflow.

**`git` on this machine is 2.16.2, from 2018.** No `git init -b`, among other omissions.
Use `git init` followed by `git symbolic-ref HEAD refs/heads/main`. `brew install git`
would fix this whenever it becomes worth doing.

**Old DSA entries broke `ssh-keygen -R`.** `~/.ssh/known_hosts` held two `ssh-dss` lines
for long-dead hosts. OpenSSH 10 has removed DSA entirely, so it read those lines as
invalid and refused to rewrite the file at all. Stripping them with
`grep -v ' ssh-dss '` fixed it.

**The stale GitHub host key.** `known_hosts` still held the RSA key GitHub retired in
March 2023, so the first connection reported a changed host key. The presented
fingerprint was checked against `https://api.github.com/meta` over HTTPS — an
independent trust path — before the old entry was removed. Several decade-old GitHub IP
entries remain in the file and may yet cause a similar warning.

**Deploy keys can push workflow files.** The `workflow` scope restriction applies to
tokens, not to SSH deploy keys.

**`git` 2.16 has no `git init -b`.** Use `git init` then
`git symbolic-ref HEAD refs/heads/main`.

**Test resources can look exactly like a bug.** Several probes created Web Workers and did
not terminate them; the leftovers saturated the worker pool and the widget's own
significance test appeared to hang for thirty seconds. It was diagnosed as a hung
computation and very nearly "fixed". Reload the page between measurements, terminate
anything a probe starts, and when something that worked starts hanging, suspect the
measuring apparatus before the thing being measured.

**`[hidden]` loses to any author `display` rule.** An element styled
`display: grid` or `display: flex` ignores the `hidden` attribute, because the browser's
`[hidden] { display: none }` is a user-agent style and author styles outrank it. Add an
explicit `[hidden] { display: none }` for any element you both style and hide.

**CSS specificity beats media queries.** A rule written as `body[data-present="1"] #grid`
outranks `#grid` inside a media query, no matter what the media query says, and a stale
rule of that shape survived a layout rewrite and forced a grid to 435 px inside a 282 px
wrapper. When a layout misbehaves after a rewrite, grep for old selectors on the same
element before anything else.
