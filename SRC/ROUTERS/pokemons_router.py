from fastapi import APIRouter, HTTPException, status
import requests
from PokeTracker.SRC.API_DATA_RETRIEVE.my_sql_auth import my_sql_auth
from PokeTracker.SRC.API_DATA_RETRIEVE.my_sql_proxy import my_sql_proxy
from PokeTracker.SRC.API_DATA_RETRIEVE.utils.querys import *

AUTH = my_sql_auth()
CONNECTOR = my_sql_proxy(AUTH)

router = APIRouter()


@router.get("/pokemons", status_code=200)
def get_pokemons_by_trainer(trainerName):
    try:
        result = CONNECTOR.execute_select_all_query(SELECT_POKEMONS_BY_TRAINERS, [
            trainerName])
        return {"pokemons": result}
    except requests.exceptions.HTTPError as err:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid trainer name"
        )


@router.get("/pokemons", status_code=200)
def get_pokemons_by_type(pokemonType):
    try:
        result = CONNECTOR.execute_select_all_query(SELECT_POKEMONS_BY_TYPE, [
            pokemonType])
        return {"pokemons": result}
    except requests.exceptions.HTTPError as err:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid pokemon type"
        )


@router.get("/pokemons/heaviest", status_code=200)
def get_pokemons_by_type():
    try:
        result = CONNECTOR.execute_select_one_query(
            SELECT_HEAVIEST_POKEMON, [])
        return {"pokemon": result}
    except requests.exceptions.HTTPError as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error"
        )


@router.get("/pokemons/popular", status_code=200)
def get_pokemons_by_type():
    try:
        result = CONNECTOR.execute_select_one_query(
            SELECT_POPULAR_POKEMON, [])
        return {"pokemon": result}
    except requests.exceptions.HTTPError as err:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error"
        )