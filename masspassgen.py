#!/usr/bin/env python3
"""
MassPassGen - Mass Password Generator
A tool to generate large quantities of unique passwords for security testing
"""

import random
import string
import argparse
import sys
from itertools import product

class MassPassGen:
    def __init__(self, min_len=6, max_len=12):
        self.min_len = min_len
        self.max_len = max_len
        self.charset = string.ascii_letters + string.digits + string.punctuation
    
    def generate_random_passwords(self, count, length=None):
        """Generate random passwords"""
        passwords = set()
        
        if length:
            target_len = length
        else:
            target_len = random.randint(self.min_len, self.max_len)
        
        print(f"[*] Generating {count} random passwords...")
        
        while len(passwords) < count:
            pwd = ''.join(random.choices(self.charset, k=target_len))
            passwords.add(pwd)
            
            if len(passwords) % 100000 == 0:
                print(f"[*] Progress: {len(passwords)}/{count}")
        
        return list(passwords)
    
    def generate_pattern_passwords(self, pattern, count):
        """Generate passwords based on patterns"""
        passwords = []
        print(f"[*] Generating pattern-based passwords...")
        
        for i in range(count):
            pwd = self.apply_pattern(pattern, i)
            if self.min_len <= len(pwd) <= self.max_len:
                passwords.append(pwd)
        
        return passwords
    
    def apply_pattern(self, pattern, seed):
        """Apply a pattern with seed variation"""
        result = pattern
        result = result.replace("{n}", str(seed))
        result = result.replace("{a}", random.choice(string.ascii_letters))
        result = result.replace("{d}", random.choice(string.digits))
        result = result.replace("{s}", random.choice(string.punctuation))
        return result
    
    def save_to_file(self, passwords, filename):
        """Save passwords to a text file"""
        try:
            with open(filename, 'w') as f:
                for pwd in passwords:
                    f.write(pwd + '\n')
            print(f"[+] Successfully saved {len(passwords)} passwords to {filename}")
            return True
        except Exception as e:
            print(f"[-] Error saving file: {e}")
            return False

def banner():
    print("""
╔═══════════════════════════════════════════╗
║         MassPassGen v1.0                  ║
║    Mass Password Generator Tool           ║
║    For Security Testing Purposes          ║
╚═══════════════════════════════════════════╝
    """)

def main():
    banner()
    
    parser = argparse.ArgumentParser(
        description='MassPassGen - Generate massive amounts of unique passwords',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 masspassgen.py -c 1000000 -o passwords.txt
  python3 masspassgen.py -c 500000 -l 8 -o pass8char.txt
  python3 masspassgen.py -c 100000 --min 6 --max 10 -o passwords.txt
        """
    )
    
    parser.add_argument('-c', '--count', type=int, required=True,
                        help='Number of passwords to generate')
    parser.add_argument('-o', '--output', type=str, required=True,
                        help='Output file name (e.g., passwords.txt)')
    parser.add_argument('-l', '--length', type=int,
                        help='Fixed length for all passwords')
    parser.add_argument('--min', type=int, default=6,
                        help='Minimum password length (default: 6)')
    parser.add_argument('--max', type=int, default=12,
                        help='Maximum password length (default: 12)')
    parser.add_argument('-p', '--pattern', type=str,
                        help='Pattern for generation (use {n} {a} {d} {s})')
    
    args = parser.parse_args()
    
    # Validation
    if args.min < 1 or args.max > 128:
        print("[-] Password length must be between 1 and 128")
        sys.exit(1)
    
    if args.min > args.max:
        print("[-] Minimum length cannot be greater than maximum length")
        sys.exit(1)
    
    if args.count < 1:
        print("[-] Count must be at least 1")
        sys.exit(1)
    
    if args.count > 10000000:
        response = input(f"[!] Warning: Generating {args.count} passwords may take significant time and memory. Continue? (y/n): ")
        if response.lower() != 'y':
            print("[*] Aborted")
            sys.exit(0)
    
    # Initialize generator
    gen = MassPassGen(min_len=args.min, max_len=args.max)
    
    # Generate passwords
    if args.pattern:
        passwords = gen.generate_pattern_passwords(args.pattern, args.count)
    else:
        passwords = gen.generate_random_passwords(args.count, args.length)
    
    # Save to file
    if not args.output.endswith('.txt'):
        args.output += '.txt'
    
    gen.save_to_file(passwords, args.output)
    
    print(f"\n[+] Generation complete!")
    print(f"[+] Total passwords: {len(passwords)}")
    print(f"[+] File: {args.output}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[!] Interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"[-] Error: {e}")
        sys.exit(1)