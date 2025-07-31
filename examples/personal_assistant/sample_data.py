"""
Sample data for the Personal AI Assistant Knowledge Base demo.

This module contains realistic sample data that tells a coherent story
of someone's personal and professional development over time.
"""

from datetime import date as date_type, datetime, timezone, timedelta
import json
from typing import List, Dict, Any

from graphiti_core.nodes import EpisodeType
from models import *


def model_to_json(model_instance) -> str:
    """Convert a Pydantic model instance to JSON string, handling date serialization."""
    def default(obj):
        if isinstance(obj, date_type):
            return obj.isoformat()
        raise TypeError(f"Object of type {type(obj)} is not JSON serializable")
    
    return json.dumps(model_instance.model_dump(), default=default)


def create_sample_episodes() -> List[Dict[str, Any]]:
    """Create a comprehensive set of sample episodes that tell a story over time."""
    
    episodes = []
    
    # Base date for the story (2 years ago)
    base_date = datetime.now(timezone.utc) - timedelta(days=730)
    
    # ==========================================
    # Chapter 1: Starting a New Career (2 years ago)
    # ==========================================
    
    # Episode 1: New job
    episodes.append({
        'name': 'Started new job at TechCorp',
        'content': '''I started my new job as a Software Engineer at TechCorp today! 
        I'm really excited about this opportunity. My manager is Sarah Chen, and I'll be 
        working on the customer data platform team. The office is in downtown Seattle, 
        and the team seems really welcoming. I'll be working with Python, React, and PostgreSQL.''',
        'type': EpisodeType.text,
        'source_description': 'personal journal',
        'reference_time': base_date + timedelta(days=1),
    })
    
    # Episode 2: Meeting colleagues
    sarah = Person(
        name="Sarah Chen",
        age=35,
        occupation="Engineering Manager",
        company="TechCorp",
        location="Seattle, WA",
        relationship_type=RelationshipType.COLLEAGUE,
        skills=["Leadership", "Python", "System Architecture"],
        interests=["Rock climbing", "Photography"]
    )
    
    episodes.append({
        'name': 'Met my new manager Sarah',
        'content': model_to_json(sarah),
        'type': EpisodeType.json,
        'source_description': 'contact information',
        'reference_time': base_date + timedelta(days=2),
    })
    
    # Episode 3: First project assignment
    customer_platform = Project(
        name="Customer Data Platform v2",
        description="Redesign and rebuild the customer data platform to handle 10x more traffic and improve data consistency",
        status=ProjectStatus.PLANNING,
        start_date=date_type.today() - timedelta(days=725),
        deadline=date_type.today() - timedelta(days=545),
        priority="high",
        team_members=["Sarah Chen", "Mike Rodriguez", "Lisa Park"],
        skills_required=["Python", "PostgreSQL", "React", "System Design"],
        technologies=["Python", "PostgreSQL", "React", "Docker", "Kubernetes"]
    )
    
    episodes.append({
        'name': 'Assigned to Customer Data Platform project',
        'content': model_to_json(customer_platform),
        'type': EpisodeType.json,
        'source_description': 'project management system',
        'reference_time': base_date + timedelta(days=5),
    })
    
    # Episode 4: Learning new skills
    episodes.append({
        'name': 'Started learning Kubernetes',
        'content': '''Began studying Kubernetes today to prepare for the infrastructure 
        work on the customer platform. I've been using Docker for a while, but K8s is new 
        to me. Found a great course on Udemy and started working through the exercises.''',
        'type': EpisodeType.text,
        'source_description': 'learning log',
        'reference_time': base_date + timedelta(days=10),
    })
    
    # ==========================================
    # Chapter 2: Building Relationships (6 months later)
    # ==========================================
    
    # Episode 5: Making friends at work
    mike = Person(
        name="Mike Rodriguez",
        age=28,
        occupation="Senior Software Engineer",
        company="TechCorp",
        location="Seattle, WA",
        relationship_type=RelationshipType.COLLEAGUE,
        skills=["React", "JavaScript", "Node.js", "GraphQL"],
        interests=["Soccer", "Gaming", "Cooking"]
    )
    
    episodes.append({
        'name': 'Getting to know Mike from my team',
        'content': model_to_json(mike),
        'type': EpisodeType.json,
        'source_description': 'social interaction',
        'reference_time': base_date + timedelta(days=180),
    })
    
    # Episode 6: Social event
    team_outing = Event(
        title="Team Building Event at Escape Room",
        description="Quarterly team building event with the engineering team",
        event_type=EventType.WORK,
        event_date=date_type.today() - timedelta(days=540),
        location="Escape the Room Seattle",
        attendees=["Sarah Chen", "Mike Rodriguez", "Lisa Park", "Alex Kim"],
        cost=25.0,
        outcomes=["Better team bonding", "Improved communication"],
        rating=4
    )
    
    episodes.append({
        'name': 'Team building escape room',
        'content': model_to_json(team_outing),
        'type': EpisodeType.json,
        'source_description': 'calendar event',
        'reference_time': base_date + timedelta(days=185),
    })
    
    # ==========================================
    # Chapter 3: Skill Development (8 months later)
    # ==========================================
    
    # Episode 7: Completing Kubernetes certification
    k8s_skill = Skill(
        name="Kubernetes",
        category="DevOps",
        level=SkillLevel.INTERMEDIATE,
        years_of_experience=0.5,
        learning_source="Udemy course + hands-on practice",
        certifications=["Certified Kubernetes Application Developer (CKAD)"],
        projects_used=["Customer Data Platform v2"],
        last_used=date_type.today() - timedelta(days=450),
    )
    
    episodes.append({
        'name': 'Earned Kubernetes certification',
        'content': model_to_json(k8s_skill),
        'type': EpisodeType.json,
        'source_description': 'certification record',
        'reference_time': base_date + timedelta(days=240),
    })
    
    # Episode 8: Project success
    episodes.append({
        'name': 'Customer Platform v2 launch success',
        'content': '''Amazing news! Our Customer Data Platform v2 went live today and 
        everything is working perfectly. We've successfully handled 10x the previous traffic 
        with 99.9% uptime. The new architecture is performing even better than expected. 
        Sarah commended the whole team, and I'm particularly proud of the Kubernetes 
        infrastructure I helped design.''',
        'type': EpisodeType.text,
        'source_description': 'work journal',
        'reference_time': base_date + timedelta(days=270),
    })
    
    # ==========================================
    # Chapter 4: Personal Growth (1 year later)
    # ==========================================
    
    # Episode 9: Investment in education
    python_course = Transaction(
        description="Advanced Python Programming Course",
        amount=-299.0,
        category=TransactionCategory.EDUCATION,
        transaction_date=date_type.today() - timedelta(days=365),
        vendor="Python Institute",
        payment_method="Credit Card",
        tax_deductible=True,
        notes="Professional development course for advanced Python techniques"
    )
    
    episodes.append({
        'name': 'Invested in advanced Python course',
        'content': model_to_json(python_course),
        'type': EpisodeType.json,
        'source_description': 'financial records',
        'reference_time': base_date + timedelta(days=365),
    })
    
    # Episode 10: Health goal
    fitness_goal = Goal(
        title="Run a Half Marathon",
        description="Train for and complete a half marathon to improve fitness and mental health",
        category="health",
        target_date=date_type.today() - timedelta(days=200),
        status="in_progress",
        priority="medium",
        progress_percentage=60,
        milestones=["5K run", "10K run", "15K run"],
        motivation="Improve overall health and prove to myself I can achieve challenging goals",
        reward="New running shoes and a weekend trip"
    )
    
    episodes.append({
        'name': 'Set half marathon goal',
        'content': model_to_json(fitness_goal),
        'type': EpisodeType.json,
        'source_description': 'goal tracking app',
        'reference_time': base_date + timedelta(days=400),
    })
    
    # ==========================================
    # Chapter 5: Recent Developments
    # ==========================================
    
    # Episode 11: Meeting a mentor
    alex = Person(
        name="Dr. Alex Kim",
        age=42,
        occupation="Principal Engineer",
        company="TechCorp",
        location="Seattle, WA",
        relationship_type=RelationshipType.MENTOR,
        skills=["System Architecture", "Machine Learning", "Leadership"],
        interests=["AI Research", "Mentoring", "Tennis"]
    )
    
    episodes.append({
        'name': 'Started mentorship with Alex Kim',
        'content': model_to_json(alex),
        'type': EpisodeType.json,
        'source_description': 'mentorship program',
        'reference_time': base_date + timedelta(days=500),
    })
    
    # Episode 12: New project with ML
    ml_project = Project(
        name="AI-Powered Customer Insights",
        description="Develop machine learning models to provide actionable customer insights",
        status=ProjectStatus.ACTIVE,
        start_date=date_type.today() - timedelta(days=180),
        deadline=date_type.today() + timedelta(days=90),
        priority="high",
        team_members=["Dr. Alex Kim", "Sarah Chen", "Data Science Team"],
        skills_required=["Python", "Machine Learning", "TensorFlow", "Data Analysis"],
        technologies=["Python", "TensorFlow", "Pandas", "PostgreSQL", "Jupyter"]
    )
    
    episodes.append({
        'name': 'Leading ML project for customer insights',
        'content': model_to_json(ml_project),
        'type': EpisodeType.json,
        'source_description': 'project assignment',
        'reference_time': base_date + timedelta(days=550),
    })
    
    # Episode 13: Learning machine learning
    ml_skill = Skill(
        name="Machine Learning",
        category="Data Science",
        level=SkillLevel.BEGINNER,
        years_of_experience=0.2,
        learning_source="Mentorship with Alex Kim + online courses",
        projects_used=["AI-Powered Customer Insights"],
        learning_goal="Become proficient in ML model development and deployment",
        related_skills=["Python", "Statistics", "Data Analysis"]
    )
    
    episodes.append({
        'name': 'Started learning machine learning',
        'content': model_to_json(ml_skill),
        'type': EpisodeType.json,
        'source_description': 'skill assessment',
        'reference_time': base_date + timedelta(days=560),
    })
    
    # Episode 14: Personal achievement
    marathon_event = Event(
        title="Seattle Half Marathon",
        description="Successfully completed my first half marathon!",
        event_type=EventType.ACHIEVEMENT,
        event_date=date_type.today() - timedelta(days=30),
        location="Seattle, WA",
        duration="2 hours 15 minutes",
        outcomes=["Personal best time", "Improved confidence", "Better fitness"],
        skills_gained=["Endurance", "Goal Setting", "Perseverance"],
        rating=5,
        cost=75.0
    )
    
    episodes.append({
        'name': 'Completed Seattle Half Marathon',
        'content': model_to_json(marathon_event),
        'type': EpisodeType.json,
        'source_description': 'fitness tracking',
        'reference_time': base_date + timedelta(days=700),
    })
    
    # Episode 15: Recent social expansion
    episodes.append({
        'name': 'Joined local AI meetup group',
        'content': '''Attended my first Seattle AI/ML meetup tonight. Met some fascinating 
        people working on cutting-edge projects. One person, Rachel, is working on natural 
        language processing at a startup. Another, David, is a researcher at UW working 
        on computer vision. I'm excited to learn from this community and maybe even 
        present my own project someday.''',
        'type': EpisodeType.text,
        'source_description': 'social media post',
        'reference_time': base_date + timedelta(days=720),
    })
    
    return episodes


