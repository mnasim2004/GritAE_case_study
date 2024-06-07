# GritAE Case Study Analysis

This project involves scraping case studies from a website, preprocessing the data, and generating TF-IDF values for further analysis.

## Prerequisites

Make sure you have the following installed:
- Python 3.8 or higher
- `pip` (Python package installer)

## Setup Instructions

1. **Clone the Repository**

   ```bash
   git clone https://github.com/yourusername/GritAE_case_study.git
   cd GritAE_case_study

2. **Create and Activate Virtual Environment**

Create a virtual environment to manage dependencies.

    ```bash
    python -m venv venv

Activate the virtual environment:

On Windows:

    ```bash
    .\venv\Scripts\activate

On macOS/Linux:

    ```bash
    source venv/bin/activate
    Install Dependencies

Install the required Python packages using pip:

    ```bash
    pip install -r requirements.txt
    
Run the Data Collection Script

The script get_data.py will scrape the case studies, preprocess the data, and generate TF-IDF values. Run the script as follows:

    ```bash
    python get_data.py


## File Descriptions

**get_data.py**: Main script to scrape data, preprocess it, and generate TF-IDF values.

**scraper.py**: Contains functions for scraping case studies and additional details.

**preprocess.py**: Contains functions for preprocessing the scraped data.

**tfidf.py**: Contains functions for generating TF-IDF values from the preprocessed data.

**requirements.txt**: Lists all the dependencies required for this project.

## Usage

After running get_data.py, the following files will be generated:

**data.csv**: Initial case studies data.

**new_data.csv**: Detailed case studies data after visiting each link.

**preprocessed_new_data.csv**: Preprocessed detailed information.

**tfidf_values.csv**: TF-IDF values generated from the preprocessed data.


These files can be used for further analysis and processing.

**Notes**

Ensure you have an active internet connection while running the scraping scripts.
If you encounter any issues, check the requirements.txt to ensure all dependencies are installed correctly.

