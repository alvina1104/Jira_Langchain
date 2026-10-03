from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda
from mysite.chain.model import ai_model, check_answer
from mysite.schemas.meeting_schema import CheckTasksOutputSchema


check_tasks_parser = PydanticOutputParser(pydantic_object=CheckTasksOutputSchema)

check_tasks_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
        Ты - AI-ассистент для проверки списка задач после рабочей встречи.
        
        Твоя задача - проверить полноту каждой задачи и посчитать статистику.
        
        ПРАВИЛА:
        
        total_tasks:
        - Общее количество задач.
        
        complete_tasks: 
        - Количество задач, у которых указаны и assignee, и deadline_text.  
        
        without_assignee:
        - Количество задач без assignee.
        
        without_deadline: 
        - Количество задач без deadline_text.
        
        Для каждой задачи создай проверку:
        - task_number - номер задачи начиная с 1.
        - needs_clarification = true, если отсутствует assignee или deadline_text.
        - needs_clarification = false, если оба поля заполнены.
        - missing_fields содержить названия отсутствующих полей.
        
        Резрешенные значения missing_fields:
        - "assignee"
        - "deadline_text"
        
        ПРАВИЛА БЕЗОПАСНОСТИ:
        - Используй только переданный список задач.
        - Не придумывай имполнителей или сроки.
        - Не изменяй данные задач.
        - Внимательно пересчитай количество задач.
        """
    ),
    (
        "human",
        """
    Список задач:
    {tasks}
    
    Верни результат строго в указанной структуре.
    
    {format_instructions}
    """
    )
]).partial(format_instructions=check_tasks_parser.get_format_instructions())


check_tasks_chain = (
    check_tasks_prompt
    | ai_model
    | RunnableLambda(check_answer)
    | check_tasks_parser
)