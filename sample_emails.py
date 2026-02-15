"""
Sample email threads for testing and demonstration.
"""

SAMPLE_EMAILS = {
    "urgent_deadline": """Subject: URGENT: Q4 Report Due Tomorrow
From: sarah.johnson@company.com
To: team@company.com
Date: Mon, 15 Feb 2026 14:30:00

Hi team,

We need to finalize the Q4 financial report by end of day tomorrow. This is critical for the board meeting on Wednesday.

Action items:
1. Alex - please review the revenue projections and send your approval by 5 PM today
2. Maria - update the expense breakdown with final numbers
3. John - prepare the executive summary (2 pages max)

This is high priority and we cannot miss this deadline. Please confirm you can complete your tasks.

Thanks,
Sarah Johnson
Director of Finance
""",

    "meeting_coordination": """Subject: Re: Project Kickoff Meeting
From: mike.chen@company.com
To: project-team@company.com
Date: Mon, 15 Feb 2026 10:15:00

Thanks for the agenda, Lisa.

I can do Thursday at 2 PM. The conference room on the 5th floor should work.

Could someone please book the room and send out calendar invites? Also, we should prepare:
- Project timeline overview
- Resource allocation plan
- Risk assessment

Let me know if you need anything else.

Best,
Mike

On Mon, 15 Feb 2026 at 09:30, Lisa Park wrote:
> Hi everyone,
> 
> Let's schedule our project kickoff meeting for this week. 
> What times work for everyone?
> 
> Thanks,
> Lisa
""",

    "long_thread": """Subject: Re: Re: Re: Website Redesign Feedback
From: alex.rivera@company.com
To: design-team@company.com
Date: Mon, 15 Feb 2026 16:45:00

I've reviewed all the feedback and here's my summary:

The new homepage design looks great overall. A few points:

1. The hero section needs more contrast - the text is hard to read
2. Mobile navigation could be simplified
3. Loading time is excellent, good job on optimization
4. The color scheme aligns well with our brand guidelines

I approve moving forward with implementation. Please create a staging environment so stakeholders can review before we go live.

Timeline:
- Staging ready: Feb 20
- Stakeholder review: Feb 21-23
- Launch: Feb 25

Let me know if this timeline works for everyone.

Alex Rivera
Head of Product

On Mon, 15 Feb 2026 at 14:20, Jamie Lee wrote:
> Updated designs are in Figma. Please review.
> 
> On Mon, 15 Feb 2026 at 11:00, Alex Rivera wrote:
> > Can we see the mobile version?
> > 
> > On Fri, 12 Feb 2026 at 16:30, Jamie Lee wrote:
> > > Here's the first draft of the homepage redesign.
> > > Feedback welcome!
""",

    "fyi_update": """Subject: Weekly Team Update - Feb 15
From: manager@company.com
To: team@company.com
Date: Mon, 15 Feb 2026 09:00:00

Hi team,

Quick updates for this week:

- The new office space is ready, we'll move next Monday
- Employee survey results will be shared on Wednesday
- Company all-hands meeting is scheduled for Friday at 3 PM
- Remember to submit your timesheets by EOD Friday

Have a great week!

Best,
Jordan
""",

    "action_required": """Subject: Action Required: Security Training Completion
From: security@company.com
To: all-employees@company.com
Date: Mon, 15 Feb 2026 08:00:00

IMPORTANT: Annual Security Training

All employees must complete the annual security awareness training by February 20, 2026.

To complete:
1. Log into the training portal at training.company.com
2. Complete the "Security Awareness 2026" course (approximately 45 minutes)
3. Pass the final quiz (80% required)

This is mandatory and your access may be restricted if not completed by the deadline.

If you have any issues accessing the portal, contact IT support immediately.

Thank you,
Security Team
Company Inc.

--
This is an automated message. Please do not reply.
""",

    "casual_quick": """Subject: Coffee chat?
From: colleague@company.com
To: you@company.com
Date: Mon, 15 Feb 2026 11:30:00

Hey!

Want to grab coffee this afternoon around 3? I'd love to catch up and hear about your new project.

Let me know!

Cheers,
Sam
""",
}


def get_sample_email(key: str = "urgent_deadline") -> str:
    """Get a sample email by key."""
    return SAMPLE_EMAILS.get(key, SAMPLE_EMAILS["urgent_deadline"])


def get_all_samples() -> dict:
    """Get all sample emails."""
    return SAMPLE_EMAILS
