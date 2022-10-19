from fastapi import APIRouter
import requests
from API_DATA_RETRIEVE.my_sql_auth import my_sql_auth
from API_DATA_RETRIEVE.my_sql_proxy import my_sql_proxy
from API_DATA_RETRIEVE.utils.querys import *
from API_DATA_RETRIEVE.utils.pokemonAPI_evolve import get_evolution
from CREATE_DB_SCRIPT.load_data import load_trainers_pokemons_table

AUTH = my_sql_auth()
CONNECTOR = my_sql_proxy(AUTH)

router = APIRouter()


@router.put("/evolve", status_code=200)
def get_pokemons_by_field(trainer_name: str, pokemon_name: str):
    # handle if pokemon evolve is not on db - so we need to add it
    # SELECT_POKEMON_BY_NAME
    pokemon_evolve = get_evolution(pokemon_name)
    if (pokemon_name == pokemon_evolve):
        return ""
    requests.delete(
        f"http://localhost:8000/trainers?trainer_name={trainer_name}&pokemon_name={pokemon_name}")
    pokemon_info = CONNECTOR.execute_select_one_query(SELECT_POKEMON_BY_NAME, [
        pokemon_name])
    trainer_info = CONNECTOR.execute_select_one_query(SELECT_TRAINER_BY_NAME, [
        trainer_name])
    load_trainers_pokemons_table(
        CONNECTOR, trainer_info["trainer_id"], pokemon_info["pokemon_id"])
    return {"pokemon": pokemon_evolve, "trainer": trainer_name}
