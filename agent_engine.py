"""
AI Research Agent Engine.
Coordinates search planning, live web perception, and structured intelligence synthesis.
Utilizes Gemini 3.5 Flash / Gemini 3.1 Flash Lite with strict Pydantic structured output.
Features 30-Day Pre-Meeting Research, Input-Divergent Intelligence, and User Meeting Training.
"""

import os
import json
from datetime import datetime, date, timedelta
from typing import Dict, Any, Optional
from tools import search_web
from schema import MeetingBriefSchema


def _calculate_30d_window(meeting_date: Any) -> str:
    """Calculate the exact 30-day preceding timeframe string."""
    try:
        if isinstance(meeting_date, str):
            # Try to parse string to date
            try:
                dt = datetime.strptime(meeting_date, "%Y-%m-%d").date()
            except ValueError:
                dt = date.today() + timedelta(days=2)
        elif isinstance(meeting_date, (datetime, date)):
            dt = meeting_date if isinstance(meeting_date, date) else meeting_date.date()
        else:
            dt = date.today() + timedelta(days=2)
            
        start_date = dt - timedelta(days=30)
        return f"{start_date.strftime('%b %d, %Y')} – {dt.strftime('%b %d, %Y')} (Preceding 30 Days)"
    except Exception:
        return "Preceding 30 Days"


