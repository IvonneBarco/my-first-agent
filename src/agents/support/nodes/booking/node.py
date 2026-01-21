# Implementación pendiente del agente booking
from langgraph.graph import StateGraph, START, END
from langgraph.graph import MessagesState

def placeholder_node(state: MessagesState):
    """Nodo temporal mientras se implementa el agente booking"""
    return {"messages": []}

builder = StateGraph(MessagesState)
builder.add_node("placeholder", placeholder_node)
builder.add_edge(START, "placeholder")
builder.add_edge("placeholder", END)

booking_node = builder.compile()
