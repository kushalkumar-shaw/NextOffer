import os
import sys

# Create the AI templates directory
ai_templates_dir = os.path.join(os.path.dirname(__file__), "app", "templates", "ai")
os.makedirs(ai_templates_dir, exist_ok=True)
print(f"Created directory: {ai_templates_dir}")
