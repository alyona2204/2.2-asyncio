import sqlite3
import aiohttp
import asyncio

# Асинхронная функция для выгрузки данных персонажей из API
async def fetch_person(session, url):
    async with session.get(url) as response:
        person = await response.json()

        films = ""
        for film in person['films']:
            async with session.get(film) as film_response:
                film_data = await film_response.json()
                films += film_data['title'] + ","

        species = ""
        for specie in person['species']:
            async with session.get(specie) as specie_response:
                specie_data = await specie_response.json()
                species += specie_data['name'] + ","

        starships = ""
        for starship in person['starships']:
            async with session.get(starship) as starship_response:
                starship_data = await starship_response.json()
                starships += starship_data['name'] + ","

        vehicles = ""
        for vehicle in person['vehicles']:
            async with session.get(vehicle) as vehicle_response:
                vehicle_data = await vehicle_response.json()
                vehicles += vehicle_data['name'] + ","

        return {
            'id': person['id'],
            'birth_year': person['birth_year'],
            'eye_color': person['eye_color'],
            'films': films[:-1],
            'gender': person['gender'],
            'hair_color': person['hair_color'],
            'height': person['height'],
            'homeworld': person['homeworld'],
            'mass': person['mass'],
            'name': person['name'],
            'skin_color': person['skin_color'],
            'species': species[:-1],
            'starships': starships[:-1],
            'vehicles': vehicles[:-1]
        }

# Асинхронная функция для загрузки данных в базу данных
async def load_to_db(data):
    conn = sqlite3.connect('mydatabase.db')
    cursor = conn.cursor()

    for item in data:
        cursor.execute("INSERT INTO mytable (id, birth_year, eye_color, films, gender, hair_color, \
            height, homeworld, mass, name, skin_color, species, starships, vehicles) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
            (item['id'], item['birth_year'], item['eye_color'], item['films'], item['gender'], \
            item['hair_color'], item['height'], item['homeworld'], item['mass'], item['name'], \
            item['skin_color'], item['species'], item['starships'], item['vehicles']))

    conn.commit()
    conn.close()

# Асинхронная функция для выгрузки и загрузки данных
async def main():
    async with aiohttp.ClientSession() as session:
        tasks = []
        for i in range(1, 11):
            url = f"https://swapi.dev/api/people/{i}/"
            task = asyncio.ensure_future(fetch_person(session, url))
            tasks.append(task)

        results = await asyncio.gather(*tasks)

        # Запуск асинхронной загрузки данных в базу данных
        await load_to_db(results)

# Запуск асинхронной выгрузки и загрузки данных
asyncio.run(main())