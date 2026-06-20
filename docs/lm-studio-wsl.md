# LM Studio + WSL

LM Studio may advertise a Windows-side address such as:

```text
http://<windows-host-ip>:1234
```

From WSL, `127.0.0.1` can refer to WSL itself rather than Windows. Use the address LM Studio shows in its Local Server panel.

Check connectivity:

```bash
curl http://<windows-host-ip>:1234/v1/models
```

Expected result:

```json
{
  "data": [
    {
      "id": "orpheus-3b-0.1-ft",
      "object": "model"
    }
  ],
  "object": "list"
}
```

Keep LM Studio bound to a local/private interface. Do not expose the endpoint to the public internet.
