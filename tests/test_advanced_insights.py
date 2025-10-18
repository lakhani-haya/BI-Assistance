"""
Test Suite for Ad AI Insights and Interactive Storytelling

"""

import pytest
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import sys
import os

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from src.advanced_insights import (
    AdvancedInsightsEngine, EnhancedInsight, DataStory, 
    InsightType, StorytellingMode
)
from src.interactive_storyteller import InteractiveStorytellerInterface


@pytest.fixture
def sample_business_data():
    """Create sample business data for testing"""
    np.random.seed(42)
    
    dates = pd.date_range(start='2023-01-01', end='2023-12-31', freq='D')
    
    data = []
    for date in dates[:100]:  # Use first 100 days for faster tests
        data.append({
            'Date': date,
            'Revenue': np.random.uniform(5000, 15000),
            'Orders': np.random.randint(50, 200),
            'Customers': np.random.randint(40, 180),
            'Product_Category': np.random.choice(['Electronics', 'Clothing', 'Books']),
            'Region': np.random.choice(['North', 'South', 'East', 'West']),
            'Marketing_Spend': np.random.uniform(500, 2000),
            'Customer_Satisfaction': np.random.uniform(3.0, 5.0),
            'Profit_Margin': np.random.uniform(10, 40)
        })
    
    return pd.DataFrame(data)


@pytest.fixture
def insights_engine():
    """Create insights engine instance"""
    return AdvancedInsightsEngine()


class TestAdvancedInsightsEngine:
    """Test suite for AdvancedInsightsEngine"""
    
    def test_initialization(self, insights_engine):
        """Test insights engine initialization"""
        assert insights_engine is not None
        assert hasattr(insights_engine, 'api_key')
        assert hasattr(insights_engine, 'use_mock_responses')
    
    def test_create_data_story(self, insights_engine, sample_business_data):
        """Test data story creation"""
        story = insights_engine.create_data_story(
            sample_business_data,
            mode=StorytellingMode.EXECUTIVE_BRIEF,
            target_audience="Business Executives",
            business_context="Test retail business"
        )
        
        assert isinstance(story, DataStory)
        assert story.title is not None
        assert story.target_audience == "Business Executives"
        assert story.mode == StorytellingMode.EXECUTIVE_BRIEF
        assert len(story.key_findings) > 0
        assert story.executive_summary is not None
    
    def test_interactive_qa_session(self, insights_engine, sample_business_data):
        """Test interactive Q&A functionality"""
        question = "What are the main trends in revenue?"
        
        answer = insights_engine.interactive_qa_session(
            sample_business_data,
            question
        )
        
        assert isinstance(answer, dict)
        assert 'answer' in answer
        assert 'confidence' in answer
        assert answer['confidence'] >= 0
        assert answer['confidence'] <= 100
        assert len(answer['answer']) > 0
    
    def test_generate_enhanced_insights(self, insights_engine, sample_business_data):
        """Test enhanced insights generation"""
        insights = insights_engine.generate_enhanced_insights(
            sample_business_data,
            business_context="Test business context",
            focus_areas=['trends', 'correlations']
        )
        
        assert isinstance(insights, list)
        assert len(insights) > 0
        
        for insight in insights:
            assert isinstance(insight, EnhancedInsight)
            assert insight.title is not None
            assert insight.summary is not None
            assert insight.confidence_score >= 0
            assert insight.confidence_score <= 100
            assert insight.priority in ['High', 'Medium', 'Low']
    
    def test_mine_opportunities(self, insights_engine, sample_business_data):
        """Test opportunity mining"""
        opportunities = insights_engine.mine_opportunities(
            sample_business_data,
            industry_context="Retail business",
            current_metrics={
                'revenue_growth': 10.0,
                'customer_acquisition_cost': 50.0,
                'retention_rate': 80.0,
                'profit_margin': 25.0
            }
        )
        
        assert isinstance(opportunities, list)
        assert len(opportunities) > 0
        
        for opp in opportunities:
            assert isinstance(opp, dict)
            assert 'title' in opp
            assert 'description' in opp
            assert 'potential_impact' in opp
            assert 'time_to_value' in opp
    
    def test_diagnose_performance(self, insights_engine, sample_business_data):
        """Test performance diagnosis"""
        diagnosis = insights_engine.diagnose_performance(
            sample_business_data,
            time_column='Date',
            performance_metrics=['Revenue', 'Orders', 'Customer_Satisfaction']
        )
        
        assert isinstance(diagnosis, dict)
        assert 'overall_assessment' in diagnosis
        assert 'strengths' in diagnosis
        assert 'areas_for_improvement' in diagnosis
        assert 'recommendations' in diagnosis
        
        assert isinstance(diagnosis['strengths'], list)
        assert isinstance(diagnosis['areas_for_improvement'], list)
        assert isinstance(diagnosis['recommendations'], list)
    
    def test_storytelling_modes(self, insights_engine, sample_business_data):
        """Test different storytelling modes"""
        modes = [
            StorytellingMode.EXECUTIVE_BRIEF,
            StorytellingMode.DETAILED_ANALYSIS,
            StorytellingMode.NARRATIVE_STORY,
            StorytellingMode.PROBLEM_SOLUTION
        ]
        
        for mode in modes:
            story = insights_engine.create_data_story(
                sample_business_data,
                mode=mode,
                target_audience="Test Audience"
            )
            
            assert story.mode == mode
            assert story.title is not None
            assert len(story.key_findings) > 0
    
    def test_insight_types(self, insights_engine, sample_business_data):
        """Test different insight types generation"""
        insights = insights_engine.generate_enhanced_insights(
            sample_business_data,
            focus_areas=['trends', 'anomalies', 'correlations', 'opportunities']
        )
        
        insight_types = [insight.insight_type for insight in insights]
        
        # Should have multiple types
        assert len(set(insight_types)) > 1
        
        # All should be valid types
        valid_types = [t.value for t in InsightType]
        for insight_type in insight_types:
            assert insight_type.value in valid_types


