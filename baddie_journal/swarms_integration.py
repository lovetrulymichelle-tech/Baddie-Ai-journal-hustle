"""
Swarms AI integration for Baddie AI Journal Hustle.

This module integrates the Swarms framework to provide AI-powered analysis
of journal entries using multiple specialized agents for different insights.
"""

import os
import json
from datetime import datetime, UTC
from typing import Dict, List, Optional, Any
from dataclasses import dataclass

# Optional imports - handle gracefully if not available
try:
    from swarms import Agent

    _swarms_available = True
except ImportError:
    Agent = None
    _swarms_available = False

try:
    from openai import OpenAI

    _openai_available = True
except ImportError:
    OpenAI = None
    _openai_available = False

from .models import InsightData
from .insights import InsightsHelper


@dataclass
class SwarmAnalysisResult:
    """Result from swarm analysis of journal entries."""

    mood_analysis: Dict[str, Any]
    pattern_insights: Dict[str, Any]
    recommendations: List[str]
    emotional_trends: Dict[str, Any]
    personal_growth_insights: Dict[str, Any]
    generated_at: datetime


class JournalAnalysisSwarm:
    """
    Swarm of AI agents specialized for different aspects of journal analysis.

    This class coordinates multiple AI agents to provide comprehensive
    analysis of journal entries from different perspectives.
    """

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the Journal Analysis Swarm.

        Args:
            api_key: OpenAI API key (optional, can use environment variable)
        """
        if not _swarms_available:
            raise ImportError(
                "Swarms framework is not available. Install with: pip install swarms>=6.0.0"
            )

        if not _openai_available:
            raise ImportError(
                "OpenAI package is not available. Install with: pip install openai>=1.0.0"
            )

        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError(
                "OpenAI API key is required. Set OPENAI_API_KEY environment variable "
                "or pass api_key parameter."
            )

        self.client = OpenAI(api_key=self.api_key)
        self._initialize_agents()

    def _create_system_prompt(self, name: str, description: str, task: str) -> str:
        """Create a system prompt for an agent."""
        return f"""You are {name}, {description}.

Your primary task is: {task}

Guidelines:
- Provide detailed, thoughtful analysis based on the provided journal data
- Focus on patterns, insights, and actionable observations
- Be respectful and supportive in your analysis
- Format your response as requested (JSON when specified)
- Be specific and concrete in your recommendations and insights

Remember: This is private journal data. Treat it with respect and confidentiality."""

    def _initialize_agents(self):
        """Initialize the specialized agents for journal analysis."""

        # Mood Analysis Agent
        self.mood_agent = Agent(
            agent_name="Mood Analyzer",
            system_prompt=self._create_system_prompt(
                name="Mood Analyzer",
                description="an expert at analyzing emotional patterns and mood trends in journal entries",
                task="Analyze journal entries to identify mood patterns, emotional triggers, "
                "and sentiment trends over time",
            ),
            model_name="gpt-4o-mini",
            max_loops=1,
            temperature=0.3,
            openai_api_key=self.api_key,
        )

        # Pattern Recognition Agent
        self.pattern_agent = Agent(
            agent_name="Pattern Recognizer",
            system_prompt=self._create_system_prompt(
                name="Pattern Recognizer",
                description="a specialist in identifying behavioral patterns, habits, and recurring themes",
                task="Identify patterns in writing habits, topics, timing, and behavioral trends from journal entries",
            ),
            model_name="gpt-4o-mini",
            max_loops=1,
            temperature=0.3,
            openai_api_key=self.api_key,
        )

        # Personal Growth Coach Agent
        self.growth_agent = Agent(
            agent_name="Growth Coach",
            system_prompt=self._create_system_prompt(
                name="Personal Growth Coach",
                description="an expert at identifying personal development opportunities and growth insights",
                task="Analyze journal entries to identify growth opportunities, achievements, "
                "and areas for personal development",
            ),
            model_name="gpt-4o-mini",
            max_loops=1,
            temperature=0.5,
            openai_api_key=self.api_key,
        )

        # Recommendation Agent
        self.recommendation_agent = Agent(
            agent_name="Recommendation Specialist",
            system_prompt=self._create_system_prompt(
                name="Recommendation Specialist",
                description="an expert at generating actionable recommendations based on journal analysis",
                task="Generate personalized recommendations for improving well-being, productivity, "
                "and personal growth based on journal insights",
            ),
            model_name="gpt-4o-mini",
            max_loops=1,
            temperature=0.6,
            openai_api_key=self.api_key,
        )

    def _prepare_journal_context(
        self, insight_data: InsightData, include_content: bool = False
    ) -> str:
        """
        Prepare journal data context for analysis.

        Args:
            insight_data: InsightData containing journal entries
            include_content: Whether to include full content (privacy consideration)

        Returns:
            Formatted context string for AI analysis
        """
        helper = InsightsHelper(insight_data)
        metrics = helper.get_total_metrics()
        mood_breakdown = helper.get_mood_breakdown()
        top_tags = helper.get_top_tags(10)

        earliest_date = (
            metrics["date_range"]["earliest"][:10]
            if metrics["date_range"]["earliest"]
            else "N/A"
        )
        latest_date = (
            metrics["date_range"]["latest"][:10]
            if metrics["date_range"]["latest"]
            else "N/A"
        )

        context = f"""
