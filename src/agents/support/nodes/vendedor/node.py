from langchain.agents import create_agent

from agents.support.nodes.vendedor.tools import tools
from agents.support.nodes.vendedor.prompt import prompt_template

system_prompt = """
Eres un asistente de ventas que ayuda a los clientes a encontrar productos adecuados según sus necesidades y dar el clima de la ciudad

Tus tools son:
- get_products: para obtener los productos que ofreces en la tienda.
- get_weather: para obtener el clima actual de una ciudad dada.
"""

vendedor_node = create_agent(
    model="openai:gpt-4o-mini",
    tools=tools,
    system_prompt=system_prompt,
)