class TestInteractiveStorytellerInterface:
    """Test suite for InteractiveStorytellerInterface"""
    
    def test_initialization(self, sample_business_data):
        """Test storyteller interface initialization"""
        storyteller = InteractiveStorytellerInterface(sample_business_data)
        
        assert storyteller.data is not None
        assert len(storyteller.data) > 0
        assert storyteller.insights_engine is not None
    
    def test_suggested_questions_generation(self, sample_business_data):
        """Test suggested questions generation"""
        storyteller = InteractiveStorytellerInterface(sample_business_data)
        
        questions = storyteller._get_suggested_questions()
        
        assert isinstance(questions, list)
        assert len(questions) > 0
        assert len(questions) <= 8  # Should limit to 8 suggestions
        
        for question in questions:
            assert isinstance(question, str)
            assert len(question) > 0
    
    def test_data_characteristics_detection(self, sample_business_data):
        """Test detection of data characteristics for question suggestions"""
        storyteller = InteractiveStorytellerInterface(sample_business_data)
        
        # Should detect numeric columns
        numeric_cols = sample_business_data.select_dtypes(include=[np.number]).columns
        assert len(numeric_cols) > 0
        
        # Should detect categorical columns
        categorical_cols = sample_business_data.select_dtypes(include=['object']).columns
        assert len(categorical_cols) > 0
        
        # Should detect date columns
        date_cols = sample_business_data.select_dtypes(include=['datetime64']).columns
        assert len(date_cols) > 0


class TestDataStoryStructure:
    """Test suite for DataStory structure and validation"""
    
    def test_data_story_completeness(self, insights_engine, sample_business_data):
        """Test that data stories have all required components"""
        story = insights_engine.create_data_story(
            sample_business_data,
            mode=StorytellingMode.DETAILED_ANALYSIS,
            target_audience="Analysts",
            business_context="Comprehensive analysis required"
        )
        
        # Check required fields
        assert hasattr(story, 'story_id')
        assert hasattr(story, 'title')
        assert hasattr(story, 'mode')
        assert hasattr(story, 'target_audience')
        assert hasattr(story, 'created_at')
        assert hasattr(story, 'key_findings')
        assert hasattr(story, 'narrative_sections')
        assert hasattr(story, 'insights')
        
        # Check data types
        assert isinstance(story.story_id, str)
        assert isinstance(story.title, str)
        assert isinstance(story.target_audience, str)
        assert isinstance(story.created_at, datetime)
        assert isinstance(story.key_findings, list)
        assert isinstance(story.narrative_sections, list)
        assert isinstance(story.insights, list)
    
    def test_enhanced_insight_structure(self, insights_engine, sample_business_data):
        """Test EnhancedInsight structure"""
        insights = insights_engine.generate_enhanced_insights(
            sample_business_data,
            focus_areas=['trends']
        )
        
        assert len(insights) > 0
        
        insight = insights[0]
        
        # Check required fields
        assert hasattr(insight, 'insight_id')
        assert hasattr(insight, 'title')
        assert hasattr(insight, 'insight_type')
        assert hasattr(insight, 'summary')
        assert hasattr(insight, 'detailed_explanation')
        assert hasattr(insight, 'confidence_score')
        assert hasattr(insight, 'priority')
        assert hasattr(insight, 'business_impact')
        assert hasattr(insight, 'recommended_actions')
        assert hasattr(insight, 'stakeholders')
        assert hasattr(insight, 'timeframe')
        assert hasattr(insight, 'tags')
        assert hasattr(insight, 'created_at')
        
        # Check data types and constraints
        assert isinstance(insight.insight_id, str)
        assert isinstance(insight.title, str)
        assert isinstance(insight.summary, str)
        assert isinstance(insight.confidence_score, (int, float))
        assert 0 <= insight.confidence_score <= 100
        assert insight.priority in ['High', 'Medium', 'Low']
        assert isinstance(insight.recommended_actions, list)
        assert isinstance(insight.stakeholders, list)
        assert isinstance(insight.tags, list)
        assert isinstance(insight.created_at, datetime)


