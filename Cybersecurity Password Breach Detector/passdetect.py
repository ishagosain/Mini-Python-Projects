"""
Password Strength & Breach Checker
------------------------------------
Checks a password against two things:
1. Strength: length, character variety, common patterns
2. Breach exposure: uses the Have I Been Pwned API to see if the
   password has appeared in known data breaches
 
Privacy note: your password is not sent over the network in full.
This uses the "k-anonymity" model — only the first 5 characters of
the password's SHA-1 hash are sent to the API. The API returns a
list of hash suffixes matching that prefix, and the match happens
locally on your machine. HIBP never sees your actual password.
"""

import hashlib
import re
import getpass
import urllib.request
import urllib.error
 
# A small sample of extremely common passwords worth flagging directly.
# (Not exhaustive -- the breach check below is the real safety net.)
COMMON_PASSWORDS = {
    "password", "123456", "123456789", "qwerty", "abc123",
    "password1", "111111", "12345678", "letmein", "iloveyou",
    "admin", "welcome", "monkey", "dragon", "football",
}
 
 
def check_strength(password):
    """Returns a score (0-5) and a list of feedback messages."""
    score = 0
    feedback = []
 
    if len(password) >= 12:
        score += 1
    else:
        feedback.append("Use at least 12 characters.")
 
    if re.search(r"[a-z]", password) and re.search(r"[A-Z]", password):
        score += 1
    else:
        feedback.append("Mix uppercase and lowercase letters.")
 
    if re.search(r"\d", password):
        score += 1
    else:
        feedback.append("Include at least one number.")
 
    if re.search(r"[^\w\s]", password):
        score += 1
    else:
        feedback.append("Include at least one special character (e.g. ! @ # $).")
 
    if password.lower() not in COMMON_PASSWORDS:
        score += 1
    else:
        feedback.append("This is a widely used password -- avoid it entirely.")
 
    labels = ["Very Weak", "Weak", "Fair", "Good", "Strong", "Very Strong"]
    return score, labels[score], feedback
 
 
def check_breach(password):
    """
    Checks the password against the Have I Been Pwned breach database
    using the k-anonymity range API. Returns (is_breached, breach_count).
    Returns (None, None) if the check couldn't be completed (e.g. no internet).
    """
    sha1_hash = hashlib.sha1(password.encode("utf-8")).hexdigest().upper()
    prefix, suffix = sha1_hash[:5], sha1_hash[5:]
 
    url = f"https://api.pwnedpasswords.com/range/{prefix}"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "password-checker-script"})
        with urllib.request.urlopen(req, timeout=5) as response:
            results = response.read().decode("utf-8")
    except (urllib.error.URLError, TimeoutError):
        return None, None
 
    for line in results.splitlines():
        hash_suffix, count = line.split(":")
        if hash_suffix == suffix:
            return True, int(count)
 
    return False, 0
 
 
def main():
    print("=== Password Strength & Breach Checker ===\n")
    password = getpass.getpass("Enter a password to check (input hidden): ")
 
    if not password:
        print("No password entered.")
        return
 
    score, label, feedback = check_strength(password)
    print(f"\nStrength: {label} ({score}/5)")
    if feedback:
        print("Suggestions:")
        for tip in feedback:
            print(f"  - {tip}")
 
    print("\nChecking against known data breaches (Have I Been Pwned)...")
    is_breached, count = check_breach(password)
 
    if is_breached is None:
        print("Could not reach the breach database (check your internet connection).")
    elif is_breached:
        print(f"⚠️  This password has appeared in {count:,} known breaches. Do not use it.")
    else:
        print("✅ This password was not found in any known breach.")
 
 
if __name__ == "__main__":
    main()