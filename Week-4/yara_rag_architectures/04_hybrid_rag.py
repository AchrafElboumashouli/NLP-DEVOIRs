
import numpy as np
from collections import defaultdict
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer

# =========================================================
# DATASET PLACEHOLDERS
# =========================================================

DOCUMENTS = [
    "Ransomware encrypting user files",
    "Keylogger capturing keyboard input",
    "Trojan malware downloading payloads"
]

YARA_RULES = [
    "rule ransomware_sample { condition: true }",
    "rule keylogger_sample { condition: true }",
    "rule trojan_sample { condition: true }"
]

CATEGORIES = [
    "ransomware",
    "spyware",
    "trojan"
]

# Fake embeddings for demonstration
original_embeddings = np.random.rand(3, 384)

# =========================================================
# EMBEDDING MODEL PLACEHOLDER
# =========================================================

class DummyEmbedder:

    def encode(self, texts):
        return np.random.rand(len(texts), 384)

EMBED_MODEL = DummyEmbedder()

# =========================================================
# LLM GENERATION
# =========================================================

def generate_yara(prompt):

    return f"""
rule generated_rule
{{
    meta:
        description = "Generated YARA rule"

    strings:
        $a = "malware"

    condition:
        $a
}}
"""


def format_yara_rule(raw_rule, query, category):

    return raw_rule


# =========================================================
# DENSE RETRIEVAL
# =========================================================

def retrieve(query, k=3):

    results = []

    for i in range(min(k, len(DOCUMENTS))):

        results.append({
            "description": DOCUMENTS[i],
            "yara_rule": YARA_RULES[i],
            "category": CATEGORIES[i],
            "score": 0.95 - i * 0.1,
            "idx": i
        })

    return results


TFIDF_VECTORIZER = TfidfVectorizer()

TFIDF_MATRIX = TFIDF_VECTORIZER.fit_transform(
    DOCUMENTS
)


def sparse_retrieve(query, k=3):

    q_vec = TFIDF_VECTORIZER.transform([query])

    scores = cosine_similarity(
        q_vec,
        TFIDF_MATRIX
    )[0]

    top_indices = np.argsort(scores)[::-1][:k]

    results = []

    for idx in top_indices:

        results.append({
            "description": DOCUMENTS[idx],
            "yara_rule": YARA_RULES[idx],
            "category": CATEGORIES[idx],
            "score": float(scores[idx]),
            "idx": idx
        })

    return results


def hybrid_retrieve(query):

    dense_docs = retrieve(query)

    sparse_docs = sparse_retrieve(query)

    fused = defaultdict(float)

    docs_store = {}

    for rank, doc in enumerate(dense_docs):

        fused[doc["idx"]] += 1 / (rank + 60)

        docs_store[doc["idx"]] = doc

    for rank, doc in enumerate(sparse_docs):

        fused[doc["idx"]] += 1 / (rank + 60)

        docs_store[doc["idx"]] = doc

    final_docs = sorted(
        fused.items(),
        key=lambda x: x[1],
        reverse=True
    )

    return [
        docs_store[idx]
        for idx, _ in final_docs
    ]


if __name__ == "__main__":

    docs = hybrid_retrieve(
        "Phishing malware"
    )

    print(docs)
