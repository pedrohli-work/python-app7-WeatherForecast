from datetime import datetime
from collections import defaultdict
import importlib
import plotly.express as px
import streamlit as st
import pandas as pd
importlib.reload(pd)
from backend import get_data, get_aqi, get_uv_open_meteo


# Add title, text_input, slider, selectbox and subheader
st.title("Weather Forecast for the Next Days")
st.write("Type the city in the box above and press Enter to see the forecast.")
place = st.text_input("Place: ", placeholder="Type city name and press Enter")
days = st.slider("Forcast Days", min_value=1, max_value=5, 
                 help="Select the number of forcasted days")
option = st.selectbox("Select data to view", 
                      ("Temperature", "Sky", "Humidity", "UV", "Air Quality"))
st.subheader(f"{option} for the next {days} days in {place}")

# Only run if user provided a place
if place:
    try:
        # Fetch weather data (temperature, humidity, sky, uv, air quality.)
        filtered_data = get_data(place, days)

        # -------- TEMPERATURE OPTION --------
        if option == "Temperature":
            # Extract temperature values, divide by 10 to scale
            temperatures = [dict["main"]["temp"] / 10 for dict in filtered_data]
            # Extract corresponding date strings
            dates = [dict["dt_txt"] for dict in filtered_data]
            # Create a line plot using Plotly
            figure = px.line(x=dates, y=temperatures, labels={"x": "Date", "y": "Temperatures (C)"})
            # Display plot in Streamlit
            st.plotly_chart(figure)

        # -------- SKY OPTION --------
        elif option == "Sky":
            # Map sky conditions to image icons
            images = {"Clear": "images/clear.png", 
                    "Clouds": "images/cloud.png", 
                    "Rain": "images/rain.png", 
                    "Snow": "images/snow.png"}
            
            # Extract "main" sky conditions (Clear, Rain, etc.)
            sky_conditions = [dict["weather"][0]["main"] for dict in filtered_data]
            # Map each condition to its corresponding image path
            image_paths = [images[condition] for condition in sky_conditions]

            # Initialize dictionaries to group forecast data by day
            # defaultdict(list) automatically creates an empty list for a new key
            grouped_labels = defaultdict(list)
            grouped_images = defaultdict(list)

            # Iterate over each forecast entry with its index
            for i, d in enumerate(filtered_data):
                # Convert the API date-time string to a Python datetime object
                dt = datetime.strptime(d["dt_txt"], "%Y-%m-%d %H:%M:%S")
                # Format the datetime as a readable day label, e.g., "Tue, Aug 19"
                day_label = dt.strftime("%a, %b %d")
                # Format the datetime as a readable time label, e.g., "03:00"
                time_label = dt.strftime("%H:%M")

                # Append the time label to the list of times for the given day
                grouped_labels[day_label].append(time_label)
                # Append the corresponding sky image path for the given time
                grouped_images[day_label].append(image_paths[i])

            # Display the sky conditions, grouped by day
            for day, times in grouped_labels.items():
                # Display the day as a header in Streamlit
                st.write(day)
                # Create one column per forecast time for visual alignment
                cols = st.columns(len(times))
                # Iterate over each time slot and its column index
                for j, t in enumerate(times):
                    # Assign content to the specific column
                    with cols[j]:
                        # Display the sky condition image
                        st.image(grouped_images[day][j], width=30)
                        # Display the time as a caption below the image
                        st.caption(t)

        # -------- HUMIDITY OPTION --------
        elif option == "Humidity":
            # Extract humidity percentages
            humidities = [forecast["main"]["humidity"] for forecast in filtered_data]

            # Map humidity levels to image icons
            humidity_images = {
                "Low": "images/humidity_low.png",
                "Medium": "images/humidity_medium.png",
                "High": "images/humidity_high.png"
            }

            # Classify each humidity into Low, Medium, or High
            humidity_conditions = []
            for h in humidities:
                if h <= 30:
                    humidity_conditions.append("Low")
                elif h <= 60:
                    humidity_conditions.append("Medium")
                else:
                    humidity_conditions.append("High")

            # Convert conditions into corresponding image paths
            image_paths = [humidity_images[cond] for cond in humidity_conditions]

            # Group humidity by day
            grouped_labels = defaultdict(list)
            grouped_images = defaultdict(list)
            grouped_humidities = defaultdict(list)

            # Iterate over each forecast entry with index i and data d
            for i, d in enumerate(filtered_data):
                # Convert the date-time string into a Python datetime object
                dt = datetime.strptime(d["dt_txt"], "%Y-%m-%d %H:%M:%S")
                # Format the datetime object into a readable day label, e.g., "Tue, Aug 19"
                day_label = dt.strftime("%a, %b %d")
                # Format the datetime object into a readable time label, e.g., "03:00"
                time_label = dt.strftime("%H:%M")

                # Append the time label to the grouped labels dictionary for this day
                grouped_labels[day_label].append(time_label)
                # Append the corresponding humidity image path for this time
                grouped_images[day_label].append(image_paths[i])
                # Append the numeric humidity value for this time
                grouped_humidities[day_label].append(humidities[i])

            # Display grouped humidity levels per day
            for day, times in grouped_labels.items():
                # Write the day as a header
                st.write(day)
                # Create a set of columns equal to the number of time slots for the day
                cols = st.columns(len(times))
                # Iterate over each time label and its column index
                for j, t in enumerate(times):
                    # Assign content to the corresponding column
                    with cols[j]:
                        # Display the humidity image for this time slot
                        st.image(grouped_images[day][j], width=30)
                        # Display the time and humidity percentage as caption
                        st.caption(f"{t} ({grouped_humidities[day][j]}%)")

        # -------- UV OPTION --------
        elif option == "UV":
            try:
                # Fetch UV forecast data
                uv_data = get_uv_open_meteo(place)
                
                if not uv_data:
                    # Show warning if none
                    st.warning("No UV data available for this location.")
                else:
                    # Info banner
                    st.info("ℹ️ UV index for the next hours.")
                    
                    # Store image paths
                    uv_images = []
                    # Store labels with values
                    uv_labels = []
                    
                    # Iterate over UV data (time, index)
                    for time_str, uv in uv_data:
                        if uv <= 2:
                            category = "Low"
                            image = "images/uv_low.png"
                        elif uv <= 5:
                            category = "Medium"
                            image = "images/uv_moderate.png"
                        elif uv <= 7:
                            category = "High"
                            image = "images/uv_high.png"
                        else:
                            category = "Very High"
                            image = "images/uv_very_high.png"
                        
                        # Save results
                        uv_images.append(image)
                        uv_labels.append(f"{time_str} (UV {uv:.1f} - {category})")

                    # Create a set of Streamlit columns equal to the number of UV images
                    cols = st.columns(len(uv_images))
                    # Iterate over each column with its index
                    for i, col in enumerate(cols):
                        # Assign content to the current column
                        with col:
                            # Display the UV image for this time slot
                            st.image(uv_images[i], width=30)
                            # Display the corresponding time and UV category as a caption
                            st.caption(uv_labels[i])

            except Exception as e:
                st.error(f"An error occurred while fetching UV data: {e}")

        # -------- AIR QUALITY OPTION --------
        elif option == "Air Quality":
            try:
                # Fetch AQI data (hourly, days*8 entries)
                aqi_data = get_aqi(place)[:days*8]
                # Map AQI categories to images
                aqi_images = {
                    "Good": "images/aqi_good.png", 
                    "Moderate": "images/aqi_moderate.png", 
                    "Unhealthy": "images/aqi_unhealthy.png", 
                    "Very Unhealthy": "images/aqi_very_unhealthy.png", 
                    "Hazardous": "images/aqi_hazardous.png"
                }

                # Group AQI forecasts by day
                grouped_labels = defaultdict(list)
                grouped_images = defaultdict(list)

                # Enumerate over the filtered forecast data with index i and data d
                for i, d in enumerate(filtered_data):
                    # Convert the date-time string from the API into a Python datetime object
                    dt = datetime.strptime(d["dt_txt"], "%Y-%m-%d %H:%M:%S")
                    # Format the datetime object into a readable day label, e.g., "Tue, Aug 19 2025"
                    day_label = dt.strftime("%a, %b %d %Y")
                    # Format the datetime object into a readable time label, e.g., "03:00"
                    time_label = dt.strftime("%H:%M")

                    # Map AQI index to category
                    aqi = aqi_data[i]
                    if aqi == 1:
                        condition = "Good"
                        readable = "Good"
                    elif aqi == 2:
                        condition = "Moderate"
                        readable = "Moderate"
                    elif aqi == 3:
                        condition = "Unhealthy"
                        readable = "Unhealthy"
                    elif aqi == 4:
                        condition = "Very Unhealthy"
                        readable = "Very Unhealthy"
                    else:
                        condition = "Hazardous"
                        readable = "Hazardous"

                    # Save data per day
                    grouped_labels[day_label].append(f"{time_label} ({readable})")
                    grouped_images[day_label].append(aqi_images[condition])

                # Display AQI per day
                for day, times in grouped_labels.items():
                    # Write the day as a header
                    st.write(day)
                    # Create a set of columns equal to the number of time slots for the day
                    cols = st.columns(len(times))

                    # Iterate over each time label with its column index
                    for j, lbl in enumerate(times):
                        # Assign content to the corresponding column
                        with cols[j]:
                            # Display the AQI icon for this time slot
                            st.image(grouped_images[day][j], width=30)
                            # Display the time and AQI category as caption
                            st.caption(lbl)

            # Handle AQI errors
            except KeyError:
                st.write("That place does not exist.")
            except ValueError as ve:
                st.write(f"Error: {ve}")
            except Exception as e:
                st.write(f"An error occurred: {e}")


    except KeyError:
        st.write("That place does not exist.")
    except ValueError as ve:
        st.write(f"Error: {ve}")
    except Exception as e:
        st.write(f"An error occurred: {e}")
