"""
Interactive Data Storytelling Interface
Provides natural language interaction with data and automated story generation
"""

import streamlit as st
import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional
import time
import json
from datetime import datetime
import plotly.graph_objects as go
import plotly.express as px
from dataclasses import asdict

# Import advanced insights components
from src.advanced_insights import (
    AdvancedInsightsEngine, EnhancedInsight, DataStory, 
    InsightType, StorytellingMode
)


class InteractiveStorytellerInterface:
    """Interactive interface for data storytelling and Q&A"""
    
    def __init__(self, data: pd.DataFrame):
        """Initialize the storyteller interface"""
        self.data = data
        self.insights_engine = AdvancedInsightsEngine()
        
        # Initialize session state for storytelling
        if 'storytelling_state' not in st.session_state:
            st.session_state.storytelling_state = {
                'current_story': None,
                'generated_insights': [],
                'qa_history': [],
                'opportunities': [],
                'performance_diagnosis': None,
                'storytelling_mode': StorytellingMode.EXECUTIVE_BRIEF,
                'target_audience': 'Business Executives'
            }
    
    def render_storytelling_interface(self):
        """Render the main storytelling interface"""
        st.markdown("## AI-Powered Data Storytelling")
        
        # Create tabs for different storytelling features
        story_tabs = st.tabs([
            "📖 Story Generation",
            "💬 Interactive Q&A", 
            "🔍 Deep Insights",
            "🎯 Opportunity Mining",
            "Performance Diagnosis"
        ])
        
        with story_tabs[0]:
            self._render_story_generation()
        
        with story_tabs[1]:
            self._render_interactive_qa()
        
        with story_tabs[2]:
            self._render_deep_insights()
        
        with story_tabs[3]:
            self._render_opportunity_mining()
        
        with story_tabs[4]:
            self._render_performance_diagnosis()
    
    def _render_story_generation(self):
        """Render story generation interface"""
        st.markdown("### 📖 Automated Data Story Generation")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("#### Story Configuration")
            
            # Story mode selection
            mode_options = {
                "Executive Brief": StorytellingMode.EXECUTIVE_BRIEF,
                "Detailed Analysis": StorytellingMode.DETAILED_ANALYSIS,
                "Narrative Story": StorytellingMode.NARRATIVE_STORY,
                "Problem-Solution": StorytellingMode.PROBLEM_SOLUTION,
                "Opportunity Focus": StorytellingMode.OPPORTUNITY_FOCUS,
                "Comparative Study": StorytellingMode.COMPARATIVE_STUDY
            }
            
            selected_mode = st.selectbox(
                "Storytelling Mode",
                list(mode_options.keys()),
                help="Choose the narrative approach for your data story"
            )
            
            # Target audience
            audience_options = [
                "Business Executives",
                "Technical Team",
                "Board of Directors", 
                "Operations Managers",
                "Sales Team",
                "Marketing Team",
                "General Audience"
            ]
            
            target_audience = st.selectbox("Target Audience", audience_options)
            
            # Business context
            business_context = st.text_area(
                "Business Context (Optional)",
                placeholder="Provide context about your business, industry, or specific situation...",
                height=100
            )
            
            # Story customization
            with st.expander("🎨 Story Customization", expanded=False):
                include_executive_summary = st.checkbox("Include Executive Summary", value=True)
                include_recommendations = st.checkbox("Include Action Items", value=True)
                include_visualizations = st.checkbox("Suggest Visualizations", value=True)
                story_length = st.selectbox("Story Length", ["Concise", "Standard", "Detailed"])
        
        with col2:
            st.markdown("#### Quick Actions")
            
            if st.button("Generate Story", type="primary"):
                self._generate_data_story(
                    mode_options[selected_mode],
                    target_audience,
                    business_context,
                    include_executive_summary,
                    include_recommendations,
                    include_visualizations,
                    story_length
                )
            
            if st.button("🔄 Regenerate Story"):
                if st.session_state.storytelling_state['current_story']:
                    st.rerun()
            
            if st.button("📋 Story Templates"):
                self._show_story_templates()
            
            # Story metrics
            if st.session_state.storytelling_state['current_story']:
                story = st.session_state.storytelling_state['current_story']
                st.metric("Story Sections", len(story.narrative_sections))
                st.metric("Key Findings", len(story.key_findings))
                st.metric("Generated Insights", len(story.insights))
        
        # Display generated story
        if st.session_state.storytelling_state['current_story']:
            self._display_data_story(st.session_state.storytelling_state['current_story'])
    
    def _render_interactive_qa(self):
        """Render interactive Q&A interface"""
        st.markdown("### 💬 Ask Questions About Your Data")
        
        # Q&A input
        col1, col2 = st.columns([3, 1])
        
        with col1:
            question = st.text_input(
                "Ask a question about your data:",
                placeholder="e.g., What are the main trends in sales data? Which factors correlate with high performance?",
                key="qa_question"
            )
        
        with col2:
            ask_button = st.button("🤔 Ask", type="primary")
        
        # Suggested questions
        with st.expander("Suggested Questions", expanded=False):
            suggested_questions = self._get_suggested_questions()
            
            for i, suggestion in enumerate(suggested_questions):
                if st.button(f"📝 {suggestion}", key=f"suggestion_{i}"):
                    st.session_state.qa_question = suggestion
                    ask_button = True
        
        # Process question
        if ask_button and question:
            with st.spinner("Analyzing your question..."):
                self._process_qa_question(question)
        
        # Display Q&A history
        qa_history = st.session_state.storytelling_state['qa_history']
        
        if qa_history:
            st.markdown("#### 📚 Q&A History")
            
            for i, qa_item in enumerate(reversed(qa_history[-5:])):  # Show last 5
                with st.expander(f"Q: {qa_item['question'][:60]}...", expanded=i==0):
                    st.markdown(f"**Question:** {qa_item['question']}")
                    st.markdown(f"**Answer:** {qa_item['answer']['answer']}")
                    
                    # Show confidence and supporting info
                    col_a, col_b = st.columns(2)
                    with col_a:
                        confidence = qa_item['answer'].get('confidence', 0)
                        st.metric("Confidence", f"{confidence}%")
                    
                    with col_b:
                        st.caption(f"Asked: {qa_item['timestamp'].strftime('%H:%M:%S')}")
                    
                    # Follow-up questions
                    follow_ups = qa_item['answer'].get('follow_up_questions', [])
                    if follow_ups:
                        st.markdown("**💭 Follow-up Questions:**")
                        for follow_up in follow_ups:
                            if st.button(f"🔍 {follow_up}", key=f"followup_{i}_{follow_up[:20]}"):
                                st.session_state.qa_question = follow_up
                                st.rerun()
                    
                    # Visualization suggestions
                    viz_suggestions = qa_item['answer'].get('visualization_suggestions', [])
                    if viz_suggestions:
                        st.markdown("**Visualization Suggestions:**")
                        for viz in viz_suggestions:
                            st.markdown(f"• {viz}")
        
        else:
            st.info("Start by asking a question about your data! I can help you understand patterns, trends, correlations, and more.")
    
    def _render_deep_insights(self):
        """Render deep insights generation interface"""
        st.markdown("### 🔍 Advanced AI Insights")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("#### Insight Configuration")
            
            # Focus areas selection
            focus_options = {
                "Trend Analysis": "trends",
                "Anomaly Detection": "anomalies", 
                "Correlation Discovery": "correlations",
                "Business Opportunities": "opportunities",
                "Performance Assessment": "performance",
                "Risk Identification": "risks"
            }
            
            selected_focus_areas = st.multiselect(
                "Analysis Focus Areas",
                list(focus_options.keys()),
                default=["Trend Analysis", "Correlation Discovery"],
                help="Select areas for AI to focus analysis on"
            )
            
            # Business context for insights
            business_domain = st.selectbox(
                "Business Domain",
                ["General", "Sales & Marketing", "Finance", "Operations", "HR", "Customer Service", "Manufacturing"],
                help="Help AI provide domain-specific insights"
            )
            
            # Analysis depth
            analysis_depth = st.selectbox(
                "Analysis Depth",
                ["Quick Overview", "Standard Analysis", "Deep Dive"],
                index=1
            )
        
        with col2:
            st.markdown("#### Generate Insights")
            
            if st.button("Generate Insights", type="primary"):
                focus_areas = [focus_options[area] for area in selected_focus_areas]
                self._generate_deep_insights(focus_areas, business_domain, analysis_depth)
            
            if st.button("🔄 Refresh Analysis"):
                if st.session_state.storytelling_state['generated_insights']:
                    st.rerun()
            
            # Insight metrics
            insights = st.session_state.storytelling_state['generated_insights']
            if insights:
                st.metric("Generated Insights", len(insights))
                avg_confidence = np.mean([insight.confidence_score for insight in insights])
                st.metric("Avg Confidence", f"{avg_confidence:.1f}%")
        
        # Display generated insights
        insights = st.session_state.storytelling_state['generated_insights']
        
        if insights:
            st.markdown("#### 🎯 Generated Insights")
            
            # Insights overview
            col_a, col_b, col_c = st.columns(3)
            
            with col_a:
                high_priority = len([i for i in insights if i.priority == 'High'])
                st.metric("High Priority", high_priority, delta=f"{high_priority/len(insights)*100:.0f}%")
            
            with col_b:
                avg_confidence = np.mean([i.confidence_score for i in insights])
                st.metric("Avg Confidence", f"{avg_confidence:.1f}%")
            
            with col_c:
                action_items = sum(len(i.recommended_actions) for i in insights)
                st.metric("Action Items", action_items)
            
            # Display individual insights
            for i, insight in enumerate(insights):
                with st.expander(f"{insight.title}", expanded=i==0):
                    self._display_enhanced_insight(insight)
        
        else:
            st.info("🔍 Generate insights to see AI-powered analysis of your data patterns and opportunities!")
    
    def _render_opportunity_mining(self):
        """Render opportunity mining interface"""
        st.markdown("### 🎯 Business Opportunity Mining")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Industry context
            industry_context = st.text_area(
                "Industry & Business Context",
                placeholder="Describe your industry, business model, competitive landscape, current challenges...",
                height=120
            )
            
            # Current metrics (optional)
            with st.expander("Current Performance Metrics", expanded=False):
                col_a, col_b = st.columns(2)
                
                with col_a:
                    revenue_growth = st.number_input("Revenue Growth (%)", value=5.0, format="%.1f")
                    customer_acquisition = st.number_input("Customer Acquisition Cost", value=100.0)
                
                with col_b:
                    retention_rate = st.number_input("Customer Retention (%)", value=85.0, format="%.1f")
                    profit_margin = st.number_input("Profit Margin (%)", value=15.0, format="%.1f")
        
        with col2:
            if st.button("⛏️ Mine Opportunities", type="primary"):
                current_metrics = {
                    'revenue_growth': revenue_growth,
                    'customer_acquisition_cost': customer_acquisition,
                    'retention_rate': retention_rate,
                    'profit_margin': profit_margin
                } if industry_context else None
                
                self._mine_business_opportunities(industry_context, current_metrics)
            
            if st.button("🔄 Refresh Analysis"):
                st.rerun()
        
        # Display opportunities
        opportunities = st.session_state.storytelling_state['opportunities']
        
        if opportunities:
            st.markdown("#### Identified Opportunities")
            
            for i, opportunity in enumerate(opportunities):
                with st.expander(f"💼 {opportunity['title']}", expanded=i==0):
                    self._display_opportunity(opportunity)
        
        else:
            st.info("⛏️ Mine your data for business opportunities! The AI will analyze patterns to identify potential areas for growth and optimization.")
    
    def _render_performance_diagnosis(self):
        """Render performance diagnosis interface"""
        st.markdown("### Performance Diagnosis")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Performance analysis configuration
            st.markdown("#### Analysis Configuration")
            
            # Time column selection
            date_columns = self.data.select_dtypes(include=['datetime64']).columns.tolist()
            time_column = None
            
            if date_columns:
                time_column = st.selectbox("Time Column", ['Auto-detect'] + date_columns)
                if time_column == 'Auto-detect':
                    time_column = date_columns[0] if date_columns else None
            
            # Performance metrics selection
            numeric_columns = self.data.select_dtypes(include=[np.number]).columns.tolist()
            performance_metrics = st.multiselect(
                "Performance Metrics",
                numeric_columns,
                default=numeric_columns[:3] if len(numeric_columns) >= 3 else numeric_columns,
                help="Select key metrics to analyze for performance diagnosis"
            )
            
            # Analysis period
            analysis_period = st.selectbox(
                "Analysis Period",
                ["All Available Data", "Last 30 Days", "Last 90 Days", "Last Year", "Custom Range"],
                help="Define the time period for performance analysis"
            )
        
        with col2:
            st.markdown("#### Run Diagnosis")
            
            if st.button("🩺 Diagnose Performance", type="primary"):
                self._run_performance_diagnosis(time_column, performance_metrics, analysis_period)
            
            if st.button("📋 Generate Report"):
                if st.session_state.storytelling_state['performance_diagnosis']:
                    self._generate_diagnosis_report()
        
        # Display diagnosis results
        diagnosis = st.session_state.storytelling_state['performance_diagnosis']
        
        if diagnosis:
            st.markdown("#### 📋 Performance Diagnosis Results")
            self._display_performance_diagnosis(diagnosis)
        
        else:
            st.info("🩺 Run a performance diagnosis to get AI-powered analysis of your key metrics, identify strengths, weaknesses, and improvement opportunities.")
    
    def _generate_data_story(self, mode: StorytellingMode, audience: str, context: str,
                           include_summary: bool, include_recommendations: bool,
                           include_visualizations: bool, length: str):
        """Generate a comprehensive data story"""
        
        with st.spinner("📖 Crafting your data story..."):
            try:
                story = self.insights_engine.create_data_story(
                    self.data,
                    mode=mode,
                    target_audience=audience,
                    business_context=context
                )
                
                st.session_state.storytelling_state['current_story'] = story
                st.success("✅ Data story generated successfully!")
                
            except Exception as e:
                st.error(f"❌ Story generation failed: {str(e)}")
    
    def _process_qa_question(self, question: str):
        """Process a Q&A question"""
        
        try:
            answer = self.insights_engine.interactive_qa_session(self.data, question)
            
            qa_item = {
                'question': question,
                'answer': answer,
                'timestamp': datetime.now()
            }
            
            st.session_state.storytelling_state['qa_history'].append(qa_item)
            
            # Display the answer immediately
            st.markdown("#### AI Response")
            st.markdown(answer['answer'])
            
            # Show confidence
            confidence = answer.get('confidence', 0)
            st.progress(confidence / 100, text=f"Confidence: {confidence}%")
            
        except Exception as e:
            st.error(f"❌ Failed to process question: {str(e)}")
    
    def _generate_deep_insights(self, focus_areas: List[str], business_domain: str, depth: str):
        """Generate deep insights"""
        
        with st.spinner("Generating advanced insights..."):
            try:
                insights = self.insights_engine.generate_enhanced_insights(
                    self.data,
                    business_context=f"Business domain: {business_domain}, Analysis depth: {depth}",
                    focus_areas=focus_areas
                )
                
                st.session_state.storytelling_state['generated_insights'] = insights
                st.success(f"✅ Generated {len(insights)} insights!")
                
            except Exception as e:
                st.error(f"❌ Insight generation failed: {str(e)}")
    
    def _mine_business_opportunities(self, industry_context: str, current_metrics: Dict[str, float]):
        """Mine business opportunities"""
        
        with st.spinner("⛏️ Mining business opportunities..."):
            try:
                opportunities = self.insights_engine.mine_opportunities(
                    self.data,
                    industry_context=industry_context,
                    current_metrics=current_metrics
                )
                
                st.session_state.storytelling_state['opportunities'] = opportunities
                st.success(f"✅ Identified {len(opportunities)} opportunities!")
                
            except Exception as e:
                st.error(f"❌ Opportunity mining failed: {str(e)}")
    
    def _run_performance_diagnosis(self, time_column: str, metrics: List[str], period: str):
        """Run performance diagnosis"""
        
        with st.spinner("🩺 Diagnosing performance..."):
            try:
                diagnosis = self.insights_engine.diagnose_performance(
                    self.data,
                    time_column=time_column,
                    performance_metrics=metrics
                )
                
                st.session_state.storytelling_state['performance_diagnosis'] = diagnosis
                st.success("✅ Performance diagnosis complete!")
                
            except Exception as e:
                st.error(f"❌ Performance diagnosis failed: {str(e)}")
    
    def _display_data_story(self, story: DataStory):
        """Display a generated data story"""
        
        st.markdown("#### 📖 Generated Data Story")
        
        # Story header
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.markdown(f"# {story.title}")
            st.markdown(f"*{story.mode.value.replace('_', ' ').title()} for {story.target_audience}*")
        
        with col2:
            st.metric("Sections", len(story.narrative_sections))
            st.metric("Key Findings", len(story.key_findings))
            st.caption(f"Generated: {story.created_at.strftime('%H:%M:%S')}")
        
        # Executive summary
        if story.executive_summary:
            st.markdown("## 📋 Executive Summary")
            st.markdown(f'<div style="background-color: #f0f2f6; padding: 1rem; border-radius: 0.5rem; border-left: 4px solid #1f77b4;">{story.executive_summary}</div>', unsafe_allow_html=True)
        
        # Key findings
        if story.key_findings:
            st.markdown("## 🔍 Key Findings")
            for i, finding in enumerate(story.key_findings, 1):
                st.markdown(f"**{i}.** {finding}")
        
        # Narrative sections
        if story.narrative_sections:
            st.markdown("## 📖 Detailed Analysis")
            
            for section in story.narrative_sections:
                st.markdown(f"### {section['section']}")
                st.markdown(section['content'])
        
        # Insights
        if story.insights:
            st.markdown("## AI-Generated Insights")
            
            insight_tabs = st.tabs([f"Insight {i+1}" for i in range(len(story.insights))])
            
            for tab, insight in zip(insight_tabs, story.insights):
                with tab:
                    self._display_enhanced_insight(insight)
        
        # Recommended visualizations
        if story.recommended_visualizations:
            st.markdown("## Recommended Visualizations")
            
            for viz in story.recommended_visualizations:
                st.markdown(f"• **{viz['type'].replace('_', ' ').title()}:** {viz['description']}")
        
        # Call to action
        if story.call_to_action:
            st.markdown("## 🎯 Next Steps")
            st.markdown(f'<div style="background-color: #d4edda; padding: 1rem; border-radius: 0.5rem; border-left: 4px solid #28a745;">{story.call_to_action}</div>', unsafe_allow_html=True)
        
        # Export options
        st.markdown("## 📤 Export Story")
        
        col_a, col_b, col_c = st.columns(3)
        
        with col_a:
            if st.button("📄 Export as PDF"):
                st.info("PDF export feature coming soon!")
        
        with col_b:
            if st.button("📧 Email Report"):
                st.info("Email feature coming soon!")
        
        with col_c:
            # JSON export
            story_json = json.dumps(asdict(story), indent=2, default=str)
            st.download_button(
                "💾 Download JSON",
                data=story_json,
                file_name=f"data_story_{story.story_id}.json",
                mime="application/json"
            )
    
    def _display_enhanced_insight(self, insight: EnhancedInsight):
        """Display an enhanced insight"""
        
        # Insight header
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            st.markdown(f"**{insight.title}**")
            st.caption(f"Type: {insight.insight_type.value.replace('_', ' ').title()}")
        
        with col2:
            confidence_color = "🟢" if insight.confidence_score >= 80 else "🟡" if insight.confidence_score >= 60 else "🟠"
            st.metric("Confidence", f"{confidence_color} {insight.confidence_score:.0f}%")
        
        with col3:
            priority_color = "🔴" if insight.priority == "High" else "🟡" if insight.priority == "Medium" else "🟢"
            st.metric("Priority", f"{priority_color} {insight.priority}")
        
        # Insight content
        st.markdown(f"**Summary:** {insight.summary}")
        
        with st.expander("📖 Detailed Explanation"):
            st.markdown(insight.detailed_explanation)
        
        # Business impact
        if insight.business_impact:
            st.markdown(f"**💼 Business Impact:** {insight.business_impact}")
        
        # Recommended actions
        if insight.recommended_actions:
            st.markdown("**🎯 Recommended Actions:**")
            for action in insight.recommended_actions:
                st.markdown(f"• {action}")
        
        # Additional info
        col_info1, col_info2 = st.columns(2)
        
        with col_info1:
            if insight.stakeholders:
                st.markdown(f"**👥 Stakeholders:** {', '.join(insight.stakeholders)}")
        
        with col_info2:
            st.markdown(f"**⏱️ Timeframe:** {insight.timeframe}")
        
        # Tags
        if insight.tags:
            st.markdown("**🏷️ Tags:** " + " • ".join([f"`{tag}`" for tag in insight.tags]))
    
    def _display_opportunity(self, opportunity: Dict[str, Any]):
        """Display a business opportunity"""
        
        st.markdown(f"**Description:** {opportunity['description']}")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"**💰 Potential Impact:** {opportunity['potential_impact']}")
            st.markdown(f"**Time to Value:** {opportunity['time_to_value']}")
        
        with col2:
            st.markdown(f"**🔧 Implementation:** {opportunity['implementation_difficulty']}")
        
        if 'success_metrics' in opportunity:
            st.markdown("**Success Metrics:**")
            for metric in opportunity['success_metrics']:
                st.markdown(f"• {metric}")
    
    def _display_performance_diagnosis(self, diagnosis: Dict[str, Any]):
        """Display performance diagnosis results"""
        
        # Overall assessment
        st.markdown(f"**Overall Assessment:** {diagnosis['overall_assessment']}")
        
        # Strengths and improvements in columns
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### ✅ Strengths")
            for strength in diagnosis.get('strengths', []):
                st.markdown(f"• {strength}")
        
        with col2:
            st.markdown("#### ⚠️ Areas for Improvement")
            for improvement in diagnosis.get('areas_for_improvement', []):
                st.markdown(f"• {improvement}")
        
        # Root causes
        if 'root_causes' in diagnosis:
            st.markdown("#### 🔍 Root Causes")
            for cause in diagnosis['root_causes']:
                st.markdown(f"• {cause}")
        
        # Recommendations
        if 'recommendations' in diagnosis:
            st.markdown("#### Recommendations")
            for rec in diagnosis['recommendations']:
                st.markdown(f"• {rec}")
    
    def _get_suggested_questions(self) -> List[str]:
        """Get suggested questions based on data characteristics"""
        
        questions = []
        
        # Basic questions
        questions.extend([
            "What are the key trends in this data?",
            "What insights can you provide about the overall patterns?",
            "Are there any notable anomalies or outliers?"
        ])
        
        # Data-specific questions
        numeric_cols = self.data.select_dtypes(include=[np.number]).columns
        categorical_cols = self.data.select_dtypes(include=['object', 'category']).columns
        
        if len(numeric_cols) > 1:
            questions.extend([
                f"What is the correlation between {numeric_cols[0]} and {numeric_cols[1]}?",
                f"How does {numeric_cols[0]} vary across different segments?"
            ])
        
        if len(categorical_cols) > 0:
            questions.extend([
                f"How does performance differ across {categorical_cols[0]}?",
                f"Which {categorical_cols[0]} category performs best?"
            ])
        
        # Time-based questions
        date_cols = self.data.select_dtypes(include=['datetime64']).columns
        if len(date_cols) > 0:
            questions.extend([
                "What are the seasonal patterns in the data?",
                "How has performance changed over time?"
            ])
        
        return questions[:8]  # Limit to 8 suggestions
    
    def _show_story_templates(self):
        """Show available story templates"""
        
        with st.expander("📋 Available Story Templates", expanded=True):
            templates = {
                "Executive Brief": "Concise summary for senior leadership with key insights and recommendations",
                "Detailed Analysis": "Comprehensive analysis with thorough examination of patterns and relationships",
                "Narrative Story": "Engaging story format that guides readers through discoveries",
                "Problem-Solution": "Structured approach focusing on identifying issues and proposing solutions",
                "Opportunity Focus": "Emphasis on business opportunities and growth potential",
                "Comparative Study": "Analysis comparing different segments, periods, or scenarios"
            }
            
            for template, description in templates.items():
                st.markdown(f"**{template}:** {description}")
    
    def _generate_diagnosis_report(self):
        """Generate a comprehensive diagnosis report"""
        
        diagnosis = st.session_state.storytelling_state['performance_diagnosis']
        
        if diagnosis:
            report = f"""
# Performance Diagnosis Report
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Overall Assessment
{diagnosis['overall_assessment']}

## Strengths
{chr(10).join(['• ' + strength for strength in diagnosis.get('strengths', [])])}

## Areas for Improvement  
{chr(10).join(['• ' + improvement for improvement in diagnosis.get('areas_for_improvement', [])])}

## Root Causes
{chr(10).join(['• ' + cause for cause in diagnosis.get('root_causes', [])])}

## Recommendations
{chr(10).join(['• ' + rec for rec in diagnosis.get('recommendations', [])])}
"""
            
            st.download_button(
                "📋 Download Report",
                data=report,
                file_name=f"performance_diagnosis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
                mime="text/markdown"
            )


# Export main class
__all__ = ['InteractiveStorytellerInterface']
