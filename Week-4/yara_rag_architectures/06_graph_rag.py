
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

import networkx as nx

def build_graph():

    G = nx.Graph()

    G.add_edge(0, 1)

    G.add_edge(1, 2)

    return G


def graph_retrieve(query, G):

    q_emb = EMBED_MODEL.encode([query])

    similarities = cosine_similarity(
        q_emb,
        original_embeddings
    )[0]

    best_idx = int(np.argmax(similarities))

    neighbors = list(
        G.neighbors(best_idx)
    )

    candidate_nodes = [best_idx] + neighbors

    docs = []

    for idx in candidate_nodes:

        docs.append({
            "description": DOCUMENTS[idx],
            "yara_rule": YARA_RULES[idx],
            "category": CATEGORIES[idx],
            "idx": idx
        })

    return docs


if __name__ == "__main__":

    G = build_graph()

    docs = graph_retrieve(
        "Botnet malware",
        G
    )

    print(docs)