JOURNAL ANALYSIS CONTEXT:

BASIC METRICS:
- Total Entries: {metrics['total_entries']}
- Current Streak: {metrics['current_streak']} days
- Date Range: {earliest_date} to {latest_date}
- Unique Moods: {metrics['unique_moods']}
- Unique Categories: {metrics['unique_categories']}
- Average Frequency (30 days): {metrics['average_frequency_30_days']:.1f} entries/day

MOOD DISTRIBUTION:
{json.dumps(mood_breakdown, indent=2)}

TOP TAGS:
{json.dumps([{'tag': tag, 'count': count} for tag, count in top_tags], indent=2)}

RECENT ENTRIES SUMMARY:
"""

        # Add recent entries (last 10 or all if fewer)
        recent_entries = sorted(
            insight_data.entries, key=lambda x: x.timestamp, reverse=True
        )[:10]

        for i, entry in enumerate(recent_entries, 1):
            if include_content:
                # For privacy, only include first 100 characters of content
                content_preview = (
                    entry.content[:100] + "..."
                    if len(entry.content) > 100
                    else entry.content
                )
                timestamp_str = entry.timestamp.strftime("%Y-%m-%d %H:%M")
                context += (
                    f"\nEntry {i}: [{timestamp_str}] Mood: {entry.mood}, Category: {entry.category}, "
                    f"Tags: {entry.tags}\nContent Preview: {content_preview}\n"
                )
            else:
                timestamp_str = entry.timestamp.strftime("%Y-%m-%d %H:%M")
                context += (
                    f"\nEntry {i}: [{timestamp_str}] Mood: {entry.mood}, Category: {entry.category}, "
                    f"Tags: {entry.tags}\n"
                )

        return context

    def analyze_mood_patterns(self, insight_data: InsightData) -> Dict[str, Any]:
        """
        Analyze mood patterns using the mood analysis agent.

        Args:
            insight_data: InsightData containing journal entries

        Returns:
            Dictionary containing mood analysis results
        """
        context = self._prepare_journal_context(insight_data)

        prompt = f"""
{context}

TASK: Analyze the mood patterns in this journal data. Focus on:
1. Mood distribution and trends
2. Emotional triggers and patterns
3. Mood consistency over time
4. Seasonal or temporal patterns
5. Correlation between moods and activities/categories

Provide your analysis in JSON format with the following structure:
{{
    "dominant_moods": ["list", "of", "top", "moods"],
    "mood_stability": "assessment of mood consistency",
    "emotional_triggers": ["identified", "triggers"],
    "temporal_patterns": "patterns related to time/season",
    "insights": ["key", "insights", "about", "emotional", "patterns"]
}}
"""

        try:
            response = self.mood_agent.run(prompt)
            # Try to parse JSON response, fallback to text analysis
            try:
                return json.loads(response)
            except json.JSONDecodeError:
                return {
                    "analysis_text": response,
                    "parsing_note": "Response could not be parsed as JSON",
                }
        except Exception as e:
            return {
                "error": f"Mood analysis failed: {str(e)}",
                "fallback_analysis": "Unable to perform AI mood analysis",
            }

    def identify_behavioral_patterns(self, insight_data: InsightData) -> Dict[str, Any]:
        """
        Identify behavioral patterns using the pattern recognition agent.

        Args:
            insight_data: InsightData containing journal entries

        Returns:
            Dictionary containing pattern analysis results
        """
        context = self._prepare_journal_context(insight_data)

        prompt = f"""
{context}

TASK: Identify behavioral and thematic patterns in this journal data. Focus on:
1. Writing frequency patterns (when, how often)
2. Recurring themes and topics
3. Category usage patterns
4. Tag patterns and evolution
5. Behavioral correlations

