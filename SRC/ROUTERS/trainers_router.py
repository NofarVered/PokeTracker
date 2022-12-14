from fastapi import APIRouter, HTTPException, Request, status
from API_DATA_RETRIEVE.my_sql_proxy import CONNECTOR
from API_DATA_RETRIEVE.utils.querys import *
from CREATE_DB_SCRIPT.queries.insert_querys import INSERT_INTO_TRAINERS_INFO
from CREATE_DB_SCRIPT.services.id_manager import *


router = APIRouter()


@router.get("/trainers", status_code=200)
def get_trainers_by_pokemon(pokemon_name: str):
    try:
        result = CONNECTOR.execute_select_all_query(SELECT_TRAINERS_BY_POKEMON, [
            pokemon_name])
        return {"trainers": result}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Exeception occured:{}".format(e)
        )


@router.post("/trainers", status_code=201)
async def adding_trainer(request: Request):
    try:
        req = await request.json()
        trainer_id = id_encoding(req["name"], req["town"])
        CONNECTOR.execute_insert_query(INSERT_INTO_TRAINERS_INFO, [
            req["name"], req["town"], trainer_id])
        return {"name": req["name"],
                "town": req["town"], "trainer id": trainer_id}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Exeception occured:{}".format(e)
        )


@router.delete("/trainers", status_code=204)
def remove_pokemon_of_trainer(pokemon_name: str, trainer_name: str):
    try:
        pokemon_info = CONNECTOR.execute_select_one_query(SELECT_POKEMON_BY_NAME, [
            pokemon_name])
        trainer_info = CONNECTOR.execute_select_one_query(SELECT_TRAINER_BY_NAME, [
            trainer_name])
        print(pokemon_info["pokemon_id"])
        print(trainer_info["trainer_id"])
        CONNECTOR.execute_insert_query(DELETE_POKEMON_OF_TRAINER, [
            trainer_info["trainer_id"], pokemon_info["pokemon_id"]])
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Exeception occured:{}".format(e)
        )
