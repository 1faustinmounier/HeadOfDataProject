import pandas as pd
import re
import math
from collections import defaultdict

def preprocess_text(text):
    # Remove punctuation and numbers
    text = re.sub(r'[^\w\s]', '', text)
    text = re.sub(r'\d+', '', text)
    # Convert to lowercase
    text = text.lower().split()
    # Remove short words
    text = [word for word in text if len(word) >= 3]
    return text

def calculate_tf(doc):
    # Term Frequency calculation
    tf_dict = defaultdict(int)
    for word in doc:
        tf_dict[word] += 1
    total_words = len(doc)
    for word in tf_dict:
        tf_dict[word] = tf_dict[word] / total_words
    return tf_dict

def calculate_idf(docs):
    # Inverse Document Frequency calculation
    idf_dict = defaultdict(int)
    total_docs = len(docs)
    all_words = set(word for doc in docs for word in doc)
    for word in all_words:
        idf_dict[word] = math.log(total_docs / sum(1 for doc in docs if word in doc))
    return idf_dict

def calculate_tfidf(tf_list, idf_dict):
    # TF-IDF calculation
    tfidf_list = []
    for tf in tf_list:
        tfidf = {word: (tf[word] * idf_dict[word]) for word in tf}
        tfidf_list.append(tfidf)
    return tfidf_list

# Read the CSV file
df = pd.read_csv('tf_idf_dataset.csv')  # Update with your actual file path
documents = df['product_name'].tolist()  # Update with your actual column name

# Preprocess documents
processed_docs = [preprocess_text(doc) for doc in documents]

# Calculate TF for each document
tf_list = [calculate_tf(doc) for doc in processed_docs]

# Calculate IDF using all documents
idf_dict = calculate_idf(processed_docs)

# Calculate TF-IDF
tfidf_list = calculate_tfidf(tf_list, idf_dict)

# Convert to DataFrame for better visualization and save to CSV
tf_df = pd.DataFrame(tf_list).fillna(0)
idf_df = pd.DataFrame([idf_dict]).T.rename(columns={0: 'IDF'}).fillna(0)
tfidf_df = pd.DataFrame(tfidf_list).fillna(0)

print("TF Matrix:")
print(tf_df)
print("\nIDF Matrix:")
print(idf_df)
print("\nTF-IDF Matrix:")
print(tfidf_df)

# Optionally, save these matrices to CSV files
tf_df.to_csv('TF_Matrix.csv')
idf_df.to_csv('IDF_Matrix.csv')
tfidf_df.to_csv('TF_IDF_Matrix.csv')