def create_sample_queries() -> List[str]:
    """Create sample queries that demonstrate different search capabilities."""
    
    return [
        # Semantic search queries
        "Who are my colleagues at TechCorp?",
        "What projects have I worked on?",
        "What skills am I currently learning?",
        "Who can help me with machine learning?",
        "What are my fitness goals?",
        
        # Temporal queries
        "What was I doing 6 months ago?",
        "How have my skills changed over time?",
        "What projects did I complete last year?",
        
        # Relationship queries
        "What projects did I work on with Sarah Chen?",
        "Who are my mentors?",
        "What events did I attend with my colleagues?",
        
        # Goal and achievement queries
        "What goals have I achieved?",
        "What are my learning investments?",
        "What skills do I need for my current projects?",
        
        # Cross-domain queries
        "How does my learning relate to my career progression?",
        "What social connections help with my professional goals?",
        "How do my health activities impact my work performance?",
    ]


def create_interactive_scenarios() -> List[Dict[str, Any]]:
    """Create scenarios for interactive exploration."""
    
    return [
        {
            'name': 'Career Progression',
            'description': 'Explore how skills, projects, and relationships contribute to career growth',
            'queries': [
                "What skills have I developed over the past two years?",
                "How do my projects connect to my skill development?",
                "Who has influenced my career progression?",
            ]
        },
        {
            'name': 'Learning Journey', 
            'description': 'Track educational investments and skill acquisition',
            'queries': [
                "What have I invested in learning?",
                "How do my certifications relate to my projects?",
                "What skills am I still developing?",
            ]
        },
        {
            'name': 'Professional Network',
            'description': 'Understand relationship building and collaboration patterns',
            'queries': [
                "Who do I collaborate with most frequently?",
                "What events have helped me build my network?",
                "How has my network evolved over time?",
            ]
        },
        {
            'name': 'Goal Achievement',
            'description': 'Track progress toward personal and professional goals',
            'queries': [
                "What goals have I set and achieved?",
                "How do my activities support my goals?",
                "What obstacles have I overcome?",
            ]
        },
        {
            'name': 'Life Balance',
            'description': 'Explore connections between work, health, and personal life',
            'queries': [
                "How do my health activities relate to work performance?",
                "What personal achievements am I most proud of?",
                "How do I balance learning, work, and personal goals?",
            ]
        }
    ]