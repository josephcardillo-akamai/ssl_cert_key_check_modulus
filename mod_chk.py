#!/usr/bin/env python3

# Script to compare modulus values between certificate and key
# Usage: test.py -c <certificate> -k <key>

import sys, getopt
import subprocess
from subprocess import run
from os.path import exists

def main(argv):
    try:
        opts, args = getopt.getopt(argv,"c:k:",["certificate=","key="])
    except getopt.GetoptError:
        print('test.py -c <certificate> -k <key>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('test.py -i <certificate> -o <key>')
            sys.exit()
        elif opt in ("-c", "--certificate"):
            certificate = arg
        elif opt in ("-k", "--key"):
            key = arg
    try:
        cert_file_exists = exists(certificate)
        key_file_exists = exists(key)
        if cert_file_exists and key_file_exists:
            # openssl modulus commands
            get_key_mod_cmd = f"openssl rsa -noout -modulus -in {key} | openssl md5"
            get_cert_mod_cmd = f"openssl x509 -noout -modulus -in {certificate} | openssl md5"

            # Get key and cert mods
            key_mod = run(get_key_mod_cmd, shell=True, capture_output=True, text=True)
            print(f"Key modulus  : {key_mod.stdout}", end = '')
            cert_mod = run(get_cert_mod_cmd, shell=True, capture_output=True, text=True)
            print(f"Cert modulus : {cert_mod.stdout}", end = '')
            # Compare key and cert mods
            if key_mod.stdout == cert_mod.stdout:
                print("==========")
                print("MODS MATCH")
                print("==========")
            else:
                print("================")
                print("MODS DON'T MATCH")
                print("================")
        else:
            print("One or more file paths are incorrect.")
    except getopt.GetoptError:
        sys.exit(1)

if __name__ == "__main__":
   main(sys.argv[1:])