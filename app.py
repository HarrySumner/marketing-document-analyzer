import streamlit as st
import os
import json
from datetime import datetime
from pathlib import Path
import plotly.graph_objects as go
import plotly.express as px
from dotenv import load_dotenv
from orchestrator.prompt_tester import PromptTester
from orchestrator.workflow_engine import WorkflowEngine
import glob

# Page configuration
st.set_page_config(
    page_title="Multi-Agent Research Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load environment variables
load_dotenv()

# Initialize session state
if 'analysis_results' not in st.session_state:
    st.session_state.analysis_results = None
if 'test_results' not in st.session_state:
    st.session_state.test_results = None
if 'document_input' not in st.session_state:
    st.session_state.document_input = ""
if 'context_input' not in st.session_state:
    st.session_state.context_input = ""

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        padding: 1rem 0;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .success-box {
        background-color: #d4edda;
        border-left: 4px solid #28a745;
        padding: 1rem;
        border-radius: 0.3rem;
        margin: 1rem 0;
    }
    .warning-box {
        background-color: #fff3cd;
        border-left: 4px solid #ffc107;
        padding: 1rem;
        border-radius: 0.3rem;
        margin: 1rem 0;
    }
    .error-box {
        background-color: #f8d7da;
        border-left: 4px solid #dc3545;
        padding: 1rem;
        border-radius: 0.3rem;
        margin: 1rem 0;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
    }
    .stTabs [data-baseweb="tab"] {
        padding: 1rem 2rem;
        font-size: 1.1rem;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<div class="main-header">🤖 Multi-Agent Research Assistant</div>', unsafe_allow_html=True)
st.markdown("---")

# Sidebar
with st.sidebar:
    st.header("🎯 Navigation")

    page = st.radio(
        "Select Mode:",
        ["📝 Analysis", "🧪 A/B Testing", "📊 Results History", "⚙️ Configuration"],
        label_visibility="collapsed"
    )

    st.markdown("---")

    # API Key Status
    st.subheader("🔑 API Status")
    if os.getenv('ANTHROPIC_API_KEY'):
        st.success("✓ API Key Loaded")
    else:
        st.error("✗ API Key Missing")
        st.info("Add ANTHROPIC_API_KEY to .env file")

    st.markdown("---")

    # Quick Stats
    st.subheader("📈 Quick Stats")

    # Count analyses
    analysis_files = glob.glob('outputs/analysis_*.json')
    test_files = glob.glob('outputs/tests/ab_test_*.json')

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Analyses", len(analysis_files))
    with col2:
        st.metric("A/B Tests", len(test_files))

    st.markdown("---")

    # Help
    with st.expander("❓ Help"):
        st.markdown("""
        **Analysis Mode**: Run full multi-agent analysis on marketing materials

        **A/B Testing**: Compare different prompt variants

        **Results History**: View past analyses and tests

        **Configuration**: Manage prompt variants and settings
        """)

# Main Content Area
if page == "📝 Analysis":
    st.header("📝 Document Analysis")
    st.markdown("Upload or paste marketing materials for multi-agent analysis.")

    # Input method selection
    input_method = st.radio("Input Method:", ["Paste Text", "Upload File"], horizontal=True)

    if input_method == "Paste Text":
        col1, col2 = st.columns([2, 1])

        with col1:
            document = st.text_area(
                "Marketing Document",
                height=300,
                placeholder="Paste your marketing copy here...",
                value=st.session_state.document_input,
                help="Enter the marketing material you want to analyze"
            )
            st.session_state.document_input = document

        with col2:
            context = st.text_area(
                "Context (Optional)",
                height=300,
                placeholder="Target audience, product category, price point, etc.",
                value=st.session_state.context_input,
                help="Provide additional context for better analysis"
            )
            st.session_state.context_input = context

    else:
        uploaded_file = st.file_uploader("Upload Document", type=['txt', 'md'])
        if uploaded_file:
            document = uploaded_file.read().decode('utf-8')
            st.session_state.document_input = document

            st.text_area("Preview:", value=document, height=200, disabled=True)

            context = st.text_area(
                "Context (Optional)",
                height=150,
                placeholder="Target audience, product category, etc.",
                value=st.session_state.context_input
            )
            st.session_state.context_input = context
        else:
            document = ""

    st.markdown("---")

    # Analysis controls
    col1, col2, col3, col4 = st.columns([2, 1, 1, 1])

    with col1:
        analyze_button = st.button("🚀 Run Analysis", type="primary", use_container_width=True)

    with col2:
        clear_button = st.button("🗑️ Clear", use_container_width=True)

    with col3:
        if st.session_state.analysis_results:
            st.download_button(
                "📥 Download",
                json.dumps(st.session_state.analysis_results, indent=2),
                file_name=f"analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                use_container_width=True
            )

    if clear_button:
        st.session_state.document_input = ""
        st.session_state.context_input = ""
        st.session_state.analysis_results = None
        st.rerun()

    if analyze_button:
        if not document:
            st.error("⚠️ Please enter a document to analyze")
        elif not os.getenv('ANTHROPIC_API_KEY'):
            st.error("⚠️ ANTHROPIC_API_KEY not found in environment")
        else:
            with st.spinner("🔄 Running multi-agent analysis..."):
                try:
                    # Initialize engine
                    engine = WorkflowEngine()
                    engine.initialize_agents()

                    # Prepare input
                    input_data = {
                        'document': document,
                        'context': context if context else ""
                    }

                    # Execute
                    result = engine.execute_workflow(input_data)

                    if result['success']:
                        st.session_state.analysis_results = result
                        st.success("✅ Analysis complete!")
                    else:
                        st.error(f"❌ Analysis failed: {result.get('error', 'Unknown error')}")

                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")

    # Display results
    if st.session_state.analysis_results:
        st.markdown("---")
        st.header("📊 Analysis Results")

        results = st.session_state.analysis_results

        # Executive Summary
        if 'final_brief' in results:
            st.subheader("📋 Executive Summary")
            st.markdown(f"```\n{results['final_brief']}\n```")

        st.markdown("---")

        # Agent Results in Tabs
        st.subheader("🤖 Agent Insights")

        if 'phase1_results' in results:
            agent_names = list(results['phase1_results'].keys())
            tabs = st.tabs([name.replace('_', ' ').title() for name in agent_names])

            for tab, agent_name in zip(tabs, agent_names):
                with tab:
                    agent_result = results['phase1_results'][agent_name]

                    if agent_result['success']:
                        output = agent_result['output']

                        # Display structured output
                        for key, value in output.items():
                            if not key.startswith('_') and key != 'raw_response':
                                st.markdown(f"**{key.replace('_', ' ').title()}:**")
                                st.info(value)

                        # Execution details
                        with st.expander("🔍 Execution Details"):
                            col1, col2, col3 = st.columns(3)
                            with col1:
                                st.metric("Execution Time", f"{agent_result.get('execution_time', 0):.2f}s")
                            with col2:
                                st.metric("Tokens Used", agent_result.get('tokens_used', 'N/A'))
                            with col3:
                                st.metric("Model", agent_result.get('model', 'N/A'))

                            if 'raw_response' in output:
                                st.markdown("**Raw Response:**")
                                st.text(output['raw_response'])
                    else:
                        st.error(f"Agent failed: {agent_result.get('error', 'Unknown error')}")

elif page == "🧪 A/B Testing":
    st.header("🧪 Prompt A/B Testing")
    st.markdown("Compare different prompt variants to find the best-performing configuration.")

    # Test configuration
    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader("📄 Test Document")

        use_existing = st.checkbox("Use document from Analysis tab", value=bool(st.session_state.document_input))

        if use_existing and st.session_state.document_input:
            document = st.session_state.document_input
            context = st.session_state.context_input

            st.text_area("Document:", value=document, height=200, disabled=True)
            if context:
                st.text_area("Context:", value=context, height=100, disabled=True)
        else:
            document = st.text_area(
                "Marketing Document",
                height=250,
                placeholder="Paste marketing copy for testing..."
            )
            context = st.text_area(
                "Context (Optional)",
                height=100,
                placeholder="Additional context..."
            )

    with col2:
        st.subheader("⚙️ Test Settings")

        agent_name = st.selectbox(
            "Agent to Test",
            ["strategic_analyst", "audience_evaluator"],
            format_func=lambda x: x.replace('_', ' ').title()
        )

        iterations = st.number_input(
            "Iterations per Variant",
            min_value=1,
            max_value=10,
            value=3,
            help="How many times to test each variant"
        )

        st.info(f"📊 Will test {len(PromptTester().variants[agent_name]['variants'])} variants")

        # Show variants
        with st.expander("🔍 View Variants"):
            tester = PromptTester()
            variants = tester.variants[agent_name]['variants']

            for variant_id, variant_config in variants.items():
                st.markdown(f"**{variant_id}**: {variant_config['name']}")
                st.caption(variant_config['hypothesis'])

    st.markdown("---")

    # Test controls
    col1, col2, col3 = st.columns([2, 1, 1])

    with col1:
        test_button = st.button("🧪 Run A/B Test", type="primary", use_container_width=True)

    with col2:
        if st.session_state.test_results:
            st.download_button(
                "📥 Download",
                json.dumps(st.session_state.test_results, indent=2),
                file_name=f"ab_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                use_container_width=True
            )

    if test_button:
        if not document:
            st.error("⚠️ Please provide a document to test")
        elif not os.getenv('ANTHROPIC_API_KEY'):
            st.error("⚠️ ANTHROPIC_API_KEY not found in environment")
        else:
            with st.spinner(f"🔄 Running A/B test ({iterations} iterations × {len(PromptTester().variants[agent_name]['variants'])} variants)..."):
                try:
                    # Initialize tester
                    tester = PromptTester()

                    # Prepare input
                    input_data = {
                        'document': document,
                        'context': context if context else ""
                    }

                    # Run test
                    results = tester.run_ab_test(
                        agent_name=agent_name,
                        input_data=input_data,
                        iterations=iterations
                    )

                    # Save results
                    tester.save_test_results(results)

                    st.session_state.test_results = results
                    st.success("✅ A/B test complete!")

                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
                    st.exception(e)

    # Display results
    if st.session_state.test_results:
        st.markdown("---")
        st.header("📊 Test Results")

        results = st.session_state.test_results

        # Winner announcement
        st.subheader("🏆 Winner")
        col1, col2, col3 = st.columns([2, 1, 1])

        with col1:
            st.markdown(f"### {results['winner']['variant_name']}")
            st.caption(f"Variant ID: {results['winner']['variant_id']}")

        with col2:
            st.metric("Composite Score", f"{results['winner']['composite_score']:.3f}")

        st.markdown("---")

        # Comparative metrics
        st.subheader("📈 Comparative Performance")

        # Create comparison dataframe
        comparison_data = []
        for variant_id, variant_data in results['results'].items():
            metrics = variant_data['metrics']
            comparison_data.append({
                'Variant': variant_data['config']['name'],
                'Consistency': metrics.get('consistency', 0),
                'Specificity': metrics.get('specificity_score', 0),
                'Actionability': metrics.get('actionability_score', 0),
                'Technical Density': metrics.get('technical_density', 0),
                'Execution Time': metrics.get('avg_execution_time', 0)
            })

        # Radar chart for top metrics
        fig = go.Figure()

        for data in comparison_data:
            fig.add_trace(go.Scatterpolar(
                r=[
                    data['Consistency'],
                    data['Specificity'],
                    data['Actionability'],
                    data['Technical Density'],
                    1.0 - min(data['Execution Time'] / 10.0, 1.0)  # Normalize execution time
                ],
                theta=['Consistency', 'Specificity', 'Actionability', 'Technical Density', 'Speed'],
                fill='toself',
                name=data['Variant']
            ))

        fig.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 1])),
            showlegend=True,
            title="Performance Comparison (All Metrics)"
        )

        st.plotly_chart(fig, use_container_width=True)

        # Bar chart comparison
        st.subheader("📊 Metric Rankings")

        metric_tabs = st.tabs(["Consistency", "Specificity", "Actionability", "Technical Density"])

        metric_names = ['consistency', 'specificity_score', 'actionability_score', 'technical_density']

        for tab, metric_name in zip(metric_tabs, metric_names):
            with tab:
                metric_data = []
                for variant_id, variant_data in results['results'].items():
                    metric_data.append({
                        'Variant': variant_data['config']['name'],
                        'Score': variant_data['metrics'].get(metric_name, 0)
                    })

                fig = px.bar(
                    metric_data,
                    x='Variant',
                    y='Score',
                    title=f"{metric_name.replace('_', ' ').title()} Comparison",
                    color='Score',
                    color_continuous_scale='Blues'
                )

                st.plotly_chart(fig, use_container_width=True)

        # Detailed results
        st.markdown("---")
        st.subheader("🔍 Detailed Results")

        for variant_id, variant_data in results['results'].items():
            with st.expander(f"{variant_data['config']['name']} - Details"):
                config = variant_data['config']
                metrics = variant_data['metrics']

                st.markdown(f"**Hypothesis:** {config['hypothesis']}")
                st.markdown(f"**Expected Performance:** {config['expected_performance']}")
                st.markdown(f"**Temperature:** {config['temperature']}")

                st.markdown("---")

                col1, col2, col3 = st.columns(3)

                with col1:
                    st.metric("Consistency", f"{metrics.get('consistency', 0):.3f}")
                    st.metric("Specificity", f"{metrics.get('specificity_score', 0):.3f}")

                with col2:
                    st.metric("Actionability", f"{metrics.get('actionability_score', 0):.3f}")
                    st.metric("Technical Density", f"{metrics.get('technical_density', 0):.3f}")

                with col3:
                    st.metric("Execution Time", f"{metrics.get('avg_execution_time', 0):.2f}s")
                    st.metric("Success Rate", f"{metrics.get('success_rate', 0):.1%}")

