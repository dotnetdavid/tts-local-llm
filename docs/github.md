# GitHub Setup

This project is ready for a GitHub remote, but no remote is configured yet.

After creating an empty GitHub repo, run:

```bash
cd /path/to/tts-local-llm
git remote add origin <your-repo-url>
git push -u origin main
```

Before the first commit, check:

```bash
git status --short
git check-ignore -v .venv
```

Do not commit:

- `.venv/`
- generated audio
- `jobs/`
- `outputs/`
- model files
- Hugging Face caches
- `config/local.yaml`
- manuscripts that do not belong in the tool repo
