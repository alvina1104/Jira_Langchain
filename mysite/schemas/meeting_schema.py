from pydantic import BaseModel, Field


class MeetingAnalyzeInputSchema(BaseModel):
    text: str = Field(min_length=1, max_length=5000)


class MeetingTaskSchema(BaseModel):
    title: str
    assignee: str | None = None
    deadline_text: str | None = None
    evidence: str


class MeetingAnalyzeOutputSchema(BaseModel):
    summary: str
    tasks: list[MeetingTaskSchema]


class CheckTaskSchema(BaseModel):
    title: str
    assignee: str | None = None
    deadline_text: str | None = None


class CheckTasksInputSchema(BaseModel):
    tasks: list[CheckTaskSchema]


class TaskStatsSchema(BaseModel):
    total_tasks: int
    complete_tasks: int
    without_assignee: int
    without_deadline: int


class TaskCheckSchema(BaseModel):
    task_number: int
    needs_clarification: bool
    missing_fields: list[str]


class CheckTasksOutputSchema(BaseModel):
    stats: TaskStatsSchema
    checks: list[TaskCheckSchema]