elif page == "📊 Results History":
    st.header("📊 Results History")
    st.markdown("Browse and compare past analyses and A/B tests.")

    # Type selector
    result_type = st.radio("Result Type:", ["Analyses", "A/B Tests"], horizontal=True)

    if result_type == "Analyses":
        # List analysis files
        analysis_files = sorted(glob.glob('outputs/analysis_*.json'), reverse=True)

        if not analysis_files:
            st.info("📭 No analyses found. Run an analysis first!")
        else:
            st.markdown(f"**Found {len(analysis_files)} analyses**")

            # File selector
            selected_file = st.selectbox(
                "Select Analysis",
                analysis_files,
                format_func=lambda x: datetime.fromtimestamp(os.path.getmtime(x)).strftime('%Y-%m-%d %H:%M:%S')
            )

            if selected_file:
                with open(selected_file, 'r') as f:
                    result = json.load(f)

                # Display metadata
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Date", datetime.fromtimestamp(os.path.getmtime(selected_file)).strftime('%Y-%m-%d'))
                with col2:
                    st.metric("Agents", len(result.get('phase1_results', {})))
                with col3:
                    st.metric("Success", "✓" if result.get('success') else "✗")

                st.markdown("---")

                # Display brief if available
                brief_file = selected_file.replace('.json', '_brief.txt')
                if os.path.exists(brief_file):
                    with open(brief_file, 'r') as f:
                        st.text_area("Executive Summary", f.read(), height=400)

                # Download button
                with open(selected_file, 'r') as f:
                    st.download_button(
                        "📥 Download Full Results",
                        f.read(),
                        file_name=os.path.basename(selected_file)
                    )

    else:  # A/B Tests
        # List test files
        test_files = sorted(glob.glob('outputs/tests/ab_test_*.json'), reverse=True)

        if not test_files:
            st.info("📭 No A/B tests found. Run a test first!")
        else:
            st.markdown(f"**Found {len(test_files)} tests**")

            # File selector
            selected_file = st.selectbox(
                "Select Test",
                test_files,
                format_func=lambda x: f"{os.path.basename(x).split('_')[2]} - {datetime.fromtimestamp(os.path.getmtime(x)).strftime('%Y-%m-%d %H:%M')}"
            )

            if selected_file:
                with open(selected_file, 'r') as f:
                    result = json.load(f)

                # Display winner
                st.subheader("🏆 Winner")
                col1, col2 = st.columns([2, 1])

                with col1:
                    st.markdown(f"### {result['winner']['variant_name']}")
                with col2:
                    st.metric("Score", f"{result['winner']['composite_score']:.3f}")

                st.markdown("---")

                # Quick comparison chart
                variant_scores = []
                for variant_id, score in result['winner']['all_scores'].items():
                    variant_name = result['results'][variant_id]['config']['name']
                    variant_scores.append({'Variant': variant_name, 'Score': score})

                fig = px.bar(
                    variant_scores,
                    x='Variant',
                    y='Score',
                    title="Composite Scores",
                    color='Score',
                    color_continuous_scale='Viridis'
                )

                st.plotly_chart(fig, use_container_width=True)

                # Download buttons
                col1, col2 = st.columns(2)

                with col1:
                    with open(selected_file, 'r') as f:
                        st.download_button(
                            "📥 Download JSON",
                            f.read(),
                            file_name=os.path.basename(selected_file)
                        )

                with col2:
                    report_file = selected_file.replace('.json', '_report.txt')
                    if os.path.exists(report_file):
                        with open(report_file, 'r') as f:
                            st.download_button(
                                "📥 Download Report",
                                f.read(),
                                file_name=os.path.basename(report_file)
                            )

