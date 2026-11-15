                        f"""
                        <div class="dashboard-card" style="border-left: 3px solid #6366f1;">
                            <div style="font-size: 0.85rem; color: #64748b; margin-bottom: 0.25rem;">
                                <strong>Situation / Question:</strong> {item['q']}
                            </div>
                            <div style="font-size: 0.98rem; font-weight: 600; color: #1e293b; line-height: 1.5;">
                                💡 {item['a']}
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

    # ==========================================
    # EXPORT & DISTRIBUTION SECTION
    # ==========================================
    st.markdown("---")
    st.markdown("#### 📤 Export & Share with Meeting Attendees")
    st.caption("Distribute the intelligence brief or a compact 60-second attendee cheat sheet.")

    training = brief.get("training_module", {})
    cheat = brief.get("attendee_cheat_sheet", {})
    
    dos_str = "\n".join([f"- DO: {d}" for d in cheat.get("dos", [])])
    donts_str = "\n".join([f"- DON'T: {d}" for d in training.get("meeting_landmines", cheat.get("donts", []))])

    pts_summary = ""
    for idx, p in enumerate(brief.get("suggested_discussion_points", [])[:3], 1):
        pts_summary += f"{idx}. {p['topic']}: \"{p['talking_point']}\"\n"

    qs_summary = ""
    for q in brief.get("questions_to_ask", [])[:3]:
        qs_summary += f"- \"{q['question']}\" (Goal: {q['objective']})\n"

    # Full Markdown Content
    markdown_content = f"""# Meeting Intelligence Brief: {brief['entity_name']}
**Target Entity:** {brief['entity_name']} ({brief['entity_type']})  
**Meeting Date:** {brief['meeting_date']}  
**Research Window:** {timeframe_text}  
**Attendee:** {brief.get('attendee_info', 'Attendee')}  
**Purpose:** {brief['meeting_purpose']}  
**Engine:** {brief.get('engine', 'Gemini AI Agent')}  

---

## Executive Summary
{brief['executive_summary']}

---

## 1. Recent Developments (Preceding 30 Days)
"""
    for dev in brief.get("recent_developments", []):
        rel = f"\n  *Relevance:* {dev['relevance_to_meeting']}" if dev.get('relevance_to_meeting') else ""
        markdown_content += f"- **[{dev['category']}] {dev['headline']}** ({dev['date']})\n  {dev['summary']}{rel}\n  *Source: {dev['source']}*\n\n"

    markdown_content += "## 2. Key Insights\n"
    for ins in brief.get("key_insights", []):
        markdown_content += f"- **{ins['tag']} - {ins['title']}**\n  {ins['description']}\n\n"

    markdown_content += "## 3. Suggested Discussion Points\n"
    for pt in brief.get("suggested_discussion_points", []):
        markdown_content += f"- **[{pt['priority']}] {pt['topic']}**\n  \"{pt['talking_point']}\"\n  *Rationale:* {pt['rationale']}\n\n"

    markdown_content += "## 4. Questions to Ask\n"
    for q in brief.get("questions_to_ask", []):
        markdown_content += f"- **[{q['category']}]** \"{q['question']}\"\n  *Goal:* {q['objective']}\n\n"

    markdown_content += "## 5. Sources & Citations\n"
    for src in brief.get("sources", []):
        markdown_content += f"- [{src['credibility']}] **{src['title']}** - {src['publisher']} ({src['date']})\n  Link: {src['url']}\n\n"

    attendee_email_summary = f"""*MEETING INTELLIGENCE 1-PAGER FOR {brief.get('attendee_info', 'ATTENDEE').upper()}*
Target: {brief['entity_name']}
Date: {brief['meeting_date']}
Window: {timeframe_text}
Goal: {brief['meeting_purpose']}

========================================
60-SECOND PRE-FLIGHT:
{brief['executive_summary']}

========================================
TOP TALKING POINTS:
{pts_summary}
========================================
OPEN QUESTIONS TO ASK:
{qs_summary}
========================================
OPENING HOOK:
"{training.get('opening_hook', 'I was reviewing your team’s recent milestones...')}"

LANDMINES TO AVOID:
{donts_str}
"""

    col_exp1, col_exp2 = st.columns([1, 1])

    with col_exp1:
        st.download_button(
            label="📥 Download Full Brief (.md)",
            data=markdown_content,
            file_name=f"brief_{brief['entity_name'].lower().replace(' ', '_')}.md",
            mime="text/markdown",
            use_container_width=True,
        )

    with col_exp2:
        st.download_button(
            label="📋 Download One-Page Summary (.txt)",
            data=attendee_email_summary,
            file_name=f"onepager_{brief['entity_name'].lower().replace(' ', '_')}.txt",
            mime="text/plain",
            use_container_width=True,
        )

    with st.expander("👁️ View One-Pager Summary (Copy for Slack / Email)"):
        st.code(attendee_email_summary, language="text")
