import hashlib
from collections import Counter
import re

# Function defination taking a single string argument
# The function intends to return a dictionary 
def analyze_string(value: str) -> dict:
    #Handling whitespace/clean string
    clean_str = value.strip()

    # Checking if string is palidrome
    normalized = re.sub(r'[^a-zA-Z0-9]', '', clean_str).lower()
    is_palindrome = normalized == normalized[::-1]

    #Number of characters in the string
    length = len(clean_str)
    # Counting of distinct characters in the string
    unique_chars = len(set(normalized))

    # word count for strings separated by whitespace
    word_count = len(clean_str.split())

    # SHA-256 hash of the string for unique identification
    sha256_hash = hashlib.sha256(clean_str.encode()).hexdigest()

    # dictionary mapping each character to its occurrence count
    character_frequency = dict(Counter(normalized))

    return {
        "length": length,
        "is_palindrome": is_palindrome,
        "unique_chars": unique_chars,
        "word_count": word_count,
        "sha256_hash": sha256_hash,
        "character_frequency": character_frequency
    }

#if __name__ == "__main__":
#   import sys 
#
#  input_string = sys.argv[1]
#   result = analyze_string(input_string)
#   print(result)