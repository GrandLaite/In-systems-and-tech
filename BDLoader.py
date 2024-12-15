import hashlib
import requests
import time
import psycopg2

public_key = "здесь были данные"
private_key = "здесь были данные"

ts = str(time.time())
hash_value = hashlib.md5(f"{ts}{private_key}{public_key}".encode()).hexdigest()

limit = 100
offset = 0  

connection = psycopg2.connect(
    dbname="marvel",
    user="postgres", 
    password="1",     
    host="localhost", 
    port="5432"       
)
cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS characters (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT,
    thumbnail TEXT
)
""")
connection.commit()

while True:
    url = f"https://gateway.marvel.com:443/v1/public/characters?ts={ts}&apikey={public_key}&hash={hash_value}&limit={limit}&offset={offset}"
    
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        
        results = data["data"]["results"]
        if not results:
            print("Все данные загружены.")
            break
        
        for char in results:
            char_id = char["id"]
            name = char["name"]
            description = char["description"]
            thumbnail = f"{char['thumbnail']['path']}.{char['thumbnail']['extension']}"  # Генерация URL изображения
            
            cursor.execute("""
            INSERT INTO characters (id, name, description, thumbnail)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (id) DO NOTHING
            """, (char_id, name, description, thumbnail))
        
        connection.commit()
        print(f"Данные с offset={offset} успешно сохранены.")
        
        offset += limit
    else:
        print(f"Error {response.status_code}: {response.text}")
        break

cursor.close()
connection.close()
