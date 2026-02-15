# Email Triage Assistant

An AI-powered tool designed to help you manage email overload by automatically summarizing long threads, detecting action items, and highlighting what matters most.

## Overview

Long email chains are exhausting. They're full of repeated replies, signatures, and formatting that make it hard to find the important stuff. This project tackles that problem by using AI to compress conversations, generate summaries, and help you quickly identify what needs your attention.

The goal here is to build something actually useful for productivity, not just another AI demo.

## Features

### What It Does

- Intelligent email thread summarization using Google Gemini
- Automatic extraction of action items, tasks, and deadlines
- Priority scoring system (0-100 scale) based on multiple signals
- Focus Mode for distraction-free reading
- Dark mode support
- Visual priority breakdown showing urgency, importance, and time sensitivity

### Technical Features

- ScaleDown compression removes quoted text, signatures, and noise
- Automatic metadata extraction (subject, from, to, date)
- Handles both plain text and HTML emails
- Fallback processing works without API key using keyword analysis
- Modern, responsive web interface

## Getting Started

### What You'll Need

- Python 3.8 or higher
- pip package manager
- Google Gemini API key (optional but recommended for full features)

### Installation

Clone the repository:
```bash
git clone https://github.com/your-username/email-triage-assistant.git
cd email-triage-assistant
```

Install dependencies:
```bash
pip install -r requirements.txt
```

Set up your environment (optional but recommended):
```bash
copy .env.example .env
# Edit .env and add your Gemini API key
# Get a free key at: https://makersuite.google.com/app/apikey
```

Run the application:
```bash
python app.py
```

Open your browser and go to `http://localhost:5000`

## How to Use

### Quick Demo

The easiest way to see what this does is to use one of the sample emails:

1. Open the app in your browser
2. Click the "Try a sample" dropdown
3. Select any sample email (try "Urgent Deadline" for a good demo)
4. Click "Analyze Email"
5. Toggle between Full Analysis and Focus Mode to see different views

### Analyzing Your Own Emails

1. Copy an email thread from your inbox (include headers like Subject, From, To if possible)
2. Paste it into the text area
3. Click "Analyze Email"
4. Review the results: priority score, summary, action items, and key points

### Focus Mode

Focus Mode strips away everything except the essentials. It shows you:
- Priority level
- Brief summary
- Action items with deadlines
- Key points

You can copy the Focus Mode text to your clipboard with one click.

## How It Works

The processing pipeline looks like this:

```
Email Input → ScaleDown Compression → AI Processing → Priority Scoring → Output
```

### Processing Stages

**1. Preprocessing** (`comp/cleaner.py`)
- Removes HTML tags and converts to plain text
- Extracts metadata (subject, sender, recipients, date)
- Strips out quoted text and signatures
- Normalizes whitespace

**2. AI Analysis** (`comp/ai_processor.py`)
- Generates a concise summary of the email content
- Extracts action items with confidence scores
- Detects priority signals and tone

**3. Priority Scoring** (`comp/priority_scorer.py`)
- Analyzes urgency based on keywords and context
- Evaluates importance
- Calculates action density
- Considers sender importance
- Assesses time sensitivity

**4. Output Generation** (`comp/models.py`)
- Structures all data into clean models
- Generates Focus Mode text
- Prepares JSON for the frontend

## Tech Stack

### Backend
- Python 3.8+
- Flask 3.0 for the web framework
- Google Gemini for AI processing
- BeautifulSoup4 for HTML parsing

### Frontend
- HTML5 with semantic structure
- CSS3 with modern styling and CSS variables
- Vanilla JavaScript (no frameworks)
- Inter font from Google Fonts

### Key Dependencies
- `google-generativeai` for Gemini API integration
- `python-dotenv` for environment configuration
- `Flask-CORS` for cross-origin support

## Project Structure

```
email-triage-assistant/
├── app.py                  # Flask application and API endpoints
├── config.py               # Configuration management
├── sample_emails.py        # Demo email data
├── requirements.txt        # Python dependencies
├── .env.example           # Environment template
├── comp/                  # Core processing modules
│   ├── cleaner.py         # Email cleaning and metadata extraction
│   ├── ai_processor.py    # AI summarization and analysis
│   ├── priority_scorer.py # Priority calculation
│   └── models.py          # Data models
├── templates/
│   └── index.html         # Main application page
├── static/
│   ├── css/
│   │   └── styles.css     # Styling
│   └── js/
│       └── app.js         # Frontend logic
└── scaledown/
    └── documentation.md   # Technical documentation
```

## API Endpoints

### POST /api/process
Processes an email and returns the analysis.

Request body:
```json
{
  "email_text": "your email content here"
}
```

### GET /api/samples
Returns all available sample emails for demo purposes.

### GET /api/sample/<key>
Returns a specific sample email by key.

### GET /api/health
Health check endpoint that also reports AI status.

## Design Decisions

The interface uses vibrant gradients instead of flat colors, glassmorphism effects for a modern look, and smooth animations throughout. Dark mode is fully supported with carefully chosen colors that maintain readability.

The UX focuses on minimal cognitive load with a clean interface, progressive disclosure of details, instant feedback through loading states, and proper accessibility with semantic HTML.

## Future Ideas

Some things I'd like to add eventually:
- Gmail and Outlook API integration
- Batch processing for multiple emails
- Email thread visualization
- Custom priority rules
- Export to task management tools
- Browser extension
- Mobile app

## Author

Olina Kundu

Built while exploring AI agents, productivity tools, and practical NLP workflows.

## License

MIT License - feel free to use this for learning or building your own tools.

## Acknowledgments

Thanks to Google for the Gemini API, the Flask community for great documentation, and various sources for design inspiration.


