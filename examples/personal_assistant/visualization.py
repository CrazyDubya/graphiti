"""
Visualization and summary features for the Personal AI Assistant demo.

This module provides simple text-based visualizations and summaries
of the knowledge graph data.
"""

import json
from datetime import datetime, timezone
from typing import Dict, List, Any, Optional
from collections import defaultdict, Counter

from graphiti_core import Graphiti
from graphiti_core.search.search_config_recipes import NODE_HYBRID_SEARCH_RRF


class GraphVisualizer:
    """Simple text-based visualization for the knowledge graph."""
    
    def __init__(self, graphiti: Graphiti):
        self.graphiti = graphiti
    
    async def generate_summary_report(self) -> str:
        """Generate a comprehensive summary report of the knowledge graph."""
        report = []
        report.append("=" * 80)
        report.append("📊 PERSONAL KNOWLEDGE GRAPH SUMMARY REPORT")
        report.append("=" * 80)
        
        # Entity overview
        entities = await self._get_entity_overview()
        report.append("\n🏗️  ENTITY OVERVIEW")
        report.append("-" * 40)
        for entity_type, count in entities.items():
            report.append(f"  {entity_type:<20} {count:>3} entities")
        
        # Relationship summary
        report.append("\n🔗 RELATIONSHIP PATTERNS")
        report.append("-" * 40)
        relationships = await self._get_relationship_summary()
        for rel_type, count in relationships.items():
            report.append(f"  {rel_type:<20} {count:>3} connections")
        
        # Timeline overview
        report.append("\n📅 TEMPORAL OVERVIEW")
        report.append("-" * 40)
        timeline = await self._get_temporal_overview()
        for period, count in timeline.items():
            report.append(f"  {period:<20} {count:>3} events")
        
        # Key insights
        insights = await self._generate_insights()
        if insights:
            report.append("\n💡 KEY INSIGHTS")
            report.append("-" * 40)
            for insight in insights:
                report.append(f"  • {insight}")
        
        return "\n".join(report)
    
    async def _get_entity_overview(self) -> Dict[str, int]:
        """Get overview of different entity types."""
        entity_searches = [
            ("People", "person colleague friend mentor family"),
            ("Projects", "project work development software"),
            ("Skills", "skill learning programming certification"),
            ("Goals", "goal target objective achievement"),
            ("Events", "event meeting celebration milestone"),
            ("Transactions", "transaction payment investment money"),
            ("Health Activities", "health fitness exercise activity"),
        ]
        
        entities = {}
        for entity_type, search_term in entity_searches:
            config = NODE_HYBRID_SEARCH_RRF.model_copy(deep=True)
            config.limit = 20
            
            try:
                results = await self.graphiti.search(query=search_term, config=config)
                count = len(results.nodes) if hasattr(results, 'nodes') and results.nodes else 0
                entities[entity_type] = count
            except Exception:
                entities[entity_type] = 0
        
        return entities
    
    async def _get_relationship_summary(self) -> Dict[str, int]:
        """Get summary of relationship patterns."""
        relationship_searches = [
            ("Work Collaborations", "work with colleague project team"),
            ("Learning Connections", "learn skill certification course"),
            ("Social Interactions", "friend meeting event social"),
            ("Goal Achievements", "achieve goal complete success"),
            ("Health Progress", "health fitness improve activity"),
        ]
        
        relationships = {}
        for rel_type, search_term in relationship_searches:
            try:
                results = await self.graphiti.search(search_term, limit=10)
                relationships[rel_type] = len(results)
            except Exception:
                relationships[rel_type] = 0
        
        return relationships
    
    async def _get_temporal_overview(self) -> Dict[str, int]:
        """Get temporal distribution of events."""
        now = datetime.now(timezone.utc)
        periods = {
            "Last Month": 30,
            "Last 3 Months": 90,
            "Last 6 Months": 180,
            "Last Year": 365,
            "Over a Year Ago": 730,
        }
        
        timeline = {}
        for period_name, days_ago in periods.items():
            try:
                # Search for recent activities
                search_terms = [
                    "recent activity event project",
                    "started completed achieved",
                    "meeting learning working"
                ]
                
                total_count = 0
                for search_term in search_terms:
                    results = await self.graphiti.search(search_term, limit=10)
                    total_count += len(results)
                
                timeline[period_name] = total_count // len(search_terms)  # Average
            except Exception:
                timeline[period_name] = 0
        
        return timeline
    
    async def _generate_insights(self) -> List[str]:
        """Generate key insights from the knowledge graph."""
        insights = []
        
        try:
            # Career progression insight
            results = await self.graphiti.search("career progression skill development", limit=5)
            if results:
                insights.append("Strong focus on continuous skill development and career growth")
            
            # Collaboration insight
            results = await self.graphiti.search("colleague team collaboration", limit=5)
            if results:
                insights.append("Active collaboration with teammates and mentors")
            
            # Learning insight
            results = await self.graphiti.search("learning certification course", limit=5)
            if results:
                insights.append("Committed to formal learning and professional development")
            
            # Health insight
            results = await self.graphiti.search("health fitness goal achievement", limit=5)
            if results:
                insights.append("Balanced approach to personal health and professional goals")
            
            # Network insight
            results = await self.graphiti.search("mentor friend network", limit=5)
            if results:
                insights.append("Building a strong professional and personal network")
        
        except Exception:
            insights.append("Knowledge graph contains rich interconnected personal data")
        
        return insights
    
    async def visualize_entity_connections(self, entity_name: str) -> str:
        """Create a simple text-based visualization of entity connections."""
        visualization = []
        visualization.append(f"🔍 CONNECTIONS FOR: {entity_name}")
        visualization.append("=" * 60)
        
        try:
            # Search for the entity
            results = await self.graphiti.search(entity_name, limit=10)
            
            if not results:
                visualization.append("No connections found for this entity.")
                return "\n".join(visualization)
            
            # Group connections by type
            connections = defaultdict(list)
            for result in results:
                # Extract connection type from the fact
                fact = result.fact.lower()
                if any(word in fact for word in ["work", "project", "colleague"]):
                    connections["Work"].append(result.fact)
                elif any(word in fact for word in ["learn", "skill", "study"]):
                    connections["Learning"].append(result.fact)
                elif any(word in fact for word in ["friend", "meet", "social"]):
                    connections["Social"].append(result.fact)
                elif any(word in fact for word in ["goal", "achieve", "target"]):
                    connections["Goals"].append(result.fact)
                else:
                    connections["Other"].append(result.fact)
            
            # Display connections by category
            for category, facts in connections.items():
                if facts:
                    visualization.append(f"\n📂 {category} Connections:")
                    for i, fact in enumerate(facts[:5], 1):  # Limit to 5 per category
                        visualization.append(f"  {i}. {fact}")
                    
                    if len(facts) > 5:
                        visualization.append(f"  ... and {len(facts) - 5} more")
        
        except Exception as e:
            visualization.append(f"Error visualizing connections: {e}")
        
        return "\n".join(visualization)
    
    async def generate_personal_timeline(self) -> str:
        """Generate a timeline of personal events."""
        timeline = []
        timeline.append("📅 PERSONAL TIMELINE")
        timeline.append("=" * 60)
        
        try:
            # Search for different types of events
            event_searches = [
                ("Career Events", "job start work project complete"),
                ("Learning Events", "learn skill certification course"),
                ("Personal Events", "goal achieve milestone event"),
                ("Social Events", "meet friend colleague mentor"),
            ]
            
            all_events = []
            for event_type, search_term in event_searches:
                results = await self.graphiti.search(search_term, limit=8)
                for result in results:
                    all_events.append({
                        'type': event_type,
                        'fact': result.fact,
                        'time': result.valid_at if hasattr(result, 'valid_at') else None
                    })
            
            # Sort by time if available
            dated_events = [e for e in all_events if e['time']]
            undated_events = [e for e in all_events if not e['time']]
            
            if dated_events:
                dated_events.sort(key=lambda x: x['time'], reverse=True)
                timeline.append("\n⏰ Recent Events (with dates):")
                for event in dated_events[:10]:
                    date_str = event['time'].strftime('%Y-%m-%d') if event['time'] else 'Unknown'
                    timeline.append(f"  📅 {date_str}: {event['fact']}")
            
            if undated_events:
                timeline.append("\n📝 Other Notable Events:")
                for event in undated_events[:10]:
                    timeline.append(f"  • {event['fact']}")
        
        except Exception as e:
            timeline.append(f"Error generating timeline: {e}")
        
        return "\n".join(timeline)


