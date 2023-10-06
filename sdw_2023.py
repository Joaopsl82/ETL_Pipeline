pip install openai # Instalar a API do ChatGPT

import requests, json, openai
import pandas as pd

# Utilize sua própria URL se quiser
sdw2023_api_url = ' https://sdw-2023-prd.up.railway.app'

df = pd.read_csv('sdw2023.csv')
user_ids = df['UserID'].tolist()
print(user_ids)

def get_user(id):
  response = requests.get(f'{sdw2023_api_url}/users/{id}')
  return response.json() if response.status_code == 200 else None

def update_user(user):
  response = requests.put(f'{sdw2023_api_url}/users/{user["id"]}', json=user)
  return True if response.status_code == 200 else False

def generate_ai_news(user):
  completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
      {
          "role": "system",
          "content": "Você é um especialista em marketing para venda de carros."
      },
      {
          "role": "user",
          "content": f"Crie uma mensagem para {user['name']} sobre a importância dos investimentos em carros (máximo de 100 caracteres)"
      }
      ]
  )
  return completion.choices[0].message.content.strip('\"')

users = [user for id in user_ids if (user := get_user(id)) is not None]
print(json.dumps(users, indent=2))

open_api_key = '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'

openai.api_key = open_api_key

for user in users:
  news = generate_ai_news(user)
  print(news)
  user['news'].append({
      "icon": "https://digitalinnovationone.github.io/santander-dev-week-2023-api/icons/credit.svg",
      "description": news
  })
  success = update_user(user)
  print(f'User {user["name"]} updated? {success}!')
  
