#!/usr/bin/env python3
"""
Personal AI Assistant Knowledge Base Demo

This comprehensive demo showcases all of Graphiti's capabilities through
a personal knowledge management system that tracks relationships, projects,
skills, goals, and life events over time.

Usage:
    python personal_assistant_demo.py [--database neo4j|falkordb] [--interactive]
"""

import argparse
import asyncio
import json
import logging
import os
import sys
from datetime import datetime, timezone
from typing import Dict, List, Optional

from dotenv import load_dotenv

# Add the parent directory to the path to import graphiti_core
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from graphiti_core import Graphiti
from graphiti_core.driver.neo4j_driver import Neo4jDriver
from graphiti_core.search.search_config_recipes import (
    NODE_HYBRID_SEARCH_RRF,
    EDGE_HYBRID_SEARCH_RRF
)

# Try to import FalkorDB driver, but don't fail if not available
try:
    from graphiti_core.driver.falkordb_driver import FalkorDriver
    FALKORDB_AVAILABLE = True
except ImportError:
    FALKORDB_AVAILABLE = False
    FalkorDriver = None

from sample_data import create_sample_episodes, create_sample_queries, create_interactive_scenarios, model_to_json
from visualization import GraphVisualizer, generate_quick_stats, create_ascii_chart


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)
logger = logging.getLogger(__name__)


