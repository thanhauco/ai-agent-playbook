"""
Pydantic AI Validation Agent Example

Demonstrates advanced validation, nested models, and error handling.
"""

from pydantic_ai import Agent, RunContext
from pydantic import BaseModel, Field, field_validator
from typing import List
from datetime import datetime

# Note: Install with: pip install pydantic-ai


class Task(BaseModel):
    """A single task with validation"""
    title: str = Field(..., min_length=3, max_length=100)
    priority: int = Field(..., ge=1, le=5, description="Priority from 1-5")
    due_date: datetime
    tags: List[str] = Field(default_factory=list)
    
    @field_validator('title')
    @classmethod
    def title_must_not_be_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError('Title cannot be empty or whitespace')
        return v.strip()


class ProjectPlan(BaseModel):
    """A project plan with multiple tasks"""
    project_name: str
    description: str
    tasks: List[Task]
    estimated_days: int = Field(..., gt=0)
    
    @field_validator('tasks')
    @classmethod
    def must_have_tasks(cls, v: List[Task]) -> List[Task]:
        if len(v) == 0:
            raise ValueError('Project must have at least one task')
        return v


# Create agent with complex validation
agent = Agent(
    'openai:gpt-4',
    result_type=ProjectPlan,
    system_prompt=(
        'You are a project manager AI. Create detailed project plans with '
        'multiple tasks. Each task must have a title, priority (1-5), '
        'due date, and optional tags. Ensure all data is valid.'
    ),
)


def run_validation_agent():
    """Run the validation agent"""
    try:
        result = agent.run_sync(
            'Create a project plan for building a chatbot application. '
            'Include 3-5 tasks with different priorities.'
        )
        
        plan = result.data
        print(f"Project: {plan.project_name}")
        print(f"Description: {plan.description}")
        print(f"Estimated Duration: {plan.estimated_days} days")
        print(f"\nTasks ({len(plan.tasks)}):")
        
        for i, task in enumerate(plan.tasks, 1):
            print(f"\n{i}. {task.title}")
            print(f"   Priority: {'★' * task.priority}")
            print(f"   Due: {task.due_date.strftime('%Y-%m-%d')}")
            if task.tags:
                print(f"   Tags: {', '.join(task.tags)}")
        
        # All data is validated and type-safe
        assert isinstance(plan, ProjectPlan)
        assert all(isinstance(task, Task) for task in plan.tasks)
        assert all(1 <= task.priority <= 5 for task in plan.tasks)
        
        print("\n✅ All validation passed!")
        
    except Exception as e:
        print(f"Error: {e}")
        print("Note: This example requires 'pydantic-ai' and OPENAI_API_KEY.")


if __name__ == "__main__":
    run_validation_agent()