class TestBusinessContextHandling:
    """Test suite for business context handling"""
    
    def test_industry_specific_insights(self, insights_engine, sample_business_data):
        """Test industry-specific insight generation"""
        retail_context = "Retail business with seasonal patterns"
        tech_context = "Technology startup with rapid growth"
        
        retail_insights = insights_engine.generate_enhanced_insights(
            sample_business_data,
            business_context=retail_context
        )
        
        tech_insights = insights_engine.generate_enhanced_insights(
            sample_business_data,
            business_context=tech_context
        )
        
        # Should generate insights for both contexts
        assert len(retail_insights) > 0
        assert len(tech_insights) > 0
        
        # Insights should reference context appropriately
        retail_text = " ".join([insight.summary for insight in retail_insights])
        tech_text = " ".join([insight.summary for insight in tech_insights])
        
        # Both should be meaningful
        assert len(retail_text) > 100
        assert len(tech_text) > 100
    
    def test_audience_targeting(self, insights_engine, sample_business_data):
        """Test audience-specific story generation"""
        audiences = [
            "C-Suite Executives",
            "Technical Team",
            "Operations Managers",
            "Marketing Team"
        ]
        
        stories = []
        for audience in audiences:
            story = insights_engine.create_data_story(
                sample_business_data,
                target_audience=audience,
                mode=StorytellingMode.EXECUTIVE_BRIEF
            )
            stories.append(story)
        
        # Should generate stories for all audiences
        assert len(stories) == len(audiences)
        
        for story, audience in zip(stories, audiences):
            assert story.target_audience == audience
            assert story.title is not None
            assert len(story.key_findings) > 0


def test_error_handling():
    """Test error handling for edge cases"""
    insights_engine = AdvancedInsightsEngine()
    
    # Test with empty data
    empty_data = pd.DataFrame()
    
    # Should handle empty data gracefully
    try:
        story = insights_engine.create_data_story(empty_data)
        # If it doesn't raise an error, should return a story with appropriate content
        assert story.title is not None
    except Exception as e:
        # If it raises an error, should be informative
        assert len(str(e)) > 0
    
    # Test with invalid questions
    sample_data = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
    
    try:
        answer = insights_engine.interactive_qa_session(sample_data, "")
        assert answer is not None
    except Exception as e:
        assert len(str(e)) > 0


def test_performance_benchmarks(sample_business_data):
    """Test performance benchmarks for key operations"""
    insights_engine = AdvancedInsightsEngine()
    
    # Test story generation performance
    start_time = datetime.now()
    story = insights_engine.create_data_story(
        sample_business_data,
        mode=StorytellingMode.EXECUTIVE_BRIEF
    )
    story_time = (datetime.now() - start_time).total_seconds()
    
    # Should complete in reasonable time (adjust based on mock vs real API)
    assert story_time < 30  # 30 seconds max
    assert story is not None
    
    # Test Q&A performance
    start_time = datetime.now()
    answer = insights_engine.interactive_qa_session(
        sample_business_data,
        "What are the main trends?"
    )
    qa_time = (datetime.now() - start_time).total_seconds()
    
    assert qa_time < 20  # 20 seconds max
    assert answer is not None


if __name__ == "__main__":
    # Run specific tests
    pytest.main([__file__, "-v"])
