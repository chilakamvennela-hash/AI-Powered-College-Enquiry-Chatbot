import re
from nltk.stem import PorterStemmer
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer, ENGLISH_STOP_WORDS
from sklearn.metrics.pairwise import cosine_similarity
from database import get_qa_rows

class CollegeChatbot:
    """Retrieval chatbot using NLTK preprocessing, TF-IDF and cosine similarity."""

    def __init__(self, threshold=0.22):
        self.threshold = threshold
        self.tokenizer = RegexpTokenizer(r"[a-zA-Z0-9']+")
        self.stemmer = PorterStemmer()
        try:
            self.stop_words = set(stopwords.words("english"))
        except LookupError:
            # Offline-safe fallback if the optional NLTK stopwords corpus is unavailable.
            self.stop_words = set(ENGLISH_STOP_WORDS)
        self.rows = []
        self.vectorizer = None
        self.matrix = None
        self.refresh()

    def preprocess(self, text):
        tokens = self.tokenizer.tokenize(str(text).lower())
        cleaned = [
            self.stemmer.stem(token)
            for token in tokens
            if token not in self.stop_words and len(token) > 1
        ]
        return " ".join(cleaned)

    def refresh(self):
        self.rows = get_qa_rows()
        questions = [row["question"] for row in self.rows]
        if not questions:
            self.vectorizer, self.matrix = None, None
            return
        self.vectorizer = TfidfVectorizer(
            tokenizer=str.split,
            preprocessor=self.preprocess,
            token_pattern=None,
            lowercase=False,
            ngram_range=(1, 2)
        )
        self.matrix = self.vectorizer.fit_transform(questions)

    def get_response(self, user_text):
        text = (user_text or "").strip()
        if not text:
            return {"answer": "Please type a question so I can help you.", "matched": False, "score": 0.0}
        if self.matrix is None:
            return {"answer": "The college knowledge base is currently empty. Please contact the administrator.", "matched": False, "score": 0.0}
        query_vector = self.vectorizer.transform([text])
        scores = cosine_similarity(query_vector, self.matrix).flatten()
        best_index = int(scores.argmax())
        best_score = float(scores[best_index])
        if best_score < self.threshold:
            answer = (
                "I'm sorry, I couldn't find a reliable answer to that question. "
                "Please try asking about admissions, courses, fees, exams, scholarships, "
                "hostel, transport, library, faculty, placements or college contact details."
            )
            return {"answer": answer, "matched": False, "score": round(best_score, 3)}
        return {
            "answer": self.rows[best_index]["answer"],
            "matched": True,
            "tag": self.rows[best_index]["tag"],
            "score": round(best_score, 3)
        }
