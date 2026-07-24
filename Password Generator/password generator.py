import random 
import string 

def generate_password(min_length, numbers = True, special_characters = True):
    """Generate a random password with the specified minimum length and options for including numbers and special characters."""
    
    # Define character sets
    letters = string.ascii_letters
    digits = string.digits
    special = string.punctuation
    
    # Start with letters
    characters = letters
    
    # Add digits if requested
    if numbers:
        characters += digits
    # Add special characters if requested
    if special_characters:
        characters += special
    
    pwd = ""
    meets_criteria = False
    has_number = False
    has_special = False

    while not meets_criteria or len(pwd) < min_length:
        new_char = random.choice(characters)
        pwd += new_char

        if new_char in digits:
            has_number = True
        if new_char in special:
            has_special = True

        meets_criteria = True
        if numbers:
            meets_criteria = has_number
        if special_characters:
            meets_criteria = meets_criteria and has_special
        
    return pwd

generate_password(10)
