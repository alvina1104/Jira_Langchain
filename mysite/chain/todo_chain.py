from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda

from mysite.chain.model import ai_model, check_answer
from mysite.schemas.todo_schema import TodoPlanOutputSchema


todo_parser = PydanticOutputParser(
    pydantic_object=TodoPlanOutputSchema
)

todo_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
Ты — AI-ассистент для планирования рабочих задач.

Твоя задача — составить конкретный и реалистичный план достижения цели пользователя.

ПРАВИЛА:
- Используй цель и ограничения пользователя.
- Создай ровно столько задач, сколько указано в count_tasks.
- Не создавай задачи, которые противоречат constraints.
- Каждая задача должна быть конкретной и выполнимой.
- Не дублируй задачи.

ДЛЯ КАЖДОЙ ЗАДАЧИ:
- task_number — порядковый номер, начиная с 1.
- title — короткое название действия.
- details — краткое описание того, что нужно сделать.
- priority — число от 1 до 3.
- 1 = низкий приоритет.
- 2 = средний приоритет.
- 3 = высокий приоритет.
- status всегда "todo".

ОБЩИЙ РЕЗУЛЬТАТ:
- plan_status всегда "draft".
- tasks_count должен соответствовать реальному количеству созданных задач.
- tasks_count должен быть равен count_tasks.
- Сохраняй язык цели пользователя.
"""
    ),
    (
        "human",
        """
Цель:
{goal}

Ограничения:
{constraints}

Количество задач:
{count_tasks}

Верни результат строго в указанной структуре.

{format_instructions}
"""
    )
]).partial(
    format_instructions=todo_parser.get_format_instructions()
)

todo_chain = (
    todo_prompt
    | ai_model
    | RunnableLambda(check_answer)
    | todo_parser
)