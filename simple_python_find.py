import hashlib
import itertools
import requests
import time  # For timing the execution

# Function to generate SHA-1 hash
def sha1_hash(word):
    return hashlib.sha1(word.encode('utf-8')).hexdigest()

# Function to perform substitutions and case changes
def generate_variants(word):
    substitutions = {
        'o': ['o', '0', 'O'],
        'l': ['l', '1', 'L'],
        'i': ['i', '1', 'I'],
        's': ['s', '5', 'S']
    }

    # Step 1: Generate case combinations
    case_combinations = map(''.join, itertools.product(*((char.lower(), char.upper()) for char in word)))
    
    # Step 2: Apply substitutions to each case combination
    all_variants = set()
    for case_variant in case_combinations:
        options = [[char] if char not in substitutions else substitutions[char] for char in case_variant]
        for variant in itertools.product(*options):
            all_variants.add(''.join(variant))
    
    return all_variants

# Function to download the wordlist
def download_wordlist(url):
    print("Downloading wordlist...")
    response = requests.get(url)
    if response.status_code == 200:
        print("Wordlist downloaded successfully.")
        return response.text.splitlines()
    else:
        print("Failed to download wordlist.")
        exit()

# Main function to find the matching hash
def find_original_value(target_hash, url):
    words = download_wordlist(url)
    print("Searching for the original word...")
    for word in words:
        # Generate all variants of the current word
        variants = generate_variants(word)
        for variant in variants:
            if sha1_hash(variant) == target_hash:
                print(f"Original value found: {variant}")
                return
    print("No match found.")

# Timer to measure execution speed
if __name__ == "__main__":
    target_hash = "d54cc1fe76f5186380a0939d2fc1723c44e8a5f7"
    wordlist_url = "https://raw.githubusercontent.com/danielmiessler/SecLists/master/Passwords/Common-Credentials/10k-most-common.txt"

    # Start the timer
    start_time = time.time()

    # Run the program
    find_original_value(target_hash, wordlist_url)

    # Stop the timer
    end_time = time.time()
    print(f"Execution Time: {end_time - start_time:.2f} seconds")
