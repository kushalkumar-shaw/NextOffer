import os
from app import create_app

if __name__ == '__main__':
    # Create AI templates directory and chatbot.html if it doesn't exist
    project_root = os.path.dirname(os.path.abspath(__file__))
    ai_templates_dir = os.path.join(project_root, "app", "templates", "ai")
    os.makedirs(ai_templates_dir, exist_ok=True)
    
    chatbot_template_path = os.path.join(ai_templates_dir, "chatbot.html")
    if not os.path.exists(chatbot_template_path):
        # We'll let the app create this on first run if needed
        pass
    
    app = create_app(os.environ.get('FLASK_ENV', 'development'))
    app.run(debug=True, host='127.0.0.1', port=5000)