class PersonalAssistantDemo:
    """Main demo class that orchestrates the personal assistant knowledge base."""
    
    def __init__(self, database_type: str = "neo4j"):
        """Initialize the demo with the specified database backend."""
        self.database_type = database_type
        self.graphiti: Optional[Graphiti] = None
        self.visualizer: Optional[GraphVisualizer] = None
        
    async def initialize(self) -> None:
        """Initialize the Graphiti instance and database connections."""
        logger.info(f"🚀 Initializing Personal Assistant Demo with {self.database_type}")
        
        if self.database_type == "neo4j":
            # Neo4j configuration
            uri = os.environ.get('NEO4J_URI', 'bolt://localhost:7687')
            user = os.environ.get('NEO4J_USER', 'neo4j')
            password = os.environ.get('NEO4J_PASSWORD', 'password')
            
            if not all([uri, user, password]):
                raise ValueError("NEO4J_URI, NEO4J_USER, and NEO4J_PASSWORD must be set")
            
            # Create Neo4j driver with custom database name
            driver = Neo4jDriver(uri=uri, user=user, password=password, database="personal_assistant")
            self.graphiti = Graphiti(graph_driver=driver)
            
        elif self.database_type == "falkordb":
            if not FALKORDB_AVAILABLE:
                raise ValueError("FalkorDB is not available. Install with: pip install graphiti-core[falkordb]")
            
            # FalkorDB configuration
            uri = os.environ.get('FALKORDB_URI', 'falkor://localhost:6379')
            host = "localhost"
            port = 6379
            
            # Parse URI to extract host and port
            if uri.startswith('falkor://'):
                parts = uri.replace('falkor://', '').split(':')
                if len(parts) >= 1:
                    host = parts[0]
                if len(parts) >= 2:
                    port = int(parts[1])
            
            # Create FalkorDB driver with custom database name
            driver = FalkorDriver(host=host, port=port, database="personal_assistant")
            self.graphiti = Graphiti(graph_driver=driver)
            
        else:
            raise ValueError(f"Unsupported database type: {database_type}")
        
        # Initialize indices and constraints
        logger.info("📚 Building database indices and constraints...")
        await self.graphiti.build_indices_and_constraints()
        
        # Initialize visualizer
        self.visualizer = GraphVisualizer(self.graphiti)
        
        logger.info("✅ Database initialization complete")
    
    async def load_sample_data(self) -> None:
        """Load the sample episodes that tell our personal story."""
        logger.info("📖 Loading sample personal data...")
        
        episodes = create_sample_episodes()
        total_episodes = len(episodes)
        
        for i, episode in enumerate(episodes, 1):
            logger.info(f"📝 Adding episode {i}/{total_episodes}: {episode['name']}")
            
            await self.graphiti.add_episode(
                name=episode['name'],
                episode_body=episode['content'] if isinstance(episode['content'], str) 
                           else episode['content'],  # Already JSON serialized by model_to_json
                source=episode['type'],
                source_description=episode['source_description'],
                reference_time=episode['reference_time'],
            )
        
        logger.info(f"✅ Successfully loaded {total_episodes} episodes")
    
    async def demonstrate_search_capabilities(self) -> None:
        """Demonstrate various search capabilities with sample queries."""
        logger.info("\n🔍 Demonstrating Search Capabilities")
        print("=" * 80)
        
        queries = create_sample_queries()
        
        # Demonstrate different search approaches
        search_types = [
            ("Basic Hybrid Search", self._basic_search),
            ("Node-Focused Search", self._node_search), 
            ("Graph-Aware Search", self._graph_aware_search),
        ]
        
        for search_name, search_func in search_types:
            print(f"\n🎯 {search_name}")
            print("-" * 50)
            
            # Use a subset of queries for each demo
            demo_queries = queries[:3] if search_name == "Basic Hybrid Search" else queries[3:6] if search_name == "Node-Focused Search" else queries[6:9]
            
            for query in demo_queries:
                print(f"\nQuery: '{query}'")
                await search_func(query)
    
    async def _basic_search(self, query: str) -> None:
        """Perform basic hybrid search (edges)."""
        try:
            results = await self.graphiti.search(query, limit=3)
            
            if results:
                for i, result in enumerate(results, 1):
                    print(f"  {i}. {result.fact}")
                    if hasattr(result, 'valid_at') and result.valid_at:
                        print(f"     📅 Valid from: {result.valid_at}")
            else:
                print("  No results found")
        except Exception as e:
            print(f"  ❌ Search error: {e}")
            logger.error(f"Basic search error for query '{query}': {e}")
    
    async def _node_search(self, query: str) -> None:
        """Perform node-focused search."""
        try:
            config = NODE_HYBRID_SEARCH_RRF.model_copy(deep=True)
            config.limit = 3
            
            results = await self.graphiti._search(query=query, config=config)
            
            if results.nodes:
                for i, node in enumerate(results.nodes, 1):
                    print(f"  {i}. {node.name}")
                    summary = node.summary[:100] if node.summary else "No summary available"
                    print(f"     📝 {summary}...")
                    print(f"     🏷️  Labels: {', '.join(node.labels)}")
            else:
                print("  No nodes found")
        except Exception as e:
            print(f"  ❌ Node search error: {e}")
            logger.error(f"Node search error for query '{query}': {e}")
    
    async def _graph_aware_search(self, query: str) -> None:
        """Perform graph-aware search with center node."""
        try:
            # First get initial results
            initial_results = await self.graphiti.search(query, limit=5)
            
            if initial_results and len(initial_results) > 0:
                # Use the first result's source node as center
                center_node_uuid = initial_results[0].source_node_uuid
                
                # Rerank based on graph distance
                reranked_results = await self.graphiti.search(
                    query, 
                    center_node_uuid=center_node_uuid, 
                    limit=3
                )
                
                print(f"  🎯 Center node: {center_node_uuid}")
                for i, result in enumerate(reranked_results, 1):
                    print(f"  {i}. {result.fact}")
            else:
                print("  No results to rerank")
        except Exception as e:
            print(f"  ❌ Graph-aware search error: {e}")
            logger.error(f"Graph-aware search error for query '{query}': {e}")
    
    async def demonstrate_scenarios(self) -> None:
        """Demonstrate predefined exploration scenarios."""
        logger.info("\n🎭 Demonstrating Life Scenarios")
        print("=" * 80)
        
        scenarios = create_interactive_scenarios()
        
        for scenario in scenarios:
            print(f"\n📚 Scenario: {scenario['name']}")
            print(f"📖 {scenario['description']}")
            print("-" * 50)
            
            for query in scenario['queries']:
                print(f"\nQuery: '{query}'")
                await self._basic_search(query)
    
    async def demonstrate_visualization_features(self) -> None:
        """Demonstrate visualization and summary features."""
        logger.info("\n📊 Demonstrating Visualization Features")
        print("=" * 80)
        
        try:
            # Generate comprehensive summary report
            print("\n🎯 Comprehensive Summary Report:")
            summary_report = await self.visualizer.generate_summary_report()
            print(summary_report)
            
            # Generate personal timeline
            print("\n📅 Personal Timeline:")
            timeline = await self.visualizer.generate_personal_timeline()
            print(timeline)
            
            # Quick statistics
            print("\n📊 Quick Statistics:")
            quick_stats = await generate_quick_stats(self.graphiti)
            print(quick_stats)
            
        except Exception as e:
            logger.error(f"Error in visualization demonstration: {e}")
            print(f"❌ Visualization error: {e}")
    
    async def demonstrate_error_recovery(self) -> None:
        """Demonstrate error handling and recovery."""
        logger.info("\n🛡️  Demonstrating Error Handling")
        print("=" * 80)
        
        # Test with invalid queries
        test_queries = [
            "",  # Empty query
            "🚀" * 1000,  # Very long query
            "nonexistent_entity_xyz_123",  # Likely to return no results
        ]
        
        for i, query in enumerate(test_queries, 1):
            print(f"\n🧪 Test {i}: Error handling for problematic query")
            try:
                display_query = query[:50] + "..." if len(query) > 50 else query
                print(f"Query: '{display_query}'")
                
                results = await self.graphiti.search(query, limit=3)
                if results:
                    print(f"✅ Handled gracefully: {len(results)} results")
                else:
                    print("✅ Handled gracefully: No results found")
                    
            except Exception as e:
                print(f"⚠️  Caught error: {type(e).__name__}: {e}")
                print("✅ Error handled and system remains stable")
    
    async def interactive_mode(self) -> None:
        """Interactive mode for exploring the knowledge base."""
        logger.info("\n🎮 Entering Interactive Mode")
        print("=" * 80)
        print("Welcome to Interactive Exploration!")
        print("You can ask questions about the personal knowledge base.")
        print("Type 'help' for commands, 'scenarios' for predefined scenarios, or 'quit' to exit.")
        print("-" * 80)
        
        while True:
            try:
                user_input = input("\n💭 Your query: ").strip()
                
                if user_input.lower() in ['quit', 'exit', 'q']:
                    print("👋 Goodbye!")
                    break
                
                elif user_input.lower() == 'help':
                    await self._show_help()
                
                elif user_input.lower() == 'scenarios':
                    await self._show_scenarios()
                
                elif user_input.lower() == 'stats':
                    await self.demonstrate_visualization_features()
                
                elif user_input.lower() == 'summary':
                    print("\n📊 Generating comprehensive summary...")
                    summary = await self.visualizer.generate_summary_report()
                    print(summary)
                
                elif user_input.lower() == 'timeline':
                    print("\n📅 Generating personal timeline...")
                    timeline = await self.visualizer.generate_personal_timeline()
                    print(timeline)
                
                elif user_input.lower().startswith('add '):
                    await self._add_episode_interactive(user_input[4:])
                
                elif user_input.lower().startswith('visualize '):
                    entity_name = user_input[10:].strip()
                    if entity_name:
                        print(f"\n🔍 Visualizing connections for: {entity_name}")
                        visualization = await self.visualizer.visualize_entity_connections(entity_name)
                        print(visualization)
                    else:
                        print("❌ Please specify an entity name after 'visualize'")
                
                elif user_input.lower().startswith('search '):
                    query = user_input[7:].strip()
                    if query:
                        await self._enhanced_search(query)
                    else:
                        print("❌ Please specify a search query after 'search'")
                
                elif user_input:
                    await self._enhanced_search(user_input)
                
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
                logger.error(f"Interactive mode error: {e}")
    
    async def _enhanced_search(self, query: str) -> None:
        """Enhanced search with multiple result types."""
        print(f"\n🔍 Searching for: '{query}'")
        print("-" * 40)
        
        try:
            # Perform multiple search types
            print("🎯 Relationship Search:")
            await self._basic_search(query)
            
            print("\n🏷️  Entity Search:")
            await self._node_search(query)
            
            # Show entity connections if it looks like an entity name
            if len(query.split()) <= 3 and not any(word in query.lower() for word in ['what', 'how', 'when', 'where', 'who', 'why']):
                print("\n🔗 Connection Visualization:")
                visualization = await self.visualizer.visualize_entity_connections(query)
                # Show just a summary of connections
                lines = visualization.split('\n')
                for line in lines[:15]:  # Show first 15 lines
                    print(line)
                if len(lines) > 15:
                    print("  ... (use 'visualize <entity>' for full visualization)")
        
        except Exception as e:
            print(f"❌ Search error: {e}")
            logger.error(f"Enhanced search error: {e}")
    
    async def _show_help(self) -> None:
        """Show help information."""
        print("""
🆘 Available Commands:
  help        - Show this help message
  scenarios   - Show predefined exploration scenarios
  stats       - Show comprehensive statistics and visualizations
  summary     - Generate knowledge graph summary report
  timeline    - Show personal timeline of events
  add <text>  - Add a new episode to the knowledge base
  visualize <entity> - Visualize connections for a specific entity
  search <query>     - Enhanced search with multiple result types
  quit/exit/q - Exit interactive mode

💡 Query Examples:
  - "Who are my colleagues?"
  - "What projects have I worked on?"
  - "What skills am I learning?"
  - "What goals have I achieved?"
  - "Who can help me with machine learning?"
  - "What events did I attend last year?"
  - "visualize Sarah Chen"
  - "search Python projects"
        """)
    
    async def _show_scenarios(self) -> None:
        """Show available scenarios."""
        scenarios = create_interactive_scenarios()
        print("\n🎭 Available Scenarios:")
        
        for i, scenario in enumerate(scenarios, 1):
            print(f"\n{i}. {scenario['name']}")
            print(f"   📖 {scenario['description']}")
            print("   🔍 Sample queries:")
            for query in scenario['queries']:
                print(f"     • {query}")
    
    async def _add_episode_interactive(self, content: str) -> None:
        """Add a new episode interactively."""
        try:
            episode_name = f"Interactive input {datetime.now().strftime('%Y-%m-%d %H:%M')}"
            
            await self.graphiti.add_episode(
                name=episode_name,
                episode_body=content,
                source="text",
                source_description="interactive user input",
                reference_time=datetime.now(timezone.utc),
            )
            
            print(f"✅ Added new episode: '{episode_name}'")
            print(f"📝 Content: {content}")
            
        except Exception as e:
            print(f"❌ Error adding episode: {e}")
    
    async def run_demo(self, interactive: bool = False) -> None:
        """Run the complete demo."""
        try:
            # Initialize
            await self.initialize()
            
            # Load sample data
            await self.load_sample_data()
            
            # Show visualization features
            await self.demonstrate_visualization_features()
            
            # Demonstrate search capabilities
            await self.demonstrate_search_capabilities()
            
            # Demonstrate scenarios
            await self.demonstrate_scenarios()
            
            # Demonstrate error handling
            await self.demonstrate_error_recovery()
            
            # Interactive mode if requested
            if interactive:
                await self.interactive_mode()
            else:
                logger.info("\n🎉 Demo completed! Run with --interactive to explore further.")
                print("\n" + "=" * 80)
                print("🎉 Personal Assistant Demo Complete!")
                print("💡 Run with --interactive flag to explore the knowledge base yourself")
                print("📚 Check the README.md for more information about the features demonstrated")
                print("🔗 Available database backends: Neo4j (default), FalkorDB")
        
        except Exception as e:
            logger.error(f"Demo execution error: {e}")
            print(f"❌ Demo error: {e}")
            print("📋 Check the logs for more details")
        
        finally:
            if self.graphiti:
                await self.graphiti.close()
                logger.info("🔌 Database connection closed")


async def main():
    """Main entry point for the demo."""
    parser = argparse.ArgumentParser(description="Personal AI Assistant Knowledge Base Demo")
    parser.add_argument(
        '--database', 
        choices=['neo4j', 'falkordb'], 
        default='neo4j',
        help='Database backend to use (default: neo4j)'
    )
    parser.add_argument(
        '--interactive', 
        action='store_true',
        help='Run in interactive mode for exploration'
    )
    
    args = parser.parse_args()
    
    # Load environment variables
    load_dotenv()
    
    # Check for OpenAI API key
    if not os.environ.get('OPENAI_API_KEY'):
        print("❌ Error: OPENAI_API_KEY environment variable is required")
        print("Please set your OpenAI API key:")
        print("export OPENAI_API_KEY=your_api_key_here")
        sys.exit(1)
    
    # Run the demo
    demo = PersonalAssistantDemo(args.database)
    await demo.run_demo(args.interactive)


if __name__ == "__main__":
    asyncio.run(main())