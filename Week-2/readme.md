# 🚗 NLP Pipeline for Structuring the Moroccan Highway Code

## 📌 Project Overview

This project implements a complete **Natural Language Processing (NLP) pipeline** for transforming raw legal text from the **Moroccan Highway Code** into a structured and machine-readable dataset.

The notebook processes both:

- 🇲🇦 Arabic legal text
- 🇫🇷 French legal text

and automatically extracts:

- Traffic infractions
- Financial penalties
- Point deductions
- Vehicle categories
- Speed limits
- Alcohol limits
- License suspension information
- Legal metadata

The final result is exported into a structured CSV dataset named:

```bash
export_final.csv
```

---

# 🎓 Academic Context

**Master IASD 2026 — Week 2 Assignment**  
Université Abdelmalek Essaadi — FST Tanger  
Professor: **Pr. I. BENABDELOUAHAB**

Developed by:

**ACHARF EL BOUMASHOULI**

---

# 🧠 Main Objectives

The objective of this project is to build a robust multilingual NLP system capable of:

✅ Cleaning Arabic legal text  
✅ Segmenting legal articles  
✅ Extracting legal entities using Regex and NLP techniques  
✅ Structuring information into tabular format  
✅ Applying Machine Learning clustering on infractions  
✅ Comparing rule-based NLP vs pre-trained NER approaches  
✅ Exporting a reusable legal dataset

---

# 📂 Project Structure

```bash
.
├── devoir1_nlp_code_route.ipynb
├── export_final.csv
├── README.md
└── requirements.txt
```

---

# ⚙️ Technologies Used

## Core Libraries

- Python 3.x
- Pandas
- NumPy
- Regex (`re`)
- scikit-learn
- spaCy
- PyArabic

## NLP Techniques

- Arabic normalization
- Rule-based NLP
- Regex entity extraction
- TF-IDF vectorization
- KMeans clustering
- Named Entity Recognition (NER)

---

# 📥 Installation

## 1. Clone the Repository

```bash
git clone https://github.com/Achrafelboumashouli/nlp-code-route.git
cd nlp-code-route
```

## 2. Create a Virtual Environment (Optional)

```bash
python -m venv venv
```

### Activate Environment

#### Windows

```bash
venv\Scripts\activate
```

#### Linux / macOS

```bash
source venv/bin/activate
```

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 📦 Requirements

Create a `requirements.txt` file with:

```txt
pandas
numpy
scikit-learn
spacy
pyarabic
```

Optional French spaCy model:

```bash
python -m spacy download fr_core_news_sm
```

---

# 📚 Dataset Description

The corpus is extracted from:

📖 **Bulletin Officiel n° 5874 (16-09-2010)**  
Moroccan Highway Code

Official source:

https://www.sgg.gov.ma/BulletinOfficiel.aspx

The notebook includes representative examples in:

- Arabic
- French

Each article may contain:

- Legal obligations
- Speed regulations
- Financial penalties
- Point deductions
- Driving restrictions

---

# 🔄 NLP Pipeline

## 1️⃣ Arabic Text Normalization

The project first normalizes Arabic legal text.

### Operations performed:

- Remove Tashkeel (diacritics)
- Normalize Hamza
- Normalize Ya
- Normalize Ta Marbuta
- Remove Tatweel
- Remove extra spaces
- Remove noisy characters

### Example

Before:

```text
يُحدَّد الحد الأقصى للسرعة
```

After:

```text
يحدد الحد الاقصى للسرعه
```

---

# ✂️ 2️⃣ Article Segmentation

Legal articles are segmented automatically using Regex patterns.

### Arabic Pattern

```python
(?:مادة|ماده)\s+(\d+)
```

### French Pattern

The French version is segmented similarly using article numbering.

The output structure:

```python
(article_id, article_body)
```

---

# 🧾 3️⃣ Infraction & Sanction Separation

Each legal article is divided into:

## Infraction Section

Contains:

- The offense
- Legal rule
- Driving restriction

## Sanction Section

Contains:

- Fine amount
- Point deduction
- Suspension information

---

# 🔍 4️⃣ Entity Extraction (Regex-based NLP)

The notebook extracts legal entities using handcrafted Regex patterns.

## Extracted Entities

