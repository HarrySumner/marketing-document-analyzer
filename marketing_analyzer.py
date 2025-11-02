import streamlit as st
import os
from datetime import datetime
import json
from pathlib import Path

# NLP and Analysis imports
try:
    from textblob import TextBlob
except ImportError:
    TextBlob = None

import re
from collections import Counter

# Page config
st.set_page_config(
    page_title="Marketing Document Analyzer",
    page_icon="📊",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main-title {
        font-size: 2.5rem;
        font-weight: bold;
        color: #2c3e50;
        text-align: center;
        margin-bottom: 1rem;
    }
    .persona-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .insight-box {
        background-color: #f8f9fa;
        border-left: 4px solid #667eea;
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 5px;
    }
    .metric-card {
        background: white;
        border: 1px solid #e0e0e0;
        border-radius: 10px;
        padding: 1rem;
        text-align: center;
    }
    .score-good { color: #28a745; font-weight: bold; }
    .score-warning { color: #ffc107; font-weight: bold; }
    .score-poor { color: #dc3545; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'feedback_data' not in st.session_state:
    st.session_state.feedback_data = []
if 'analysis_history' not in st.session_state:
    st.session_state.analysis_history = []

# Title
st.markdown('<div class="main-title">📊 Marketing Document Analyzer</div>', unsafe_allow_html=True)
st.markdown("**Instant analysis of your marketing copy with AI-powered insights**")
st.markdown("---")

# Sidebar - Persona Selection
with st.sidebar:
    st.header("🎭 Analysis Personas")
    st.markdown("Select which perspectives to analyze your document:")

    personas = {
        "Strategic Consultant": {
            "icon": "🎯",
            "description": "Expert marketing strategist analyzing positioning and competitive advantage",
            "focus": ["Strategy", "Positioning", "Differentiation"]
        },
        "Target Customer": {
            "icon": "👤",
            "description": "Your ideal customer's perspective on the message",
            "focus": ["Appeal", "Clarity", "Trust"]
        },
        "Skeptical Buyer": {
            "icon": "🤔",
            "description": "Critical consumer looking for red flags and concerns",
            "focus": ["Objections", "Credibility", "Value"]
        },
        "SEO Specialist": {
            "icon": "🔍",
            "description": "Digital marketing expert analyzing online performance",
            "focus": ["Keywords", "Readability", "Engagement"]
        },
        "Brand Strategist": {
            "icon": "✨",
            "description": "Brand expert evaluating tone, voice, and positioning",
            "focus": ["Voice", "Emotion", "Differentiation"]
        }
    }

    selected_personas = []
    for persona_name, persona_info in personas.items():
        if st.checkbox(f"{persona_info['icon']} {persona_name}", value=persona_name in ["Strategic Consultant", "Target Customer", "Skeptical Buyer"]):
            selected_personas.append(persona_name)

    st.markdown("---")
    st.info(f"💡 **{len(selected_personas)} personas** selected for analysis")

    st.markdown("---")
    st.header("📚 Quick Stats")
    st.metric("Analyses Run", len(st.session_state.analysis_history))
    st.metric("Feedback Given", len(st.session_state.feedback_data))

# Main content
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("📝 Your Marketing Document")

    input_method = st.radio("Input Method:", ["Paste Text", "Upload File"], horizontal=True)

    if input_method == "Paste Text":
        document = st.text_area(
            "Paste your marketing copy here:",
            height=300,
            placeholder="Example:\n\nNew Product Launch!\n\nTransform your workflow with our AI-powered solution...",
            help="Paste any marketing material: ads, emails, landing pages, social posts, etc."
        )
    else:
        uploaded_file = st.file_uploader("Upload your document", type=['txt', 'md', 'docx'])
        if uploaded_file:
            document = uploaded_file.read().decode('utf-8')
            st.text_area("Preview:", value=document, height=200, disabled=True)
        else:
            document = ""

    # Optional context
    with st.expander("➕ Add Context (Optional but Recommended)"):
        context_col1, context_col2 = st.columns(2)

        with context_col1:
            target_audience = st.text_input("Target Audience", placeholder="e.g., B2B SaaS buyers, 30-45")
            industry = st.text_input("Industry", placeholder="e.g., Technology, Healthcare")

        with context_col2:
            price_point = st.text_input("Price Point", placeholder="e.g., $99/mo, Premium tier")
            campaign_type = st.selectbox("Campaign Type", ["", "Email", "Landing Page", "Social Media", "Print Ad", "Video Script", "Other"])

with col2:
    st.subheader("⚙️ Analysis Options")

    st.markdown("**Quick Analysis**")
    include_nlp = st.checkbox("📊 NLP Metrics", value=True, help="Sentiment, readability, keyword analysis")
    include_heuristics = st.checkbox("🎯 Marketing Heuristics", value=True, help="Proven marketing principles checklist")
    include_sentiment = st.checkbox("😊 Emotional Analysis", value=True, help="Emotional tone and sentiment")

    st.markdown("---")

    analyze_button = st.button("🚀 Analyze Document", type="primary", use_container_width=True)

# Analysis Section
if analyze_button:
    if not document or len(document.strip()) < 20:
        st.error("⚠️ Please enter a marketing document (at least 20 characters)")
    elif not selected_personas:
        st.error("⚠️ Please select at least one persona from the sidebar")
    else:
        with st.spinner("🔄 Analyzing your document..."):

            # Store in history
            analysis_record = {
                'timestamp': datetime.now().isoformat(),
                'document_length': len(document),
                'personas': selected_personas
            }
            st.session_state.analysis_history.append(analysis_record)

            st.success("✅ Analysis Complete!")
            st.markdown("---")

            # NLP Analysis Section
            if include_nlp:
                st.subheader("📊 Document Metrics")

                # Basic metrics
                words = document.split()
                sentences = document.split('.')

                metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)

                with metric_col1:
                    st.metric("Word Count", len(words))

                with metric_col2:
                    st.metric("Sentences", len(sentences))

                with metric_col3:
                    avg_word_length = sum(len(word) for word in words) / len(words) if words else 0
                    st.metric("Avg Word Length", f"{avg_word_length:.1f}")

                with metric_col4:
                    reading_time = len(words) / 200  # Average reading speed
                    st.metric("Read Time", f"{reading_time:.1f} min")

                # Sentiment Analysis
                if include_sentiment and TextBlob:
                    try:
                        blob = TextBlob(document)
                        sentiment_score = blob.sentiment.polarity

                        st.markdown("### 😊 Sentiment Analysis")

                        sent_col1, sent_col2 = st.columns([1, 2])

                        with sent_col1:
                            if sentiment_score > 0.3:
                                st.markdown('<p class="score-good">Positive ✅</p>', unsafe_allow_html=True)
                            elif sentiment_score < -0.1:
                                st.markdown('<p class="score-poor">Negative ⚠️</p>', unsafe_allow_html=True)
                            else:
                                st.markdown('<p class="score-warning">Neutral ➖</p>', unsafe_allow_html=True)

                        with sent_col2:
                            st.progress((sentiment_score + 1) / 2)  # Normalize to 0-1
                            st.caption(f"Sentiment Score: {sentiment_score:.2f} (Range: -1 to +1)")
                    except:
                        st.info("Install textblob for sentiment analysis: `pip install textblob`")

                # Keyword extraction
                st.markdown("### 🔑 Top Keywords")
                words_clean = [word.lower() for word in words if len(word) > 4 and word.isalpha()]
                keyword_counts = Counter(words_clean).most_common(10)

                keyword_col1, keyword_col2 = st.columns(2)

                with keyword_col1:
                    for word, count in keyword_counts[:5]:
                        st.markdown(f"**{word.title()}** - {count} times")

                with keyword_col2:
                    for word, count in keyword_counts[5:10]:
                        st.markdown(f"**{word.title()}** - {count} times")

                st.markdown("---")

            # Heuristic Evaluation
            if include_heuristics:
                st.subheader("🎯 Marketing Heuristics Checklist")
                st.caption("Based on proven marketing principles")

                heuristics = {
                    "Clear Value Proposition": {
                        "check": any(word in document.lower() for word in ['benefit', 'save', 'improve', 'increase', 'reduce', 'transform']),
                        "tip": "Clearly state what benefit the customer gets"
                    },
                    "Specific Claims": {
                        "check": bool(re.search(r'\d+%|\$\d+|\d+ (days|hours|minutes)', document)),
                        "tip": "Use specific numbers and data points"
                    },
                    "Call to Action": {
                        "check": any(word in document.lower() for word in ['buy', 'get', 'start', 'try', 'download', 'sign up', 'contact', 'learn more']),
                        "tip": "Include a clear next step for the reader"
                    },
                    "Urgency/Scarcity": {
                        "check": any(word in document.lower() for word in ['limited', 'now', 'today', 'exclusive', 'only', 'hurry']),
                        "tip": "Create urgency (but don't overdo it)"
                    },
                    "Social Proof": {
                        "check": any(word in document.lower() for word in ['customers', 'users', 'clients', 'testimonial', 'review', 'rated', 'trusted']),
                        "tip": "Include customer testimonials or statistics"
                    },
                    "Credibility Markers": {
                        "check": any(word in document.lower() for word in ['proven', 'tested', 'certified', 'guarantee', 'expert', 'professional']),
                        "tip": "Build trust with credentials or guarantees"
                    }
                }

                score = sum(1 for h in heuristics.values() if h['check'])
                total = len(heuristics)

                st.progress(score / total)
                st.markdown(f"**Score: {score}/{total}** heuristics present")

                heur_col1, heur_col2 = st.columns(2)

                for idx, (heuristic, data) in enumerate(heuristics.items()):
                    col = heur_col1 if idx % 2 == 0 else heur_col2

                    with col:
                        if data['check']:
                            st.success(f"✅ {heuristic}")
                        else:
                            st.warning(f"⚠️ {heuristic}")
                            st.caption(f"💡 {data['tip']}")

                st.markdown("---")

            # Persona Analysis
            st.subheader("🎭 Persona Insights")
            st.caption(f"Top 3 insights from each of your {len(selected_personas)} selected personas")

            for persona_name in selected_personas:
                persona_info = personas[persona_name]

                with st.expander(f"{persona_info['icon']} **{persona_name}** - {persona_info['description']}", expanded=True):

                    st.markdown(f"**Focus Areas:** {', '.join(persona_info['focus'])}")
                    st.markdown("---")

                    # Generate persona-specific insights
                    if persona_name == "Strategic Consultant":
                        insights = [
                            {
                                "title": "🎯 Positioning Strategy",
                                "insight": "The document positions the offering as a premium solution, but could strengthen differentiation by highlighting unique features.",
                                "action": "Add 1-2 specific features that competitors don't offer"
                            },
                            {
                                "title": "💪 Key Strength",
                                "insight": f"Strong use of {'benefit-focused' if 'benefit' in document.lower() else 'feature-focused'} language. The messaging clearly communicates value.",
                                "action": "Maintain this approach and apply consistently across all channels"
                            },
                            {
                                "title": "⚠️ Key Weakness",
                                "insight": "Missing clear competitive advantage. Why choose you over alternatives?",
                                "action": "Add explicit comparison or unique selling proposition"
                            }
                        ]

                    elif persona_name == "Target Customer":
                        insights = [
                            {
                                "title": "👀 First Impression",
                                "insight": f"The {'clear headline' if len(document.split('\\n')[0]) < 60 else 'lengthy opening'} {'captures' if len(document.split('\\n')[0]) < 60 else 'may lose'} attention quickly.",
                                "action": "Consider A/B testing the opening line for maximum impact"
                            },
                            {
                                "title": "💭 Clarity Score",
                                "insight": f"Message clarity is {'high' if avg_word_length < 6 else 'moderate'} - average word length of {avg_word_length:.1f} letters.",
                                "action": "Use simpler language where possible for broader appeal"
                            },
                            {
                                "title": "🤝 Trust Factors",
                                "insight": f"{'Strong' if any(word in document.lower() for word in ['guarantee', 'proven', 'trusted']) else 'Limited'} trust signals present.",
                                "action": "Add guarantees, testimonials, or credibility markers"
                            }
                        ]

                    elif persona_name == "Skeptical Buyer":
                        insights = [
                            {
                                "title": "🚩 Red Flags",
                                "insight": f"{'Few' if len(re.findall(r'amazing|incredible|revolutionary|best', document.lower())) < 2 else 'Multiple'} hyperbolic claims detected.",
                                "action": "Replace superlatives with specific, measurable benefits"
                            },
                            {
                                "title": "❓ Unanswered Questions",
                                "insight": f"Price {'is' if price_point else 'is NOT'} mentioned - transparency {'good' if price_point else 'lacking'}.",
                                "action": "Be upfront about pricing to build trust"
                            },
                            {
                                "title": "🛡️ Risk Reversal",
                                "insight": f"{'Good' if 'guarantee' in document.lower() or 'refund' in document.lower() else 'No'} risk reversal present.",
                                "action": "Add money-back guarantee or free trial to reduce purchase risk"
                            }
                        ]

                    elif persona_name == "SEO Specialist":
                        insights = [
                            {
                                "title": "🔍 Keyword Optimization",
                                "insight": f"Top keyword '{keyword_counts[0][0] if keyword_counts else 'N/A'}' appears {keyword_counts[0][1] if keyword_counts else 0} times.",
                                "action": "Ensure primary keywords appear in headline and first 100 words"
                            },
                            {
                                "title": "📱 Readability",
                                "insight": f"{'Short' if len(sentences) > 10 else 'Long'} sentences - average {len(words)/len(sentences):.1f} words per sentence.",
                                "action": "Aim for 15-20 words per sentence for online readability"
                            },
                            {
                                "title": "🎯 Meta Description Ready",
                                "insight": f"First {'100' if len(document) > 100 else len(document)} characters could serve as meta description.",
                                "action": "Extract this for your SEO meta description"
                            }
                        ]

                    else:  # Brand Strategist
                        insights = [
                            {
                                "title": "🎨 Brand Voice",
                                "insight": f"Tone is {'professional' if avg_word_length > 5 else 'casual'} with {'positive' if sentiment_score > 0 else 'neutral'} sentiment.",
                                "action": "Ensure this aligns with your overall brand personality"
                            },
                            {
                                "title": "💫 Emotional Resonance",
                                "insight": f"{'Strong' if sentiment_score > 0.3 else 'Moderate'} emotional appeal detected.",
                                "action": "Consider adding more emotional triggers for engagement"
                            },
                            {
                                "title": "🎭 Differentiation",
                                "insight": f"{'Unique' if len(set(words_clean)) / len(words_clean) > 0.5 else 'Generic'} language - vocabulary diversity {len(set(words_clean)) / len(words_clean):.1%}.",
                                "action": "Use distinctive language that competitors don't use"
                            }
                        ]

                    # Display insights
                    for i, insight_data in enumerate(insights, 1):
                        st.markdown(f"""
                        <div class="insight-box">
                            <strong>{i}. {insight_data['title']}</strong><br>
                            {insight_data['insight']}<br>
                            <small>💡 <em>{insight_data['action']}</em></small>
                        </div>
                        """, unsafe_allow_html=True)

            st.markdown("---")

            # Feedback Section
            st.subheader("📣 Help Us Improve")
            st.markdown("Was this analysis helpful? Your feedback makes our AI smarter!")

            feedback_col1, feedback_col2, feedback_col3 = st.columns(3)

            with feedback_col1:
                if st.button("👍 Very Helpful", use_container_width=True):
                    st.session_state.feedback_data.append({
                        'timestamp': datetime.now().isoformat(),
                        'rating': 'positive',
                        'personas': selected_personas
                    })
                    st.success("Thanks! We'll keep doing this!")

            with feedback_col2:
                if st.button("😐 Somewhat Helpful", use_container_width=True):
                    st.session_state.feedback_data.append({
                        'timestamp': datetime.now().isoformat(),
                        'rating': 'neutral',
                        'personas': selected_personas
                    })
                    st.info("Thanks! We'll work on improving!")

            with feedback_col3:
                if st.button("👎 Not Helpful", use_container_width=True):
                    st.session_state.feedback_data.append({
                        'timestamp': datetime.now().isoformat(),
                        'rating': 'negative',
                        'personas': selected_personas
                    })
                    st.warning("Thanks for the feedback!")

            with st.expander("💬 Add Detailed Feedback (Optional)"):
                detailed_feedback = st.text_area("What could we improve?", placeholder="Tell us what wasn't helpful or what you'd like to see...")
                if st.button("Submit Feedback"):
                    if detailed_feedback:
                        st.session_state.feedback_data[-1]['detailed'] = detailed_feedback
                        st.success("✅ Detailed feedback saved! Thank you!")

            # Export options
            st.markdown("---")
            st.subheader("💾 Export Results")

            export_col1, export_col2 = st.columns(2)

            with export_col1:
                export_data = {
                    'timestamp': datetime.now().isoformat(),
                    'document': document,
                    'context': {
                        'target_audience': target_audience,
                        'industry': industry,
                        'price_point': price_point,
                        'campaign_type': campaign_type
                    },
                    'personas_analyzed': selected_personas,
                    'metrics': {
                        'word_count': len(words),
                        'sentence_count': len(sentences),
                        'avg_word_length': avg_word_length,
                        'sentiment_score': sentiment_score if 'sentiment_score' in locals() else None,
                        'heuristic_score': f"{score}/{total}" if 'score' in locals() else None
                    }
                }

                st.download_button(
                    "📥 Download JSON Report",
                    json.dumps(export_data, indent=2),
                    file_name=f"analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json",
                    use_container_width=True
                )

            with export_col2:
                # Create text report
                text_report = f"""MARKETING DOCUMENT ANALYSIS REPORT
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

DOCUMENT METRICS
- Word Count: {len(words)}
- Sentences: {len(sentences)}
- Reading Time: {reading_time:.1f} minutes

PERSONAS ANALYZED
{', '.join(selected_personas)}

See JSON export for detailed insights.
"""
                st.download_button(
                    "📄 Download Text Report",
                    text_report,
                    file_name=f"analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                    use_container_width=True
                )

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 2rem;'>
    <p><strong>Marketing Document Analyzer</strong> | Built for Marketing Consultants</p>
    <p style='font-size: 0.9rem;'>💡 Tip: Select 2-3 personas for balanced insights</p>
</div>
""", unsafe_allow_html=True)
