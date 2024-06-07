from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd

def generate_tfidf_values(input_csv_path, output_csv_path):
    # Read the preprocessed data from the CSV file
    df = pd.read_csv(input_csv_path)

    # Extract the preprocessed clean additional information
    clean_additional_info = df['clean_additional_info'].tolist()

    # Initialize TF-IDF vectorizer
    tfidf_vectorizer = TfidfVectorizer()

    # Fit and transform the preprocessed clean additional information
    tfidf_matrix = tfidf_vectorizer.fit_transform(clean_additional_info)

    # Get feature names (words)
    feature_names = tfidf_vectorizer.get_feature_names_out()

    # Convert TF-IDF matrix to DataFrame for better visualization
    tfidf_df = pd.DataFrame(tfidf_matrix.toarray(), columns=feature_names)

    # Concatenate TF-IDF DataFrame with the original DataFrame
    merged_df = pd.concat([df, tfidf_df], axis=1)

    # Save the merged DataFrame to a new CSV file
    merged_df.to_csv(output_csv_path, index=False)

