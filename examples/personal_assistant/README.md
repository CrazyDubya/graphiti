# Personal AI Assistant Knowledge Base Demo

This demo showcases the full functionality of Graphiti through a comprehensive Personal AI Assistant Knowledge Base that tracks various aspects of a person's life over time.

## Features Demonstrated

### Core Graphiti Features
- **Real-time incremental updates**: Add information as it happens
- **Bi-temporal data model**: Track when events occurred vs when they were recorded
- **Hybrid retrieval**: Semantic search + keyword search (BM25) + graph traversal
- **Custom entity definitions**: Person, Project, Skill, Transaction, Event entities
- **Graph relationships**: Discover connections between different life aspects
- **Multiple database backends**: Works with both Neo4j and FalkorDB

### Life Tracking Categories
- **Personal Relationships**: Family, friends, colleagues, interactions
- **Work & Projects**: Job history, projects, achievements, collaborations
- **Learning & Skills**: Courses, certifications, skill development
- **Health & Fitness**: Activities, goals, progress tracking
- **Financial**: Transactions, investments, financial goals
- **Events & Memories**: Important life events, travel, experiences

## Prerequisites

- Python 3.10+
- OpenAI API key (set as `OPENAI_API_KEY` environment variable)
- **Neo4j**: Neo4j Desktop with a local database running, OR
- **FalkorDB**: FalkorDB server running

## Setup

1. Install dependencies:
```bash
pip install graphiti-core[dev]
```

2. Set environment variables:
```bash
export OPENAI_API_KEY=your_openai_api_key

# For Neo4j (default)
export NEO4J_URI=bolt://localhost:7687
export NEO4J_USER=neo4j
export NEO4J_PASSWORD=password

# OR for FalkorDB
export FALKORDB_URI=falkor://localhost:6379
```

3. Run the demo:
```bash
# Interactive demo with sample data
python personal_assistant_demo.py

# Or run with FalkorDB
python personal_assistant_demo.py --database falkordb
```

## What This Demo Shows

### 1. Custom Entity Models
Demonstrates how to define custom Pydantic models for:
- `Person`: Individuals with relationships and attributes
- `Project`: Work projects with timelines and participants
- `Skill`: Learning areas with proficiency levels
- `Transaction`: Financial activities with categories
- `Event`: Life events with locations and participants

### 2. Temporal Data Management
- Shows how the same information can change over time
- Demonstrates valid_at/invalid_at timestamps
- Tracks skill progression, relationship changes, project evolution

### 3. Incremental Knowledge Building
- Starts with basic information
- Progressively adds more details and connections
- Shows how the graph grows and evolves

### 4. Advanced Search Capabilities
- **Semantic Search**: "Who are my close friends?"
- **Keyword Search**: Find specific project names or skills
- **Graph Traversal**: "What projects did I work on with John?"
- **Temporal Queries**: "What was I learning in 2023?"
- **Hybrid Queries**: Combine all search methods for best results

### 5. Relationship Discovery
- Find indirect connections between people, projects, and skills
- Discover patterns in learning and career progression
- Track influence networks and collaboration patterns

### 6. Interactive Exploration
- Add new episodes in real-time
- Query the knowledge base with natural language
- Explore the graph structure
- Export insights and summaries

## Demo Scenarios

The demo includes several pre-built scenarios:

1. **Career Journey**: Track job changes, skill development, and professional network
2. **Learning Path**: Follow educational progression and certification achievements
3. **Social Network**: Map relationships and social interactions over time
4. **Health & Wellness**: Track fitness goals and health-related activities
5. **Financial Growth**: Monitor investments and financial goal progression

## Interactive Features

- **Add Episode**: Input new information and see immediate graph updates
- **Search & Query**: Ask questions about your data using natural language
- **Explore Connections**: Discover relationships between different aspects of life
- **Time Travel**: Query the knowledge base at different points in time
- **Export Insights**: Generate summaries and reports

## Technical Highlights

- Custom entity validation with Pydantic
- Efficient incremental updates without full recomputation
- Multi-strategy search with automatic ranking
- Temporal relationship management
- Graph-based recommendation system

## Next Steps

After exploring this demo, you can:
1. Adapt the entity models for your specific use case
2. Integrate with real data sources (calendar, email, social media)
3. Add more sophisticated relationship rules
4. Implement automated insight generation
5. Create custom visualization interfaces

This demo serves as a foundation for building comprehensive knowledge management systems using Graphiti.