# Password Strength Analyzer

A command-line tool that analyzes password strength using real-world 
security techniques. Built in Python as a cybersecurity portfolio project.

## Features
- Checks against 14 million real leaked passwords (rockyou.txt)
- Checks against Have I Been Pwned database of 1 billion+ breached passwords
- Estimates crack time based on charset size and password length
- Color-coded strength rating: Weak / Fair / Strong / Very Strong / Compromised
- Visual score bar out of 10
- Breakdown checklist of exactly what the password is missing
- Bonus scoring for 20+ character length and high character entropy
- Tips on exactly what to improve when score is under 10

## How it works

### Wordlist check
The rockyou.txt wordlist is loaded once at startup into a Python set,
which uses hash-based O(1) lookup. Checking against 14 million passwords
is virtually instant — no loops, no scanning line by line.

### Have I Been Pwned (k-anonymity)
Passwords are checked against the HIBP breach database without ever 
sending the full password over the internet. The tool:
1. Hashes the password using SHA-1
2. Sends only the first 5 characters of the hash to the API
3. Receives all hashes that match that prefix
4. Checks locally if the full hash is in the results

This technique is called k-anonymity. It's the same method used by 
Firefox and Google Chrome to warn users about compromised passwords.

### Scoring (out of 10)
| Criteria                     | Points |
|------------------------------|--------|
| 8-11 characters              | +1     |
| 12-15 characters             | +2     |
| 16+ characters               | +3     |
| Lowercase letters            | +1     |
| Uppercase letters            | +1     |
| Numbers                      | +1     |
| Special characters           | +2     |
| 20+ characters (bonus)       | +1     |
| High character entropy (bonus)| +1    |
| Repeated characters          | -1     |
| Sequential patterns          | -1     |

## How to run
1. Download rockyou.txt and place it in the same folder as the script
2. Run in Terminal: `python password_analyzer.py` 

## Wordlist
rockyou.txt is not included in this repo (130MB). Download it here:
https://github.com/brannondorsey/naive-hashcat/releases/download/data/rockyou.txt

## Author
github.com/MiguelAlatorre