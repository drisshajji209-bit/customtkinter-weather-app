import io
import customtkinter as ctk
from PIL import Image
import requests
import os

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

API_KEY = "ADD_YOUR_OPENWEATHERMAP_API_KEY_HERE"  # Replace with your OpenWeatherMap API key
IPGEO_API_KEY = "ADD_YOUR_IPGEOLOCATION_API_KEY_HERE"  # Replace with your IP Geolocation API key

class WeatherApp(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("Modern Weather App")
        self.geometry("400x520")
        self.resizable(True, True)

        # Track currently fetched weather data temporarily before adding
        self.current_city_data = None
        # List to store all saved cities data
        self.saved_cities = []

        # Title Label
        self.title_label = ctk.CTkLabel(
            self, text="Weather Lookup", font=("Arial", 22, "bold")
        )
        self.title_label.pack(pady=(20, 10))

        # Search Frame
        self.search_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.search_frame.pack(pady=10, padx=20, fill="x")

        self.city_entry = ctk.CTkEntry(
            self.search_frame,
            placeholder_text="Enter city name...",
            border_width=2,
            border_color="#007BFF",
            width=250,
            height=30,
            corner_radius=15,
            fg_color="#1E1E1E",
            text_color="white",
        )
        self.city_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.city_entry.bind("<Return>", lambda event: self.get_weather())

        self.search_btn = ctk.CTkButton(
            self.search_frame,
            text="Search",
            width=80,
            corner_radius=15,
            fg_color="#007BFF",
            hover_color="#0056b3",
            command=self.get_weather,
        )
        self.search_btn.pack(side="right")

        # Weather Card Container (Main Page)
        self.card_frame = ctk.CTkFrame(
            self,
            corner_radius=15,
            fg_color="#1E1E1E",
            border_width=2,
            border_color="#007BFF",
        )
        self.card_frame.pack(pady=15, padx=20, fill="both", expand=True)

        self.city_label = ctk.CTkLabel(
            self.card_frame, text="--", font=("Arial", 20, "bold")
        )
        self.city_label.pack(pady=(20, 5))

        self.icon_label = ctk.CTkLabel(self.card_frame, text="")
        self.icon_label.pack(pady=5)

        self.temp_label = ctk.CTkLabel(
            self.card_frame, text="--°C", font=("Arial", 36, "bold")
        )
        self.temp_label.pack(pady=5)

        self.desc_label = ctk.CTkLabel(
            self.card_frame, text="--", font=("Arial", 14, "italic")
        )
        self.desc_label.pack(pady=5)

        self.details_frame = ctk.CTkFrame(
            self.card_frame, fg_color="transparent"
        )
        self.details_frame.pack(pady=15, fill="x", padx=20)

        self.humidity_label = ctk.CTkLabel(
            self.details_frame, text="Humidity: --%", font=("Arial", 12)
        )
        self.humidity_label.pack(side="left", expand=True)

        self.wind_label = ctk.CTkLabel(
            self.details_frame, text="Wind: -- m/s", font=("Arial", 12)
        )
        self.wind_label.pack(side="right", expand=True)

        # Bottom Buttons Frame
        self.buttons_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.buttons_frame.pack(side="bottom", fill="x", pady=(0, 15), padx=20)

        self.city_btn = ctk.CTkButton(
            self.buttons_frame,
            text="+ Add City",
            width=150,
            height=32,
            corner_radius=15,
            fg_color="#007BFF",
            hover_color="#0056b3",
            command=self.add_city_button,
        )
        self.city_btn.pack(side="top", anchor="center")

        self.return_btn = ctk.CTkButton(
            self.buttons_frame,
            text="Return >",
            width=70,
            height=30,
            corner_radius=15,
            fg_color="#007BFF",
            hover_color="#0056b3",
            command=self.return_button,
        )

        self.location_btn = ctk.CTkButton(
            self.buttons_frame,
            text="Use My Location",
            width=150,
            height=32,
            corner_radius=15,
            fg_color="#2b2b2b",
            hover_color="#404040",
            command=self.get_my_location,
        )
        self.location_btn.pack(
            side="top",
            anchor="center",
            pady=10,
            padx=5
        )

    def get_my_location(self):
        self.desc_label.configure(text="Detecting your location...")
        self.update_idletasks()

        if not IPGEO_API_KEY:
            self.desc_label.configure(text="Location API key is missing.")
            return

        try:
            response = requests.get(
                "https://api.ipgeolocation.io/v3/ipgeo",
                params={"apiKey": IPGEO_API_KEY},
                timeout=15,
            )
            response.raise_for_status()
            data = response.json()

            location = data.get("location", {})
            city = location.get("city")
            country = location.get("country_code2")

            if not city:
                self.desc_label.configure(text="Could not detect your city.")
                return

            search_city = f"{city},{country}" if country else city
            self.city_entry.delete(0, "end")
            self.city_entry.insert(0, search_city)
            self.get_weather()

        except requests.exceptions.RequestException as error:
            print("Location API error:", error)
            self.desc_label.configure(
                text="Could not connect to location service."
            )

        except ValueError as error:
            print("Invalid API response:", error)
            self.desc_label.configure(text="Invalid location response.")

    def get_weather(self):
        city = self.city_entry.get().strip()
        if not city:
            self.desc_label.configure(text="Please enter a city name!")
            return

        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

        try:
            response = requests.get(url)
            data = response.json()

            if response.status_code == 200:
                city_name = data["name"]
                country = data["sys"]["country"]
                temp = round(data["main"]["temp"])
                description = data["weather"][0]["description"].title()
                humidity = data["main"]["humidity"]
                wind_speed = data["wind"]["speed"]
                icon_code = data["weather"][0]["icon"]

                # Fetch Icon Image
                icon_url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"
                icon_response = requests.get(icon_url)
                pil_img = Image.open(io.BytesIO(icon_response.content))
                ctk_img = ctk.CTkImage(
                    light_image=pil_img, dark_image=pil_img, size=(50, 50)
        
                )

                small_img = ctk.CTkImage(
                    light_image=pil_img, dark_image=pil_img, size=(25, 25)
                )

                # Save current data payload
                self.current_city_data = {
                    "city": f"{city_name}, {country}",
                    "temp": f"{temp}°C",
                    "desc": description,
                    "humidity": f"Humidity: {humidity}%",
                    "wind": f"Wind: {wind_speed} m/s",
                    "img": ctk_img,
                    "small_img": small_img,
                }

                # Update Main Page UI
                self.city_label.configure(text=self.current_city_data["city"])
                self.temp_label.configure(text=self.current_city_data["temp"])
                self.desc_label.configure(text=self.current_city_data["desc"])
                self.humidity_label.configure(
                    text=self.current_city_data["humidity"]
                )
                self.wind_label.configure(text=self.current_city_data["wind"])
                self.icon_label.configure(image=ctk_img)

            elif data.get("cod") == "404":
                self.desc_label.configure(text="City not found!")
        except requests.exceptions.RequestException:
            self.desc_label.configure(text="Network Error!")

            

    def add_city_button(self):
        if not self.current_city_data:
            return  # Don't add if no valid city searched yet

        # Avoid duplicates if the city is already in saved list
        if not any(
            c["city"] == self.current_city_data["city"]
            for c in self.saved_cities
        ):
            self.saved_cities.append(self.current_city_data)

        # Hide Main Card & Search
        self.card_frame.pack_forget()
        self.search_frame.pack_forget()

        # Create Frame 2 (Scrollable container to list added cities)
        if hasattr(self, "frame2") and self.frame2.winfo_exists():
            self.frame2.destroy()

        self.frame2 = ctk.CTkScrollableFrame(
            self,
            corner_radius=15,
            fg_color="#1E1E1E",
            border_width=2,
            border_color="#007BFF",
        )
        self.frame2.pack(pady=15, padx=20, fill="both", expand=True)

        # Render each saved city as a mini card inside Frame 2
        for data in self.saved_cities:
            card = ctk.CTkFrame(
                self.frame2, fg_color="#2b2b2b", corner_radius=10
            )
            card.pack(pady=8, padx=10, fill="x")

            # Left side: City & Temp
            lbl_city = ctk.CTkLabel(
                card, text=data["city"], font=("Arial", 16, "bold")
            )
            lbl_city.pack(anchor="w", padx=15, pady=(10, 2))

            lbl_temp = ctk.CTkLabel(
                card, text=data["temp"], font=("Arial", 20, "bold")
            )
            lbl_temp.pack(anchor="w", padx=15)

            lbl_desc = ctk.CTkLabel(
                card, text=data["desc"], font=("Arial", 12, "italic")
            )
            lbl_desc.pack(anchor="w", padx=15, pady=(2, 10))

            add_button = ctk.CTkButton(
                card, text="Add", corner_radius=10, fg_color="#075cef", width=80, command=lambda d=data: self.add_city(d)
            )
            add_button.pack(side="right", padx=15, pady=10)

            self.remove_button = ctk.CTkButton(
                card, text="Remove", corner_radius=10, fg_color="#c50202", width=80, command=lambda d=data: self.remove_city(d)
            )
            self.remove_button.pack(side="right", padx=5, pady=10)

            self.error_label = ctk.CTkLabel(
                self.frame2, text="", font=("Arial", 10), text_color="red"
            )
            self.error_label.pack(anchor="w", padx=15, pady=(2, 10))

            # Weather Icon on right side of card
            icon_lbl = ctk.CTkLabel(card, text="", image=data["img"])
            icon_lbl.place(relx=0.8, rely=0.5, anchor="center")

        # Show Return Button
        self.return_btn.pack(side="right", padx=(0, 5))

    def return_button(self):
        if hasattr(self, "frame2") and self.frame2.winfo_exists():
            self.frame2.destroy()
            self.return_btn.pack_forget()
            self.search_frame.pack(pady=10, padx=20, fill="x")
            self.card_frame.pack(pady=15, padx=20, fill="both", expand=True)

    def add_city(self, city_data):
        # Avoid duplicates if the city is already in saved list
        if not any(c["city"] == city_data["city"] for c in self.saved_cities):
            self.saved_cities.append(city_data)
            self.counter = len(self.saved_cities)
            self.add_city_button_counter = 0

        elif self.add_city_button:
            self.new_city_card = ctk.CTkFrame(
                self.card_frame, fg_color="#2b2b2b",
                  corner_radius=15,
                  border_width=2,
                    border_color="#007BFF",
        
            )
            self.new_city_card.pack(side="left", pady=8, padx=10)
            self.new_city_card_count = getattr(self, "new_city_card_count", 0) + 1
            if self.new_city_card_count == 3:
                self.geometry("500x600")

            self.error_label.configure(text="City added successfully!", text_color="#007BFF")


            lbl_city2 = ctk.CTkLabel(
                            self.new_city_card, text=city_data["city"], corner_radius=15, font=("Arial", 13, "bold")
                        )
            lbl_city2.pack(anchor="w", padx=10, pady=3)
            
            lbl_temp2 = ctk.CTkLabel(
                            self.new_city_card, text=city_data["temp"], corner_radius=30, font=("Arial", 12, "bold")
                        )
            lbl_temp2.pack(anchor="w", padx=10, pady=2)
            
            lbl_desc2 = ctk.CTkLabel(
                            self.new_city_card, text=city_data["desc"], corner_radius=30, font=("Arial", 10, "italic")
                        )
            lbl_desc2.pack(anchor="w", padx=10, pady=10)

        
            icon_lbl2 = ctk.CTkLabel(self.new_city_card, width=5, height=5, bg_color="transparent", text="", image=city_data["small_img"])
            icon_lbl2.place(relx=0.8, rely=0.6, anchor="center")

        elif self.add_city_button_counter == 2:
            
            self.new_city_card = ctk.CTkFrame(
                self.card_frame, fg_color="#2b2b2b",
                  corner_radius=15,
                  border_width=2,
                    border_color="#007BFF",
        
            )
            self.new_city_card.pack(side="left", pady=8, padx=10)

            self.error_label.configure(text="City added successfully!", text_color="#007BFF")


            lbl_city2 = ctk.CTkLabel(
                            self.new_city_card, text=city_data["city"], corner_radius=15, font=("Arial", 13, "bold")
                        )
            lbl_city2.pack(anchor="w", padx=15, pady=3)
            
            lbl_temp2 = ctk.CTkLabel(
                            self.new_city_card, text=city_data["temp"], corner_radius=30, font=("Arial", 12, "bold")
                        )
            lbl_temp2.pack(anchor="w", padx=15, pady=3)
            
            lbl_desc2 = ctk.CTkLabel(
                            self.new_city_card, text=city_data["desc"], corner_radius=30, font=("Arial", 10, "italic")
                        )
            lbl_desc2.pack(anchor="w", padx=15, pady=3)

        
            icon_lbl2 = ctk.CTkLabel(self.new_city_card, width=10, height=10, bg_color="transparent", text="", image=city_data["small_img"])
            icon_lbl2.place(relx=0.8, rely=0.5, anchor="center")

        elif len(self.saved_cities) >= 5 :
            self.error_label.configure(text="Maximum of 5 cities reached!", text_color="red")

        elif self.add_city_button_counter >= 3:
            self.error_label.configure(text="Maximum of 3 cities added!", text_color="red")

        elif self.add_city_button_counter == 3:
            self.geometry("500x600")

        else:
            self.desc_label.configure(text="City already added!", text_color="007BFF")

    def remove_city(self, city_data):
        self.saved_cities = [
            c for c in self.saved_cities if c["city"] != city_data["city"]
        ]
        self.add_city_button()  # Refresh the list of cities
        if hasattr(self, "new_city_card") and self.new_city_card.winfo_exists():

            self.error_label.configure(text="City removed successfully!", text_color="red")
            self.new_city_card.destroy()
            
        else:
            self.desc_label.configure(text="No cities to remove!", text_color="007BFF")

if __name__ == "__main__":
    app = WeatherApp()
    app.mainloop()