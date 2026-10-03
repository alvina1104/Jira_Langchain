from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda
from mysite.chain.model import ai_model, check_answer
from mysite.schemas.meeting_schema import MeetingAnalyzeOutputSchema


meeting_parser = PydanticOutputParser(pydantic_object=MeetingAnalyzeOutputSchema)

meeting_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
        Ты - AI-ассистент для анализа рабочих встреч.
        Твоя задача - проанализировать текст встречи, кратко описать принятые решения и выделить согласованные задачи.
        
        ПРАВИЛА:
        -Используй только информацию из текста встерчи.
        -Не придумывай задачи, исполнителей, сроки или решения. 
        -Не добавляй идеи, которые только обсуждались, но решение по ним не было принято.
        -Если задача была согласовано, добавь е в tasks.
        -title должен кратко описывать конкретное действие.
        -assignee указывай только если исполнитель явно указан.
        -Если исполнитель не указан, assignee = null 
        -deadline_text указывай только если срок явно указан.
        -Если срок не указан, deadline_text = null.
        -evidence должен содержать фрагмент текста, подтвердающий задачу.
        -summary должен быть кратким и содержать только основные решения встречи.
        -Сохрянай язык исходного теста. 
        """
    ),
    (
        "human",
        """
        Текст встречи:
        {text}
        
        Верни результат строго в указанной структуре.
        {format_instructions}
        """
    )
]).partial(
    format_instructions=meeting_parser.get_format_instructions()
)

meeting_chain = (
    meeting_prompt
    | ai_model
    | RunnableLambda(check_answer)
    | meeting_parser
)