def run_ai_research_agent(
    entity_name: str,
    meeting_date: Any,
    meeting_purpose: str,
    attendee_info: str = "Meeting Attendee",
    gemini_api_key: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Autonomous AI Agent with Gemini + Live Web Grounding.
    Focuses on preceding 30-day developments (News, Launches, Hires, Updates)
    and produces an input-varying briefing with a full Meeting Training Module.
    """
    api_key = gemini_api_key or os.getenv("GEMINI_API_KEY")
    if not api_key:
        from mock_data import generate_mock_brief
        return generate_mock_brief(entity_name, meeting_date, meeting_purpose, attendee_info)

    from google import genai
    from google.genai import types

    client = genai.Client(api_key=api_key)
    clean_name = entity_name.strip()
    date_str = str(meeting_date)
    timeframe_str = _calculate_30d_window(meeting_date)
    attendee_role = attendee_info.strip() or "Meeting Attendee"

    # ----------------------------------------------------
    # Phase 1: Planning Queries specifically for Preceding 30 Days
    # ----------------------------------------------------
    plan_prompt = f"""
    You are an elite research agent preparing an intelligence brief for an upcoming meeting with {clean_name}.
    Target: {clean_name}
    Scheduled Meeting Date: {date_str}
    Preceding 30-Day Window: {timeframe_str}
    Meeting Purpose: {meeting_purpose}

    Generate 4 distinct, highly focused web search queries to gather intelligence from the preceding 30 days:
    1. A query targeting recent product launches, feature releases, or technical updates.
    2. A query targeting executive appointments, leadership changes, or new hires.
    3. A query targeting major company news, funding, earnings, or strategic announcements.
    4. A query researching pain points or priorities specifically relating to: '{meeting_purpose}'.

    Return ONLY a valid JSON list of 4 query strings, for example:
    ["query 1", "query 2", "query 3", "query 4"]
    """

    queries = []
    # Primary model gemini-3.5-flash with fallback to gemini-3.1-flash-lite
    model_candidates = ["gemini-3.5-flash", "gemini-3.1-flash-lite", "gemini-3.8-flash"]
    selected_model = "gemini-3.5-flash"

    for model_name in model_candidates:
        try:
            plan_res = client.models.generate_content(
                model=model_name,
                contents=plan_prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    temperature=0.2,
                ),
            )
            parsed_queries = json.loads(plan_res.text)
            if isinstance(parsed_queries, list) and len(parsed_queries) >= 3:
                queries = parsed_queries
                selected_model = model_name
                break
        except Exception as e:
            print(f"[Warning] Query planning failed with {model_name}: {e}")
            continue

    if not queries:
        queries = [
            f"{clean_name} product launch announcement last 30 days",
            f"{clean_name} executive hire appointment joined",
            f"{clean_name} latest news developments",
            f"{clean_name} {meeting_purpose}",
        ]

    # ----------------------------------------------------
    # Phase 2: Live Web Search Perception
    # ----------------------------------------------------
    collected_research = []
    for q in queries[:4]:
        results = search_web(q, max_results=3)
        collected_research.extend(results)

    # ----------------------------------------------------
    # Phase 3: Structured Intelligence & Training Synthesis
    # ----------------------------------------------------
    synthesis_prompt = f"""
    You are an executive research agent and strategic meeting coach.
    Compile an actionable, concise pre-meeting intelligence dossier for '{attendee_role}'
    who is meeting with '{clean_name}' on {date_str}.
    Meeting Purpose: {meeting_purpose}
    Research Timeframe: {timeframe_str}

    Live Web Data Harvested from Recent Signals:
    {json.dumps(collected_research, indent=2)}

    CRITICAL REQUIREMENTS:
    1. VARY W.R.T. THE INPUT: The brief must strictly reflect {clean_name}'s actual business, industry, and recent 30-day developments. Avoid canned phrases or generic boilerplates.
    2. PRECEDING 30 DAYS DEVELOPMENTS: Highlight factual updates:
       - 🚀 Launches: New products, features, or platform updates.
       - 👔 Hires: Executive transitions, board seats, key hires.
       - 📰 Major News: Market expansions, regulatory filings, or partnerships.
       - Explain the direct 'relevance_to_meeting' for each development.
    3. STRATEGIC DISCUSSION POINTS: Formulate 3-4 prioritized talking points showing deep context of their current situation.
    4. OPEN DISCOVERY QUESTIONS: 4-6 high-impact discovery questions to uncover budget, urgency, and decision criteria.
    5. SOURCES: Attribute citations using real titles, publishers, and URLs from the research data.
    6. MEETING TRAINING MODULE:
       - Profile the target's decision-making style.
       - Provide a recommended tone for {attendee_role}.
       - Craft a 30-second conversational opening hook referencing a 30-day milestone.
       - Create 2-3 realistic objection drills (the objection, why they raise it, and the exact rebuttal script).
       - List 2-3 deal-killer landmines to avoid.
    """

    brief_dict = None
    for model_name in [selected_model, "gemini-3.1-flash-lite", "gemini-3.8-flash"]:
        try:
            brief_response = client.models.generate_content(
                model=model_name,
                contents=synthesis_prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=MeetingBriefSchema,
                    temperature=0.2,
                ),
            )
            brief_dict = json.loads(brief_response.text)
            selected_model = model_name
            break
        except Exception as e:
            print(f"[Warning] Synthesis failed with {model_name}: {e}")
            continue

    if not brief_dict:
        # Fallback to local heuristic engine if API calls fail
        from mock_data import generate_mock_brief
        return generate_mock_brief(clean_name, meeting_date, meeting_purpose, attendee_role)

    brief_dict["generated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    brief_dict["attendee_info"] = attendee_role
    brief_dict["timeframe_researched"] = timeframe_str
    brief_dict["engine"] = f"🤖 Gemini Research Agent ({selected_model} + Live Web Grounding)"

    # Compatibility mapping for Attendee Cheat Sheet
    training = brief_dict.get("training_module", {})
    brief_dict["attendee_cheat_sheet"] = {
        "attendee_role": attendee_role,
        "preflight_summary": f"Target: {clean_name} | Window: {timeframe_str} | Purpose: {meeting_purpose}.",
        "dos": [
            f"Reference recent 30-day wins or public announcements to build authentic rapport.",
            f"Mirror {training.get('target_persona_style', 'their communication style')} with {training.get('recommended_tone', 'a consultative tone')}.",
            "Secure an agreed follow-up date and next step before concluding.",
        ],
        "donts": training.get("meeting_landmines", [
            "Don't speak in high-level generic generalities without citing specific operational metrics.",
            "Don't evade pricing or timeline questions.",
        ]),
        "icebreakers": [
            training.get("opening_hook", f"I was reviewing {clean_name}'s recent momentum over the past month and was eager to connect regarding {meeting_purpose}."),
        ],
    }

    return brief_dict


def evaluate_user_rehearsal_response(
    brief_context: Dict[str, Any],
    objection_scenario: str,
    user_response: str,
    gemini_api_key: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Evaluates the attendee's practice response to a tough objection drill.
    Provides a 1-10 score, constructive critique, and a polished script.
    """
    api_key = gemini_api_key or os.getenv("GEMINI_API_KEY")
    entity_name = brief_context.get("entity_name", "the target")
    purpose = brief_context.get("meeting_purpose", "this meeting")

    if api_key:
        try:
            from google import genai
            client = genai.Client(api_key=api_key)
            prompt = f"""
            You are a top-tier executive sales coach training a user for an upcoming meeting with {entity_name}.
            Meeting Context:
            - Target: {entity_name}
            - Goal: {purpose}
            - Tough Objection / Scenario: "{objection_scenario}"

            User's Practice Response:
            "{user_response}"

            Task:
            Evaluate the user's practice response:
            1. Assign a Score from 1 to 10.
            2. Strengths: 1 sentence highlighting what was done well.
            3. Areas for Improvement: 1-2 sentences on what was missing (e.g., didn't reframe value, too defensive, lacked clarity).
            4. Polished Rebuttal Script: The exact, high-impact phrasing the user should say instead.

            Return valid JSON with keys: 'score' (int), 'strengths' (str), 'improvements' (str), 'recommended_script' (str).
            """
            res = client.models.generate_content(
                model="gemini-3.5-flash",
                contents=prompt,
                config={"response_mime_type": "application/json"}
            )
            return json.loads(res.text)
        except Exception as e:
            print(f"[Warning] Coach evaluator error: {e}")

    # Heuristic fallback coaching evaluation
    word_count = len(user_response.split())
    score = min(9, max(5, int(word_count / 8) + 4))
    return {
        "score": score,
        "strengths": "Direct approach that acknowledges the target's concern without immediate concession.",
        "improvements": f"Anchor your response more firmly to {entity_name}'s 30-day goals to demonstrate clear ROI.",
        "recommended_script": f"I completely understand that concern given your recent focus at {entity_name}. That is why peers partner with us to eliminate risk early through a low-overhead, 14-day validation pilot.",
    }


def answer_in_meeting_question(brief_context: Dict[str, Any], question: str, gemini_api_key: Optional[str] = None) -> str:
    """Answers real-time questions from the attendee during or immediately before the meeting."""
    api_key = gemini_api_key or os.getenv("GEMINI_API_KEY")
    entity_name = brief_context.get("entity_name", "the target")
    purpose = brief_context.get("meeting_purpose", "this meeting")

    if api_key:
        try:
            from google import genai
            client = genai.Client(api_key=api_key)
            prompt = f"""
            You are an in-meeting executive co-pilot whispering real-time advice to an attendee in a live meeting with {entity_name}.
            Context:
            - Target: {entity_name}
            - Meeting Goal: {purpose}
            - Summary: {brief_context.get('executive_summary', '')}

            Attendee's Urgent In-Meeting Question:
            "{question}"

            Give an actionable, punchy 2-3 sentence answer with the exact words to say or the strategic move to make.
            """
            for m in ["gemini-3.5-flash", "gemini-3.1-flash-lite"]:
                try:
                    res = client.models.generate_content(model=m, contents=prompt)
                    return res.text.strip()
                except Exception:
                    continue
        except Exception as e:
            print(f"[Warning] Co-pilot AI error: {e}")

    # Intelligent Heuristic Co-Pilot fallback
    q_lower = question.lower()
    if any(w in q_lower for w in ["price", "cost", "budget", "expensive"]):
        return (
            f"Say: 'We structure pricing strictly around realized ROI and volume milestones. "
            f"Before we talk numbers, let's agree on what metric would make this a 5x return for {entity_name}. "
            f"What budget framework have you already allocated for this initiative?'"
        )
    elif any(w in q_lower for w in ["competitor", "alternative", "rival", "versus", "vs"]):
        return (
            f"Say: 'Unlike legacy point solutions, our focus with {entity_name} is frictionless integration and rapid time-to-value. "
            f"Most peers choose us specifically because we eliminate onboarding friction while preserving full data privacy.'"
        )
    elif any(w in q_lower for w in ["next step", "close", "follow up", "decision"]):
        return (
            f"Say: 'Based on our discussion, the logical next step is a low-risk 14-day technical proof of concept. "
            f"Can we put 20 minutes on the calendar for next Tuesday at 2 PM to review the success criteria with your technical lead?'"
        )
    else:
        return (
            f"Say: 'That is a critical point for {entity_name}. In our experience with similar organizations, "
            f"the key is aligning early on clear success metrics. How does your leadership team view that tradeoff right now?'"
        )
