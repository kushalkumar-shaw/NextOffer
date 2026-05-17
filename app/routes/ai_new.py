from flask import Blueprint, render_template, request, jsonify, current_app
from flask_login import login_required, current_user
from functools import wraps
import os

try:
    from google import genai
except ImportError:
    genai = None

ai_bp = Blueprint('ai', __name__, url_prefix='/ai')


def candidate_required(f):
    """Decorator to check if user is a candidate."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'candidate':
            return jsonify({'error': 'Access denied'}), 403
        return f(*args, **kwargs)
    return decorated_function


def ensure_chatbot_template():
    """Ensure the chatbot template exists."""
    template_dir = os.path.join(current_app.template_folder, 'ai')
    os.makedirs(template_dir, exist_ok=True)
    
    template_path = os.path.join(template_dir, 'chatbot.html')
    if not os.path.exists(template_path):
        # Copy from the candidate templates directory
        src_path = os.path.join(current_app.template_folder, 'candidate', 'chatbot_ai.html')
        if os.path.exists(src_path):
            import shutil
            shutil.copy(src_path, template_path)


def build_profile_context(user):
    """Build a formatted profile context string for the Gemini prompt."""
    profile = user.candidate_profile
    if not profile:
        return "No profile information available."
    
    context = f"User Profile:\n"
    context += f"Name: {user.name}\n"
    
    if profile.bio:
        context += f"Bio: {profile.bio}\n"
    if profile.location:
        context += f"Location: {profile.location}\n"
    
    # Skills
    if profile.skills:
        context += f"\nSkills:\n"
        for skill in profile.skills:
            context += f"  - {skill.skill_name} ({skill.proficiency})\n"
    
    # Education
    if profile.education:
        context += f"\nEducation:\n"
        for edu in profile.education:
            context += f"  - {edu.degree} in {edu.field} from {edu.institution} ({edu.start_year}-{edu.end_year})\n"
            if edu.grade:
                context += f"    Grade: {edu.grade}\n"
    
    # Experience
    if profile.experience:
        context += f"\nWork Experience:\n"
        for exp in profile.experience:
            status = "Current" if exp.is_current else f"Until {exp.end_date}"
            context += f"  - {exp.role} at {exp.company} ({exp.start_date} - {status})\n"
            if exp.description:
                context += f"    {exp.description}\n"
    
    # Projects
    if profile.projects:
        context += f"\nProjects:\n"
        for proj in profile.projects:
            context += f"  - {proj.title}: {proj.description}\n"
            if proj.tech_used:
                context += f"    Tech: {proj.tech_used}\n"
    
    # Awards
    if profile.awards:
        context += f"\nAwards & Achievements:\n"
        for award in profile.awards:
            context += f"  - {award.title} by {award.issuer} ({award.date})\n"
            if award.description:
                context += f"    {award.description}\n"
    
    return context


def format_chat_for_gemini(profile_context, history):
    """Format conversation history for Gemini API."""
    system_message = f"""You are a personalized career advisor and mentor for a job seeker on the NextOffer placement portal.

{profile_context}

You have detailed knowledge of this person's profile, skills, experience, education, and projects. 

Your role is to:
1. Provide personalized career guidance based on their profile
2. Suggest relevant job opportunities and career paths
3. Help them improve their resume, cover letters, and interview skills
4. Discuss their skills and how to leverage them
5. Offer advice on skill development and career growth
6. Provide encouragement and motivation

Be conversational, supportive, and specific to their background. Ask clarifying questions when needed.
If they ask about jobs, suggest types of roles that match their profile.
Always be encouraging and constructive."""
    
    messages = []
    
    for turn in history:
        if turn.get('role') == 'user':
            messages.append({
                'role': 'user',
                'parts': [{'text': turn.get('content', '')}]
            })
        elif turn.get('role') == 'assistant':
            messages.append({
                'role': 'model',
                'parts': [{'text': turn.get('content', '')}]
            })
    
    return system_message, messages


@ai_bp.route('/chatbot', methods=['GET'])
@login_required
@candidate_required
def chatbot():
    """Render the AI chatbot interface."""
    ensure_chatbot_template()
    profile = current_user.candidate_profile
    profile_pic = profile.profile_pic if profile else None
    
    return render_template(
        'ai/chatbot.html',
        name=current_user.name,
        profile_pic=profile_pic
    )


@ai_bp.route('/chatbot/send', methods=['POST'])
@login_required
@candidate_required
def send_message():
    """Handle incoming chat messages and return AI responses."""
    if not genai:
        return jsonify({'error': 'Gemini API client not available'}), 500
    
    data = request.get_json()
    if not data or 'message' not in data:
        return jsonify({'error': 'Message is required'}), 400
    
    user_message = data.get('message', '').strip()
    history = data.get('history', [])
    
    if not user_message:
        return jsonify({'error': 'Message cannot be empty'}), 400
    
    try:
        # Get API key from environment
        api_key = os.environ.get('GEMINI_API_KEY')
        if not api_key:
            return jsonify({'error': 'Gemini API key not configured'}), 500
        
        # Initialize Gemini client
        client = genai.Client(api_key=api_key)
        
        # Build profile context
        profile_context = build_profile_context(current_user)
        
        # Limit history to last 10 turns (20 messages)
        history = history[-20:] if history else []
        
        # Format messages for Gemini
        system_message, formatted_history = format_chat_for_gemini(profile_context, history)
        
        # Add current user message
        formatted_history.append({
            'role': 'user',
            'parts': [{'text': user_message}]
        })
        
        # Call Gemini API
        response = client.models.generate_content(
            model='gemini-2.5-flash-preview-05-20',
            contents=formatted_history,
            system_instruction=system_message,
            generation_config={
                'max_output_tokens': 500,
                'temperature': 0.7,
            }
        )
        
        reply_text = response.text if response and response.text else "I couldn't generate a response. Please try again."
        
        return jsonify({'reply': reply_text})
    
    except Exception as e:
        current_app.logger.error(f'Gemini API error: {str(e)}')
        return jsonify({'error': f'Failed to get response: {str(e)}'}), 500
