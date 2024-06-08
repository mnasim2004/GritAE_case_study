# Case Study Matcher

The Case Study Matcher is an application designed to assist sellers in finding relevant case studies when pitching their product to a prospective client. By inputting a prospect's website URL, the application matches the most relevant case study from the seller's past case studies and provides reasons why the selected case study is worth referring to the prospect. Additionally, it drafts an email that the seller can send to the prospect, including a link to the matched case study and the generated reasons.

## Features
- Scrape case studies from a given URL.
- Preprocess and clean the scraped data.
- Generate TF-IDF values for the case studies.
- Match the most relevant case study based on the prospect's website content.
- Provide three reasons why the selected case study is worth referring to.
- Draft an email that includes the case study link and the generated reasons.

## Setup and Installation

### Prerequisites
- Python 3.8+
- Virtual environment tool (e.g., `venv`)
- Required Python packages listed in `requirements.txt`

### Steps to Setup

1. **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd case-study-matcher
    ```

2. **Create a virtual environment:**
    ```bash
    python -m venv venv
    ```

3. **Activate the virtual environment:**
    - On Windows:
        ```bash
        venv\Scripts\activate
        ```
    - On macOS and Linux:
        ```bash
        source venv/bin/activate
        ```

4. **Install the required packages:**
    ```bash
    pip install -r requirements.txt
    ```

5. **Run the data collection script:**
    ```bash
    python get_data.py
    ```

## Usage

1. **Run the Flask application:**
    ```bash
    python app.py
    ```

2. **Open your browser and navigate to:**
    ```
    http://127.0.0.1:5000/
    ```

3. **Input the prospect's website URL and find the matching case study.**

## Project Structure

.
├── README.md
├── app.py
├── get_data.py
├── scraper.py
├── preprocess.py
├── tfidf.py
├── requirements.txt
└── templates
├── index.html
└── result.html


- **app.py:** Main Flask application file that serves the web interface.
- **get_data.py:** Script to scrape, preprocess, and generate TF-IDF values for the case studies.
- **scraper.py:** Contains functions to scrape case study data and additional details.
- **preprocess.py:** Functions to preprocess the scraped data.
- **tfidf.py:** Functions to generate TF-IDF values for the preprocessed data.
- **templates/:** HTML templates for the web interface.

## Detailed Workflow

1. **Scraping Case Studies:**
    - Scrape the initial case studies from the seller's provided URL and save them to `data.csv`.
    - Visit each case study link and scrape additional details, saving the results to `new_data.csv`.

2. **Preprocessing:**
    - Clean and preprocess the additional details in `new_data.csv`, saving the cleaned data to `preprocessed_new_data.csv`.

3. **TF-IDF Generation:**
    - Generate TF-IDF values from the cleaned data and save the values to `tfidf_values.csv`.

4. **Matching Case Studies:**
    - Use cosine similarity to match the most relevant case study based on the prospect's website content.

5. **Generating Reasons:**
    - Generate three reasons why the selected case study is relevant.

6. **Drafting Email:**
    - Draft an email that includes the case study link and the generated reasons.

![screencapture-127-0-0-1-5000-2024-06-07-21_32_57](https://github.com/mnasim2004/GritAE_case_study/assets/81107541/f72902bc-ff77-4cd8-8b03-744bfda01f38)

