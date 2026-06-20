# Troubleshooting

## LM Studio Refuses Connection

Check the address shown in LM Studio Local Server. From WSL, try:

```bash
curl http://<windows-host-ip>:1234/v1/models
```

If that fails, confirm the LM Studio server is running and the model is loaded.

## PyTorch Install Is Huge

Use the CPU wheel index:

```bash
.venv/bin/python -m pip install --index-url https://download.pytorch.org/whl/cpu --extra-index-url https://pypi.org/simple '.[audio]'
```

Avoid installing PyTorch into a Windows-mounted folder from WSL. It is slow and can look frozen. Keep the venv on the Linux filesystem.

## Weird Pauses Or Run-Ons

Use smaller chunks and explicit pause markers:

```text
I looked at the radio. [[pause:500]] Then I understood.
```

Regenerate only the affected chunk.

## Pronunciation Is Wrong

Add a pronunciation rule:

```yaml
pronunciations:
  - source: "Mara Vey"
    replacement: "Mara Vay"
```

Run a dry run and inspect the chunk text before generating audio.
