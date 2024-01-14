import csv
import nltk  # Replace with your chosen NLP library if not using NLTK
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import wordnet  # Import WordNet from NLTK
from nltk.corpus import stopwords
from nltk.cluster.util import cosine_distance
import numpy as np
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import random
import re  # Import the regular expression library
import num2words




# ... Define your summarization function here ...
def summarize_text(text):
    # Implement your summarization logic here
    # ...
    summary = "This is the generated summary."  # Replace with actual summary generation
    return summary





# ... Define your text generation functions ...

def modify_text_enhanced(description):
    # Enhanced sentence-level variations:
    sentences = sent_tokenize(description)
    random.shuffle(sentences)  # Simple shuffling


    # Enhanced word-level variations:
    words = word_tokenize(description)
    for i in range(len(words)):
        if random.random() < 0.4:  # Adjust probability
            word_synonyms = set(wordnet.synsets(words[i]))
            
            if word_synonyms:
                word_synonyms_list = list(word_synonyms)  # Convert set to list
                new_word = random.choice(word_synonyms_list).lemmas()[0].name()
                words[i] = new_word


# Convert numbers to words before combining sentences and words:
    for i, word in enumerate(words):
        if word.isdigit():  # Check if the word is a number
            try:
                words[i] = num2words.num2words(int(word))  # Use num2words.num2words()
            except ValueError:
                pass  # Ignore if not a valid integer

    # Ensure consistent lowercase for all words:
    words = [word.lower() for word in words]

    # Create the modified description:
    modified_description = " ".join(sentences) + " ".join(words)

    # Rearrange parts of the description (apply to original):
    modified_description = re.sub(r"(.*) (\d+ ml) (.*)", r"\3 \1 \2", description
    )

    # Remove duplicates:
    modified_description = " ".join(set(modified_description.split()))

    return modified_description

  

nltk.download('punkt')  # Download necessary NLTK resources if using NLTK
nltk.download('wordnet')  # Download WordNet for synonyms


# ... Web scraping code with the correct CSS selector for description ...
driver = webdriver.Chrome()  # Replace with your preferred browser driver
url = "https://www.myntra.com/personal-care"
driver.get(url)

products = WebDriverWait(driver, 10).until(
    EC.presence_of_all_elements_located((By.CLASS_NAME, "product-base"))
)

product_data = []
for product in products:
    try:
        name = product.find_element(By.CLASS_NAME, "product-brand").text
        
        description = product.find_element(By.CSS_SELECTOR, ".product-product").text  # Replace with correct selector

        
        summary = summarize_text(description)

        # Choose your preferred text generation approach:
        modified_description = modify_text_enhanced(description)  # Enhanced techniques
        

        product_data.append({
            "name": name,
            "description": description,
            "summary": summary,
            "modified_description": modified_description
        })
    except NoSuchElementException:
        print("Error: Some product elements not found. Skipping...")



with open("my_scraped_products_poss.csv", "w", newline="", encoding="utf-8") as csvfile:
    fieldnames = ["name", "description", "summary", "modified_description"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(product_data)

print("Data successfully saved to my_scraped_products_poss.csv")

driver.quit()