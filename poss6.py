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




# ... Define your summarization function here ...
def summarize_text(text):
    # Implement your summarization logic here
    # ...
    summary = "This is the generated summary."  # Replace with actual summary generation
    return summary
    # made by Debanka Das - https://github.com/erdebankadas; also follow my page - https://fossbyte.in/





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
            # if word_synonyms:
            #     new_word = random.choice(word_synonyms).lemmas()[0].name()
            #     words[i] = new_word
            if word_synonyms:
                word_synonyms_list = list(word_synonyms)  # Convert set to list
                new_word = random.choice(word_synonyms_list).lemmas()[0].name()
                words[i] = new_word

    modified_description = " ".join(sentences) + " ".join(words)
    # Rearrange parts of the description:
    # modified_description = re.sub(r"(.*) (\d+ ml) (.*)", r"\2 \1 \3", modified_description)
    modified_description = re.sub( r"(.*) (\d+ ml) (.*)", r"\2 \1 \3", description # Apply to original description
    )
    # Remove duplicates:
    modified_description = " ".join(set(modified_description.split()))  # Keep unique words

    return modified_description
    # made by Debanka Das - https://github.com/erdebankadas; also follow my page - https://fossbyte.in/

    # return modified_description

# def modify_text_with_openai(description):
#     if openai is None:
#         raise ImportError("OpenAI library not found.")

#     openai.api_key = "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"  # Replace with your API key

#     prompt = f"Rewrite this product description in a different style, while preserving the meaning:\n{description}"
#     response = openai.Completion.create(
#         engine="text-davinci-003",  # Use a powerful text generation model
#         prompt=prompt,
#         max_tokens=150,  # Adjust as needed
#         n=1,
#         stop=None,
#         temperature=0.7,  # Control creativity
#     )
#     modified_description = response.choices[0].text.strip()
#     return modified_description

    
    # return modified_description

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
        # description = product.find_element(By.CSS_SELECTOR, "CORRECT_SELECTOR_FOR_DESCRIPTION").text
        description = product.find_element(By.CSS_SELECTOR, ".product-product").text  # Replace with correct selector

        
        summary = summarize_text(description)

        # Choose your preferred text generation approach:
        modified_description = modify_text_enhanced(description)  # Enhanced techniques
        # made by Debanka Das - https://github.com/erdebankadas; also follow my page - https://fossbyte.in/
        

        product_data.append({
            "name": name,
            "description": description,
            "summary": summary,
            "modified_description": modified_description
        })
    except NoSuchElementException:
        print("Error: Some product elements not found. Skipping...")



with open("my_scraped_products_poss6.csv", "w", newline="", encoding="utf-8") as csvfile:
    fieldnames = ["name", "description", "summary", "modified_description"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(product_data)

print("Data successfully saved to my_scraped_products.csv")

driver.quit()