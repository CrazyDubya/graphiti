"""
Custom entity models for the Personal AI Assistant Knowledge Base demo.

This module defines Pydantic models for various life aspects that can be 
tracked in a personal knowledge graph.
"""

from datetime import date as date_type, datetime
from enum import Enum
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class RelationshipType(str, Enum):
    """Types of relationships between people."""
    FAMILY = "family"
    FRIEND = "friend" 
    COLLEAGUE = "colleague"
    MENTOR = "mentor"
    MENTEE = "mentee"
    ACQUAINTANCE = "acquaintance"
    ROMANTIC = "romantic"


class SkillLevel(str, Enum):
    """Proficiency levels for skills."""
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    EXPERT = "expert"


class ProjectStatus(str, Enum):
    """Status of projects."""
    PLANNING = "planning"
    ACTIVE = "active"
    ON_HOLD = "on_hold"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class TransactionCategory(str, Enum):
    """Categories for financial transactions."""
    INCOME = "income"
    INVESTMENT = "investment"
    EDUCATION = "education"
    HEALTH = "health"
    TRAVEL = "travel"
    ENTERTAINMENT = "entertainment"
    HOUSING = "housing"
    FOOD = "food"
    TRANSPORTATION = "transportation"
    OTHER = "other"


class EventType(str, Enum):
    """Types of life events."""
    MILESTONE = "milestone"
    TRAVEL = "travel"
    MEETING = "meeting"
    CELEBRATION = "celebration"
    ACHIEVEMENT = "achievement"
    LEARNING = "learning"
    HEALTH = "health"
    FAMILY = "family"
    WORK = "work"


class Person(BaseModel):
    """A person in the knowledge graph."""
    name: str = Field(description="Full name of the person")
    age: Optional[int] = Field(None, description="Age of the person")
    occupation: Optional[str] = Field(None, description="Job title or occupation")
    company: Optional[str] = Field(None, description="Company they work for")
    location: Optional[str] = Field(None, description="Current location/city")
    email: Optional[str] = Field(None, description="Email address")
    phone: Optional[str] = Field(None, description="Phone number")
    relationship_type: Optional[RelationshipType] = Field(None, description="Type of relationship")
    interests: List[str] = Field(default_factory=list, description="Areas of interest")
    skills: List[str] = Field(default_factory=list, description="Notable skills")
    social_media: Dict[str, str] = Field(default_factory=dict, description="Social media handles")
    notes: Optional[str] = Field(None, description="Additional notes about the person")

    class Config:
        use_enum_values = True


class Project(BaseModel):
    """A work or personal project."""
    name: str = Field(description="Name of the project")
    description: str = Field(description="Detailed description of the project")
    status: ProjectStatus = Field(description="Current status of the project")
    start_date: Optional[date_type] = Field(None, description="Project start date")
    end_date: Optional[date_type] = Field(None, description="Project end date (if completed)")
    deadline: Optional[date_type] = Field(None, description="Project deadline")
    priority: Optional[str] = Field(None, description="Priority level (high, medium, low)")
    budget: Optional[float] = Field(None, description="Project budget")
    team_members: List[str] = Field(default_factory=list, description="Names of team members")
    skills_required: List[str] = Field(default_factory=list, description="Skills needed for the project")
    technologies: List[str] = Field(default_factory=list, description="Technologies used")
    outcomes: List[str] = Field(default_factory=list, description="Project outcomes and results")
    lessons_learned: Optional[str] = Field(None, description="Key lessons from the project")

    class Config:
        use_enum_values = True


class Skill(BaseModel):
    """A skill or area of knowledge."""
    name: str = Field(description="Name of the skill")
    category: str = Field(description="Category (e.g., technical, soft skills, language)")
    level: SkillLevel = Field(description="Current proficiency level")
    years_of_experience: Optional[float] = Field(None, description="Years of experience with this skill")
    learning_source: Optional[str] = Field(None, description="How the skill was learned")
    certifications: List[str] = Field(default_factory=list, description="Related certifications")
    projects_used: List[str] = Field(default_factory=list, description="Projects where skill was applied")
    last_used: Optional[date_type] = Field(None, description="When the skill was last used")
    learning_goal: Optional[str] = Field(None, description="Future learning goals for this skill")
    related_skills: List[str] = Field(default_factory=list, description="Related or prerequisite skills")

    class Config:
        use_enum_values = True


