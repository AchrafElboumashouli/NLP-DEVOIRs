
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


def reformulate_query(query, docs):

    if not docs:
        return query

    category = docs[0]["category"]

    return f"{query} AND {category} behavior"


def multi_hop_rag(query, hops=2):

    all_docs = []

    current_query = query

    for _ in range(hops):

        docs = retrieve(current_query)

        all_docs.extend(docs)

        current_query = reformulate_query(
            current_query,
            docs
        )

    context = "\n".join([
        d["description"]
        for d in all_docs
    ])

    prompt = f"""
Context:
{context}

Generate YARA rule for:
{query}
"""

    raw = generate_yara(prompt)

    return raw, all_docs


if __name__ == "__main__":

    rule, docs = multi_hop_rag(
        "Advanced persistent threat"
    )

    print(rule)
