import asyncio
import aiohttp
from more_itertools import chunked

from models import init_orm, SwapiPeople, Session

MAX_REQUEST = 10


async def get_people(person_id, http_session):
    async with http_session.get(f"https://swapi.dev/api/people/{person_id}/") as response:
        return await response.json()


async def get_data(url, http_session):
    async with http_session.get(url) as response:
        return await response.json()


async def process_person(person_data, http_session):
    films = await asyncio.gather(*[get_data(film_url, http_session) for film_url in person_data['films']])
    species = await asyncio.gather(*[get_data(species_url, http_session) for species_url in person_data['species']])
    starships = await asyncio.gather(
        *[get_data(starship_url, http_session) for starship_url in person_data['starships']])
    vehicles = await asyncio.gather(*[get_data(vehicle_url, http_session) for vehicle_url in person_data['vehicles']])
    homeworld = await get_data(person_data['homeworld'], http_session)

    return {
        'id': int(person_data['url'].split('/')[-2]),
        'birth_year': person_data['birth_year'],
        'eye_color': person_data['eye_color'],
        'films': ', '.join([film['title'] for film in films]),
        'gender': person_data['gender'],
        'hair_color': person_data['hair_color'],
        'height': person_data['height'],
        'homeworld': homeworld['name'],
        'mass': person_data['mass'],
        'name': person_data['name'],
        'skin_color': person_data['skin_color'],
        'species': ', '.join([s['name'] for s in species]) if species else 'Unknown',
        'starships': ', '.join([starship['name'] for starship in starships]),
        'vehicles': ', '.join([vehicle['name'] for vehicle in vehicles])
    }


async def insert(processed_data):
    async with Session() as session:
        session.add(SwapiPeople(**processed_data))
        await session.commit()


async def main():
    await init_orm()
    async with aiohttp.ClientSession() as http_session:
        all_people = await get_people('', http_session)
        total_count = all_people['count']

        tasks = []
        for people_id_chunk in chunked(range(1, total_count + 1), MAX_REQUEST):
            coros = [get_people(i, http_session) for i in people_id_chunk]
            chunk_results = await asyncio.gather(*coros)

            for person_data in chunk_results:
                if isinstance(person_data, dict) and 'name' in person_data:
                    processed_data = await process_person(person_data, http_session)
                    task = asyncio.create_task(insert(processed_data))
                    tasks.append(task)

        await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(main())