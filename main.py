import aiohttp
import asyncio
import more_itertools
import datetime
from pydantic import BaseModel
from models import Character, init_orm, close_orm, Session

CHUNK = 10

class CharacterSchema(BaseModel):
    birth_year: str
    eye_color: str
    films: str
    gender: str
    hair_color: str
    height: str
    homeworld: str
    mass: str
    name: str
    skin_color: str
    species: str
    starships: str
    vehicles: str
    

async def get_people(person_id, http_session):
    url = f"https://swapi.dev/api/people/{person_id}/"
    http_response = await http_session.get(url)
    json_data = await http_response.json()
    return json_data


async def fetch_links_data(links, http_session):
    results = []
    for link in links:
        http_response = await http_session.get(link)
        json_data = await http_response.json()
        if "title" in json_data:
            results.append(json_data["title"])
        else:
            results.append(json_data["name"])

    return 'n/a' if not results else ", ".join(results) 


def validate_json(json_data, schema_cls):
    schema_obj = schema_cls(**json_data)    
    return schema_obj.model_dump(exclude_unset=True) 

async def insert_people(json_list):
    async with aiohttp.ClientSession() as http_session:
        validated_data = []
        for item in json_list:
            if len(item) <= 1:
                continue
            item["films"] = await fetch_links_data(item["films"], http_session)
            item["species"] = await fetch_links_data(item["species"], http_session) 
            item["starships"] = await fetch_links_data(item["starships"], http_session) 
            item["vehicles"] = await fetch_links_data(item["vehicles"], http_session)
            item["homeworld"] = await fetch_links_data([item["homeworld"]], http_session)

            validated_data.append(validate_json(item, CharacterSchema))

            async with Session() as session:
                characters = [Character(**data) for data in validated_data]
                session.add_all(characters)
                await session.commit()


async def main():
    await init_orm()

    async with aiohttp.ClientSession() as http_session:
        for i_list in more_itertools.chunked(range(1, 5), CHUNK):
            coros = [get_people(person_id, http_session) for person_id in i_list]
            result = await asyncio.gather(*coros)
            await insert_people(result) 

        tasks = asyncio.all_tasks()
        task_main = asyncio.current_task()
        tasks.remove(task_main)
        await asyncio.gather(*tasks)

    await close_orm()


start = datetime.datetime.now()
asyncio.run(main())
print(datetime.datetime.now() - start)
