import pandas as pd
import re
import string
import nltk
nltk.download('punkt')
nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer

def preprocess_text(text):
    # Convert text to lowercase
    text = text.lower()
    
    # Remove punctuation
    text = text.translate(str.maketrans('', '', string.punctuation))
    
    # Remove digits
    text = re.sub(r'\d+', '', text)
    
    # Tokenize the text
    tokens = word_tokenize(text)
    
    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    filtered_tokens = [word for word in tokens if word not in stop_words]
    
    # Join tokens back into a single string
    preprocessed_text = ' '.join(filtered_tokens)
    
    return preprocessed_text

def preprocess_additional_info(input_csv, output_csv):
    # Read the CSV file with specified encoding
    df = pd.read_csv(input_csv, encoding='utf-8')
    
    # Apply preprocessing to the 'additional_info' column
    df['clean_additional_info'] = df['additional_info'].apply(preprocess_text)
    
    # Save the preprocessed data to a new CSV file
    df.to_csv(output_csv, index=False)

