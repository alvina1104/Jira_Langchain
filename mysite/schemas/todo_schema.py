from typing import Literal
from pydantic import BaseModel, Field

class TodoPlanInputSchema(BaseModel):
    goal: str = Field(min_length=1, max_length=1000)
    constraints: str | None = Field(default=None, max_length=1000)
    count_tasks: int = Field(ge=1, le=10)


class TodoTaskSchema(BaseModel):
    task_number: int
    title: str
    details: str
    priority: int = Field(ge=1, le=3)
    status: Literal["todo"] = "todo"


class TodoPlanAIOutputSchema(BaseModel):
    tasks: list[TodoTaskSchema]


class TodoPlanOutputSchema(BaseModel):
    plan_status: Literal["draft"] = "draft"
    tasks: list[TodoTaskSchema]
    tasks_count: int