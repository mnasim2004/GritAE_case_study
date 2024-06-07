from flask import Flask, request, render_template, jsonify
import pandas as pd
from sentence_transformers import SentenceTransformer, util
import torch
from transformers import GPT2Tokenizer, GPT2LMHeadModel

import scraper2

app = Flask(__name__)

# Load case studies
case_studies_df = pd.read_csv('tfidf_values.csv')
# Load the pre-trained BERT model for encoding sentences
model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

# Load GPT-2 model and tokenizer
gpt2_tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
gpt2_model = GPT2LMHeadModel.from_pretrained('gpt2')

def find_relevant_case_study(prospect_info):
    # Check if prospect_info is a string, convert it to a dictionary if needed
    if isinstance(prospect_info, str):
        prospect_info = {'prospect_url': prospect_info}

    # Fetch the title and description using scraper2.py
    title, description = scraper2.fetch_main_body_text(prospect_info['prospect_url'])

    # Encode the prospect's title and description
    prospect_embedding = model.encode([title, description])

    # Encode the case studies' title and description
    case_study_embeddings = model.encode(case_studies_df['clean_additional_info'].tolist())

    # Calculate cosine similarity between the prospect and case studies
    similarity_scores = util.pytorch_cos_sim(prospect_embedding, case_study_embeddings)[0]

    # Find the index of the most similar case study
    max_similarity_index = int(similarity_scores.argmax())

    # Calculate the similarity percentage
    similarity_percentage = str(similarity_scores[max_similarity_index].item() * 100)
    
    # Load the additional data.csv file
    data_df = pd.read_csv('data.csv')

    # Get company information based on the index
    company_info = data_df.iloc[max_similarity_index]
    matched_case_study_dict = {
        'row_number': max_similarity_index,
        'company': company_info['title'],  # Assuming 'company' is the column name in data.csv for company name
        'description': company_info['description'],  # Use 'description' for display purposes
        'link': company_info['link'],
        'similarity_percentage': similarity_percentage  # Convert similarity score to percentage
    }
    print(matched_case_study_dict)
    return matched_case_study_dict

def analyze_with_gpt2(title, description, case_study):
    # Load the preprocessed_new_data.csv file for detailed information
    preprocessed_data_df = pd.read_csv('preprocessed_new_data.csv')
    detailed_info = preprocessed_data_df.iloc[case_study['row_number']]['clean_additional_info']

    prompt = f"Prospect Information:\nTitle: {title}\nDescription: {description}\n\n" \
             f"Case Study Information:\nTitle: {case_study['company']}\nToken Description: {detailed_info}\n\n" \
            f"Give three reasons why this case study is worth going through by the prospect.\n\n1."

 # Tokenize and generate text with GPT-2
    inputs = gpt2_tokenizer.encode(prompt, return_tensors='pt')
    attention_mask = torch.ones(inputs.shape, dtype=torch.long)
    outputs = gpt2_model.generate(
        inputs,
        attention_mask=attention_mask,
        max_length=1024,
        num_return_sequences=1,
        pad_token_id=gpt2_tokenizer.eos_token_id,
        temperature=0.7,  # Control the creativity of the model
        repetition_penalty=2.0  # Penalize repetitive phrases
    )
    generated_text = gpt2_tokenizer.decode(outputs[0], skip_special_tokens=True)
    print(generated_text)
    # Extract reasons
    reasons = []
    lines = generated_text.split('\n')
    for line in lines:
        if line.startswith("1.") or line.startswith("2.") or line.startswith("3."):
            reasons.append(line.strip())
    
    # Ensure reasons are distinct and brief
    reasons = list(set(reasons))[:3]
    while len(reasons) < 3:
        reasons.append("Reason not generated due to insufficient or repetitive output.")

    # # Tokenize and generate text with GPT-2
    # inputs = gpt2_tokenizer.encode(prompt, return_tensors='pt')
    # attention_mask = torch.ones(inputs.shape, dtype=torch.long)
    # outputs = gpt2_model.generate(
    #     inputs, 
    #     attention_mask=attention_mask, 
    #     max_length=1000, 
    #     num_return_sequences=1,
    #     pad_token_id=gpt2_tokenizer.eos_token_id
    # )
    # # outputs = gpt2_model.generate(inputs, max_length=1000, num_return_sequences=1)
    # generated_text = gpt2_tokenizer.decode(outputs[0], skip_special_tokens=True)
    # print(generated_text)
    # # Extract the reasons from the generated text
    # reasons = generated_text.split('\n')[-3:]  # Assuming the last three lines are the reasons
    
    return reasons

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/match', methods=['POST'])
def match():
    prospect_info = {'prospect_url': request.form['prospect_url']}
    title, description_p = scraper2.fetch_main_body_text(prospect_info['prospect_url'])
    input_text = {'title': title, 'description': description_p}
    case_study = find_relevant_case_study(prospect_info)
    if case_study is not None:
        company = case_study['company']
        description = case_study['description']
        link = case_study['link']
        similarity_percentage = case_study['similarity_percentage']
        reasons = analyze_with_gpt2(title, description_p, case_study)
        return jsonify({
            'company': company,
            'description': description,
            'link': link,
            'similarity_percentage': similarity_percentage,
            'reasons': reasons
        })
    else:
        return jsonify({'error': 'Failed to find matching case study'}), 404

