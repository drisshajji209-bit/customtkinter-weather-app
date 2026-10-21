# CustomTkinter Weather Dashboard

A desktop weather application built with **Python**, **CustomTkinter**, and the **OpenWeatherMap API**. Search for a city to view its current weather, then save cities as compact cards in a two-column dashboard.

## Features

- Search for a city and retrieve its current weather.
- Display temperature, weather description, humidity, wind speed, and a weather icon.
- Add multiple cities to a saved-cities section inside the main weather card.
- Display saved city cards side by side in two columns.
- Prevent the same city from being added more than once.
- Remove a saved city without removing the others.
- Show basic error messages for invalid city names and network/API problems.
- Use a dark interface with CustomTkinter.

> **Note:** Saved cities are kept in memory while the application is running. They are not saved between application launches.

## Built With

- [Python](https://www.python.org/)
- [CustomTkinter](https://customtkinter.tomschimansky.com/)
- [Requests](https://requests.readthedocs.io/)
- [Pillow](https://python-pillow.org/)
- [OpenWeatherMap Current Weather API](https://openweathermap.org/current)

## Requirements

- Python 3 installed
- An OpenWeatherMap API key
- An internet connection

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/YOUR-USERNAME/customtkinter-weather-dashboard.git
cd customtkinter-weather-dashboard
```

Replace `YOUR-USERNAME` with your GitHub username.

### 2. Create and activate a virtual environment (recommended)

**Windows PowerShell:**

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**macOS / Linux:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
python -m pip install customtkinter requests pillow
```

## Configure the OpenWeatherMap API Key

1. Create or sign in to an account at [OpenWeatherMap](https://openweathermap.org/) and get an API key.
2. In `main.py`, import `os` and read the key from an environment variable rather than hard-coding it.

Add this import with the other imports:

```python
import os
```

Set the key near the top of `main.py`:

```python
API_KEY = os.getenv("OPENWEATHERMAP_API_KEY", "")
```

In `get_weather()`, check that the key is configured before making the API request:

```python
if not API_KEY:
    self.desc_label.configure(
        text="Set OPENWEATHERMAP_API_KEY before running the app."
    )
    return
```

3. Set the environment variable in the same terminal session from which you will run the app.

**Windows PowerShell:**

```powershell
$env:OPENWEATHERMAP_API_KEY="your_api_key_here"
python main.py
```

**Windows Command Prompt:**

```bat
set OPENWEATHERMAP_API_KEY=your_api_key_here
python main.py
```

**macOS / Linux:**

```bash
export OPENWEATHERMAP_API_KEY="your_api_key_here"
python main.py
```

Replace `your_api_key_here` with your own key. Do not put your real API key in `main.py`, your README, screenshots, or a public GitHub commit.

## Run the Application

After installing the dependencies and setting the API key, run:

```bash
python main.py
```

If your Python file has a different name, replace `main.py` with that filename.

## How to Use

1. Enter a city name in the search field.
2. Click **Search** or press **Enter**.
3. Click **+ Add City** to save the displayed city's weather card.
4. Search for another city and add it. The new card appears beside the first one; more cards continue on additional rows.
5. Click **Remove** on a saved card to remove that city.

## Project Structure

```text
customtkinter-weather-dashboard/
├── main.py       # Main CustomTkinter application
├── README.md     # Project documentation
└── .gitignore    # Files that Git should ignore
```

## Troubleshooting

- **City not found:** Check the spelling and try the city name again.
- **API key error:** Verify that `OPENWEATHERMAP_API_KEY` is set in the terminal where you launch the app. Newly created API keys may take time to become active.
- **ModuleNotFoundError:** Activate your virtual environment and run the dependency installation command again.
- **Network error:** Check your internet connection and try again.
- **Weather icon missing:** The app may still display weather data if the icon image could not be downloaded.

## Future Improvements

- Persist saved cities between application launches.
- Add unit conversion between Celsius and Fahrenheit.
- Add forecasts and additional weather metrics.
- Improve loading indicators and error handling.

## Contributing

Suggestions and improvements are welcome. For larger changes, open an issue first to discuss what you would like to change.