| Entity | Description |
|---|---|
| `amende_fixe` | Fine amount |
| `points_retrait` | License points removed |
| `vitesse_limite` | Speed limit |
| `suspension_permis` | License suspension |
| `taux_alcool_g_l` | Alcohol level |
| `categorie_vehicule` | Vehicle category |
| `type_infraction` | Type of offense |

---

# 🧠 5️⃣ Machine Learning — TF-IDF + KMeans

The project uses unsupervised Machine Learning to group similar infractions.

## TF-IDF Vectorization

Configuration:

```python
TfidfVectorizer(
    analyzer='char_wb',
    ngram_range=(2,4),
    max_features=500,
    min_df=1,
    sublinear_tf=True
)
```

### Why character n-grams?

Character n-grams work well for:

- Arabic morphology
- Misspellings
- Legal variations
- Multilingual processing

---

## KMeans Clustering

The vectorized infractions are grouped into clusters representing similar legal behaviors.

Possible clusters:

- Speed violations
- Alcohol offenses
- Dangerous driving
- Administrative violations

---

# 🤖 6️⃣ Named Entity Recognition (NER)

The notebook compares:

## A. Rule-based NLP (Regex)

Advantages:

- Fast
- Explainable
- Precise on known patterns

Limitations:

- Less flexible
- Harder to generalize

---

## B. spaCy Pre-trained NER

French legal text is processed using:

```python
fr_core_news_sm
```

Fallback behavior:

If the spaCy model is unavailable, a custom legal NER system is used.

---

# 📊 Comparison: Regex vs ML-based NER

| Criteria | Regex | spaCy NER |
|---|---|---|
| Precision | High on known patterns | Moderate |
| Generalization | Limited | Better |
| Speed | Very fast | Slower |
| Interpretability | Excellent | Lower |
| Training Data Needed | No | Yes |
| Flexibility | Low | High |

---

# 📈 Dataset Statistics

The notebook computes:

- Number of legal articles
- Distribution of fines
- Number of suspensions
- Distribution of infractions
- Frequency analysis

Example:

```python
print(df['amende_fixe'].describe())
```

---

# 🧱 Final DataFrame Structure

The final dataset contains columns such as:

| Column | Description |
|---|---|
| article_id | Article identifier |
| infraction_desc_fr | French infraction description |
| infraction_desc_ar | Arabic infraction description |
| sanction_desc_fr | French sanction description |
| amende_fixe | Fixed fine amount |
| points_retrait | Points removed |
| vitesse_limite | Speed limit |
| suspension_permis | Suspension flag |
| type_infraction | Infraction category |
| localisation | Legal context/location |
| niveau_gravite | Severity level |

---

# 💾 Export

The processed dataset is exported automatically:

```python
df.to_csv('export_final.csv', index=False)
```

Generated file:

```bash
export_final.csv
```

---

# ▶️ How to Run

Launch Jupyter Notebook:

```bash
jupyter notebook
```

Open:

```bash
devoir1_nlp_code_route.ipynb
```

Run all notebook cells sequentially.

---

# 🧪 Example Output

| article_id | amende_fixe | points_retrait | type_infraction |
|---|---|---|---|
| 161 | 700 | 4 | Excès de vitesse |
| 162 | 1000 | 6 | Excès de vitesse |

---

# 📸 Notebook Features

The notebook demonstrates:

✅ Multilingual NLP  
✅ Arabic preprocessing  
✅ Legal text mining  
✅ Machine Learning clustering  
✅ NER comparison  
✅ Structured dataset creation  
✅ Explainable rule-based NLP

---

# 🤝 Contributing

Contributions are welcome.

Possible contributions:

- Improve Arabic normalization
- Add transformer models
- Extend the legal corpus
- Improve entity extraction accuracy
- Add evaluation metrics

---

# 📜 License

This project is for academic and educational purposes.

---

# 👨‍💻 Author

**ACHARF EL BOUMASHOULI**  
Master IASD 2026  
Université Abdelmalek Essaadi — FST Tanger

---

# ⭐ If You Like This Project

Give the repository a ⭐ on GitHub and share it with others interested in:

- NLP
- Arabic AI
- LegalTech
- Machine Learning
- Text Mining
- Multilingual AI

