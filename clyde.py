print("🧨 Starting Clyde...")

# ========== Imports ==========
try:
    import datetime
    print("✅ datetime imported")

    import os
    print("✅ os imported")

    import json
    print("✅ json imported")

    import openai
    print("✅ openai imported")
except Exception as e:
    print(f"💥 CRASHED during import: {e}")
    exit()
from memory.memory_handler import save_to_memory, load_memory, search_memory


# ========== Config Loading ==========
print("📦 Trying to load Clyde's config...")

try:
    with open("clyde_config.json", "r") as f:
        config = json.load(f)
    print("✅ Config loaded")
    memory_data = load_memory()
    print("🔑 Setting OpenAI API key...")
    openai.api_key = config.get("api_key")
    print("🎤 Intro:", config["intro"])
    print("🌀 Entering Clyde chat loop...")
except Exception as e:
    print(f"💥 Failed to load config: {e}")
    exit()

# ========== Constants ==========
MEMORY_FILE = "memory.txt"
CONFIG_FILE = "clyde_config.json"

# ========== Functions ==========

from memory.memory_handler import save_to_memory, load_memory, search_memory

def clyde_response(query, config):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Search memory for relevant context
    keywords = query.lower().split()
    memory_hits = []
    for word in keywords:
        memory_hits.extend(search_memory(word))
    memory_hits = list(set(memory_hits))[-3:]  # De-dupe and limit

    memory_context = ""
    if memory_hits:
        memory_context = "📎 Recalling what you said before:\n" + "\n".join(memory_hits) + "\n\n"

    if config.get("use_gpt", False):
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": (
                            f"You are Clyde, an R-rated, noir-style AI assistant. "
                            f"You're stoic, hyper-logical, commanding, and professional, "
                            f"but swear like a seasoned detective when appropriate. "
                            f"No sugarcoating. Speak with grit and clarity.\n\n"
                            f"Mood: {config['mood']} | Tone: {config['tone']} | Style: {config['style']} | "
                            f"Specialty: {config['specialty']} | Catchphrase: {config['catchphrase']}"
                        )
                    },
                    {
                        "role": "user",
                        "content": memory_context + query
                    }
                ]
            )

            answer = response.choices[0].message.content.strip()
            save_to_memory({"user": query, "clyde": answer})
            return answer
        except Exception as e:
            return f"Error using GPT: {str(e)}"

    # Fallback if GPT is turned off
    if "recall" in query.lower():
        past = recall_memory()[-5:]
        return "Here's what I remember:\n" + "".join(past)
    else:
        return f"{config['catchphrase']} You said: {query}."



# ========== Main Chat Loop ==========

def main():
    try:
        while True:
            query = input("You: ")
            if query.lower() in ["exit", "quit"]:
                print(f"{config['name']}: Shutting down. Try not to break anything.")
                break
            print("🧠 Processing input:", query)
            response = clyde_response(query, config)
            save_to_memory({config["name"]: response})

            print(f"{config['name']}: {response}")
    except Exception as e:
        print(f"💥 Clyde crashed: {e}")

# ========== Entry Point ==========
if __name__ == "__main__":
    main()
