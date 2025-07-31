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
from graphiti_core.driver.falkordb_driver import FalkorDriver
from graphiti_core.search.search_config_recipes import (
    NODE_HYBRID_SEARCH_RRF,
    EDGE_HYBRID_SEARCH_RRF
)

from sample_data import create_sample_episodes, create_sample_queries, create_interactive_scenarios, model_to_json


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
        results = await self.graphiti.search(query, limit=3)
        
        if results:
            for i, result in enumerate(results, 1):
                print(f"  {i}. {result.fact}")
                if hasattr(result, 'valid_at') and result.valid_at:
                    print(f"     📅 Valid from: {result.valid_at}")
        else:
            print("  No results found")
    
    async def _node_search(self, query: str) -> None:
        """Perform node-focused search."""
        config = NODE_HYBRID_SEARCH_RRF.model_copy(deep=True)
        config.limit = 3
        
        results = await self.graphiti._search(query=query, config=config)
        
        if results.nodes:
            for i, node in enumerate(results.nodes, 1):
                print(f"  {i}. {node.name}")
                print(f"     📝 {node.summary[:100]}...")
                print(f"     🏷️  Labels: {', '.join(node.labels)}")
        else:
            print("  No nodes found")
    
    async def _graph_aware_search(self, query: str) -> None:
        """Perform graph-aware search with center node."""
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
    
    async def show_graph_statistics(self) -> None:
        """Display statistics about the knowledge graph."""
        logger.info("\n📊 Graph Statistics")
        print("=" * 80)
        
        # Search for different entity types to show graph diversity
        entity_searches = [
            ("People", "person colleague friend mentor"),
            ("Projects", "project work software development"),
            ("Skills", "skill learning programming"),
            ("Events", "event achievement milestone"),
            ("Goals", "goal target objective")
        ]
        
        print("\n🏗️  Knowledge Graph Overview:")
        for entity_type, search_term in entity_searches:
            config = NODE_HYBRID_SEARCH_RRF.model_copy(deep=True)
            config.limit = 10
            
            results = await self.graphiti._search(query=search_term, config=config)
            node_count = len(results.nodes) if results.nodes else 0
            print(f"  📊 {entity_type}: {node_count} entities found")
    
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
                    await self.show_graph_statistics()
                
                elif user_input.lower().startswith('add '):
                    await self._add_episode_interactive(user_input[4:])
                
                elif user_input:
                    print(f"\n🔍 Searching for: '{user_input}'")
                    print("-" * 40)
                    
                    # Perform multiple search types
                    print("🎯 Relationship Search:")
                    await self._basic_search(user_input)
                    
                    print("\n🏷️  Entity Search:")
                    await self._node_search(user_input)
                
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
    
    async def _show_help(self) -> None:
        """Show help information."""
        print("""
🆘 Available Commands:
  help        - Show this help message
  scenarios   - Show predefined exploration scenarios
  stats       - Show knowledge graph statistics
  add <text>  - Add a new episode to the knowledge base
  quit/exit/q - Exit interactive mode

💡 Query Examples:
  - "Who are my colleagues?"
  - "What projects have I worked on?"
  - "What skills am I learning?"
  - "What goals have I achieved?"
  - "Who can help me with machine learning?"
  - "What events did I attend last year?"
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
            
            # Show graph statistics
            await self.show_graph_statistics()
            
            # Demonstrate search capabilities
            await self.demonstrate_search_capabilities()
            
            # Demonstrate scenarios
            await self.demonstrate_scenarios()
            
            # Interactive mode if requested
            if interactive:
                await self.interactive_mode()
            else:
                logger.info("\n🎉 Demo completed! Run with --interactive to explore further.")
                print("\n" + "=" * 80)
                print("🎉 Personal Assistant Demo Complete!")
                print("💡 Run with --interactive flag to explore the knowledge base yourself")
                print("📚 Check the README.md for more information about the features demonstrated")
        
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