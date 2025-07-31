#!/usr/bin/env python3
"""Simple test to verify imports work correctly."""

import sys
import os

# Add the parent directory to the path to import graphiti_core
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

# Test local imports
try:
    import models
    import sample_data
    from models import Person, Project, Skill, Event, Transaction
    from sample_data import create_sample_episodes, create_sample_queries
    print("✅ Local imports successful")
except ImportError as e:
    print(f"❌ Local import error: {e}")
    sys.exit(1)

# Test graphiti imports
try:
    from graphiti_core import Graphiti
    from graphiti_core.nodes import EpisodeType
    print("✅ Graphiti imports successful")
except ImportError as e:
    print(f"❌ Graphiti import error: {e}")
    sys.exit(1)

# Test sample data generation
try:
    episodes = create_sample_episodes()
    queries = create_sample_queries()
    print(f"✅ Generated {len(episodes)} sample episodes")
    print(f"✅ Generated {len(queries)} sample queries")
except Exception as e:
    print(f"❌ Sample data generation error: {e}")
    sys.exit(1)

# Test model creation
try:
    person = Person(
        name="Test Person",
        occupation="Software Engineer",
        skills=["Python", "JavaScript"]
    )
    print(f"✅ Created person model: {person.name}")
except Exception as e:
    print(f"❌ Model creation error: {e}")
    sys.exit(1)

print("\n🎉 All tests passed! Demo should work correctly.")