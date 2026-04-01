---
name: travel_outpost
description: Generates a pre-trip travel brief using real-time local info and advice.
---
# Travel Outpost (旅遊前哨站)

When a user asks to plan a trip or generate a pre-trip brief for a specific `{city}`, use the provided Python tools to fetch information and format exactly as requested.

## Prerequisites
Ensure required Python packages are installed:
```bash
pip install -r requirements.txt
```

## Tools Overview
- `tools/get_weather.py {city}`: Retrieves real-time weather and temperature for the destination.
- `tools/search_places.py "{city} 景點"`: Uses DuckDuckGo search to find top 3 local tourist attractions.
- `tools/get_advice.py`: Fetches a random travel or life advice as a reminder.

## Execution Steps

1. **Weather**: Run `python tools/get_weather.py {city}`. It will output a string like "18°C，Clear". Determine from the string if it is suitable for outdoor activities and add a small remark (e.g. 適合戶外活動).
2. **Attractions**: Run `python tools/search_places.py "{city} 景點"`. It will return a comma-separated list of attractions (e.g., "淺草寺、新宿御苑、秋葉原").
3. **Advice/Reminder**: Run `python tools/get_advice.py`. It returns an English advice slip. Translate or summarize it to a concise Chinese travel reminder, but also inject practical travel advice if sensible.

## Output Format

Combine the gathered information and generate a precise markdown output that matches the following template EXACTLY:

=== {city} 行前簡報 ===

[天氣]  {weather_string}，{weather_remark}

[景點]  {attractions_string}

[提醒]  {advice_string}

### Example Output

=== Tokyo 行前簡報 ===

[天氣]  18°C，Clear，適合戶外活動

[景點]  淺草寺、新宿御苑、秋葉原

[提醒]  無論去哪，記得帶上一份好心情！(備好 IC 卡，地鐵四通八達)
