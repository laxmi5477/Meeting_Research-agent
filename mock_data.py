"""
Mock Research Engine for Meeting Research Agent.
Generates realistic, context-aware pre-meeting research briefs based on
Company/Person Name, Meeting Date, and Meeting Purpose.
"""

from datetime import datetime, date
from typing import Dict, Any, List


def _is_likely_person(name: str) -> bool:
    """Heuristic check to detect whether the query represents a person or company."""
    titles = ["dr.", "dr", "mr.", "mr", "ms.", "ms", "mrs.", "mrs", "prof.", "prof"]
    tokens = name.strip().lower().split()
    if any(tokens[0] == t for t in titles if tokens):
        return True
    # Two words without typical company suffixes often denote a person
    company_suffixes = ["inc", "inc.", "corp", "corp.", "ltd", "ltd.", "llc", "technologies", "ai", "labs", "systems", "group", "holdings", "co"]
    if any(suffix in tokens for suffix in company_suffixes):
        return False
    return len(tokens) == 2 and not any(s in name.lower() for s in ["health", "software", "analytics", "capital", "ventures"])


def generate_mock_brief(entity_name: str, meeting_date: Any, meeting_purpose: str, attendee_info: str = "Meeting Attendee") -> Dict[str, Any]:
    """
    Generate a structured, professional mock research dossier.
    """
    cleaned_name = entity_name.strip() if entity_name else "Target Organization"
    attendee_role = attendee_info.strip() or "Meeting Attendee"
    is_person = _is_likely_person(cleaned_name)
    purpose_lower = (meeting_purpose or "").lower()

    if isinstance(meeting_date, (datetime, date)):
        date_str = meeting_date.strftime("%B %d, %Y")
    else:
        date_str = str(meeting_date)

    # Contextual keywords detection
    is_sales = any(w in purpose_lower for w in ["sale", "pitch", "demo", "client", "vendor", "contract", "deal"])
    is_partner = any(w in purpose_lower for w in ["partner", "collaboration", "joint", "alliance", "ecosystem"])
    is_invest = any(w in purpose_lower for w in ["invest", "fundraise", "venture", "series", "capital", "portfolio"])
    is_tech = any(w in purpose_lower for w in ["tech", "api", "architecture", "product", "software", "ai", "cloud"])

    # 1. Executive Summary & Overview
    if is_person:
        executive_summary = (
            f"{cleaned_name} is a seasoned executive and decision-maker currently driving core initiatives "
            f"in their domain. Known for pragmatic leadership and strategic technology adoption, "
            f"they frequently evaluate cross-functional partnerships that demonstrate quantifiable ROI. "
            f"The upcoming meeting on {date_str} focuses on '{meeting_purpose or 'Strategic Discussion'}', "
            f"representing a high-value opportunity to establish strategic alignment and build long-term rapport."
        )
    else:
        executive_summary = (
            f"{cleaned_name} is currently experiencing significant strategic acceleration, focusing on market expansion "
            f"and operational efficiency. In recent quarters, the organization has prioritized modernizing core workflows, "
            f"evaluating best-in-class technology vendors, and expanding strategic industry partnerships. "
            f"This session scheduled for {date_str} aims to address '{meeting_purpose or 'Core Business Exploration'}', "
            f"aligning directly with their fiscal year growth milestones and innovation roadmap."
        )

    # 2. Recent Developments
    if is_person:
        developments: List[Dict[str, str]] = [
            {
                "headline": f"{cleaned_name} featured in Industry Leadership Forum",
                "date": "2 weeks ago",
                "category": "Keynote & Speech",
                "summary": f"Delivered a well-received keynote highlighting efficiency breakthroughs, automated operational tooling, and the necessity of agile execution in today's macroeconomic landscape.",
                "source": "Global Tech Review",
            },
            {
                "headline": f"Steering major strategic repositioning initiative",
                "date": "1 month ago",
                "category": "Organizational Leadership",
                "summary": f"Spearheaded the consolidation of internal innovation programs to focus on high-impact initiatives and scalable enterprise partnerships.",
                "source": "Executive Business Journal",
            },
            {
                "headline": f"Published thought leadership on market resilience",
                "date": "2 months ago",
                "category": "Thought Leadership",
                "summary": f"Authored an analytical essay examining vendor consolidation trends and the strategic shift toward integrated platform solutions over fragmented point tools.",
                "source": "LinkedIn Insights",
            },
            {
                "headline": f"Appointed to advisory committee on digital transformation",
                "date": "3 months ago",
                "category": "Industry Governance",
                "summary": f"Joined an industry advisory council focusing on ethical technology adoption, cybersecurity compliance, and enterprise data interoperability.",
                "source": "Tech Governance Wire",
            },
        ]
    else:
        developments: List[Dict[str, str]] = [
            {
                "headline": f"{cleaned_name} announced Q3 performance milestone and global expansion",
                "date": "10 days ago",
                "category": "Business Growth",
                "summary": f"Reported strong quarter-over-quarter expansion driven by enterprise customer acquisitions and entry into EMEA and APAC regional markets.",
                "source": "Financial Post Daily",
            },
            {
                "headline": f"Launched Next-Gen Automated Enterprise Capabilities",
                "date": "3 weeks ago",
                "category": "Product Release",
                "summary": f"Unveiled automated workflows and enterprise-grade integration frameworks aimed at reducing operational friction for B2B stakeholders.",
                "source": "Enterprise Tech News",
            },
            {
                "headline": f"Formed strategic cloud and data distribution alliance",
                "date": "1 month ago",
                "category": "Strategic Partnership",
                "summary": f"Entered a multi-year collaborative initiative to streamline data ingestion pipelines, reduce latency, and ensure strict SOC2/ISO compliance.",
                "source": "Industry Wire",
            },
            {
                "headline": f"Appointed New Chief Operating Officer to accelerate scaling",
                "date": "2 months ago",
                "category": "Executive Appointment",
                "summary": f"Welcomed former Tier-1 tech executive to oversee global customer success, procurement protocols, and operational infrastructure.",
                "source": "Market Insider",
            },
        ]

    # 3. Key Insights
    key_insights: List[Dict[str, str]] = [
        {
            "title": "Strategic Focus & Immediate Priorities",
            "tag": "Strategic Focus",
            "badge_color": "blue",
            "description": (
                f"Currently focused on streamlining operations, reducing turnaround cycles, and accelerating ROI. "
                f"Any proposal or discussion framed around quick time-to-value and reduced operational burden will resonate strongly."
            ),
        },
        {
            "title": "Vendor & Partnership Philosophy",
            "tag": "Ecosystem Dynamics",
            "badge_color": "green",
            "description": (
                f"Prefers transparent, outcome-oriented partners over complex multi-tiered arrangements. "
                f"Decisions are heavily influenced by proof of security compliance, clear milestones, and predictable integration pathways."
            ),
        },
        {
            "title": "Key Friction Points & Challenges",
            "tag": "Vulnerabilities & Needs",
            "badge_color": "amber",
            "description": (
                f"Balancing aggressive scaling targets with resource efficiency. "
                f"Internal stakeholders are vigilant about avoiding vendor lock-in and minimizing onboarding friction across technical teams."
            ),
        },
        {
            "title": "Competitive Positioning",
            "tag": "Market Advantage",
            "badge_color": "purple",
            "description": (
                f"Maintaining a strong market differentiator through superior customer experience and reliable technology infrastructure. "
                f"Viewing collaborative opportunities as an avenue to reinforce market leadership."
            ),
        },
    ]

    # 4. Suggested Discussion Points
    if is_sales:
        discussion_points = [
            {
                "priority": "High Priority",
                "topic": "Direct Alignment with Current Operational Goals",
                "talking_point": f"Address how our solution directly accelerates {cleaned_name}'s recent efficiency mandates while minimizing implementation overhead.",
                "rationale": "Directly maps value to their stated Q3/Q4 objectives, establishing immediate relevance.",
            },
            {
                "priority": "High Priority",
                "topic": "Time-to-Value & Proof of Concept Framework",
                "talking_point": "Present a frictionless 14-day evaluation structure with defined success criteria and zero integration disruption.",
                "rationale": "Removes perceived adoption risk and lowers decision barriers for senior leadership.",
            },
            {
                "priority": "Medium Priority",
                "topic": "Security, Governance, and Interoperability",
                "talking_point": "Highlight enterprise-grade data privacy protocols, architecture guarantees, and automated audit trails.",
                "rationale": "Proactively overcomes common procurement and compliance hurdles.",
            },
            {
                "priority": "Medium Priority",
                "topic": "Scalability Roadmap & Long-Term Value",
                "talking_point": f"Share benchmarks from peer deployments illustrating cost containment as transaction volumes scale.",
                "rationale": "Validates durability and ensures decision makers see an enduring commercial partnership.",
            },
        ]
    elif is_partner:
        discussion_points = [
            {
                "priority": "High Priority",
                "topic": "Mutual Value Proposition & Joint Capabilities",
                "talking_point": f"Explore synergies combining {cleaned_name}'s reach with our core capabilities to create a differentiated joint offering.",
                "rationale": "Establishes a win-win baseline before diving into tactical integration requirements.",
            },
            {
                "priority": "High Priority",
                "topic": "Phased Co-Development & Pilot Milestone",
                "talking_point": "Propose an initial co-branded pilot targeting an underserved segment or specific friction point.",
                "rationale": "Produces tangible validation without requiring extensive initial commitment.",
            },
            {
                "priority": "Medium Priority",
                "topic": "Go-to-Market & Commercial Mechanics",
                "talking_point": "Outline shared distribution channels, co-marketing webinars, and reciprocal referral models.",
                "rationale": "Shows thoughtful commercial readiness and mutual incentive alignment.",
            },
        ]
    elif is_invest:
        discussion_points = [
            {
                "priority": "High Priority",
                "topic": "Unit Economics & Defensibility Moat",
                "talking_point": f"Walk through capital efficiency, customer acquisition dynamics, and retention cohorts relevant to {cleaned_name}'s thesis.",
                "rationale": "Addresses primary investor hurdles and proves sustainable traction.",
            },
            {
                "priority": "High Priority",
                "topic": "Market Expansion & Growth Vectors",
                "talking_point": "Demonstrate expansion into adjacent verticals and scalable go-to-market channels.",
                "rationale": "Quantifies the total addressable market trajectory and return profile.",
            },
            {
                "priority": "Medium Priority",
                "topic": "Talent, Governance, and Milestone Execution",
                "talking_point": "Review core milestones delivered to date and leadership capability to navigate market headwinds.",
                "rationale": "Builds confidence in execution discipline and leadership depth.",
            },
        ]
    else:
        discussion_points = [
            {
                "priority": "High Priority",
                "topic": f"Strategic Alignment with {cleaned_name}'s Initiatives",
                "talking_point": f"Anchor the conversation around their stated objectives regarding '{meeting_purpose or 'Strategic Priorities'}' and identify high-leverage collaboration areas.",
                "rationale": "Demonstrates respect for their strategic roadmap and builds consultative trust early.",
            },
            {
                "priority": "High Priority",
                "topic": "Addressing High-Impact Bottlenecks",
                "talking_point": "Discuss common friction points peers face in this domain and compare approaches to mitigating execution risk.",
                "rationale": "Positions you as a domain expert with deep contextual understanding.",
            },
            {
                "priority": "Medium Priority",
                "topic": "Concrete Next Steps & Decision Milestones",
                "talking_point": "Agree upon a structured follow-up cadence, technical review scope, or collaborative milestone.",
                "rationale": "Ensures the meeting concludes with clear accountability and momentum.",
            },
        ]

    # 5. Questions to Ask
    questions_to_ask = [
        {
            "category": "Strategic Alignment",
            "question": f"Given your recent initiatives, what is the single biggest milestone {cleaned_name} must achieve by the end of this quarter?",
            "objective": "Uncovers their immediate North Star metric and confirms budget/resource allocation focus.",
        },
        {
            "category": "Strategic Alignment",
            "question": f"How does the topic of '{meeting_purpose or 'this initiative'}' rank against other competing organizational priorities right now?",
            "objective": "Measures project urgency, stakeholder sponsorship, and execution readiness.",
        },
        {
            "category": "Operational & Technical",
            "question": "What internal systems or operational dependencies would be most critical for any solution in this area to integrate with?",
            "objective": "Identifies potential technical roadblocks or security gatekeepers early.",
        },
        {
            "category": "Operational & Technical",
            "question": "What past approaches or vendor partnerships have failed to deliver on expectations, and why?",
            "objective": "Reveals sensitive pain points and unspoken criteria for what 'good' looks like.",
        },
        {
            "category": "Decision-Making & Next Steps",
            "question": "Who besides your immediate team needs to be involved to establish consensus and sign off on a formal pilot?",
            "objective": "Maps the buying committee, legal/security gatekeepers, and procurement steps.",
        },
        {
            "category": "Decision-Making & Next Steps",
            "question": "If we define an ideal pilot outcome today, what specific metric would make this an undisputed success for you in 60 days?",
            "objective": "Establishes quantifiable criteria that guarantee mutual satisfaction upon delivery.",
        },
    ]

    # 6. Sources
    sources = [
        {
            "title": f"{cleaned_name} Strategic Corporate Dossier & Filings",
            "publisher": "Securities & Financial Disclosures Database",
            "date": "November 2024",
            "type": "Regulatory & Corporate Filing",
            "credibility": "High",
            "url": f"https://www.sec.gov/edgar/searchedgar/companysearch",
        },
        {
            "title": f"Executive Profile, Public Speeches & Leadership Analysis: {cleaned_name}",
            "publisher": "Bloomberg Professional Intelligence",
            "date": "October 2024",
            "type": "Market Intelligence Report",
            "credibility": "High",
            "url": "https://www.bloomberg.com/professional",
        },
        {
            "title": f"Recent Product Milestones, Partnerships & Growth Metrics",
            "publisher": "TechCrunch & VentureBeat Coverage",
            "date": "Last 45 Days",
            "type": "Verified Tech Journalism",
            "credibility": "Medium-High",
            "url": "https://techcrunch.com",
        },
        {
            "title": f"Keynote Address & Panel Discussion Transcript",
            "publisher": "Global Industry Leadership Summit 2024",
            "date": "September 2024",
            "type": "Conference Proceedings",
            "credibility": "Direct Source",
            "url": "https://industrysummits.example.org",
        },
        {
            "title": f"Professional Network Verification & Organizational Hierarchy",
            "publisher": "Verified Executive Database & LinkedIn Talent Insights",
            "date": "Updated Current Month",
            "type": "Organizational Intelligence",
            "credibility": "Direct Source",
            "url": "https://www.linkedin.com",
        },
    ]

    attendee_cheat_sheet = {
        "attendee_role": attendee_role,
        "preflight_summary": f"Target: {cleaned_name} | Goal: {meeting_purpose or 'Strategic Alignment'} | Attendee: {attendee_role}. Maintain a consultative stance, validate pain points early, and agree on next milestones.",
        "dos": [
            f"Connect every value proposition directly to {cleaned_name}'s Q3/Q4 initiatives.",
            "Ask open-ended discovery questions before presenting technical details.",
            "Agree on a calendar date for the next follow-up call before hanging up.",
        ],
        "donts": [
            "Don't monopolize the conversation—let the target share their pain points.",
            "Don't make unverified commitments on delivery dates without technical sign-off.",
            "Don't leave without knowing the full stakeholder buying committee.",
        ],
        "icebreakers": [
            f"I was reviewing {cleaned_name}'s recent milestones and wanted to congratulate your team on the impressive momentum.",
            f"To make sure our session on {date_str} is ultra-valuable for you, what is the #1 question you're hoping we address today?",
        ],
    }

    training_module = {
        "target_persona_style": "Analytical, velocity-driven, and highly metrics-focused. Values concrete proof-of-concepts over slide decks.",
        "recommended_tone": "Concise, outcome-oriented, and consultative. Speak in terms of quantifiable time-to-value.",
        "opening_hook": f"I was reviewing {cleaned_name}'s recent momentum over the past 30 days and wanted to congratulate your team on the impressive milestones.",
        "objection_drills": [
            {
                "objection": f"We already have internal tooling and incumbent vendors handling this for {cleaned_name}.",
                "why_they_raise_it": "They want to protect existing sunk cost and avoid implementation churn across engineering teams.",
                "recommended_rebuttal": f"Most of our enterprise partners felt the same way initially. Where we shine is complementing your existing stack with zero-disruption integration and immediate ROI.",
            },
            {
                "objection": "Our budget for this fiscal cycle is committed; we cannot greenlight new contracts right now.",
                "why_they_raise_it": "Proactive defense against unexpected mid-quarter software expenses.",
                "recommended_rebuttal": "We completely respect your budget cycles. That is why we structure an evaluation pilot now so that you have verified ROI data ready when your next cycle opens.",
            },
        ],
        "meeting_landmines": [
            "Don't speak in high-level generic generalities without citing specific operational metrics.",
            "Don't evade security, data privacy, or compliance questions.",
            "Don't assume single-stakeholder authority—always uncover the buying committee.",
        ],
    }

    return {
        "entity_name": cleaned_name,
        "is_person": is_person,
        "entity_type": "Executive / Individual" if is_person else "Company / Enterprise",
        "meeting_date": date_str,
        "timeframe_researched": "Preceding 30 Days",
        "meeting_purpose": meeting_purpose or "Exploratory & Strategic Alignment",
        "attendee_info": attendee_role,
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "engine": "⚡ Mock Engine (Instant Simulation)",
        "executive_summary": executive_summary,
        "recent_developments": developments,
        "key_insights": key_insights,
        "suggested_discussion_points": discussion_points,
        "questions_to_ask": questions_to_ask,
        "sources": sources,
        "attendee_cheat_sheet": attendee_cheat_sheet,
        "training_module": training_module,
    }
