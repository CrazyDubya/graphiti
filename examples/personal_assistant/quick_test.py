#!/usr/bin/env python3
"""
Quick test script for the Personal AI Assistant demo.
This script runs basic functionality tests without requiring a full database setup.
"""

import asyncio
import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

async def test_basic_functionality():
    """Test basic functionality without database connection."""
    print("🧪 Testing Personal AI Assistant Demo Components")
    print("=" * 60)
    
    # Test imports
    print("📦 Testing imports...")
    try:
        import models
        from models import Person, Project, Skill, Event, Transaction
        from sample_data import create_sample_episodes, create_sample_queries
        from visualization import GraphVisualizer, generate_quick_stats
        print("✅ All imports successful")
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    
    # Test model creation
    print("\n🏗️  Testing model creation...")
    try:
        person = Person(
            name="Test Person",
            occupation="Software Engineer",
            skills=["Python", "JavaScript"],
            interests=["AI", "Music"]
        )
        
        project = Project(
            name="Test Project",
            description="A sample project for testing",
            status="active"
        )
        
        skill = Skill(
            name="Python",
            category="Programming",
            level="intermediate"
        )
        
        print(f"✅ Created Person: {person.name}")
        print(f"✅ Created Project: {project.name}")
        print(f"✅ Created Skill: {skill.name}")
    except Exception as e:
        print(f"❌ Model creation error: {e}")
        return False
    
    # Test sample data generation
    print("\n📊 Testing sample data generation...")
    try:
        episodes = create_sample_episodes()
        queries = create_sample_queries()
        print(f"✅ Generated {len(episodes)} sample episodes")
        print(f"✅ Generated {len(queries)} sample queries")
        
        # Show a sample episode
        if episodes:
            sample = episodes[0]
            print(f"   Sample episode: {sample['name']}")
    except Exception as e:
        print(f"❌ Sample data generation error: {e}")
        return False
    
    # Test JSON serialization
    print("\n🔄 Testing JSON serialization...")
    try:
        from sample_data import model_to_json
        person_json = model_to_json(person)
        print("✅ JSON serialization successful")
        print(f"   Sample JSON length: {len(person_json)} characters")
    except Exception as e:
        print(f"❌ JSON serialization error: {e}")
        return False
    
    print("\n🎉 All basic tests passed!")
    print("💡 To run the full demo with database:")
    print("   python run_demo.py --interactive")
    
    return True

def test_demo_files():
    """Test that all required demo files exist."""
    print("\n📁 Testing demo file structure...")
    
    required_files = [
        "models.py",
        "sample_data.py", 
        "personal_assistant_demo.py",
        "visualization.py",
        "run_demo.py",
        "test_imports.py",
        "requirements.txt",
        "README.md",
        ".env.example"
    ]
    
    missing_files = []
    for file in required_files:
        if not Path(file).exists():
            missing_files.append(file)
        else:
            print(f"✅ Found {file}")
    
    if missing_files:
        print(f"❌ Missing files: {missing_files}")
        return False
    
    print("✅ All required files present")
    return True

async def main():
    """Run all tests."""
    print("🚀 Personal AI Assistant Demo - Quick Test Suite")
    print("=" * 60)
    
    # Test file structure
    if not test_demo_files():
        sys.exit(1)
    
    # Test basic functionality
    if not await test_basic_functionality():
        sys.exit(1)
    
    print("\n" + "=" * 60)
    print("🎉 Quick test suite completed successfully!")
    print("📚 Demo is ready for use")

if __name__ == "__main__":
    asyncio.run(main())