#!/usr/bin/env python3
"""
Comprehensive setup script for AI Career Chatbot feature.
This script should be run once before starting the application.
"""

import os
import shutil

def setup_ai_chatbot():
    """Set up all necessary files and directories for the AI chatbot feature."""
    
    project_root = os.path.dirname(os.path.abspath(__file__))
    
    print("=" * 60)
    print("Setting up AI Career Chatbot Feature")
    print("=" * 60)
    
    # 1. Create AI templates directory
    ai_templates_dir = os.path.join(project_root, "app", "templates", "ai")
    os.makedirs(ai_templates_dir, exist_ok=True)
    print(f"✓ Created/Verified AI templates directory: {ai_templates_dir}")
    
    # 2. Copy chatbot template
    src_template = os.path.join(project_root, "app", "templates", "candidate", "chatbot_ai.html")
    dst_template = os.path.join(ai_templates_dir, "chatbot.html")
    
    if os.path.exists(src_template):
        shutil.copy(src_template, dst_template)
        print(f"✓ Created chatbot template: {dst_template}")
    else:
        print(f"⚠ Warning: Source template not found at {src_template}")
    
    # 3. Update requirements.txt
    requirements_path = os.path.join(project_root, "requirements.txt")
    if os.path.exists(requirements_path):
        with open(requirements_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if 'google-genai' not in content:
            with open(requirements_path, 'a', encoding='utf-8') as f:
                f.write('google-genai==0.3.0\n')
            print(f"✓ Added google-genai to requirements.txt")
        else:
            print(f"✓ google-genai already in requirements.txt")
    
    # 4. Create uploads directory if it doesn't exist
    uploads_dir = os.path.join(project_root, "app", "static", "uploads")
    os.makedirs(uploads_dir, exist_ok=True)
    print(f"✓ Created/Verified uploads directory: {uploads_dir}")
    
    print("\n" + "=" * 60)
    print("Setup completed!")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Set environment variable: GEMINI_API_KEY=<your-api-key>")
    print("2. Run: pip install -r requirements.txt")
    print("3. Run: python run.py")
    print("\nTo access the chatbot:")
    print("- Login as a candidate")
    print("- Click 'AI Advisor' in the navigation menu")
    print("=" * 60)

if __name__ == '__main__':
    setup_ai_chatbot()
