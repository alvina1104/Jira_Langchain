import asyncio
import json
from fastapi import APIRouter, HTTPException
from langchain_core.exceptions import OutputParserException
from mysite.chain.meeting_chain import meeting_chain
from mysite.chain.check_tasks_chain import check_tasks_chain
from mysite.schemas.meeting_schema import MeetingAnalyzeInputSchema, MeetingAnalyzeOutputSchema, CheckTasksInputSchema, CheckTasksOutputSchema


meeting_router = APIRouter(prefix="/meetings", tags=["Meetings"])


@meeting_router.post("/analyze/", response_model=MeetingAnalyzeOutputSchema)
async def analyze_meeting(data: MeetingAnalyzeInputSchema):
    text = data.text.strip()

    if not text:
        raise HTTPException(status_code=422, detail="Текст встречи не должен быть пустым")

    try:
        result = await asyncio.wait_for(
            meeting_chain.ainvoke({"text": text}),
            timeout=120
        )
    except TimeoutError:
        raise HTTPException(status_code=504, detail="Модель не успела обработать текст встречи")
    except OutputParserException:
        raise HTTPException(status_code=500, detail="Ответ модели не соответствует схеме")
    except ValueError as error:
        raise HTTPException(status_code=500, detail=str(error))

    return result


@meeting_router.post("/check_tasks/", response_model=CheckTasksOutputSchema)
async def check_tasks(data: CheckTasksInputSchema):
    if not data.tasks:
        raise HTTPException(status_code=422, detail="Список задач не должен быть пустым")

    tasks = [task.model_dump() for task in data.tasks]

    try:
        result = await asyncio.wait_for(
            check_tasks_chain.ainvoke({
                "tasks": json.dumps(tasks, ensure_ascii=False)
            }),
            timeout=120
        )
    except TimeoutError:
        raise HTTPException(status_code=504, detail="Модель не успела проверить задачи")
    except OutputParserException:
        raise HTTPException(status_code=500, detail="Ответ модели не соответствует схеме")
    except ValueError as error:
        raise HTTPException(status_code=500, detail=str(error))

    return result