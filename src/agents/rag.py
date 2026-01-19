import random
from typing import TypedDict
from langgraph.graph import MessagesState
from langchain_core.messages import AIMessage
from langchain.chat_models import init_chat_model

llm = init_chat_model("openai:gpt-4o", temperature=0)
file_search_tools = {
    "type": "file_search",
    "vector_store_ids": ["vs_696aa449413c8191b40ac97651032d94"],
}

llm_with_tools = llm.bind_tools([file_search_tools])

class State(MessagesState):
    customer_name: str
    phone: str
    my_age: str

state: State = {}
customer_name = state.get("customer_name", None)
print(f"Customer name: {customer_name}")

from pydantic import BaseModel, Field
class ContactInfo(BaseModel):
    name: str = Field(description="The full name of the person")
    email: str = Field(description="The email address of the person")
    phone: str = Field(description="The phone number of the person")
    age: str = Field(description="The age of the person")

llm_with_structured_output = init_chat_model("openai:gpt-4o", temperature=0)
llm_with_structured_output = llm_with_structured_output.with_structured_output(schema=ContactInfo)

def extractor(state: State):
    history = state["messages"]
    customer_name = state.get("customer_name", None)
    new_state = State = {}

    # El extractor solo se ejecuta si no tenemos el nombre del cliente 
    # o tenemos más de 10 mensajes en el historial
    # En caso contrario, devolvemos el nuevo estadWo
    if customer_name is None or len(history)> 10:
        schema = llm_with_structured_output.invoke(history)
        new_state["customer_name"] = schema.name
        new_state["phone"] = schema.phone
        new_state["my_age"] = schema.age
    return new_state

def conversation(state: State):
    new_state = State = {}
    history = state["messages"]
    last_message = history[-1]
    customer_name = state.get('customer_name', 'Desconocido')
    system_message = f"El nombre del cliente es {customer_name}."
    ai_message = llm.invoke([("system", system_message), ("user", last_message.text)])
    new_state["messages"] = [ai_message]
    return new_state

from langgraph.graph import StateGraph, START, END

builder = StateGraph(State)
builder.add_node("conversation", conversation)
builder.add_node("extractor", extractor)

builder.add_edge(START, "extractor")
builder.add_edge("extractor", "conversation")
builder.add_edge("conversation", END)

agent = builder.compile()