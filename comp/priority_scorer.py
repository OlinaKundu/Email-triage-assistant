import re
from typing import Dict, List
from datetime import datetime, timedelta

class PriorityScorer:
    """Calculate priority scores for emails based on multiple signals."""
    
    URGENT_KEYWORDS = [
        'urgent', 'asap', 'immediately', 'critical', 'emergency',
        'time-sensitive', 'high priority', 'deadline'
    ]
    
    IMPORTANT_KEYWORDS = [
        'important', 'priority', 'required', 'must', 'need',
        'action required', 'please review', 'approval needed'
    ]
    
    VIP_DOMAINS = [
        'ceo', 'cto', 'cfo', 'president', 'director', 'vp',
        'manager', 'lead', 'head'
    ]
    
    def __init__(self):
        self.weights = {
            'urgency': 0.30,
            'importance': 0.25,
            'action_density': 0.20,
            'sender_importance': 0.15,
            'time_sensitivity': 0.10
        }
    
    def calculate_priority(
        self,
        email_text: str,
        metadata: Dict = None,
        ai_signals: Dict = None,
        action_items: List[Dict] = None
    ) -> Dict:
        """
        Calculate overall priority score (0-100).
        
        Args:
            email_text: Email content
            metadata: Email metadata (from, subject, date)
            ai_signals: AI-detected priority signals
            action_items: Extracted action items
            
        Returns:
            Dictionary with score, level, and breakdown
        """
        scores = {
            'urgency': self._score_urgency(email_text, metadata, ai_signals),
            'importance': self._score_importance(email_text, metadata, ai_signals),
            'action_density': self._score_action_density(action_items),
            'sender_importance': self._score_sender(metadata),
            'time_sensitivity': self._score_time_sensitivity(email_text, action_items)
        }
        
        # Calculate weighted total
        total_score = sum(
            scores[key] * self.weights[key]
            for key in scores
        )
        
        # Determine priority level
        if total_score >= 75:
            level = 'critical'
            color = '#ef4444'  # red
        elif total_score >= 50:
            level = 'high'
            color = '#f59e0b'  # orange
        elif total_score >= 25:
            level = 'medium'
            color = '#3b82f6'  # blue
        else:
            level = 'low'
            color = '#6b7280'  # gray
        
        return {
            'score': round(total_score, 1),
            'level': level,
            'color': color,
            'breakdown': scores
        }
    
    def _score_urgency(self, email_text: str, metadata: Dict, ai_signals: Dict) -> float:
        """Score urgency (0-100)."""
        score = 0
        text_lower = email_text.lower()
        subject_lower = metadata.get('subject', '').lower() if metadata else ''
        
        # Check for urgent keywords
        urgent_count = sum(1 for keyword in self.URGENT_KEYWORDS if keyword in text_lower)
        score += min(urgent_count * 20, 60)
        
        # Subject line urgency
        if any(keyword in subject_lower for keyword in self.URGENT_KEYWORDS):
            score += 30
        
        # AI-detected urgency
        if ai_signals and ai_signals.get('urgency') == 'urgent':
            score += 40
        
        return min(score, 100)
    
    def _score_importance(self, email_text: str, metadata: Dict, ai_signals: Dict) -> float:
        """Score importance (0-100)."""
        score = 0
        text_lower = email_text.lower()
        
        # Check for important keywords
        important_count = sum(1 for keyword in self.IMPORTANT_KEYWORDS if keyword in text_lower)
        score += min(important_count * 15, 50)
        
        # AI-detected importance
        if ai_signals:
            importance = ai_signals.get('importance', 'informational')
            if importance == 'critical':
                score += 50
            elif importance == 'important':
                score += 30
        
        # Exclamation marks (but cap it to avoid spam)
        exclamation_count = email_text.count('!')
        score += min(exclamation_count * 5, 20)
        
        return min(score, 100)
    
    def _score_action_density(self, action_items: List[Dict]) -> float:
        """Score based on number and confidence of action items (0-100)."""
        if not action_items:
            return 0
        
        score = 0
        
        # Base score for having actions
        score += min(len(action_items) * 20, 60)
        
        # Bonus for high-confidence actions
        high_confidence = sum(1 for item in action_items if item.get('confidence') == 'high')
        score += min(high_confidence * 15, 40)
        
        return min(score, 100)
    
    def _score_sender(self, metadata: Dict) -> float:
        """Score sender importance (0-100)."""
        if not metadata or 'from' not in metadata:
            return 50  # Default neutral score
        
        sender = metadata['from'].lower()
        score = 50  # Base score
        
        # Check for VIP titles
        for vip_term in self.VIP_DOMAINS:
            if vip_term in sender:
                score += 30
                break
        
        # External vs internal (simple heuristic)
        if '@' in sender:
            # Could be enhanced with company domain checking
            pass
        
        return min(score, 100)
    
    def _score_time_sensitivity(self, email_text: str, action_items: List[Dict]) -> float:
        """Score time sensitivity based on deadlines (0-100)."""
        score = 0
        
        # Check for deadline-related keywords
        deadline_keywords = ['deadline', 'due', 'by end of', 'before', 'until']
        text_lower = email_text.lower()
        
        for keyword in deadline_keywords:
            if keyword in text_lower:
                score += 20
        
        # Check action items for deadlines
        if action_items:
            for item in action_items:
                deadline = item.get('deadline', 'none')
                if deadline and deadline != 'none':
                    # Try to parse deadline urgency
                    if any(word in deadline.lower() for word in ['today', 'asap', 'immediately']):
                        score += 40
                    elif any(word in deadline.lower() for word in ['tomorrow', 'this week']):
                        score += 30
                    else:
                        score += 20
        
        # Look for time patterns (today, tomorrow, specific dates)
        time_patterns = [
            r'\btoday\b', r'\btomorrow\b', r'\bthis week\b',
            r'\d{1,2}/\d{1,2}', r'\d{1,2}-\d{1,2}'
        ]
        
        for pattern in time_patterns:
            if re.search(pattern, text_lower):
                score += 15
        
        return min(score, 100)
    
    def get_priority_label(self, score: float) -> str:
        """Get human-readable priority label."""
        if score >= 75:
            return '🔴 Critical'
        elif score >= 50:
            return '🟠 High Priority'
        elif score >= 25:
            return '🔵 Medium Priority'
        else:
            return '⚪ Low Priority'
