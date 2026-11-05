# Personal Octop v1.0.3b3

This branch starts at the official `v1.0.3b3` tag and retains:

- The independent `image-inspector` plugin from PR #2286.
- Localized media-delivery failures and content deduplication from PR #2683.
- Cron tool-preamble filtering from PR #2684.
- The current-turn attachment guard already included in the official release.
- The personal memory auxiliary-call stream guard, adapted to harness 1.0.7.

The memory guard lives in the installed harness dependency. Apply and verify it
with the Python interpreter used by the deployment:

```sh
python scripts/apply-personal-harness-patch.py --check
python scripts/apply-personal-harness-patch.py
python scripts/verify-personal-harness-patch.py
```

The patch preserves the upstream empty-callback configuration and adds the
`memory_aux` metadata marker and protocol filter. It does not change model
selection, retries, temperature handling, or memory storage.

Existing plugins, configuration, users, agents, channels, schedules and workspace
content are deployment data. Keep them in the existing Octop data directory.
Back up the SQLite database before starting a new version because startup may
apply schema migrations. Keep the previous environment for rollback.

The existing server's optional local-vector capability is retained with
`fastembed==0.9.1`, which supports the release's required Pillow 13. Keep the
existing embedding model directory; upgrading the Python package does not
require replacing stored models or changing configured providers.
