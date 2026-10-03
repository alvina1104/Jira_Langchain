import asyncio
from fastapi import APIRouter, HTTPException
from langchain_core.exceptions import OutputParserException
from mysite.chain.todo_chain import todo_chain
from mysite.schemas.todo_schema import TodoPlanInputSchema, TodoPlanOutputSchema


todo_router = APIRouter(prefix="/todos", tags=["Todos"])


@todo_router.post("/plan/", response_model=TodoPlanOutputSchema)
async def create_plan(data: TodoPlanInputSchema):
    goal = data.goal.strip()

    if not goal:
        raise HTTPException(status_code=422, detail="Цель не должна быть пустой")

    constraints = data.constraints.strip() if data.constraints else "Ограничений нет"

    try:
        result = await asyncio.wait_for(
            todo_chain.ainvoke({
                "goal": goal,
                "constraints": constraints,
                "count_tasks": data.count_tasks
            }),
            timeout=120
        )
    except TimeoutError:
        raise HTTPException(status_code=504, detail="Модель не успела составить план")
    except OutputParserException:
        raise HTTPException(status_code=500, detail="Ответ модели не соответствует схеме")
    except ValueError as error:
        raise HTTPException(status_code=500, detail=str(error))

    return result