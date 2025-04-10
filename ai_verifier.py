# ai_verifier.py (finalized)

import subprocess
import json

def is_ollama_available():
    try:
        result = subprocess.run(["ollama", "list"], capture_output=True, text=True)
        return "mistral" in result.stdout.lower()
    except Exception:
        return False

def verify_with_ai(options, ocr_text):
    if not is_ollama_available():
        print("[⚠️] Ollama AI not available.")
        return []

    prompt = (
        f"From the following chart text:\n{ocr_text}\n\n"
        f"And live option chain data:\n{json.dumps(options[:10], indent=2)}\n\n"
        f"Return only the best trading suggestions (max 3), "
        f"in JSON list format like:\n"
        f"[{{'type': 'CALL', 'strike': 22500, 'confidence': 0.8, 'reason': 'volume + trend'}}]"
    )

    try:
        result = subprocess.run(
            ["ollama", "run", "mistral", prompt],
            capture_output=True, text=True, timeout=10
        )
        text = result.stdout
        print("[🤖] AI response:\n", text)

        # Try to parse JSON list
        if "[" in text:
            start = text.index("[")
            parsed = json.loads(text[start:])
            return parsed if isinstance(parsed, list) else []
    except Exception as e:
        print("[❌] AI parsing failed:", e)

    return []
