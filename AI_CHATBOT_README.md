# AI Career Chatbot Feature - Setup & Usage Guide

## Overview

The AI Career Chatbot is a personalized career advisor powered by Google's Gemini API. It analyzes a candidate's profile (skills, experience, education, projects, awards) and provides tailored career guidance, job recommendations, and professional development advice.

## Features

- **Personalized Context**: The chatbot has access to the logged-in candidate's complete profile
- **Conversation History**: Maintains the last 10 conversation turns for contextual responses
- **Markdown Support**: AI responses support bold text and bullet points
- **Quick Suggestions**: Pre-populated quick-reply buttons for common questions
- **Typing Indicator**: Visual feedback while waiting for AI responses
- **Responsive Design**: Works on desktop and mobile devices

## Architecture

### Backend (app/routes/ai.py)

- **GET /ai/chatbot**: Renders the chatbot interface with candidate's name and profile picture
- **POST /ai/chatbot/send**: Accepts JSON with user message and conversation history, returns AI response

### Frontend (app/templates/ai/chatbot.html)

- Beautiful chat UI with message bubbles
- Scrollable message history
- Input box with send button
- Quick-reply suggestion buttons
- Typing indicator animation
- Markdown rendering for AI responses

### Gemini Integration

- Model: `gemini-2.5-flash-preview-05-20`
- System prompt includes candidate's full profile context
- Conversation history (last 20 messages / 10 turns) is maintained for continuity
- Configured for career guidance, job matching, and resume improvement advice

## Installation & Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

The `google-genai==0.3.0` package is already added to requirements.txt

### 2. Set Environment Variable

Set your Gemini API key as an environment variable:

**On Windows (Command Prompt):**
```bash
set GEMINI_API_KEY=your_api_key_here
```

**On Windows (PowerShell):**
```powershell
$env:GEMINI_API_KEY="your_api_key_here"
```

**On Linux/Mac:**
```bash
export GEMINI_API_KEY=your_api_key_here
```

### 3. Run Setup Script (Optional)

```bash
python setup_chatbot.py
```

This script will:
- Create the AI templates directory
- Copy the chatbot template to the correct location
- Verify the google-genai package is in requirements.txt
- Create the uploads directory if needed

### 4. Start the Application

```bash
python run.py
```

The app will automatically:
- Create the AI templates directory during initialization (in `app/__init__.py`)
- Set up the chatbot route

## Usage

1. **Login as a Candidate**
   - Register or login with candidate credentials
   
2. **Access the Chatbot**
   - Click "AI Advisor" in the navigation menu (visible only for candidates)
   - Or navigate directly to `/ai/chatbot`

3. **Start Chatting**
   - See the greeting message with your name
   - Use quick-reply buttons or type your question
   - Chat history is maintained during your session

## Quick-Reply Suggestions

The chatbot provides three pre-populated suggestions:
- "Review my profile" - Get feedback on your profile
- "What jobs suit me?" - Get job recommendations based on your skills
- "How can I improve my resume?" - Get resume improvement tips

## System Prompt & Context

The chatbot receives a comprehensive system prompt that includes:
- Candidate's name, bio, and location
- All skills with proficiency levels
- Education history (degree, field, institution, year, grade)
- Work experience (company, role, dates, description)
- Projects (title, description, technologies)
- Awards and achievements

This ensures all responses are personalized to the candidate's background.

## API Key Management

### Getting a Gemini API Key

1. Go to [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Click "Create API Key" in a new Google Cloud project
3. Copy the API key
4. Set it as the `GEMINI_API_KEY` environment variable

### Security Notes

- **Never commit API keys** to version control
- Use environment variables or `.env` files (with `.env` in `.gitignore`)
- In production, use secure secret management (AWS Secrets Manager, Azure Key Vault, etc.)
- The API key is only used on the backend; the frontend never sees it

## File Structure

```
NextOffer/
├── app/
│   ├── routes/
│   │   └── ai.py                    # AI chatbot routes (NEW)
│   ├── templates/
│   │   ├── ai/
│   │   │   └── chatbot.html         # Chatbot UI (NEW)
│   │   ├── candidate/
│   │   │   └── chatbot_ai.html      # Template source (NEW)
│   │   └── base.html                # Updated with AI Advisor link
│   ├── models.py                    # (unchanged)
│   ├── __init__.py                  # Updated to register ai blueprint
│   └── ...
├── requirements.txt                 # Added google-genai
├── run.py                           # Updated with template setup
├── setup_chatbot.py                 # Setup script (NEW)
└── ...
```

## Error Handling

### "Gemini API key not configured"
- Make sure `GEMINI_API_KEY` environment variable is set
- Verify the API key is valid

### "Access denied" (403)
- Only candidates can access the chatbot
- Login with a candidate account

### Template loading errors
- Run `python setup_chatbot.py` to ensure templates are created
- Check that `app/templates/ai/chatbot.html` exists

## Troubleshooting

### Chatbot not appearing in navigation
- Make sure you're logged in as a candidate
- Check that the `ai` blueprint is registered in `app/__init__.py`

### API calls failing
- Check browser developer tools (F12 → Network tab)
- Verify `GEMINI_API_KEY` environment variable is set
- Check Flask logs for detailed error messages

### Template not found
- Run `python setup_chatbot.py`
- Or manually ensure `app/templates/ai/chatbot.html` exists

## Performance Considerations

- Conversation history is limited to last 10 turns (20 messages) to reduce API costs
- Profile context is fetched once per chat load from the database
- AI responses are limited to 500 tokens (approximately 150 words)
- Temperature is set to 0.7 for balanced creativity and consistency

## Future Enhancements

- [ ] Save chat history to database
- [ ] Export conversation as PDF
- [ ] Voice input/output support
- [ ] Multiple chatbot personas (career coach, interview prep, salary negotiator)
- [ ] Integration with job recommendations
- [ ] Chat analytics (topics discussed, sentiment analysis)
- [ ] Scheduled check-ins and reminders
- [ ] Integration with LinkedIn profile import

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review Flask error logs
3. Verify environment variables are set correctly
4. Check API key validity on Google AI Studio

## Resources

- [Google Generative AI Python SDK](https://github.com/google/generative-ai-python)
- [Gemini API Documentation](https://ai.google.dev/docs)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [NextOffer Custom Instructions](./CLAUDE.md)
