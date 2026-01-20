from agents.support.state import State
from pydantic import BaseModel, Field

from langchain.chat_models import init_chat_model
from agents.support.nodes.extractor.prompt import SYSTEM_PROMPT

class ContactInfo(BaseModel):
    name: str = Field(description="The full name of the person")
    email: str = Field(description="The email address of the person")
    phone: str = Field(description="The phone number of the person")
    age: int = Field(description="The age of the person")

llm = init_chat_model("openai:gpt-4o", temperature=0)
llm_with_structured_output = llm.with_structured_output(schema=ContactInfo)


def extractor(state: State):
    history = state["messages"]
    customer_name = state.get("customer_name", None)
    new_state = State = {}

    # El extractor solo se ejecuta si no tenemos el nombre del cliente 
    # o tenemos más de 10 mensajes en el historial
    # En caso contrario, devolvemos el nuevo estadWo
    if customer_name is None or len(history)> 10:
        schema = llm_with_structured_output.invoke([("system", SYSTEM_PROMPT)] + history)
        new_state["customer_name"] = schema.name
        new_state["phone"] = schema.phone
        new_state["my_age"] = schema.age
    return new_state