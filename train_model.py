import nltk
from database import init_db
from chatbot import CollegeChatbot

def main():
    print("Preparing NLTK stopwords (uses a local fallback if offline)...")
    try:
        nltk.download("stopwords", quiet=True)
    except Exception:
        print("Could not download NLTK stopwords; the built-in fallback will be used.")
    print("Initializing SQLite database...")
    init_db()
    print("Training TF-IDF question-matching model...")
    bot = CollegeChatbot()
    print(f"Model ready. Indexed {len(bot.rows)} sample questions.")
    print("Training complete.")

if __name__ == "__main__":
    main()
