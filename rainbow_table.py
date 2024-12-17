import hashlib
import itertools
import requests
import time
import sys
import pickle  # For saving and loading the table
import csv  # For saving to CSV

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

# Function to create a rainbow table
def create_rainbow_table(url):
    words = download_wordlist(url)
    rainbow_table = {}
    print("Creating rainbow table...")

    for word in words:
        # Generate all variants of the current word
        variants = generate_variants(word)
        for variant in variants:
            hashed_value = sha1_hash(variant)
            rainbow_table[hashed_value] = variant  # Hash as key, original word as value
    
    return rainbow_table

# Function to save the rainbow table to a CSV file
def save_rainbow_table_as_csv(rainbow_table, filename):
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Hash', 'Original Word'])  # Write header row
        for hash_value, original_word in rainbow_table.items():
            writer.writerow([hash_value, original_word])  # Write each hash and original word
    print(f"Rainbow table saved to {filename} in CSV format.")

# Function to measure the size of an object
def get_size(obj):
    return sys.getsizeof(pickle.dumps(obj))  # Serialize object to measure size

# Main script
if __name__ == "__main__":
    wordlist_url = "https://raw.githubusercontent.com/danielmiessler/SecLists/master/Passwords/Common-Credentials/10k-most-common.txt"
    rainbow_table_filename = "rainbow_table.csv"
    
    # Try to load the rainbow table from the file
    rainbow_table = None
    try:
        with open(rainbow_table_filename, 'r', newline='') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  # Skip the header row
            rainbow_table = {rows[0]: rows[1] for rows in reader}  # Create dictionary from CSV
        print(f"Rainbow table loaded from {rainbow_table_filename}")
    except FileNotFoundError:
        print(f"{rainbow_table_filename} not found. Creating a new rainbow table.")
    
    # If rainbow table does not exist, create it
    if rainbow_table is None:
        # Start timer
        start_time = time.time()

        # Create rainbow table
        rainbow_table = create_rainbow_table(wordlist_url)

        # End timer
        end_time = time.time()
        elapsed_time = end_time - start_time

        # Measure size of the rainbow table
        table_size = get_size(rainbow_table)

        # Print results
        print(f"Rainbow table created successfully!")
        print(f"Number of entries: {len(rainbow_table)}")
        print(f"Time taken: {elapsed_time:.2f} seconds")
        print(f"Size of the table: {table_size / 1024 / 1024:.2f} MB")

        # Save the table to a CSV file
        save_rainbow_table_as_csv(rainbow_table, rainbow_table_filename)
