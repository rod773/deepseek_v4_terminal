import os
import sys
import json
import urllib.request
import urllib.error

def load_env(path=None):
    if path is None:
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, val = line.partition("=")
            os.environ[key.strip()] = val.strip().strip("\"'")

load_env()
HF_TOKEN = os.getenv("HF_TOKEN")
BASE_URL = os.getenv("BASE_URL", "https://router.huggingface.co/v1/chat/completions")

if not HF_TOKEN:
    print("Error: HF_TOKEN not found in .env")
    sys.exit(1)

def chat(messages):
    data = json.dumps({
        "model": "deepseek-ai/DeepSeek-V4-Pro",
        "messages": messages,
        "max_tokens": 4096,
        "temperature": 1.0,
        "top_p": 1.0,
        "stream": False,
    }).encode()
    req = urllib.request.Request(
        BASE_URL,
        data=data,
        headers={
            "Authorization": f"Bearer {HF_TOKEN}",
            "Content-Type": "application/json",
        },
    )
    try:
        with urllib.request.urlopen(req) as resp:
            result = json.loads(resp.read())
        return result["choices"][0]["message"]["content"]
    except urllib.error.HTTPError as e:
        return f"[HTTP {e.code}] {e.read().decode(errors='replace')}"
    except Exception as e:
        return f"[Error] {e}"

def main():
    print("=" * 60)
    print("  DeepSeek V4 Pro Terminal (via Hugging Face Router)")
    print("  Commands: /exit  /clear")
    print("=" * 60)
    messages = [{"role": "system", "content": "You are DeepSeek V4 Pro, a helpful assistant."}]
    while True:
        try:
            user = input("\n>>> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye.")
            break
        if not user:
            continue
        if user == "/exit":
            print("Goodbye.")
            break
        if user == "/clear":
            messages = messages[:1]
            os.system("cls" if os.name == "nt" else "clear")
            continue
        messages.append({"role": "user", "content": user})
        print("\nDeepSeek: ", end="", flush=True)
        reply = chat(messages)
        print(reply)
        messages.append({"role": "assistant", "content": reply})

if __name__ == "__main__":
    main()
