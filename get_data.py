import scraper
import preprocess
import tfidf

# Scrape initial case studies and save to data.csv
scraper.scrape_case_studies("https://www.intercom.com/customers", 'data.csv')

# Open data.csv, visit each link, and save additional details to new_data.csv
scraper.scrape_additional_details_from_links('data.csv', 'new_data.csv')

# Preprocess the additional information in new_data.csv
preprocess.preprocess_additional_info('new_data.csv', 'preprocessed_new_data.csv')

#To generate TF-IDF values from preprocessed CSV
tfidf.generate_tfidf_values('preprocessed_new_data.csv', 'tfidf_values.csv')