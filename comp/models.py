from dataclasses import dataclass, field
from typing import List, Dict, Optional
from datetime import datetime

@dataclass
class EmailMetadata:
    """Email metadata structure."""
    subject: str = ""
    from_address: str = ""
    to_addresses: List[str] = field(default_factory=list)
    date: Optional[datetime] = None
    thread_id: Optional[str] = None
    
    def to_dict(self) -> Dict:
        return {
            'subject': self.subject,
            'from': self.from_address,
            'to': self.to_addresses,
            'date': self.date.isoformat() if self.date else None,
            'thread_id': self.thread_id
        }

@dataclass
class ActionItem:
    """Action item structure."""
    text: str
    assignee: str = "unspecified"
    deadline: str = "none"
    confidence: str = "medium"
    
    def to_dict(self) -> Dict:
        return {
            'text': self.text,
            'assignee': self.assignee,
            'deadline': self.deadline,
            'confidence': self.confidence
        }

@dataclass
class EmailSummary:
    """Email summary structure."""
    summary: str
    key_points: List[str] = field(default_factory=list)
    tone: str = "professional"
    
    def to_dict(self) -> Dict:
        return {
            'summary': self.summary,
            'key_points': self.key_points,
            'tone': self.tone
        }

@dataclass
class PriorityInfo:
    """Priority information structure."""
    score: float
    level: str
    color: str
    breakdown: Dict = field(default_factory=dict)
    
    def to_dict(self) -> Dict:
        return {
            'score': self.score,
            'level': self.level,
            'color': self.color,
            'breakdown': self.breakdown
        }

@dataclass
class ProcessedEmail:
    """Complete processed email result."""
    original_text: str
    cleaned_text: str
    metadata: EmailMetadata
    summary: EmailSummary
    action_items: List[ActionItem] = field(default_factory=list)
    priority: Optional[PriorityInfo] = None
    focus_mode_text: str = ""
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON serialization."""
        return {
            'original_text': self.original_text,
            'cleaned_text': self.cleaned_text,
            'metadata': self.metadata.to_dict(),
            'summary': self.summary.to_dict(),
            'action_items': [item.to_dict() for item in self.action_items],
            'priority': self.priority.to_dict() if self.priority else None,
            'focus_mode_text': self.focus_mode_text
        }
    
    def generate_focus_mode(self) -> str:
        """Generate focus mode text with only critical information."""
        focus_parts = []
        
        # Priority indicator
        if self.priority and self.priority.score >= 50:
            focus_parts.append(f"⚠️ {self.priority.level.upper()} PRIORITY\n")
        
        # Summary
        focus_parts.append(f"📋 {self.summary.summary}\n")
        
        # Action items
        if self.action_items:
            focus_parts.append("\n✅ ACTION ITEMS:")
            for i, item in enumerate(self.action_items, 1):
                deadline_info = f" (Due: {item.deadline})" if item.deadline != "none" else ""
                assignee_info = f" [@{item.assignee}]" if item.assignee != "unspecified" else ""
                focus_parts.append(f"{i}. {item.text}{deadline_info}{assignee_info}")
        
        # Key points
        if self.summary.key_points:
            focus_parts.append("\n🔑 KEY POINTS:")
            for point in self.summary.key_points:
                focus_parts.append(f"• {point}")
        
        self.focus_mode_text = '\n'.join(focus_parts)
        return self.focus_mode_text
