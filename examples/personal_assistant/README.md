# Personal AI Assistant Knowledge Base Demo

This demo showcases the full functionality of Graphiti through a comprehensive Personal AI Assistant Knowledge Base that tracks various aspects of a person's life over time.

## 🌟 Features Demonstrated

### Core Graphiti Features
- **Real-time incremental updates**: Add information as it happens
- **Bi-temporal data model**: Track when events occurred vs when they were recorded
- **Hybrid retrieval**: Semantic search + keyword search (BM25) + graph traversal
- **Custom entity definitions**: Person, Project, Skill, Transaction, Event entities
- **Graph relationships**: Discover connections between different life aspects
- **Multiple database backends**: Works with both Neo4j and FalkorDB
- **Error handling**: Robust error recovery and graceful degradation
- **Visualizations**: Text-based visualizations and summaries

### Life Tracking Categories
- **Personal Relationships**: Family, friends, colleagues, interactions
- **Work & Projects**: Job history, projects, achievements, collaborations
- **Learning & Skills**: Courses, certifications, skill development
- **Health & Fitness**: Activities, goals, progress tracking
- **Financial**: Transactions, investments, financial goals
- **Events & Memories**: Important life events, travel, experiences

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- OpenAI API key (set as `OPENAI_API_KEY` environment variable)
- **Neo4j**: Neo4j Desktop with a local database running, OR
- **FalkorDB**: FalkorDB server running (optional, requires `pip install graphiti-core[falkordb]`)

### Installation & Setup

1. **Clone and install dependencies:**
```bash
cd examples/personal_assistant
pip install -e ../../  # Install graphiti-core
```

2. **Set up environment:**
```bash
# Copy the sample environment file
cp .env.example .env

# Edit .env with your actual API keys
export OPENAI_API_KEY=your_openai_api_key

# For Neo4j (default)
export NEO4J_URI=bolt://localhost:7687
export NEO4J_USER=neo4j
export NEO4J_PASSWORD=password

# OR for FalkorDB (requires additional installation)
pip install graphiti-core[falkordb]
export FALKORDB_URI=falkor://localhost:6379
```

3. **Run the demo:**
```bash
# Quick start with setup verification
python run_demo.py --setup-only

# Run the full demo
python run_demo.py

# Interactive exploration mode
python run_demo.py --interactive

# Use FalkorDB instead of Neo4j
python run_demo.py --database falkordb --interactive
```

## 🎯 Demo Components

### 1. Custom Entity Models (`models.py`)
Demonstrates how to define custom Pydantic models for:
- `Person`: Individuals with relationships and attributes
- `Project`: Work projects with timelines and participants
- `Skill`: Learning areas with proficiency levels
- `Transaction`: Financial activities with categories
- `Event`: Life events with locations and participants
- `HealthActivity`: Fitness and health tracking
- `Goal`: Personal and professional objectives

### 2. Temporal Data Management (`sample_data.py`)
- Shows how the same information can change over time
- Demonstrates valid_at/invalid_at timestamps
- Tracks skill progression, relationship changes, project evolution
- Realistic 2-year timeline of personal and professional development

### 3. Hybrid Search Capabilities
**Three search strategies demonstrated:**
- **Semantic search**: Find related concepts using embeddings
- **Keyword search**: BM25-based text matching
- **Graph traversal**: Relationship-aware search with center nodes

**Sample queries:**
- "Who are my colleagues at TechCorp?"
- "What machine learning projects have I worked on?"
- "How have my skills evolved over time?"
- "Who can help me with my career goals?"

### 4. Visualization Features (`visualization.py`)
- **Summary Reports**: Comprehensive knowledge graph overview
- **Personal Timeline**: Chronological view of life events
- **Entity Connections**: Visualize relationships around specific entities
- **Quick Statistics**: Fast overview of graph contents
- **ASCII Charts**: Simple text-based data visualizations

### 5. Interactive Exploration
**Enhanced interactive mode with commands:**
- `help` - Show available commands
- `stats` - Comprehensive statistics and visualizations
- `summary` - Generate knowledge graph summary report
- `timeline` - Show personal timeline of events
- `visualize <entity>` - Show connections for specific entities
- `search <query>` - Enhanced search with multiple result types
- `add <text>` - Add new episodes in real-time
- `scenarios` - Show predefined exploration scenarios

## 📊 What You'll Learn

