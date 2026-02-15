import re
from typing import Dict, Tuple
from datetime import datetime
from bs4 import BeautifulSoup

def extract_metadata(email_text: str) -> Dict:
    """
    Extract email metadata (from, to, subject, date).
    """
    metadata = {
        'subject': '',
        'from': '',
        'to': [],
        'date': None
    }
    
    # Extract subject
    subject_match = re.search(r'Subject:\s*(.+?)(?:\n|$)', email_text, re.IGNORECASE)
    if subject_match:
        metadata['subject'] = subject_match.group(1).strip()
    
    # Extract from
    from_match = re.search(r'From:\s*(.+?)(?:\n|$)', email_text, re.IGNORECASE)
    if from_match:
        metadata['from'] = from_match.group(1).strip()
    
    # Extract to
    to_match = re.search(r'To:\s*(.+?)(?:\n|$)', email_text, re.IGNORECASE)
    if to_match:
        to_addresses = to_match.group(1).strip()
        metadata['to'] = [addr.strip() for addr in to_addresses.split(',')]
    
    # Extract date
    date_match = re.search(r'Date:\s*(.+?)(?:\n|$)', email_text, re.IGNORECASE)
    if date_match:
        try:
            # Try to parse common date formats
            date_str = date_match.group(1).strip()
            # This is a simple parser, could be enhanced
            metadata['date'] = date_str
        except:
            pass
    
    return metadata


def remove_html_tags(email_text: str) -> str:
    """
    Remove HTML tags and convert to plain text.
    """
    if '<html' in email_text.lower() or '<body' in email_text.lower():
        soup = BeautifulSoup(email_text, 'html.parser')
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()
        text = soup.get_text()
        # Clean up whitespace
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = '\n'.join(chunk for chunk in chunks if chunk)
        return text
    return email_text


def remove_quoted_text(email_text: str) -> str:
    """
    Remove quoted/forwarded text from previous emails in thread.
    """
    # Remove "On ... wrote:" style quotes
    pattern = r'On .+? wrote:.*?(?=\n\n|\Z)'
    cleaned = re.sub(pattern, '', email_text, flags=re.DOTALL)
    
    # Remove lines starting with >
    lines = cleaned.split('\n')
    cleaned_lines = [line for line in lines if not line.strip().startswith('>')]
    cleaned = '\n'.join(cleaned_lines)
    
    # Remove forwarded message markers
    cleaned = re.sub(r'-+\s*Forwarded message\s*-+.*?(?=\n\n|\Z)', '', cleaned, flags=re.DOTALL | re.IGNORECASE)
    cleaned = re.sub(r'-+\s*Original Message\s*-+.*?(?=\n\n|\Z)', '', cleaned, flags=re.DOTALL | re.IGNORECASE)
    
    return cleaned


def remove_signatures(email_text: str) -> str:
    """
    Remove common email signatures.
    """
    signature_patterns = [
        r'--\s*\n.*',               
        r'Thanks,?\s*\n[^\n]+(?:\n[^\n]+){0,3}',
        r'Regards,?\s*\n[^\n]+(?:\n[^\n]+){0,3}',
        r'Best,?\s*\n[^\n]+(?:\n[^\n]+){0,3}',
        r'Sincerely,?\s*\n[^\n]+(?:\n[^\n]+){0,3}',
        r'Cheers,?\s*\n[^\n]+(?:\n[^\n]+){0,3}',
        r'Sent from my \w+',
        r'Get Outlook for \w+',
    ]
    
    for pattern in signature_patterns:
        email_text = re.sub(pattern, '', email_text, flags=re.DOTALL | re.IGNORECASE)
    
    return email_text


def remove_email_headers(email_text: str) -> str:
    """
    Remove email headers while preserving metadata.
    """
    # Remove common headers but keep the important ones
    headers_to_remove = [
        r'Message-ID:.*?\n',
        r'MIME-Version:.*?\n',
        r'Content-Type:.*?\n',
        r'Content-Transfer-Encoding:.*?\n',
        r'X-.*?:.*?\n',
        r'Received:.*?\n',
        r'Return-Path:.*?\n',
    ]
    
    for pattern in headers_to_remove:
        email_text = re.sub(pattern, '', email_text, flags=re.IGNORECASE)
    
    return email_text


def normalize_whitespace(email_text: str) -> str:
    """
    Normalize whitespace and clean up formatting.
    """
    # Replace multiple newlines with double newline
    email_text = re.sub(r'\n\s*\n\s*\n+', '\n\n', email_text)
    
    # Remove trailing whitespace from lines
    lines = [line.rstrip() for line in email_text.split('\n')]
    email_text = '\n'.join(lines)
    
    # Trim leading/trailing whitespace
    email_text = email_text.strip()
    
    return email_text


def structural_cleanup(email_text: str) -> str:
    """
    Perform complete structural cleanup of email.
    """
    text = remove_html_tags(email_text)
    text = remove_email_headers(text)
    text = remove_quoted_text(text)
    text = remove_signatures(text)
    text = normalize_whitespace(text)
    return text


def clean_and_extract(email_text: str) -> Tuple[str, Dict]:
    """
    Clean email and extract metadata in one pass.
    
    Returns:
        Tuple of (cleaned_text, metadata_dict)
    """
    # Extract metadata first
    metadata = extract_metadata(email_text)
    
    # Then clean the text
    cleaned = structural_cleanup(email_text)
    
    return cleaned, metadata