class Transaction(BaseModel):
    """A financial transaction."""
    description: str = Field(description="Description of the transaction")
    amount: float = Field(description="Transaction amount (positive for income, negative for expenses)")
    category: TransactionCategory = Field(description="Transaction category")
    transaction_date: date_type = Field(description="Transaction date")
    account: Optional[str] = Field(None, description="Account used for transaction")
    vendor: Optional[str] = Field(None, description="Vendor or company")
    payment_method: Optional[str] = Field(None, description="Payment method used")
    recurring: bool = Field(default=False, description="Whether this is a recurring transaction")
    investment_type: Optional[str] = Field(None, description="Type of investment (if applicable)")
    roi: Optional[float] = Field(None, description="Return on investment (if applicable)")
    tax_deductible: bool = Field(default=False, description="Whether transaction is tax deductible")
    notes: Optional[str] = Field(None, description="Additional notes")

    class Config:
        use_enum_values = True


class Event(BaseModel):
    """A life event or important occurrence."""
    title: str = Field(description="Title of the event")
    description: str = Field(description="Detailed description")
    event_type: EventType = Field(description="Type of event")
    event_date: date_type = Field(description="Event date")
    location: Optional[str] = Field(None, description="Event location")
    duration: Optional[str] = Field(None, description="Duration of the event")
    attendees: List[str] = Field(default_factory=list, description="People who attended")
    organizer: Optional[str] = Field(None, description="Event organizer")
    cost: Optional[float] = Field(None, description="Cost of attending/organizing")
    outcomes: List[str] = Field(default_factory=list, description="Results or outcomes from the event")
    photos: List[str] = Field(default_factory=list, description="Photo URLs or filenames")
    related_projects: List[str] = Field(default_factory=list, description="Related projects")
    skills_gained: List[str] = Field(default_factory=list, description="Skills acquired from the event")
    follow_up_actions: List[str] = Field(default_factory=list, description="Follow-up actions needed")
    rating: Optional[int] = Field(None, ge=1, le=5, description="Personal rating of the event (1-5)")

    class Config:
        use_enum_values = True


class HealthActivity(BaseModel):
    """A health or fitness related activity."""
    activity_type: str = Field(description="Type of activity (exercise, medical, nutrition)")
    description: str = Field(description="Description of the activity")
    activity_date: date_type = Field(description="Date of the activity")
    duration: Optional[str] = Field(None, description="Duration of the activity")
    intensity: Optional[str] = Field(None, description="Intensity level (low, medium, high)")
    calories_burned: Optional[int] = Field(None, description="Calories burned")
    location: Optional[str] = Field(None, description="Where the activity took place")
    equipment_used: List[str] = Field(default_factory=list, description="Equipment or tools used")
    metrics: Dict[str, Any] = Field(default_factory=dict, description="Quantitative metrics")
    mood_before: Optional[str] = Field(None, description="Mood before the activity")
    mood_after: Optional[str] = Field(None, description="Mood after the activity")
    goals_achieved: List[str] = Field(default_factory=list, description="Goals achieved")
    notes: Optional[str] = Field(None, description="Additional notes")


class Goal(BaseModel):
    """A personal or professional goal."""
    title: str = Field(description="Goal title")
    description: str = Field(description="Detailed description")
    category: str = Field(description="Goal category (career, health, financial, personal)")
    target_date: Optional[date_type] = Field(None, description="Target completion date")
    status: str = Field(description="Current status (not_started, in_progress, completed, paused)")
    priority: str = Field(description="Priority level (high, medium, low)")
    progress_percentage: Optional[int] = Field(None, ge=0, le=100, description="Progress percentage")
    milestones: List[str] = Field(default_factory=list, description="Key milestones")
    obstacles: List[str] = Field(default_factory=list, description="Obstacles encountered")
    resources_needed: List[str] = Field(default_factory=list, description="Resources needed")
    people_involved: List[str] = Field(default_factory=list, description="People who can help")
    motivation: Optional[str] = Field(None, description="Why this goal is important")
    reward: Optional[str] = Field(None, description="Reward for achieving the goal")
    review_date: Optional[date_type] = Field(None, description="Next review date")
    notes: Optional[str] = Field(None, description="Additional notes")


# Export all models for easy importing
__all__ = [
    'Person', 'Project', 'Skill', 'Transaction', 'Event', 'HealthActivity', 'Goal',
    'RelationshipType', 'SkillLevel', 'ProjectStatus', 'TransactionCategory', 'EventType'
]