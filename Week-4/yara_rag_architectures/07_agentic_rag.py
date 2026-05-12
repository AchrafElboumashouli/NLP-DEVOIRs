
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


def choose_strategy(query):

    q = query.lower()

    if "encrypt" in q or "bitcoin" in q:
        return "graph"

    if "email" in q or "keylogger" in q:
        return "rerank"

    return "hybrid"


def agentic_rag(query):

    strategy = choose_strategy(query)

    if strategy == "graph":

        result = "Using Graph RAG"

    elif strategy == "rerank":

        result = "Using Re-ranking RAG"

    else:

        result = "Using Hybrid RAG"

    return {
        "query": query,
        "strategy": strategy,
        "result": result
    }


if __name__ == "__main__":

    response = agentic_rag(
        "Ransomware using bitcoin payments"
    )

    print(response)
