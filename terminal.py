import os
import json
import requests

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
OPENROUTER_KEY = os.getenv("OPENROUTER_KEY")

def chat(messages):
    response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {OPENROUTER_KEY}",
            "Content-Type": "application/json",
        },
        data=json.dumps({
            "model": "deepseek/deepseek-v4-flash:free",
            "messages": messages,
            "max_tokens": 4096,
            "temperature": 1.0,
            "top_p": 1.0,
            "reasoning": {"enabled": True},
        })
    )
    try:
        response = response.json()
        msg = response['choices'][0]['message']
        return msg.get('content'), msg.get('reasoning_details')
    except Exception as e:
        return f"[Error] {e}", None

def main():
    print("=" * 60)
    print("  DeepSeek V4 Flash Terminal (via OpenRouter)")
    print("  Commands: /exit  /clear")
    print("=" * 60)
    messages = [{"role": "system", "content": "You are DeepSeek V4 Flash, a helpful assistant."}]
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
        content, reasoning_details = chat(messages)
        print(content)
        assistant_msg = {"role": "assistant", "content": content}
        if reasoning_details:
            assistant_msg["reasoning_details"] = reasoning_details
        messages.append(assistant_msg)

if __name__ == "__main__":
    main()