elif page == "⚙️ Configuration":
    st.header("⚙️ Configuration")
    st.markdown("Manage prompt variants and system settings.")

    # Load current config
    config_file = 'config/prompt_variants.json'

    with open(config_file, 'r') as f:
        config = json.load(f)

    # Agent selector
    agent_name = st.selectbox(
        "Select Agent",
        list(config.keys()),
        format_func=lambda x: x.replace('_', ' ').title()
    )

    st.markdown("---")

    # Display variants
    st.subheader(f"🔧 Prompt Variants for {agent_name.replace('_', ' ').title()}")

    variants = config[agent_name]['variants']

    for variant_id, variant_config in variants.items():
        with st.expander(f"{variant_id}: {variant_config['name']}"):
            # Display config
            col1, col2 = st.columns([3, 1])

            with col1:
                st.markdown(f"**Hypothesis:** {variant_config['hypothesis']}")
                st.markdown(f"**Expected Performance:** {variant_config['expected_performance']}")

            with col2:
                st.metric("Temperature", variant_config['temperature'])

            st.markdown("---")
            st.markdown("**System Prompt:**")
            st.code(variant_config['system_prompt'], language="text")

    st.markdown("---")

    # Add new variant
    st.subheader("➕ Add New Variant")

    with st.form("new_variant_form"):
        new_id = st.text_input("Variant ID", placeholder="v5_my_variant")
        new_name = st.text_input("Variant Name", placeholder="My Custom Variant")
        new_temp = st.slider("Temperature", 0.0, 1.0, 0.3, 0.1)
        new_hypothesis = st.text_input("Hypothesis", placeholder="Why this prompt should work...")
        new_expected = st.text_input("Expected Performance", placeholder="What you expect to see...")
        new_prompt = st.text_area("System Prompt", height=200, placeholder="Your custom system prompt...")

        submitted = st.form_submit_button("➕ Add Variant")

        if submitted:
            if not all([new_id, new_name, new_hypothesis, new_expected, new_prompt]):
                st.error("⚠️ Please fill all fields")
            elif new_id in variants:
                st.error(f"⚠️ Variant {new_id} already exists")
            else:
                # Add new variant
                config[agent_name]['variants'][new_id] = {
                    'name': new_name,
                    'temperature': new_temp,
                    'system_prompt': new_prompt,
                    'hypothesis': new_hypothesis,
                    'expected_performance': new_expected
                }

                # Save config
                with open(config_file, 'w') as f:
                    json.dump(config, f, indent=2)

                st.success(f"✅ Added variant {new_id}")
                st.rerun()

    st.markdown("---")

    # Export/Import
    st.subheader("💾 Export/Import Configuration")

    col1, col2 = st.columns(2)

    with col1:
        st.download_button(
            "📥 Export Configuration",
            json.dumps(config, indent=2),
            file_name="prompt_variants.json",
            mime="application/json"
        )

    with col2:
        uploaded_config = st.file_uploader("📤 Import Configuration", type=['json'])
        if uploaded_config:
            try:
                new_config = json.load(uploaded_config)
                with open(config_file, 'w') as f:
                    json.dump(new_config, f, indent=2)
                st.success("✅ Configuration imported successfully!")
                st.rerun()
            except Exception as e:
                st.error(f"❌ Error importing config: {str(e)}")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #888; padding: 2rem 0;'>
    <p>Multi-Agent Research Assistant | Built with Streamlit & Claude</p>
    <p style='font-size: 0.9rem;'>💡 Tip: Use Ctrl+R to refresh the page</p>
</div>
""", unsafe_allow_html=True)
