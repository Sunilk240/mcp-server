# MCP Weather Service

A weather service built using Model-Context-Protocol (MCP) that provides current weather and forecasts for Indian cities using WeatherAPI.com.

## Prerequisites

- Python 3.13 or higher
- [uv](https://github.com/astral-sh/uv) package manager
- WeatherAPI.com API key
- Groq API key (for the chat interface)
- Claude for Desktop (for testing with Claude)

## Installation

1. Clone the repository:
```bash
git clone <your-repo-url>
cd mcp-server
```

2. Create a `.env` file in the project root with your API keys:
```env
# WeatherAPI.com API Key
WEATHER_API_KEY=your_weather_api_key_here

# Groq API Key
GROQ_API_KEY=your_groq_api_key_here
```

3. Install dependencies using uv:
```bash
uv pip install -e .
```

## Running the Service

### Development Mode
To run the weather service in development mode:
```bash
uv run mcp dev server/weather.py
```

### Install and Run
To install and run the service on desktop claude:
```bash
uv run mcp install server/weather.py
```

## Setting up weather.json
The `weather.json` configuration file is required for the chat interface.

1, Testing your server with Claude for Desktop:
   - Open VS Code and run:
     ```bash
     code $env:AppData\Claude\claude_desktop_config.json
     ```
   - Add the following configuration:
     ```json
     {
         "mcpServers": {
             "weather": {
                 "command": "uv",
                 "args": [
                     "--directory",
                     "C:\\ABSOLUTE\\PATH\\TO\\YOUR\\mcp-server",
                     "run",
                     "server/weather.py"
                 ]
             }
         }
     }
     ```
   - Replace `C:\\ABSOLUTE\\PATH\\TO\\YOUR\\mcp-server` with your actual project path

2. For Chat Interface (client.py):
   - The `weather.json` file should be in your `server` directory
   - Make sure it contains:
     ```json
     {
         "mcpServers": {
             "weather": {
                 "command": "uv",
                 "args": [
                     "--directory",
                     "C:\\ABSOLUTE\\PATH\\TO\\YOUR\\mcp-server",
                     "run",
                     "server/weather.py"
                 ]
             }
         }
     }
     ```
   - Replace `C:\\ABSOLUTE\\PATH\\TO\\YOUR\\mcp-server` with your actual project path

3. Restart Claude for Desktop after making changes

## Using the Chat Interface

Run the chat client to interact with the weather service:
```bash
python server/client.py
```

The chat interface supports:
- Getting current weather for any Indian city
- Getting 3-day weather forecasts
- Natural language queries about weather

Commands:
- Type 'exit' or 'quit' to end the conversation
- Type 'clear' to clear conversation history

## Features

- Current weather information:
  - Temperature in Celsius
  - Weather condition
  - Humidity
  - Wind speed
  - Last updated timestamp

- 3-day weather forecast:
  - Daily high and low temperatures
  - Weather conditions
  - Date-specific forecasts

## Project Structure

```
mcp-server/
├── server/
│   ├── weather.py      # Weather service implementation
│   ├── client.py       # Chat interface
│   └── weather.json    # MCP server configuration
├── .env               # API keys configuration
├── pyproject.toml     # Project dependencies
└── README.md         # This file
```

## API Keys

1. WeatherAPI.com:
   - Sign up at [WeatherAPI.com](https://www.weatherapi.com/)
   - Get your free API key
   - Add it to `.env` as `WEATHER_API_KEY`

2. Groq API:
   - Sign up at [Groq Console](https://console.groq.com/)
   - Get your API key
   - Add it to `.env` as `GROQ_API_KEY`

## Contributing

Feel free to submit issues and enhancement requests!


