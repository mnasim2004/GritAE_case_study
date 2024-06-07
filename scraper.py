from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import csv


def scrape_case_studies(url, csv_filename):
    # Set up the WebDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    # Open the target website
    driver.get(url)

    # Prepare the CSV file
    with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['title', 'description', 'link']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        def scrape_page():
            # Find elements by the customer-story-card__content class
            cards = driver.find_elements(By.CLASS_NAME, "customer-story-card__content")
            for card in cards:
                try:
                    title_element = card.find_element(By.CLASS_NAME, "customer-story-card__title")
                    title = title_element.find_element(By.TAG_NAME, "b").text

                    description_element = card.find_element(By.CLASS_NAME, "rich-text")
                    description = description_element.find_element(By.TAG_NAME, "p").text

                    link_element = card.find_element(By.CSS_SELECTOR, "a[data-testid='cta-link-read-story']")
                    link = link_element.get_attribute("href")

                    writer.writerow({'title': title, 'description': description, 'link': link})
                    print(f"Title: {title}, Description: {description}, Link: {link}")
                except Exception as e:
                    print(f"Error processing card: {e}")

        def click_pagination_button(page_number):
            try:
                pagination_buttons = driver.find_elements(By.CLASS_NAME, "pagination__button")
                for button in pagination_buttons:
                    if button.text == str(page_number):
                        driver.execute_script("arguments[0].scrollIntoView(true);", button)  # Scroll to the button
                        time.sleep(1)  # Wait for the scroll
                        button.click()
                        time.sleep(2)  # Wait for the page to load
                        return True
            except Exception as e:
                print(f"Error clicking pagination button {page_number}: {e}")
                return False

        page_number = 1
        while True:
            scrape_page()

            page_number += 1
            if not click_pagination_button(page_number):
                break

    # Close the WebDriver
    driver.quit()

def scrape_additional_details_from_links(input_csv, output_csv):
    # Set up the WebDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    # Prepare the output CSV file
    with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['title', 'additional_info']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        # Read from the input CSV file
        with open(input_csv, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                link = row['link']
                driver.get(link)
                time.sleep(2)  # Wait for the page to load

                try:
                    # Extract the title from the class 'customer-story-hero__heading'
                    title_element = driver.find_element(By.CLASS_NAME, "customer-story-hero__heading")
                    title = title_element.text

                    # Extract additional information from the class 'editorial-wrap__content'
                    # additional_info_element = driver.find_element(By.CLASS_NAME, "editorial-wrap__content")
                    # additional_info = additional_info_element.text

                    # Extract description from multiple 'rich-text__typography' classes
                    description_elements = driver.find_elements(By.CLASS_NAME, "rich-text__typography")
                    description = " ".join([elem.text for elem in description_elements])

                    # Combine additional info and description
                    # combined_info = f"{additional_info} {description}"


                    # writer.writerow({'title': title, 'additional_info': combined_info })
                    writer.writerow({'title': title, 'additional_info': description })
                    print(f"Title: {title}, Additional Info: {description}")
                except Exception as e:
                    print(f"Error processing link {link}: {e}")

    # Close the WebDriver
    driver.quit()


