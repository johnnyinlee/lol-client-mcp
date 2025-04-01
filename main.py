import functools
from typing import TypeVar, Callable, Awaitable, Any

import httpx
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("lol-client-mcp")

# Define a type variable for generic type hinting
T = TypeVar('T')

# Constants
DEFAULT_TIMEOUT = 3.0
LOL_CLIENT_HOST = "https://127.0.0.1:2999"


def with_timeout(func: Callable[..., Awaitable[T]]) -> Callable[..., Awaitable[T]]:
    """
    Decorator to handle timeout exceptions for async functions.
    """
    @functools.wraps(func)
    async def wrapper(*args: Any, **kwargs: Any) -> T:
        try:
            return await func(*args, **kwargs)
        except httpx.TimeoutException:
            return {
                "error": "Game has not started or connection failed.",
                "code": "TIMEOUT"
            }
        except httpx.ConnectError:
            return {
                "error": "Cannot connect to the game client. Please check if the game is running.",
                "code": "CONNECTION_ERROR"
            }
        except httpx.HTTPStatusError as e:
            return {
                "error": f"Server error: HTTP {e.response.status_code}",
                "code": "HTTP_ERROR",
                "status": e.response.status_code
            }
        except Exception as e:
            return {
                "error": f"An error occurred: {str(e)}",
                "code": "UNKNOWN_ERROR"
            }
    return wrapper


def get_lol_client():
    """
    Create an HTTP client for the League of Legends client.
    """
    return httpx.AsyncClient(
        base_url=LOL_CLIENT_HOST,
        verify="./certs/riotgames.pem",
        timeout=DEFAULT_TIMEOUT
    )



@mcp.tool()
@with_timeout
async def get_all_game_data() -> dict:
    """
    The Live League of Legends Client Data API has a number of endpoints
    that return a subset of the data returned by the /allgamedata endpoint.
    This endpoint is great for testing the Live Client Data API,
    but unless you actually need all the data from this endpoint,
    use one of the endpoints listed below that return a subset of the response.
    """
    async with get_lol_client() as client:
        response = await client.get("/liveclientdata/allgamedata")
        return response.json()


@mcp.tool()
@with_timeout
async def get_active_player() -> dict:
    """
    Get all data about the active player.
    """
    async with get_lol_client() as client:
        response = await client.get("/liveclientdata/activeplayer")
        return response.json()


@mcp.tool()
@with_timeout
async def get_active_player_name() -> str:
    """
    Returns the player name.
    """
    async with get_lol_client() as client:
        response = await client.get("/liveclientdata/activeplayername")
        return response.text


@mcp.tool()
@with_timeout
async def get_active_player_abilities() -> dict:
    """
    Get Abilities for the active player.
    """
    async with get_lol_client() as client:
        response = await client.get("/liveclientdata/activeplayerabilities")
        return response.json()


@mcp.tool()
@with_timeout
async def get_active_player_runes() -> dict:
    """
    Retrieve the full list of runes for the active player.
    """
    async with get_lol_client() as client:
        response = await client.get("/liveclientdata/activeplayerrunes")
        return response.json()


@mcp.tool()
@with_timeout
async def get_player_list() -> list[dict]:
    """
    Retrieve the list of heroes in the game and their stats.
    """
    async with get_lol_client() as client:
        response = await client.get("/liveclientdata/playerlist")
        return response.json()


@mcp.tool()
@with_timeout
async def get_player_scores(riot_id: str) -> dict:
    """
    Retrieve the list of the current scores for the player.
    """
    async with get_lol_client() as client:
        response = await client.get(f"/liveclientdata/playerscores?riotId={riot_id}")
        return response.json()


@mcp.tool()
@with_timeout
async def get_player_summoner_spells(riot_id: str) -> dict:
    """
    Retrieve the list of the summoner spells for the player.
    """
    async with get_lol_client() as client:
        response = await client.get(f"/liveclientdata/playersummonerspells?riotId={riot_id}")
        return response.json()


@mcp.tool()
@with_timeout
async def get_player_main_runes(riot_id: str) -> dict:
    """
    Retrieve the basic runes of any player.
    """
    async with get_lol_client() as client:
        response = await client.get(f"/liveclientdata/playermainrunes?riotId={riot_id}")
        return response.json()


@mcp.tool()
@with_timeout
async def get_player_items(riot_id: str) -> list[dict]:
    """
    Retrieve the list of items for the player.
    """
    async with get_lol_client() as client:
        response = await client.get(f"/liveclientdata/playeritems?riotId={riot_id}")
        return response.json()


@mcp.tool()
@with_timeout
async def get_event_data() -> dict:
    """
    Get a list of events that have occurred in the game.
    """
    async with get_lol_client() as client:
        response = await client.get("/liveclientdata/eventdata")
        return response.json()


@mcp.tool()
@with_timeout
async def get_game_stats() -> dict:
    """
    Basic data about the game.
    """
    async with get_lol_client() as client:
        response = await client.get("/liveclientdata/gamestats")
        return response.json()


if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='stdio')
    