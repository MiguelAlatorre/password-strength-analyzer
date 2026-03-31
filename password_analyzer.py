import re
import math
import getpass

COMMON_PASSWORDS = [
    "password", "123456", "123456789", "qwerty", "abc123",
    "password1", "111111", "iloveyou", "admin", "welcome",
    "monkey", "dragon", "master", "sunshine", "princess",
    "letmein", "shadow", "superman", "michael", "football"
]

def estimate_crack_time(password):
    charset = 0
    if re.search(r'[a-z]', password): charset += 26
    if re.search(r'[A-Z]', password): charset += 26
    if re.search(r'[0-9]', password): charset += 10
    if re.search(r'[^a-zA-Z0-9]', password): charset += 32

    combinations = charset ** len(password)
    guesses_per_second = 1_000_000_000  # 1 billion guesses/sec (modern GPU)
    seconds = combinations / guesses_per_second

    if seconds < 1:
        return "less than a second"
    elif seconds < 60:
        return f"{int(seconds)} seconds"
    elif seconds < 3600:
        return f"{int(seconds // 60)} minutes"
    elif seconds < 86400:
        return f"{int(seconds // 3600)} hours"
    elif seconds < 31536000:
        return f"{int(seconds // 86400)} days"
    elif seconds < 3153600000:
        return f"{int(seconds // 31536000)} years"
    else:
        return "centuries"

def analyze_password(password):
    score = 0
    feedback = []

    # Check common passwords
    if password.lower() in COMMON_PASSWORDS:
        print("\n  [!] This is one of the most common passwords ever. Change it immediately.\n")
        print("  Rating : TERRIBLE")
        print("  Score  : 0/10")
        print("  Crack  : Instantly (it's on every hacker's list)")
        return

    # Length check
    length = len(password)
    if length >= 16:
        score += 3
    elif length >= 12:
        score += 2
    elif length >= 8:
        score += 1
    else:
        feedback.append("  [-] Too short — aim for at least 12 characters")

    # Character variety checks
    has_lower = bool(re.search(r'[a-z]', password))
    has_upper = bool(re.search(r'[A-Z]', password))
    has_digit = bool(re.search(r'[0-9]', password))
    has_special = bool(re.search(r'[^a-zA-Z0-9]', password))

    if has_lower:
        score += 1
    else:
        feedback.append("  [-] Add lowercase letters")

    if has_upper:
        score += 1
    else:
        feedback.append("  [-] Add uppercase letters")

    if has_digit:
        score += 1
    else:
        feedback.append("  [-] Add numbers")

    if has_special:
        score += 2
        feedback.append("  [+] Great use of special characters!")
    else:
        feedback.append("  [-] Add special characters (e.g. !@#$%)")

    # Repeating characters check
    if re.search(r'(.)\1{2,}', password):
        score -= 1
        feedback.append("  [-] Avoid repeating characters (e.g. 'aaa')")

    # Sequential patterns
    if re.search(r'(012|123|234|345|456|567|678|789|abc|bcd|cde|qwe|wer)', password.lower()):
        score -= 1
        feedback.append("  [-] Avoid sequential patterns (e.g. '123', 'abc')")

    # Cap score
    score = max(0, min(score, 10))

    # Rating
    if score <= 2:
        rating = "WEAK"
        color = "\033[91m"     # red
    elif score <= 4:
        rating = "FAIR"
        color = "\033[93m"     # yellow
    elif score <= 6:
        rating = "STRONG"
        color = "\033[92m"     # green
    else:
        rating = "VERY STRONG"
        color = "\033[96m"     # cyan
    reset = "\033[0m"

    crack_time = estimate_crack_time(password)

    print(f"\n  Rating : {color}{rating}{reset}")
    print(f"  Score  : {score}/10")
    print(f"  Length : {length} characters")
    print(f"  Crack  : Estimated {crack_time} to brute-force")

    if feedback:
        print("\n  Feedback:")
        for tip in feedback:
            print(" ", tip)

def main():
    print("=" * 45)
    print("       PASSWORD STRENGTH ANALYZER")
    print("       github.com/miguelalatorre | 2026")
    print("=" * 45)

    while True:
        print()
        password = getpass.getpass("  Enter password (hidden): ")

        if not password:
            print("  No password entered. Try again.")
            continue

        analyze_password(password)

        print()
        again = input("  Analyze another? (y/n): ").strip().lower()
        if again != 'y':
            print("\n  Stay safe out there. \n")
            break

if __name__ == "__main__":
    main()