if __name__ == "__main__":
    app.run(debug=True)








# from flask import Flask, request, render_template, jsonify
# import pandas as pd
# from sentence_transformers import SentenceTransformer, util
# import torch 

# import scraper2

# app = Flask(__name__)

# # Load case studies
# case_studies_df = pd.read_csv('tfidf_values.csv')
# # Load the pre-trained BERT model for encoding sentences
# model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

# def find_relevant_case_study(prospect_info):
#     # Check if prospect_info is a string, convert it to a dictionary if needed
#     if isinstance(prospect_info, str):
#         prospect_info = {'prospect_url': prospect_info}

#     # Fetch the title and description using scraper2.py
#     title, description = scraper2.fetch_main_body_text(prospect_info['prospect_url'])

#     # Encode the prospect's title and description
#     prospect_embedding = model.encode([title, description])

#     # Encode the case studies' title and description
#     case_study_embeddings = model.encode(case_studies_df['clean_additional_info'].tolist())

#     # Calculate cosine similarity between the prospect and case studies
#     similarity_scores = util.pytorch_cos_sim(prospect_embedding, case_study_embeddings)[0]

#     # Find the index of the most similar case study
#     max_similarity_index = int(similarity_scores.argmax())

#     # Calculate the similarity percentage
#     similarity_percentage = str(similarity_scores[max_similarity_index].item() * 100)
#     # Load the additional data.csv file
#     data_df = pd.read_csv('data.csv')

#     # Get company information based on the index
#     company_info = data_df.iloc[max_similarity_index]
#     matched_case_study_dict = {
#         'row_number': max_similarity_index,
#         'company': company_info['title'],  # Assuming 'company' is the column name in data.csv for company name
#         'description': company_info['description'],  # Use 'clean_additional_info' instead of 'description'
#         'link':company_info['link'],
#         'similarity_percentage': similarity_percentage # Convert similarity score to percentage
#     }
#     print(matched_case_study_dict)
#     return matched_case_study_dict


# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/match', methods=['POST'])
# def match():
#     prospect_info = {'prospect_url': request.form['prospect_url']}
#     case_study = find_relevant_case_study(prospect_info)
#     if case_study is not None:
#         company = case_study['company']
#         description = case_study['description']
#         link = case_study['link']
#         similarity_percentage = case_study['similarity_percentage']
#         reasons = ["Similar industry", "Proven results", "Positive feedback"]
#         return jsonify({
#             'company': company,
#             'description': description,
#             'link': link,
#             'similarity_percentage': similarity_percentage,
#             'reasons': reasons
#         })
#     else:
#         return jsonify({'error': 'Failed to find matching case study'}), 404


# if __name__ == "__main__":
#     app.run(debug=True)
