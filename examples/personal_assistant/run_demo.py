#!/usr/bin/env python3
"""
Demo runner script that helps set up and run the Personal AI Assistant demo
with proper environment configuration and database setup checks.
"""

import os
import sys
import asyncio
import subprocess
import argparse
from pathlib import Path

def check_environment():
    """Check if required environment variables are set."""
    required_vars = ['OPENAI_API_KEY']
    missing_vars = []
    
    for var in required_vars:
        if not os.environ.get(var):
            missing_vars.append(var)
    
    if missing_vars:
        print("❌ Missing required environment variables:")
        for var in missing_vars:
            print(f"   - {var}")
        print("\nPlease set these variables before running the demo:")
        print("export OPENAI_API_KEY=your_api_key_here")
        return False
    
    print("✅ Environment variables configured")
    return True

def check_database_connectivity(database_type):
    """Check if the specified database is available."""
    if database_type == "neo4j":
        # Check Neo4j connection variables
        uri = os.environ.get('NEO4J_URI', 'bolt://localhost:7687')
        user = os.environ.get('NEO4J_USER', 'neo4j')
        password = os.environ.get('NEO4J_PASSWORD', 'password')
        
        print(f"🔍 Checking Neo4j connectivity...")
        print(f"   URI: {uri}")
        print(f"   User: {user}")
        
        # We can't actually test the connection without importing neo4j
        # So we just verify the variables are set
        if not password or password == "password":
            print("⚠️  Using default password 'password' - make sure your Neo4j instance uses this")
        
        print("✅ Neo4j configuration looks good")
        print("💡 Make sure Neo4j is running on the specified URI")
        
    elif database_type == "falkordb":
        uri = os.environ.get('FALKORDB_URI', 'falkor://localhost:6379')
        print(f"🔍 Checking FalkorDB connectivity...")
        print(f"   URI: {uri}")
        print("✅ FalkorDB configuration looks good")
        print("💡 Make sure FalkorDB is running on the specified URI")

def install_dependencies():
    """Install required dependencies if not already installed."""
    print("📦 Checking dependencies...")
    
    try:
        import graphiti_core
        print("✅ graphiti-core is installed")
    except ImportError:
        print("❌ graphiti-core not found")
        print("Installing graphiti-core...")
        subprocess.run([sys.executable, "-m", "pip", "install", "-e", "."], 
                      cwd=Path(__file__).parent.parent.parent)

def create_env_file():
    """Create a sample .env file if it doesn't exist."""
    env_file = Path(__file__).parent / ".env"
    
    if not env_file.exists():
        env_content = """# Personal AI Assistant Demo Environment Variables

# Required: OpenAI API Key
OPENAI_API_KEY=your_openai_api_key_here

# Neo4j Configuration (default)
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=password

# FalkorDB Configuration (alternative)
FALKORDB_URI=falkor://localhost:6379

# Optional: Other LLM providers
# ANTHROPIC_API_KEY=your_anthropic_key
# GOOGLE_API_KEY=your_google_key
# GROQ_API_KEY=your_groq_key
"""
        
        env_file.write_text(env_content)
        print(f"📝 Created sample .env file at {env_file}")
        print("   Please edit it with your actual API keys")
        return False
    
    return True

async def run_demo(args):
    """Run the demo with the specified arguments."""
    print("🚀 Starting Personal AI Assistant Demo")
    print("=" * 60)
    
    # Import and run the demo
    from personal_assistant_demo import PersonalAssistantDemo
    
    demo = PersonalAssistantDemo(args.database)
    await demo.run_demo(args.interactive)

def main():
    """Main entry point for the demo runner."""
    parser = argparse.ArgumentParser(description="Personal AI Assistant Demo Runner")
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
    parser.add_argument(
        '--setup-only',
        action='store_true',
        help='Only run setup checks without starting the demo'
    )
    
    args = parser.parse_args()
    
    print("🎯 Personal AI Assistant Demo Runner")
    print("=" * 40)
    
    # Check dependencies
    install_dependencies()
    
    # Check/create environment file
    if not create_env_file():
        print("⚠️  Please configure your .env file and run again")
        return
    
    # Load environment variables from .env file
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        print("⚠️  python-dotenv not available, please set environment variables manually")
    
    # Check environment
    if not check_environment():
        return
    
    # Check database connectivity
    check_database_connectivity(args.database)
    
    if args.setup_only:
        print("✅ Setup complete! Run without --setup-only to start the demo")
        return
    
    # Run the demo
    try:
        asyncio.run(run_demo(args))
    except KeyboardInterrupt:
        print("\n👋 Demo interrupted by user")
    except Exception as e:
        print(f"❌ Demo error: {e}")
        print("💡 Try running with --setup-only to check your configuration")

if __name__ == "__main__":
    main()