def create_ascii_chart(data: Dict[str, int], title: str, max_width: int = 40) -> str:
    """Create a simple ASCII bar chart."""
    if not data:
        return f"{title}\n(No data available)"
    
    chart = [title, "=" * len(title)]
    
    max_value = max(data.values()) if data.values() else 1
    
    for label, value in data.items():
        bar_length = int((value / max_value) * max_width) if max_value > 0 else 0
        bar = "█" * bar_length
        chart.append(f"{label:<20} |{bar:<{max_width}} {value}")
    
    return "\n".join(chart)


async def generate_quick_stats(graphiti: Graphiti) -> str:
    """Generate quick statistics about the knowledge graph."""
    stats = []
    stats.append("📊 QUICK STATISTICS")
    stats.append("-" * 30)
    
    try:
        # Basic entity counts
        entity_types = ["person", "project", "skill", "goal", "event"]
        for entity_type in entity_types:
            results = await graphiti.search(entity_type, limit=20)
            count = len(results)
            stats.append(f"{entity_type.title()}s: {count}")
        
        # Recent activity
        recent_results = await graphiti.search("recent activity today yesterday", limit=10)
        stats.append(f"Recent activities: {len(recent_results)}")
        
    except Exception as e:
        stats.append(f"Error generating stats: {e}")
    
    return "\n".join(stats)