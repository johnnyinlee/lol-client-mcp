# LoL Client MCP

An MCP (Model-Controller-Processor) server for accessing League of Legends client data. This server provides a collection of tools that communicate with the League of Legends Live Client Data API to retrieve in-game data.

## Overview

This project accesses real-time game data using the League of Legends game client's Live Client Data API. It utilizes the FastMCP framework to expose various endpoints as tools.

API information can be found at https://developer.riotgames.com/docs/lol.

## Installation and Usage

### Prerequisites

- Python 3.8 or higher
- [uv](https://github.com/astral-sh/uv) - Fast and reliable Python package manager
  - Installation: `pip install uv`
- League of Legends client installed

### Project Setup

1. Clone this repository:

```bash
git clone https://github.com/yourusername/lol-client-mcp.git
cd lol-client-mcp
```

2. Install required packages using uv:

```bash
uv pip install httpx fastmcp
```

### Running the MCP Server

To run directly:

```bash
python main.py
```

### Integration with Claude

There are two ways to use this with Claude:

#### 1. Claude Desktop Configuration

Add the following to your `claude_desktop_config.json` file:

```json
{
    "mcpServers": {
        "lol-client-mcp": {
            "command": "uv",
            "args": [
                "--directory",
                "C:\\ABSOLUTE\\PATH\\TO\\PARENT\\FOLDER\\lol-client-mcp",
                "run",
                "main.py"
            ]
        }
    }
}
```

**Important**: Replace `C:\\ABSOLUTE\\PATH\\TO\\PARENT\\FOLDER\\lol-client-mcp` with the actual path to your project.

#### 2. Using with Web Application

To connect the MCP server to the Claude web application:

1. Run the MCP server:
   ```bash
   python main.py
   ```

2. Configure the server connection in the Claude web interface:
   - Go to MCP settings at the bottom when starting a conversation
   - Select 'lol-client-mcp' and connect

## API Tools List

### Game Data

- `get_all_game_data()`: The Live League of Legends Client Data API has a number of endpoints that return a subset of the data returned by the /allgamedata endpoint. This endpoint is great for testing the Live Client Data API, but unless you actually need all the data from this endpoint, use one of the endpoints listed below that return a subset of the response.
- `get_game_stats()`: Basic data about the game.
- `get_event_data()`: Get a list of events that have occurred in the game.

### Active Player Data

- `get_active_player()`: Get all data about the active player.
- `get_active_player_name()`: Returns the player name.
- `get_active_player_abilities()`: Get Abilities for the active player.
- `get_active_player_runes()`: Retrieve the full list of runes for the active player.

### Player List and Individual Player Data

- `get_player_list()`: Retrieve the list of heroes in the game and their stats.
- `get_player_scores(riot_id)`: Retrieve the list of the current scores for the player.
- `get_player_summoner_spells(riot_id)`: Retrieve the list of the summoner spells for the player.
- `get_player_main_runes(riot_id)`: Retrieve the basic runes of any player.
- `get_player_items(riot_id)`: Retrieve the list of items for the player.

## Troubleshooting

- **Connection Error**: Check if the League of Legends client is running.
- **Timeout Error**: Verify that the game has actually started. This API does not work in the game lobby.

## Precautions

- This API only works when the League of Legends client is running and a game is in progress.
- Use in compliance with Riot Games API policies.

## License

All rights belong to Riot Games.