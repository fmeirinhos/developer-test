#!/usr/bin/env python3

import sys
sys.path.append('src')

import argparse
from backend import solve

def main():
    parser = argparse.ArgumentParser(description="Calculate the probability of success.")
    parser.add_argument("millennium_falcon", help="Path to millennium-falcon.json file.")
    parser.add_argument("empire", help="Path to empire.json file.")

    args = parser.parse_args()
    
    result = solve(args.millennium_falcon, args.empire)
    
    print(result * 100)

if __name__ == "__main__":
    main()
