from typing import TypedDict
from langgraph.graph import MessagesState
from langchain_core.messages import AIMessage

class State(MessagesState):
    customer_name: str
    my_age: int

state: State = {}
customer_name = state.get("customer_name", None)
print(f"Customer name: {customer_name}")

def node_1(state: State):
    if state.get("customer_name") is None:
        return {
            "customer_name": "Alice"
        }
    else:
        ai_msg = AIMessage(content="Hello, Message from the AI!")
        return {
            "messages": [ai_msg]
        }

from langgraph.graph import StateGraph, START, END

builder = StateGraph(State)
builder.add_node("node_1", node_1)

builder.add_edge(START, "node_1")
builder.add_edge("node_1", END)

agent = builder.compile()