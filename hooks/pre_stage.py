#!/usr/bin/env python3
"""Example hook. Reads stage name as argv[1]; blocks only via exit status."""
import sys
print(f"[pre-stage] {sys.argv[1] if len(sys.argv)>1 else 'unknown'}")
