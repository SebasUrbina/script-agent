import openai
import os
from pydantic import BaseModel
from typing import List, Optional
from time import sleep
from dotenv import load_dotenv
import pandas as pd
import json
load_dotenv()
from openai import OpenAI
client = OpenAI()

# Función para leer el archivo CSV de equipos
def cargar_equipos(file_path='equipos.csv'):
    return pd.read_csv(file_path)

def verificar_stock(nombre_equipo: str):
    equipos = cargar_equipos(file_path='equipos.csv')
    equipo = equipos[equipos['Nombre'].str.contains(nombre_equipo, case=False)]
    if not equipo.empty and equipo.iloc[0]['Stock'] > 0:
        return f"El equipo {nombre_equipo} está disponible con un stock de {equipo.iloc[0]['Stock']} unidades."
    elif not equipo.empty:
        return f"El equipo {nombre_equipo} está agotado."
    else:
        return f"No se encontró el equipo {nombre_equipo}."

tools = [
    {
        "type": "function",
        "function": {
            "name": "verificar_stock",
            "description": "Verifica que haya stock del smartphone consultado. Utiliza esta funcion solo cuando pregunten información sobre el stock de equipos o smartphones",
            "parameters": {
                "type": "object",
                "properties": {
                    "nombre_equipo": {
                        "type": "string",
                        "description": "Nombre del smartphone a buscar en stock"
                    },
                },
                "required": ["nombre_equipo"],
                "additionalProperties": False
            },
            "strict": True
        },
    }
]

class AgenteComercial():
    def __init__(self):
        openai.api_key = os.getenv("OPENAI_API_KEY")
        self.messages = [{"role": "system", "content": "You are a Generative AI Agent that recommend smartphones to a client."}]

    def call_openai(self, messages):
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            tools=tools
        )

        if (response.choices[0].finish_reason == "tool_calls"):
            print("Model made a tool call.")
            self.messages.append(response.choices[0].message)
            return self.handle_tool_response(response)
        
        elif response.choices[0].finish_reason  == "stop":
            print("Model respond directly to user")
            self.messages.append(response.choices[0].message)
            return self.handle_normal_response(response) 

    def handle_normal_response(self, response):
        return response.choices[0].message.content

    def handle_tool_response(self, response):

        tool_calls = response.choices[0].message.tool_calls
        if tool_calls:
            tool_call_id = tool_calls[0].id
            tool_call_nombre_equipo =   json.loads(response.choices[0].message.tool_calls[0].function.arguments)['nombre_equipo']
            
            stock_response = verificar_stock(tool_call_nombre_equipo)
            print(stock_response)
            self.messages.append({
                "role":"tool", 
                "tool_call_id":tool_call_id, 
                "content":stock_response
            })

            response = client.chat.completions.create(
                model="gpt-4o",
                messages=self.messages,
                tools=tools
            )

            return response.choices[0].message.content

    def start_chat(self):
        print("¡Bienvenido al agente comercial! Escribe 'salir' para terminar la conversación.")

        while True:
            user_input = input("User: ")

            # Verificar si el usuario quiere salir
            if user_input.lower() == 'salir':
                print("Agente Comercial: ¡Hasta luego!")
                break

            # Añadir el mensaje del usuario al contexto
            self.messages.append({"role": "user", "content": user_input})

            # Obtener la respuesta de OpenAI
            answer = self.call_openai(self.messages)

            # Añadir la respuesta al historial y mostrarla
            self.messages.append({"role": "assistant", "content": answer})
            print(f"Agente Comercial: {answer}")



if __name__=="__main__":

    agent = AgenteComercial() #Hola, ando buscando un equipo iphone 15 
    agent.start_chat()