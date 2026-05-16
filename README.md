# DeepSeek V4 Terminal

A command-line terminal for DeepSeek V4 via Hugging Face Router.

## Usage

```bash
terminal
```

## Adding to PATH

To run `terminal` from anywhere, add this directory to your system PATH.

### Option 1: PowerShell (Admin)

```powershell
[Environment]::SetEnvironmentVariable("Path", [Environment]::GetEnvironmentVariable("Path", "Machine") + ";D:\deepseek_v4_terminal", "Machine")
```

Then restart your terminal.

### Option 2: Manual

1. Open **System Properties** → **Advanced** → **Environment Variables**
2. Under **System variables**, find `Path` and click **Edit**
3. Click **New** and add `D:\deepseek_v4_terminal`
4. Click **OK** and restart your terminal

### Verify

```bash
where terminal
```

Should output:

```
D:\deepseek_v4_terminal\terminal.py
```

## Setup

Set these environment variables via `.env` file or System environment variables:

| Variable | Required | Default | Description |
|---|---|---|---|
| `HF_TOKEN` | Yes | — | Your Hugging Face API token |
| `BASE_URL` | No | `https://router.huggingface.co/v1/chat/completions` | API endpoint URL |

### Option 1: `.env` file

Copy `.env.example` to `.env` and fill in your values:

```bash
copy .env.example .env
```

### Option 2: System environment variables

Add `HF_TOKEN` (and optionally `BASE_URL`) as System environment variables (same steps as adding to PATH above).
