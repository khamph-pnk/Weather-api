#!/usr/bin/env python3
"""
Weather Forecast App with Colorful ASCII Art
Programmed by Jeff and Khamph
Supports 5 languages: English, Spanish, French, German, Japanese
"""

import requests
import json
from colorama import init, Fore, Back, Style
import os
import sys

# Initialize colorama for cross-platform colored terminal output
init(autoreset=True)

class WeatherApp:
    def __init__(self):
        self.api_key = "223cbc4ef9d3e64a1b0319e396cf0106"
        self.base_url = "http://api.openweathermap.org/data/2.5/weather"
        self.languages = {
            'en': 'English',
            'es': 'Spanish',
            'fr': 'French',
            'de': 'German',
            'ja': 'Japanese'
        }
        self.weather_messages = self.load_messages()
        self.current_lang = 'en'
    
    def load_messages(self):
        """Load multilingual messages"""
        return {
            'en': {
                'welcome': "🌤️ Weather Forecast App 🌤️",
                'select_lang': "Select language:",
                'enter_city': "Enter city name: ",
                'loading': "Fetching weather data...",
                'error': "Error: City not found or API error",
                'temp': "Temperature",
                'feels_like': "Feels like",
                'humidity': "Humidity",
                'pressure': "Pressure",
                'wind': "Wind Speed",
                'description': "Conditions",
                'goodbye': "Thank you for using our weather app!",
                'by': "Programmed by Jeff and Khamph"
            },
            'es': {
                'welcome': "🌤️ Aplicación de Pronóstico del Tiempo 🌤️",
                'select_lang': "Seleccione idioma:",
                'enter_city': "Ingrese nombre de la ciudad: ",
                'loading': "Obteniendo datos del tiempo...",
                'error': "Error: Ciudad no encontrada o error de API",
                'temp': "Temperatura",
                'feels_like': "Sensación térmica",
                'humidity': "Humedad",
                'pressure': "Presión",
                'wind': "Velocidad del viento",
                'description': "Condiciones",
                'goodbye': "¡Gracias por usar nuestra aplicación del tiempo!",
                'by': "Programado por Jeff y Khamph"
            },
            'fr': {
                'welcome': "🌤️ Application de Prévisions Météorologiques 🌤️",
                'select_lang': "Sélectionnez la langue:",
                'enter_city': "Entrez le nom de la ville: ",
                'loading': "Récupération des données météo...",
                'error': "Erreur: Ville non trouvée ou erreur API",
                'temp': "Température",
                'feels_like': "Ressenti",
                'humidity': "Humidité",
                'pressure': "Pression",
                'wind': "Vitesse du vent",
                'description': "Conditions",
                'goodbye': "Merci d'avoir utilisé notre application météo!",
                'by': "Programmé par Jeff et Khamph"
            },
            'de': {
                'welcome': "🌤️ Wettervorhersage-App 🌤️",
                'select_lang': "Sprache auswählen:",
                'enter_city': "Stadtname eingeben: ",
                'loading': "Wetterdaten werden abgerufen...",
                'error': "Fehler: Stadt nicht gefunden oder API-Fehler",
                'temp': "Temperatur",
                'feels_like': "Gefühlt wie",
                'humidity': "Luftfeuchtigkeit",
                'pressure': "Luftdruck",
                'wind': "Windgeschwindigkeit",
                'description': "Bedingungen",
                'goodbye': "Danke, dass Sie unsere Wetter-App verwenden!",
                'by': "Programmiert von Jeff und Khamph"
            },
            'ja': {
                'welcome': "🌤️ 天気予報アプリ 🌤️",
                'select_lang': "言語を選択:",
                'enter_city': "都市名を入力: ",
                'loading': "天気データを取得中...",
                'error': "エラー: 都市が見つからないかAPIエラー",
                'temp': "気温",
                'feels_like': "体感温度",
                'humidity': "湿度",
                'pressure': "気圧",
                'wind': "風速",
                'description': "状態",
                'goodbye': "天気アプリをご利用いただきありがとうございます！",
                'by': "JeffとKhamphによってプログラムされました"
            }
        }
    
    def display_banner(self):
        """Display colorful ASCII art banner"""
        banner = f"""
{Fore.CYAN}
╔══════════════════════════════════════════════════════════╗
║                                                          ║
║  {Fore.YELLOW}▒█░░▒█ █▀▀ █░░ █▀▀ █▀▀█ █▀▀▄ ▀▀█▀▀ █▀▀█ █▀▀▄{Fore.CYAN}        ║
║  {Fore.YELLOW}▒█▒█▒█ █▀▀ █░░ █░░ █░░█ █░░█ ░░█░░ █▄▄█ █░░█{Fore.CYAN}        ║
║  {Fore.YELLOW}▒█▄▀▄█ ▀▀▀ ▀▀▀ ▀▀▀ ▀▀▀▀ ▀░░▀ ░░▀░░ ▀░░▀ ▀▀▀░{Fore.CYAN}        ║
║                                                          ║
║  {Fore.GREEN}╔════════════════════════════════════════════════╗{Fore.CYAN}  ║
║  {Fore.GREEN}║        🌈 COLORFUL WEATHER FORECAST 🌈        ║{Fore.CYAN}  ║
║  {Fore.GREEN}╚════════════════════════════════════════════════╝{Fore.CYAN}  ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
{Style.RESET_ALL}
"""
        print(banner)
        print(f"{Fore.MAGENTA}{self.weather_messages[self.current_lang]['by']}{Style.RESET_ALL}\n")
    
    def select_language(self):
        """Let user select language"""
        print(f"{Fore.YELLOW}{self.weather_messages['en']['select_lang']}{Style.RESET_ALL}")
        for i, (code, name) in enumerate(self.languages.items(), 1):
            print(f"{Fore.CYAN}[{i}] {name} ({code}){Style.RESET_ALL}")
        
        while True:
            try:
                choice = int(input(f"{Fore.GREEN}Select (1-5): {Style.RESET_ALL}"))
                if 1 <= choice <= 5:
                    self.current_lang = list(self.languages.keys())[choice-1]
                    break
            except ValueError:
                print(f"{Fore.RED}Please enter a number 1-5{Style.RESET_ALL}")
    
    def get_weather_ascii(self, weather_id, temp):
        """Return ASCII art based on weather condition"""
        # Clear
        if weather_id == 800:
            return f"""
{Fore.YELLOW}    \\   /     {Fore.CYAN}☼
{Fore.YELLOW}     .-.      {self.get_temp_color(temp)}SUNNY{Style.RESET_ALL}
{Fore.YELLOW}  ― (   ) ―  
{Fore.YELLOW}     `-᾿      
{Fore.YELLOW}    /   \\     
"""
        # Clouds
        elif 801 <= weather_id <= 804:
            return f"""
{Fore.WHITE}     .--.    
{Fore.WHITE}  .-(    ).  {Fore.CYAN}☁{Style.RESET_ALL}
{Fore.WHITE} (___.__)__) {self.get_temp_color(temp)}CLOUDY{Style.RESET_ALL}
"""
        # Rain
        elif 500 <= weather_id <= 531:
            return f"""
{Fore.BLUE}    .-.
{Fore.BLUE}   (   ).   {Fore.CYAN}☂{Style.RESET_ALL}
{Fore.BLUE}  (___(__)  {self.get_temp_color(temp)}RAINY{Style.RESET_ALL}
{Fore.BLUE}   ‚ʻ‚ʻ‚ʻ
{Fore.BLUE}   ‚ʻ‚ʻ‚ʻ
"""
        # Snow
        elif 600 <= weather_id <= 622:
            return f"""
{Fore.CYAN}    .-.      {Fore.WHITE}❄{Style.RESET_ALL}
{Fore.CYAN}   (   ).    {self.get_temp_color(temp)}SNOWY{Style.RESET_ALL}
{Fore.CYAN}  (___(__)  
{Fore.CYAN}   *  *  *
{Fore.CYAN}   *  *  *
"""
        # Thunderstorm
        elif 200 <= weather_id <= 232:
            return f"""
{Fore.MAGENTA}    .-.     {Fore.YELLOW}⚡{Style.RESET_ALL}
{Fore.MAGENTA}   (   ).   {self.get_temp_color(temp)}STORM{Style.RESET_ALL}
{Fore.MAGENTA}  (___(__) 
{Fore.MAGENTA}  / / / /
{Fore.MAGENTA} / / / /
"""
        # Default
        else:
            return f"""
{Fore.GREEN}    .-.     
{Fore.GREEN}   (   ).   {Fore.CYAN}☁{Style.RESET_ALL}
{Fore.GREEN}  (___(__)  {self.get_temp_color(temp)}WEATHER{Style.RESET_ALL}
"""
    
    def get_temp_color(self, temp):
        """Return color based on temperature"""
        if temp < 0:
            return Fore.CYAN  # Freezing - Cyan
        elif temp < 10:
            return Fore.BLUE  # Cold - Blue
        elif temp < 20:
            return Fore.GREEN  # Cool - Green
        elif temp < 30:
            return Fore.YELLOW  # Warm - Yellow
        else:
            return Fore.RED  # Hot - Red
    
    def get_weather(self, city):
        """Fetch weather data from API"""
        try:
            print(f"\n{Fore.GREEN}{self.weather_messages[self.current_lang]['loading']}{Style.RESET_ALL}")
            
            params = {
                'q': city,
                'appid': self.api_key,
                'units': 'metric',
                'lang': self.current_lang
            }
            
            response = requests.get(self.base_url, params=params)
            data = response.json()
            
            if response.status_code == 200:
                return data
            else:
                print(f"{Fore.RED}{self.weather_messages[self.current_lang]['error']}: {data.get('message', 'Unknown error')}{Style.RESET_ALL}")
                return None
                
        except requests.exceptions.RequestException as e:
            print(f"{Fore.RED}Connection error: {e}{Style.RESET_ALL}")
            return None
    
    def display_weather(self, data):
        """Display weather information with formatting"""
        if not data:
            return
        
        city = data['name']
        country = data['sys']['country']
        temp = data['main']['temp']
        feels_like = data['main']['feels_like']
        humidity = data['main']['humidity']
        pressure = data['main']['pressure']
        wind_speed = data['wind']['speed']
        description = data['weather'][0]['description']
        weather_id = data['weather'][0]['id']
        
        # Display ASCII art
        ascii_art = self.get_weather_ascii(weather_id, temp)
        print(ascii_art)
        
        # Display weather information
        print(f"{Fore.CYAN}{'═' * 50}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}📍 {city}, {country}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'═' * 50}{Style.RESET_ALL}")
        
        print(f"{Fore.WHITE}{self.weather_messages[self.current_lang]['description']}: {Fore.GREEN}{description.title()}{Style.RESET_ALL}")
        
        temp_color = self.get_temp_color(temp)
        feels_color = self.get_temp_color(feels_like)
        
        print(f"{Fore.WHITE}{self.weather_messages[self.current_lang]['temp']}: {temp_color}{temp}°C{Style.RESET_ALL}")
        print(f"{Fore.WHITE}{self.weather_messages[self.current_lang]['feels_like']}: {feels_color}{feels_like}°C{Style.RESET_ALL}")
        print(f"{Fore.WHITE}{self.weather_messages[self.current_lang]['humidity']}: {Fore.BLUE}{humidity}%{Style.RESET_ALL}")
        print(f"{Fore.WHITE}{self.weather_messages[self.current_lang]['pressure']}: {Fore.MAGENTA}{pressure} hPa{Style.RESET_ALL}")
        print(f"{Fore.WHITE}{self.weather_messages[self.current_lang]['wind']}: {Fore.CYAN}{wind_speed} m/s{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'═' * 50}{Style.RESET_ALL}")
    
    def run(self):
        """Main application loop"""
        self.display_banner()
        self.select_language()
        
        print(f"\n{Fore.YELLOW}{self.weather_messages[self.current_lang]['welcome']}{Style.RESET_ALL}")
        
        while True:
            print(f"\n{Fore.CYAN}{'─' * 50}{Style.RESET_ALL}")
            city = input(f"\n{Fore.GREEN}{self.weather_messages[self.current_lang]['enter_city']}{Style.RESET_ALL}")
            
            if city.lower() in ['exit', 'quit', 'q']:
                print(f"\n{Fore.MAGENTA}{self.weather_messages[self.current_lang]['goodbye']}{Style.RESET_ALL}")
                break
            
            weather_data = self.get_weather(city)
            if weather_data:
                self.display_weather(weather_data)
            
            print(f"\n{Fore.YELLOW}Press Enter to check another city or type 'exit' to quit{Style.RESET_ALL}")

def main():
    """Main function"""
    app = WeatherApp()
    app.run()

if __name__ == "__main__":
    main()
