import hashlib
from collections import Counter
import re

# Function defination taking a single string argument
# The function intends to return a dictionary 
def analyze_string(value: str) -> dict:
    #Handling whitespace/clean string
    clean_str = value.strip()

    #Number of characters in the string
    length = len(clean_str)

    # Checking if string is palidrome
    normalized = re.sub(r'[^a-zA-Z0-9]', '', clean_str).lower()
    is_palindrome = normalized == normalized[::-1]

    # Counting of distinct characters in the string
    unique_char = len(set(clean_str))

    # word count for strings separated by whitespace
    word_count = len(clean_str.split())

    # SHA-256 hash of the string for unique identification
    SHA256_hash = hashlib.sha256(clean_str.encode()).hexdigest()

    # dictionary mapping each character to its occurrence count
    char_frequency = dict(Counter(clean_str))

    return {
        "length": length,
        "is_palindrome": is_palindrome,
        "unique_char": unique_char,
        "word_count": word_count,
        "SHA256_hash": SHA256_hash,
        "char_frequency": char_frequency
    }

if __name__ == "__main__":
    import sys
    
    input_string = sys.argv[1]
    result = analyze_string(input_string)
    print(result)