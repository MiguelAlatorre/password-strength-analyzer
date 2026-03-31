import re
import os
import getpass

FALLBACK_PASSWORDS = {
    "password", "123456", "123456789", "qwerty", "abc123",
    "password1", "111111", "iloveyou", "admin", "welcome",
    "monkey", "dragon", "master", "sunshine", "princess",
    "letmein", "shadow", "superman", "michael", "football"
}

# Colors
RED    = "\033[91m"
YELLOW = "\033[93m"
GREEN  = "\033[92m"
CYAN   = "\033[96m"
GRAY   = "\033[90m"
BOLD   = "\033[1m"
RESET  = "\033[0m"

def load_wordlist():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    wordlist_path = os.path.join(script_dir, "rockyou.txt")
    if os.path.exists(wordlist_path):
        print(f"  {GRAY}Loading wordlist...{RESET}", end="\r")
        try:
            with open(wordlist_path, "r", encoding="latin-1") as f:
                words = {line.strip().lower() for line in f if line.strip()}
            print(f"  {GREEN}Wordlist loaded — {len(words):,} known passwords{RESET}     ")
            return words
        except Exception:
            pass
    print(f"  {YELLOW}rockyou.txt not found — using fallback list{RESET}")
    return FALLBACK_PASSWORDS

def color_check(passed, label):
    if passed:
        return f"  {GREEN}\u2714{RESET} {label}"
    else:
        return f"  {RED}\u2718{RESET} {label}"

def score_bar(score, max_score=10):
    filled = round((score / max_score) * 20)
    empty = 20 - filled
    if score <= 2:
        bar_color = RED
    elif score <= 4:
        bar_color = YELLOW
    elif score <= 6:
        bar_color = GREEN
    else:
        bar_color = CYAN
    return f"  [{bar_color}{'\u2588' * filled}{GRAY}{'\u2591' * empty}{RESET}] {score}/{max_score}"

def estimate_crack_time(password):
    charset = 0
    if re.search(r'[a-z]', password): charset += 26
    if re.search(r'[A-Z]', password): charset += 26
    if re.search(r'[0-9]', password): charset += 10
    if re.search(r'[^a-zA-Z0-9]', password): charset += 32

    if charset == 0:
        return "instantly", RED

    combinations = charset ** len(password)
    guesses_per_second = 1_000_000_000
    seconds = combinations / guesses_per_second

    if seconds < 1:
        return "less than a second", RED
    elif seconds < 60:
        return f"{int(seconds)} seconds", RED
    elif seconds < 3600:
        return f"{int(seconds // 60)} minutes", YELLOW
    elif seconds < 86400:
        return f"{int(seconds // 3600)} hours", YELLOW
    elif seconds < 31536000:
        return f"{int(seconds // 86400)} days", GREEN
    elif seconds < 3153600000:
        return f"{int(seconds // 31536000)} years", GREEN
    else:
        return "centuries", CYAN

def analyze_password(password, wordlist):
    print()

    if password.lower() in wordlist:
        print(f"  {RED}[!] This password appears in a real-world breach list.{RESET}")
        print(f"\n  Rating : {RED}TERRIBLE{RESET}")
        print(f"  Score  :{score_bar(0)}")
        print(f"  Crack  : {RED}instantly{RESET} - it's in every hacker's dictionary")
        print()
        return

    score = 0
    length = len(password)

    if length >= 16:
        score += 3
    elif length >= 12:
        score += 2
    elif length >= 8:
        score += 1

    has_lower     = bool(re.search(r'[a-z]', password))
    has_upper     = bool(re.search(r'[A-Z]', password))
    has_digit     = bool(re.search(r'[0-9]', password))
    has_special   = bool(re.search(r'[^a-zA-Z0-9]', password))
    has_no_repeat = not bool(re.search(r'(.)\1{2,}', password))
    has_no_seq    = not bool(re.search(r'(012|123|234|345|456|567|678|789|abc|bcd|cde|qwe|wer)', password.lower()))
    is_very_long    = length >= 20
    is_high_entropy = len(set(password)) >= int(length * 0.75)

    if has_lower:         score += 1
    if has_upper:         score += 1
    if has_digit:         score += 1
    if has_special:       score += 2
    if not has_no_repeat: score -= 1
    if not has_no_seq:    score -= 1
    if is_very_long:      score += 1
    if is_high_entropy:   score += 1

    score = max(0, min(score, 10))

    if score <= 2:
        rating, rating_color = "WEAK", RED
    elif score <= 4:
        rating, rating_color = "FAIR", YELLOW
    elif score <= 6:
        rating, rating_color = "STRONG", GREEN
    else:
        rating, rating_color = "VERY STRONG", CYAN

    crack_time, time_color = estimate_crack_time(password)

    print(f"  Rating : {rating_color}{BOLD}{rating}{RESET}")
    print(f"  Score  :{score_bar(score)}")
    print(f"  Length : {length} characters")
    print(f"  Crack  : Estimated {time_color}{crack_time}{RESET} to brute-force")

    all_basic = has_lower and has_upper and has_digit and has_special and has_no_repeat and has_no_seq
    print(f"\n  Breakdown:")
    print(color_check(has_lower,      "Lowercase letters"))
    print(color_check(has_upper,      "Uppercase letters"))
    print(color_check(has_digit,      "Numbers"))
    print(color_check(has_special,    "Special characters"))
    print(color_check(has_no_repeat,  "No repeated characters"))
    print(color_check(has_no_seq,     "No sequential patterns"))
    print(color_check(is_very_long,   "20+ characters (bonus)"))
    print(color_check(is_high_entropy,"High character variety (bonus)"))

    if all_basic and score < 10:
        tips = []
        if not is_very_long:
            tips.append("20+ characters")
        if not is_high_entropy:
            tips.append("more unique characters")
        if tips:
            print(f"\n  {YELLOW}Tip: Add {' and '.join(tips)} to reach 10/10{RESET}")
    print()

def main():
    print()
    print(f"  {CYAN}{'=' * 41}{RESET}")
    print(f"  {BOLD}     PASSWORD STRENGTH ANALYZER{RESET}")
    print(f"  {GRAY}     github.com/MiguelAlatorre{RESET}")
    print(f"  {CYAN}{'=' * 41}{RESET}")
    print()

    wordlist = load_wordlist()

    while True:
        print()
        password = getpass.getpass("  Enter password (hidden): ")

        if not password:
            print(f"  {YELLOW}No password entered. Try again.{RESET}")
            continue

        analyze_password(password, wordlist)

        print(f"  {GRAY}{'-' * 41}{RESET}")
        again = input(f"\n  Analyze another? (y/n): ").strip().lower()
        if again != 'y':
            print(f"\n  {CYAN}Stay secure out there.{RESET}\n")
            break

if __name__ == "__main__":
    main()
