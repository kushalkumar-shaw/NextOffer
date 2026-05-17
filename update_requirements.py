#!/usr/bin/env python3
"""Update requirements.txt with google-genai package."""

requirements_path = "requirements.txt"

# Read existing requirements
with open(requirements_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Check if google-genai is already there
if 'google-genai' not in content:
    # Append google-genai
    with open(requirements_path, 'a', encoding='utf-8') as f:
        f.write('google-genai==0.3.0\n')
    print("✓ Added google-genai to requirements.txt")
else:
    print("✓ google-genai already in requirements.txt")
