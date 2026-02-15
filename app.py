from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import os
from config import Config
from comp.cleaner import clean_and_extract
from comp.ai_processor import AIProcessor
from comp.priority_scorer import PriorityScorer
from comp.models import (
    EmailMetadata, ActionItem, EmailSummary, 
    PriorityInfo, ProcessedEmail
)
from sample_emails import get_all_samples, get_sample_email

app = Flask(__name__)
app.config.from_object(Config)
CORS(app, origins=Config.CORS_ORIGINS)

# Initialize processors
ai_processor = AIProcessor()
priority_scorer = PriorityScorer()


@app.route('/')
def index():
    """Serve the main application page."""
    return render_template('index.html')


@app.route('/api/process', methods=['POST'])
def process_email():
    """
    Process an email and return analysis.
    
    Expected JSON:
    {
        "email_text": "raw email content"
    }
    
    Returns:
    {
        "success": true,
        "data": {
            "summary": {...},
            "action_items": [...],
            "priority": {...},
            "cleaned_text": "...",
            "focus_mode_text": "..."
        }
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'email_text' not in data:
            return jsonify({
                'success': False,
                'error': 'No email text provided'
            }), 400
        
        email_text = data['email_text']
        
        if not email_text.strip():
            return jsonify({
                'success': False,
                'error': 'Email text is empty'
            }), 400
        
        # Step 1: Clean and extract metadata
        cleaned_text, metadata_dict = clean_and_extract(email_text)
        
        # Step 2: AI processing
        summary_dict = ai_processor.summarize_email(cleaned_text, metadata_dict)
        action_items_list = ai_processor.extract_action_items(cleaned_text)
        ai_signals = ai_processor.detect_priority_signals(cleaned_text, metadata_dict)
        
        # Step 3: Priority scoring
        priority_dict = priority_scorer.calculate_priority(
            cleaned_text,
            metadata_dict,
            ai_signals,
            action_items_list
        )
        
        # Step 4: Build structured response
        metadata = EmailMetadata(
            subject=metadata_dict.get('subject', ''),
            from_address=metadata_dict.get('from', ''),
            to_addresses=metadata_dict.get('to', []),
            date=metadata_dict.get('date')
        )
        
        summary = EmailSummary(
            summary=summary_dict.get('summary', ''),
            key_points=summary_dict.get('key_points', []),
            tone=summary_dict.get('tone', 'professional')
        )
        
        action_items = [
            ActionItem(
                text=item.get('text', ''),
                assignee=item.get('assignee', 'unspecified'),
                deadline=item.get('deadline', 'none'),
                confidence=item.get('confidence', 'medium')
            )
            for item in action_items_list
        ]
        
        priority = PriorityInfo(
            score=priority_dict.get('score', 0),
            level=priority_dict.get('level', 'low'),
            color=priority_dict.get('color', '#6b7280'),
            breakdown=priority_dict.get('breakdown', {})
        )
        
        # Step 5: Create processed email object
        processed = ProcessedEmail(
            original_text=email_text,
            cleaned_text=cleaned_text,
            metadata=metadata,
            summary=summary,
            action_items=action_items,
            priority=priority
        )
        
        # Generate focus mode text
        processed.generate_focus_mode()
        
        # Return response
        return jsonify({
            'success': True,
            'data': processed.to_dict()
        })
    
    except Exception as e:
        print(f"Error processing email: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/samples', methods=['GET'])
def get_samples():
    """Get all sample emails for demo purposes."""
    try:
        samples = get_all_samples()
        return jsonify({
            'success': True,
            'samples': {
                key: {
                    'name': key.replace('_', ' ').title(),
                    'content': content
                }
                for key, content in samples.items()
            }
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/sample/<sample_key>', methods=['GET'])
def get_sample(sample_key):
    """Get a specific sample email."""
    try:
        sample = get_sample_email(sample_key)
        if sample:
            return jsonify({
                'success': True,
                'sample': sample
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Sample not found'
            }), 404
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'ai_enabled': ai_processor.model is not None
    })


if __name__ == '__main__':
    print("=" * 60)
    print("🚀 Email Triage Assistant Starting...")
    print("=" * 60)
    print(f"📍 Server: http://{Config.HOST}:{Config.PORT}")
    print(f"🤖 AI Status: {'Enabled' if ai_processor.model else 'Disabled (using fallback)'}")
    if not Config.GEMINI_API_KEY:
        print("⚠️  Warning: GEMINI_API_KEY not set. Using fallback processing.")
        print("   Set GEMINI_API_KEY in .env file for full AI features.")
    print("=" * 60)
    
    app.run(
        host=Config.HOST,
        port=Config.PORT,
        debug=Config.DEBUG
    )

