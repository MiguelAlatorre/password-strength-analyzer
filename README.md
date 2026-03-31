### \# Password Strength Analyzer

### 

### A command-line tool that analyzes password strength and estimates how long it would take to brute-force. Built in Python as a cybersecurity portfolio project.

### 

### \## Features

### \- Checks against 14 million real-world leaked passwords (rockyou.txt)

### \- Estimates crack time based on charset size and password length

### \- Color-coded strength rating: Weak / Fair / Strong / Very Strong

### \- Visual score bar out of 10

### \- Breakdown of exactly what the password is missing

### \- Penalizes repeated characters and sequential patterns

### \- Bonus scoring for 20+ character length and high character entropy

### 

### \## How it works

### The wordlist is loaded once at startup into a Python \*\*set\*\*, which uses hash-based O(1) lookup. This means checking a password against 14 million entries is virtually instant — no loops, no scanning. A list would be O(n) and noticeably slow at that scale.

### 

### \## How to run

### 1\. Download rockyou.txt and place it in the same folder as the script

### 2\. Run: `python password\_analyzer.py`

### 

### \## Wordlist

### rockyou.txt is not included in this repo (130MB). You can download it here:

### https://github.com/brannondorsey/naive-hashcat/releases/download/data/rockyou.txt

### 

### \## Author

### github.com/MiguelAlatorre

