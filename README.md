# Weather Forecast App

A **Python-based web application** that provides weather forecasts, UV index, humidity, sky conditions, and air quality index (AQI) for any location using OpenWeatherMap and Open-Meteo APIs. Built with **Streamlit** for interactive dashboards and **Plotly** for visualization.

---

## Table of Contents

1. [Features](#features)  
2. [Technologies](#technologies)  
3. [Installation](#installation)  
4. [Usage](#usage)  
5. [Project Structure](#project-structure)  
6. [Functionality](#functionality)  
7. [API Keys](#api-keys)  
8. [Notes](#notes)  
9. [License](#license)  

---

## Features

- Display 1–5 day weather forecasts.  
- Temperature visualization using Plotly line charts.  
- Sky condition display with icons per time slot.  
- Humidity visualization with categorized icons.  
- UV index forecast using Open-Meteo API with icons and categories.  
- Air Quality Index (AQI) display with icons and readable categories.  
- Interactive Streamlit interface: text input, slider, and selectbox.  
- Error handling for missing data or invalid locations.

---

## Technologies

- Python 3.10+  
- [Streamlit](https://streamlit.io/) for web interface  
- [Plotly](https://plotly.com/python/) for charts  
- [Pandas](https://pandas.pydata.org/) for data handling  
- OpenWeatherMap API (Weather & AQI)  
- Open-Meteo API (UV index)  

---

## Installation

1. Clone the repository:

```bash
git clone https://github.com/pedrohli-work/python-app7-WeatherForecast

Create a virtual environment (optional but recommended):

python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
Install dependencies:

pip install -r requirements.txt
Add your OpenWeatherMap API key in backend.py:

API_KEY = "YOUR_API_KEY_HERE"
Usage
Run the Streamlit app:

streamlit run main.py
Enter the city name in the Place input.

Select the number of forecast days (1–5) using the slider.

Choose the type of data to view: Temperature, Sky, Humidity, UV, or Air Quality.

Interact with the dashboard: see charts, icons, and detailed values for each time slot.

Project Structure
bash
Copiar
Editar
weather-forecast-app/
│
├─ images/                 # Icons for weather, humidity, UV, AQI
├─ backend.py              # Functions for fetching weather, UV, and AQI
├─ main.py                 # Streamlit frontend application
├─ requirements.txt        # Python dependencies
├─ README.md               # Project documentation
└─ .gitignore              # Git ignore rules

Functionality

Temperature
Extracts temperature values from API response.

Converts Kelvin or API units to Celsius if needed.

Plots a line chart with time on the X-axis and temperature on the Y-axis.

Sky
Extracts sky conditions (Clear, Clouds, Rain, Snow).

Maps conditions to icon images.

Groups forecast data per day and per time slot.

Displays icons with corresponding time captions in columns.

Humidity
Extracts humidity percentage values.

Categorizes humidity into Low (≤30%), Medium (31–60%), High (>60%).

Maps categories to icons.

Groups by day and displays icons + numeric values.

UV Index
Fetches UV data from Open-Meteo API (no key required).

Categorizes UV index: Low, Medium, High, Very High.

Displays icon + label for each upcoming hour.

Handles missing data gracefully with warnings.

Air Quality Index (AQI)
Fetches AQI from OpenWeatherMap API.

Maps numeric AQI (1–5) to human-readable categories (Good, Moderate, etc.) and icons.

Groups data per day and per time slot.

Displays icons with readable labels.

API Keys
OpenWeatherMap API key is required for weather and AQI.

Open-Meteo API does not require a key.

Notes
Ensure an active internet connection to fetch live data.

Streamlit columns handle multiple time slots visually.

Error handling is implemented for invalid city names, missing API responses, and network errors.