import requests
from langchain_core.tools import tool

@tool("get_products", description="Obtiene la lista de productos disponibles desde la API de la tienda.")
def get_products():

    # Conectar con API externa (simulada aquí con datos estáticos)
    response = requests.get("https://api.escuelajs.co/api/v1/products")
    products = response.json()
    # return [product for product in products if product["price"] < price]
    return "".join([f"{product['title']} - ${product['price']}\n" for product in products])

@tool("get_weather", description="Obtiene el clima actual de una ciudad dada.")
def get_weather(city: str) -> str:
    # Llamada a una API de clima
    response = requests.get(f"https://geocoding-api.open-meteo.com/v1/search?name=bogota&count=1")
    data = response.json()
    latitude = data['results'][0]['latitude']
    longitude = data['results'][0]['longitude']
    response = requests.get(f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current_weather=true")
    data = response.json()
    response = f"El clima en {city} es {data['current_weather']['temperature']}°C con vientos de {data['current_weather']['windspeed']} km/h."
    return response

get_weather.invoke({"city": "Bogotá"})

tools = [get_products, get_weather]