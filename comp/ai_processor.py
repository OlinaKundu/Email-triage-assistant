import os
import re
from typing import Dict, List, Optional
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

class AIProcessor:
    """AI-powered email analysis using Google Gemini."""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize the AI processor with Gemini API."""
        self.api_key = api_key or os.getenv('GEMINI_API_KEY')
        if self.api_key:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-pro')
        else:
            self.model = None
    
    def summarize_email(self, email_text: str, metadata: Dict = None) -> Dict:
        """
        Generate a comprehensive summary of the email thread.
        
        Args:
            email_text: Cleaned email content
            metadata: Email metadata (subject, from, to, date)
            
        Returns:
            Dictionary with summary, key points, and tone
        """
        if not self.model:
            return self._fallback_summary(email_text)
        
        try:
            prompt = f"""Analyze this email thread and provide a concise summary.

Email Content:
{email_text}

Please provide:
1. A brief 2-3 sentence summary of the main topic
2. Key points (bullet points, max 5)
3. Overall tone (professional/urgent/casual/friendly)

Format your response as:
SUMMARY: [your summary]
KEY_POINTS:
- [point 1]
- [point 2]
TONE: [tone]"""

            response = self.model.generate_content(prompt)
            return self._parse_summary_response(response.text)
        
        except Exception as e:
            print(f"AI processing error: {e}")
            return self._fallback_summary(email_text)
    
    def extract_action_items(self, email_text: str) -> List[Dict]:
        """
        Extract action items from the email with confidence scores.
        
        Returns:
            List of action items with text, assignee, deadline, and confidence
        """
        if not self.model:
            return self._fallback_actions(email_text)
        
        try:
            prompt = f"""Extract all action items from this email thread.

Email Content:
{email_text}

For each action item, identify:
- The specific task or action required
- Who is responsible (if mentioned)
- Any deadline or time constraint (if mentioned)
- Confidence level (high/medium/low)

Format each action as:
ACTION: [task description]
ASSIGNEE: [person or "unspecified"]
DEADLINE: [date/time or "none"]
CONFIDENCE: [high/medium/low]
---

If there are no clear action items, respond with: NO_ACTIONS"""

            response = self.model.generate_content(prompt)
            return self._parse_action_items(response.text)
        
        except Exception as e:
            print(f"Action extraction error: {e}")
            return self._fallback_actions(email_text)
    
    def detect_priority_signals(self, email_text: str, metadata: Dict = None) -> Dict:
        """
        Detect priority signals in the email.
        
        Returns:
            Dictionary with urgency level, importance, and key signals
        """
        if not self.model:
            return self._fallback_priority(email_text)
        
        try:
            subject = metadata.get('subject', '') if metadata else ''
            prompt = f"""Analyze the priority and urgency of this email.

Subject: {subject}
Content:
{email_text}

Determine:
1. Urgency level (urgent/normal/low)
2. Importance (critical/important/informational)
3. Key signals that indicate priority (deadlines, urgent keywords, etc.)

Format:
URGENCY: [level]
IMPORTANCE: [level]
SIGNALS: [comma-separated signals]"""

            response = self.model.generate_content(prompt)
            return self._parse_priority_response(response.text)
        
        except Exception as e:
            print(f"Priority detection error: {e}")
            return self._fallback_priority(email_text)
    
    def _parse_summary_response(self, response_text: str) -> Dict:
        """Parse the AI summary response."""
        summary = ""
        key_points = []
        tone = "professional"
        
        lines = response_text.strip().split('\n')
        current_section = None
        
        for line in lines:
            line = line.strip()
            if line.startswith('SUMMARY:'):
                summary = line.replace('SUMMARY:', '').strip()
            elif line.startswith('KEY_POINTS:'):
                current_section = 'points'
            elif line.startswith('TONE:'):
                tone = line.replace('TONE:', '').strip().lower()
                current_section = None
            elif current_section == 'points' and line.startswith('-'):
                key_points.append(line[1:].strip())
        
        return {
            'summary': summary,
            'key_points': key_points,
            'tone': tone
        }
    
    def _parse_action_items(self, response_text: str) -> List[Dict]:
        """Parse action items from AI response."""
        if 'NO_ACTIONS' in response_text:
            return []
        
        actions = []
        current_action = {}
        
        for line in response_text.strip().split('\n'):
            line = line.strip()
            if line.startswith('ACTION:'):
                if current_action:
                    actions.append(current_action)
                current_action = {'text': line.replace('ACTION:', '').strip()}
            elif line.startswith('ASSIGNEE:'):
                current_action['assignee'] = line.replace('ASSIGNEE:', '').strip()
            elif line.startswith('DEADLINE:'):
                current_action['deadline'] = line.replace('DEADLINE:', '').strip()
            elif line.startswith('CONFIDENCE:'):
                current_action['confidence'] = line.replace('CONFIDENCE:', '').strip()
            elif line == '---' and current_action:
                actions.append(current_action)
                current_action = {}
        
        if current_action:
            actions.append(current_action)
        
        return actions
    
    def _parse_priority_response(self, response_text: str) -> Dict:
        """Parse priority detection response."""
        urgency = "normal"
        importance = "informational"
        signals = []
        
        for line in response_text.strip().split('\n'):
            line = line.strip()
            if line.startswith('URGENCY:'):
                urgency = line.replace('URGENCY:', '').strip().lower()
            elif line.startswith('IMPORTANCE:'):
                importance = line.replace('IMPORTANCE:', '').strip().lower()
            elif line.startswith('SIGNALS:'):
                signals_text = line.replace('SIGNALS:', '').strip()
                signals = [s.strip() for s in signals_text.split(',')]
        
        return {
            'urgency': urgency,
            'importance': importance,
            'signals': signals
        }
    
    def _fallback_summary(self, email_text: str) -> Dict:
        """Fallback summary when AI is unavailable."""
        lines = [l.strip() for l in email_text.split('\n') if l.strip()]
        summary = ' '.join(lines[:3])[:200] + '...'
        
        return {
            'summary': summary,
            'key_points': lines[:3],
            'tone': 'professional'
        }
    
    def _fallback_actions(self, email_text: str) -> List[Dict]:
        """Fallback action detection using keywords."""
        action_keywords = [
            'please', 'could you', 'can you', 'need to', 'should',
            'must', 'required', 'action', 'todo', 'task'
        ]
        
        actions = []
        for line in email_text.split('\n'):
            line = line.strip()
            if any(keyword in line.lower() for keyword in action_keywords):
                actions.append({
                    'text': line,
                    'assignee': 'unspecified',
                    'deadline': 'none',
                    'confidence': 'low'
                })
        
        return actions[:5]  # Limit to 5 actions
    
    def _fallback_priority(self, email_text: str) -> Dict:
        """Fallback priority detection using keywords."""
        urgent_keywords = ['urgent', 'asap', 'immediately', 'critical', 'emergency']
        important_keywords = ['important', 'priority', 'deadline', 'required']
        
        text_lower = email_text.lower()
        urgency = 'normal'
        importance = 'informational'
        signals = []
        
        for keyword in urgent_keywords:
            if keyword in text_lower:
                urgency = 'urgent'
                signals.append(keyword)
        
        for keyword in important_keywords:
            if keyword in text_lower:
                importance = 'important'
                if keyword not in signals:
                    signals.append(keyword)
        
        return {
            'urgency': urgency,
            'importance': importance,
            'signals': signals
        }