Provide your analysis in JSON format with the following structure:
{{
    "writing_patterns": "analysis of when and how often person writes",
    "recurring_themes": ["identified", "themes"],
    "category_insights": "insights about category usage",
    "tag_evolution": "how tag usage has evolved",
    "behavioral_correlations": ["correlations", "between", "behaviors"]
}}
"""

        try:
            response = self.pattern_agent.run(prompt)
            try:
                return json.loads(response)
            except json.JSONDecodeError:
                return {
                    "analysis_text": response,
                    "parsing_note": "Response could not be parsed as JSON",
                }
        except Exception as e:
            return {
                "error": f"Pattern analysis failed: {str(e)}",
                "fallback_analysis": "Unable to perform AI pattern analysis",
            }

    def generate_growth_insights(self, insight_data: InsightData) -> Dict[str, Any]:
        """
        Generate personal growth insights using the growth coach agent.

        Args:
            insight_data: InsightData containing journal entries

        Returns:
            Dictionary containing growth insights
        """
        context = self._prepare_journal_context(insight_data)

        prompt = f"""
{context}

TASK: Analyze this journal data for personal growth insights. Focus on:
1. Evidence of personal development and growth
2. Achievement patterns and progress
3. Areas for potential improvement
4. Strengths and positive patterns
5. Growth opportunities

Provide your analysis in JSON format with the following structure:
{{
    "growth_indicators": ["signs", "of", "personal", "growth"],
    "achievements": ["identified", "achievements"],
    "strengths": ["personal", "strengths", "observed"],
    "improvement_areas": ["areas", "for", "growth"],
    "growth_trajectory": "overall assessment of growth direction"
}}
"""

        try:
            response = self.growth_agent.run(prompt)
            try:
                return json.loads(response)
            except json.JSONDecodeError:
                return {
                    "analysis_text": response,
                    "parsing_note": "Response could not be parsed as JSON",
                }
        except Exception as e:
            return {
                "error": f"Growth analysis failed: {str(e)}",
                "fallback_analysis": "Unable to perform AI growth analysis",
            }

    def generate_recommendations(
        self, insight_data: InsightData, previous_analyses: Dict[str, Any]
    ) -> List[str]:
        """
        Generate personalized recommendations based on all analyses.

        Args:
            insight_data: InsightData containing journal entries
            previous_analyses: Results from other agent analyses

        Returns:
            List of personalized recommendations
        """
        context = self._prepare_journal_context(insight_data)

        prompt = f"""
{context}

PREVIOUS ANALYSES:
{json.dumps(previous_analyses, indent=2)}

TASK: Based on the journal data and previous analyses, generate specific, actionable recommendations for:
1. Improving emotional well-being
2. Enhancing personal growth
3. Optimizing journaling habits
4. Addressing identified patterns or concerns
5. Building on strengths

Provide 5-10 specific, actionable recommendations in JSON format:
{{
    "recommendations": [
        "Specific actionable recommendation 1",
        "Specific actionable recommendation 2",
        "..."
    ]
}}
"""

        try:
            response = self.recommendation_agent.run(prompt)
            try:
                result = json.loads(response)
                return result.get("recommendations", [])
            except json.JSONDecodeError:
                # Fallback: try to extract recommendations from text
                lines = response.split("\n")
                recommendations = []
                for line in lines:
                    line = line.strip()
                    if line and (
                        line.startswith("-")
                        or line.startswith("*")
                        or line.startswith("•")
                    ):
                        recommendations.append(line[1:].strip())
                return recommendations[:10]  # Limit to 10 recommendations
        except Exception as e:
            return [f"Unable to generate AI recommendations: {str(e)}"]

    def perform_comprehensive_analysis(
        self, insight_data: InsightData
    ) -> SwarmAnalysisResult:
        """
        Perform comprehensive analysis using all agents in the swarm.

        Args:
            insight_data: InsightData containing journal entries

        Returns:
            SwarmAnalysisResult containing all analysis results
        """
        # Run all analyses
        mood_analysis = self.analyze_mood_patterns(insight_data)
        pattern_insights = self.identify_behavioral_patterns(insight_data)
        growth_insights = self.generate_growth_insights(insight_data)

        # Combine analyses for recommendations
        combined_analyses = {
            "mood_analysis": mood_analysis,
            "pattern_insights": pattern_insights,
            "growth_insights": growth_insights,
        }

        recommendations = self.generate_recommendations(insight_data, combined_analyses)

        # Create comprehensive result
        return SwarmAnalysisResult(
            mood_analysis=mood_analysis,
            pattern_insights=pattern_insights,
            recommendations=recommendations,
            emotional_trends=mood_analysis,  # Alias for backwards compatibility
            personal_growth_insights=growth_insights,
            generated_at=datetime.now(UTC),
        )
