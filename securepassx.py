#!/usr/bin/env python3
"""
SecurePassX - Full Password Security Suite (Kali Linux)
Author: Cybersecurity Student Project
Purpose: Ethical password testing & generation
"""

import argparse
import hashlib
import random
import string
import shutil
import time
import sys
from datetime import datetime

# -------- COLORS -------- #
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
RESET = "\033[0m"

VERSION = "2.0"


# -------- BANNER -------- #
def banner():
    print(CYAN + "=" * 55)
    print("        SecurePassX - Password Security Suite")
    print("        Ethical Password Testing Toolkit")
    print("=" * 55 + RESET)


# -------- PROGRESS BAR -------- #
def progress_bar(msg="Processing..."):
    print(YELLOW + f"\n{msg}" + RESET)
    for i in range(1, 11):
        sys.stdout.write(f"\rProgress: {i*10}%")
        sys.stdout.flush()
        time.sleep(0.15)
    print("\n")


# -------- PASSWORD STRENGTH TEST -------- #
def test_password(password):
    score = 0

    if len(password) >= 8:
        score += 1
    if any(c.isupper() for c in password):
        score += 1
    if any(c.islower() for c in password):
        score += 1
    if any(c.isdigit() for c in password):
        score += 1
    if any(c in "!@#$%^&*()_+" for c in password):
        score += 1

    return score


def strength_result(score):
    if score <= 2:
        return RED + "Weak Password ❌" + RESET
    elif score == 3:
        return YELLOW + "Medium Password ⚠️" + RESET
    else:
        return GREEN + "Strong Password ✅" + RESET


# -------- PASSWORD GENERATOR -------- #
def generate_password(length=16):
    chars = string.ascii_letters + string.digits + "!@#$%^&*()_+"
    return ''.join(random.choice(chars) for _ in range(length))


# -------- HASH GENERATOR -------- #
def generate_hash(text, algo="sha256"):
    if algo == "md5":
        return hashlib.md5(text.encode()).hexdigest()
    else:
        return hashlib.sha256(text.encode()).hexdigest()


# -------- CRACKLIB CHECK -------- #
def cracklib_check(password):
    if not shutil.which("cracklib-check"):
        return RED + "Cracklib not installed!" + RESET

    import subprocess
    result = subprocess.run(
        ["cracklib-check"],
        input=password.encode(),
        stdout=subprocess.PIPE
    )
    return result.stdout.decode().strip()


# -------- SAVE REPORT -------- #
def save_report(content, filename):
    with open(filename, "a") as f:
        f.write("\n" + "=" * 50 + "\n")
        f.write(f"SecurePassX Report - {datetime.now()}\n")
        f.write(content + "\n")
        f.write("=" * 50 + "\n")

    print(GREEN + f"\n[+] Report saved to {filename}" + RESET)


# -------- CHECK KALI TOOLS -------- #
def check_kali_tools():
    tools = ["john", "hydra", "hashcat", "cracklib-check"]

    print(CYAN + "\nChecking Kali Password Tools...\n" + RESET)
    for tool in tools:
        if shutil.which(tool):
            print(GREEN + f"[OK] {tool} installed" + RESET)
        else:
            print(RED + f"[MISSING] {tool} not found" + RESET)


# -------- MAIN -------- #
def main():
    banner()

    parser = argparse.ArgumentParser(
        description="SecurePassX - Full Password Security Suite"
    )

    parser.add_argument("--test", help="Test password strength")
    parser.add_argument("--generate", action="store_true", help="Generate strong password")
    parser.add_argument("--len", type=int, default=16, help="Length for generated password")

    parser.add_argument("--hash", help="Generate hash for text")
    parser.add_argument("--algo", choices=["md5", "sha256"], default="sha256",
                        help="Hash algorithm")

    parser.add_argument("--cracklib", help="Check password with cracklib dictionary")

    parser.add_argument("--check-tools", action="store_true",
                        help="Check installed Kali password tools")

    parser.add_argument("--report", help="Save output to TXT file")

    parser.add_argument("--version", action="version",
                        version=f"SecurePassX Version {VERSION}")

    args = parser.parse_args()

    output_log = ""

    # ---- TOOL CHECK ---- #
    if args.check_tools:
        check_kali_tools()
        return

    # ---- PASSWORD TEST ---- #
    if args.test:
        progress_bar("Testing password strength...")
        score = test_password(args.test)
        result = strength_result(score)

        print(CYAN + "Password Strength:" + RESET, result)
        output_log += f"Password Tested: {args.test}\nResult: {result}\n"

    # ---- PASSWORD GENERATOR ---- #
    if args.generate:
        progress_bar("Generating strong password...")
        pwd = generate_password(args.len)

        print(GREEN + "Generated Password:" + RESET, pwd)
        output_log += f"Generated Password: {pwd}\n"

    # ---- HASH GENERATOR ---- #
    if args.hash:
        progress_bar("Generating hash...")
        h = generate_hash(args.hash, args.algo)

        print(CYAN + f"{args.algo.upper()} Hash:" + RESET, h)
        output_log += f"Hash ({args.algo}): {h}\n"

    # ---- CRACKLIB CHECK ---- #
    if args.cracklib:
        progress_bar("Running Cracklib dictionary check...")
        result = cracklib_check(args.cracklib)

        print(CYAN + "Cracklib Result:" + RESET, result)
        output_log += f"Cracklib Check: {result}\n"

    # ---- SAVE REPORT ---- #
    if args.report and output_log:
        save_report(output_log, args.report)

    if not any(vars(args).values()):
        print(RED + "No arguments provided. Use -h for help." + RESET)


# -------- RUN -------- #
if __name__ == "__main__":
    main()

