import requests
from tabulate import tabulate
import asyncio


async def get_weather(city):
    # Retrieve weather information for a specific city
    api_key = "2nPhryFZQP2GRSGdgaRojCLs3xwK5GOv"
    base_url = "http://dataservice.accuweather.com"
    # Get the location key for the city
    location_url = f"{base_url}/locations/v1/cities/search"
    location_params = {
        "apikey": api_key,
        "q": city
    }
    try:
        location_response = requests.get(location_url, params=location_params)
        location_response.raise_for_status()
        location_data = location_response.json()

        if location_data:
            location_key = location_data[0]["Key"]
            weather_url = f"{base_url}/currentconditions/v1/{location_key}"
            weather_params = {
                "apikey": api_key,
                "details": True
            }

            weather_response = requests.get(weather_url, params=weather_params)
            weather_response.raise_for_status()
            weather_data = weather_response.json()

            if weather_data:
                weather_info = [
                    ["City", city],
                    ["Temperature (C)", weather_data[0]["Temperature"]["Metric"]["Value"]],
                    ["Humidity (%)", weather_data[0]["RelativeHumidity"]],
                    ["Description", weather_data[0]["WeatherText"]]
                ]

                return weather_info
            else:
                print("No weather data available.")
                return None
        else:
            print(f"No location found for city: {city}")
            return None

    except requests.exceptions.RequestException as e:
        print(f"Error occurred while fetching weather data: {e}")
        return None


class WeatherBot:
    def __init__(self):
        self.cities = []

    async def add_city(self, city):
        # Add a city to the list of cities
        if city not in self.cities:
            self.cities.append(city)
        return city


    async def display_weather(self):
        # Display weather information for all cities
        weather_data = []
        for city in self.cities:
            weather = await get_weather(city)
            weather_data.append(weather)
        print(tabulate(weather_data, headers=["City", "Temperature (C)", "Humidity (%)", "Description"], tablefmt="grid"))

    async def run(self):
        await self.display_weather()

    async def main(self):
        bot = WeatherBot()
        await bot.add_city("Almere")
        await bot.add_city("Kharkiv")
        await bot.add_city("London")
        await bot.run()


if __name__ == '__main__':
    asyncio.run(WeatherBot().main())
