from fastapi import FastAPI
from mysite.api import meeting, todo
import uvicorn


jira_app = FastAPI(title="Operator for work")
jira_app.include_router(meeting.meeting_router)
jira_app.include_router(todo.todo_router)


if __name__ == "__main__":
    uvicorn.run(jira_app, host='127.0.0.1', port=8000)