### 1. Temporal Knowledge Management
```python
# Example: Track skill progression over time
skill_beginner = Skill(
    name="Machine Learning",
    level=SkillLevel.BEGINNER,
    years_of_experience=0.2
)

# Later update...
skill_intermediate = Skill(
    name="Machine Learning", 
    level=SkillLevel.INTERMEDIATE,
    years_of_experience=1.0,
    certifications=["TensorFlow Developer Certificate"]
)
```

### 2. Multi-dimensional Search
```python
# Search for relationships
results = await graphiti.search("collaborations with Sarah Chen")

# Search for entities
config = NODE_HYBRID_SEARCH_RRF
results = await graphiti._search("machine learning projects", config=config)

# Graph-aware search
results = await graphiti.search(
    "Python skills", 
    center_node_uuid=person_node_id
)
```

### 3. Real-time Updates
```python
# Add new information as it happens
await graphiti.add_episode(
    name="Completed AI course",
    episode_body="Finished the Stanford CS229 machine learning course today!",
    reference_time=datetime.now(timezone.utc)
)
```

## 🎭 Predefined Scenarios

The demo includes several exploration scenarios:

1. **Career Progression**: Track skill development and project evolution
2. **Learning Journey**: Educational investments and certifications
3. **Professional Network**: Relationship building and collaboration patterns
4. **Goal Achievement**: Progress tracking and milestone completion
5. **Life Balance**: Connections between work, health, and personal life

## 🛠️ Advanced Features

### Database Backend Switching
```bash
# Use Neo4j (default)
python run_demo.py --database neo4j

# Use FalkorDB
python run_demo.py --database falkordb
```

### Error Handling & Recovery
The demo includes comprehensive error handling:
- Graceful degradation when services are unavailable
- Input validation and sanitization
- Connection retry logic
- Detailed error logging

### Extensibility
Easy to extend with new entity types:
```python
class Hobby(BaseModel):
    name: str
    category: str
    skill_level: str
    time_invested: Optional[float]
    equipment: List[str] = Field(default_factory=list)
```

## 📝 Sample Output

```
🌟 Personal AI Assistant Demo
=====================================
📊 Comprehensive Summary Report
=====================================

🏗️ ENTITY OVERVIEW
----------------------------------------
People                    8 entities
Projects                  5 entities  
Skills                   12 entities
Goals                     6 entities
Events                   15 entities

💡 KEY INSIGHTS
----------------------------------------
• Strong focus on continuous skill development
• Active collaboration with teammates and mentors
• Committed to formal learning and professional development
• Balanced approach to personal health and professional goals
```

## 🔍 Troubleshooting

### Common Issues

1. **Missing API Key**
   ```bash
   export OPENAI_API_KEY=your_actual_key_here
   ```

2. **Database Connection Issues**
   ```bash
   # For Neo4j
   docker run -p 7474:7474 -p 7687:7687 -e NEO4J_AUTH=neo4j/password neo4j:latest
   
   # For FalkorDB
   docker run -p 6379:6379 falkordb/falkordb:latest
   ```

3. **Import Errors**
   ```bash
   pip install -e ../../  # Install graphiti-core in development mode
   ```

### Getting Help

- Check the logs for detailed error messages
- Use `python run_demo.py --setup-only` to verify configuration
- Ensure your database is running and accessible
- Verify API keys are correctly set

## 🏗️ Architecture

```
personal_assistant/
├── models.py              # Custom entity definitions
├── sample_data.py         # Realistic sample dataset
├── personal_assistant_demo.py  # Main demo orchestration
├── visualization.py       # Visualization and summary tools
├── run_demo.py           # Setup and runner script
├── test_imports.py       # Import verification
├── requirements.txt      # Dependencies
└── README.md            # This documentation
```

## 🎯 Next Steps

After running this demo, you can:

1. **Extend the entity models** with your own data types
2. **Add real data** from your own life or organization
3. **Implement custom search strategies** using Graphiti's flexible search system
4. **Build a web interface** using the FastAPI server in the `server/` directory
5. **Deploy to production** with proper database configuration
6. **Integrate with external data sources** via the MCP server

## 📚 Related Examples

- **E-commerce Demo**: Product catalog and recommendation system
- **Podcast Demo**: Episode transcription and knowledge extraction
- **Wizard of Oz Demo**: Classic literature analysis
- **LangGraph Agent**: AI agent integration patterns

---

💡 **This demo represents a complete, production-ready example of building a personal knowledge graph with Graphiti. Use it as a template for your own knowledge management systems!**