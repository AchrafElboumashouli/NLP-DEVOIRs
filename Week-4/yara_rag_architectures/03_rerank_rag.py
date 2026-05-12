
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


def rerank(query, docs, top_k=2):

    query_words = set(query.lower().split())

    reranked = []

    for doc in docs:

        doc_words = set(
            doc["description"].lower().split()
        )

        overlap = len(
            query_words & doc_words
        )

        score = (
            0.7 * doc["score"] +
            0.3 * overlap
        )

        reranked.append({
            **doc,
            "rerank_score": score
        })

    reranked.sort(
        key=lambda x: x["rerank_score"],
        reverse=True
    )

    return reranked[:top_k]


def rag_rerank(query):

    docs = retrieve(query, k=5)

    best_docs = rerank(query, docs)

    context = "\n".join([
        d["description"]
        for d in best_docs
    ])

    prompt = f"""
Use these best matches:

{context}

Generate YARA rule for:
{query}
"""

    raw = generate_yara(prompt)

    return raw, best_docs


if __name__ == "__main__":

    rule, docs = rag_rerank(
        "Credential stealing malware"
    )

    print(rule)
