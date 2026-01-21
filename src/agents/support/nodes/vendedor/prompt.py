from langchain_core.prompts import PromptTemplate
from datetime import date

template = """\
Eres un asistente de ventas que ayuda a los clientes a encontrar productos adecuados según sus necesidades y dar el clima de la ciudad
Recuerda que hoy es {today}.

Tus tools son:
- get_products: para obtener los productos que ofreces en la tienda.
- get_weather: para obtener el clima actual de una ciudad dada.
"""

today = date.today().strftime("%Y-%m-%d")

prompt_template = PromptTemplate.from_template(template)
prompt = prompt_template.format(today=today)
print(prompt)
