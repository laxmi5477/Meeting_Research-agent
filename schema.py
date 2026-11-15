"""
Data schemas for the Meeting Research Agent.
Defines strict Pydantic structures for:
1. Preceding 30-day developments (News, Launches, Hires, Updates)
2. Strategic Insights & Discussion Points
3. Open Discovery Questions
4. Sources & Citations
5. User Meeting Training & Coaching Module
6. One-Page Concise Executive Memo
"""

from typing import List, Optional
from pydantic import BaseModel, Field


class RecentDevelopment(BaseModel):
    headline: str = Field(description="Title of recent news, launch, hire, or public event from the last 30 days")
    date: str = Field(description="Approximate date or timeframe within the last 30 days, e.g. 'Nov 04, 2026' or '2 weeks ago'")
    category: str = Field(description="'🚀 Product Launch', '👔 Executive Hire', '📰 Major News', or '🤝 Strategic Move'")
    summary: str = Field(description="2-3 sentence factual, objective summary based on real web signals")
    source: str = Field(description="Publisher, platform, or citation name")
    relevance_to_meeting: str = Field(description="Why this specific development matters for the upcoming conversation")


class KeyInsight(BaseModel):
    title: str = Field(description="Strategic insight title")
    tag: str = Field(description="Domain tag (e.g., 'Strategic Focus', 'Vulnerabilities', 'Market Position')")
    badge_color: str = Field(description="Visual accent color: 'blue', 'green', 'amber', or 'purple'")
    description: str = Field(description="Deep analytical context explaining why this matters")


class SuggestedDiscussionPoint(BaseModel):
    priority: str = Field(description="'High Priority' or 'Medium Priority'")
    topic: str = Field(description="High-level topic or discussion domain")
    talking_point: str = Field(description="Actionable, conversational point to raise in the meeting")
    rationale: str = Field(description="Strategic reasoning explaining why this point resonates with the target's 30-day priorities")


class QuestionToAsk(BaseModel):
    category: str = Field(description="Grouping category (e.g., 'Strategic Alignment', 'Operational & Technical', 'Next Steps')")
    question: str = Field(description="The exact strategic discovery question to ask")
    objective: str = Field(description="What critical signal, pain point, or requirement this question aims to uncover")


class SourceCitation(BaseModel):
    title: str = Field(description="Title of the article, filing, or public profile")
    publisher: str = Field(description="Publisher or platform (e.g., 'TechCrunch', 'SEC Edgar', 'Bloomberg')")
    date: str = Field(description="Publication or retrieval date")
    type: str = Field(description="Source category (e.g., 'Verified Journalism', 'Company Press Release', 'Leadership Profile')")
    credibility: str = Field(description="Assessment rating: 'High', 'Medium-High', or 'Direct Source'")
    url: str = Field(description="Web URL or reference link")


class ObjectionDrill(BaseModel):
    objection: str = Field(description="The exact pushback or tough question the target is most likely to raise")
    why_they_raise_it: str = Field(description="The underlying concern or past 30-day development triggering this objection")
    recommended_rebuttal: str = Field(description="The exact script or strategic counter-response the user should say")


class MeetingTrainingModule(BaseModel):
    target_persona_style: str = Field(description="How this person/organization makes decisions (e.g., highly analytical, velocity-driven, relationship-led)")
    recommended_tone: str = Field(description="The ideal conversational tone (e.g., 'Concise & data-backed', 'Consultative & empathetic')")
    opening_hook: str = Field(description="A polished 30-second conversational opening referencing a recent 30-day development")
    objection_drills: List[ObjectionDrill] = Field(description="Top 2-3 realistic objection drills to prepare and train the user")
    meeting_landmines: List[str] = Field(description="2-3 specific phrases, topics, or assumptions to strictly avoid during the session")


class MeetingBriefSchema(BaseModel):
    entity_name: str
    is_person: bool
    entity_type: str = Field(description="'Executive / Individual' or 'Company / Enterprise'")
    meeting_date: str
    timeframe_researched: str = Field(description="Explicit 30-day window researched, e.g. 'Last 30 Days preceding scheduled session'")
    meeting_purpose: str
    executive_summary: str = Field(description="High-level executive briefing summarizing the strategic opportunity and 30-day context")
    recent_developments: List[RecentDevelopment]
    key_insights: List[KeyInsight]
    suggested_discussion_points: List[SuggestedDiscussionPoint]
    questions_to_ask: List[QuestionToAsk]
    sources: List[SourceCitation]
    training_module: MeetingTrainingModule
