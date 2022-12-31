# Import Tkinter
from tkinter import *
# Import urllib library
from urllib.request import urlopen
# Import geopy library
from geopy.geocoders import Nominatim
# import json
import json
from PIL import Image, ImageTk

# Create Tkinter window
root = Tk()
# title bar text
root.title("Weather App")
# Title bar icon
root.iconbitmap("icons/sun.ico")
# set background colour
root.configure(bg="#57adff")
root.resizable(False, False)

# Set height and width of window
app_height = 600
app_width = 400

# Get screen dimensions
screen_height = root.winfo_screenheight()
screen_width = root.winfo_screenwidth()

# Calculate centered screen position
x = (screen_width / 2) - (app_width / 2)
y = (screen_height / 2) - (app_height / 2)
# Place window in center of screen
root.geometry(f'{app_width}x{app_height}+{int(x)}+{int(y)}')

label_destroy = False
label_list = []

def bClick():
    global wind_arrow, weather_icon, label_destroy, label_list

    if label_destroy == True:
        for label in label_list:
            label.destroy()
    else:
        main_logo.destroy()

    city = city_input.get()

    # Initialize Nominatim API which will give our latitude and longitude
    geolocator = Nominatim(user_agent="MyApp")

    # Set the location for lat & lon
    location = geolocator.geocode(f"{city}")

    # access API and get info from Json
    # store the url with our weather api
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={location.latitude}&lon={location.longitude}&appid=fe95d16925908ed391d84274c6b84ef0&units=metric"

    # store the response of URL
    response = urlopen(url)

    # storing the JSON response
    # from url in data
    data_json = json.loads(response.read())

    # separate json data
    temperature = data_json["main"]
    wind = data_json["wind"]
    weather = data_json["weather"]

    # Display name of town/city
    city_label = Label(root, text=f"{city.title()}", font=("arial", 30), fg="white", bg="#57adff")
    city_label.place(x=200, y=100, anchor="center")

    # Display temperature
    temperature_label = Label(root, text=f"{int(temperature['temp'])}°", font=("arial", 60), fg="white", bg="#57adff")
    temperature_label.place(x=200, y=180, anchor="center")

    # Display weather icon
    weather_icon = PhotoImage(file=f"icons/{weather[0]['icon']}.png")
    icon = Label(root, image=weather_icon, bg="#57adff")
    icon.place(x=140, y=210)

    # Display weather
    weather_label = Label(root, text=f"{weather[0]['description']}", font=("arial", 15), fg="white", bg="#57adff")
    weather_label.place(x=200, y=320, anchor="center")

    # Display high/low temperature
    High_low_label = Label(root, text=f"H: {int(temperature['temp_max'])}° / L: {int(temperature['temp_min'])}°", font=("arial", 15), fg="white", bg="#57adff")
    High_low_label.place(x=200, y=360, anchor="center")

    # Display wind speed
    wind_speed_label = Label(root, text=f"Wind Speed: {wind['speed']}m/s", font=("arial", 15), fg="white", bg="#57adff")
    wind_speed_label.place(x=200, y=410, anchor="center")

    # Display wind direction
    wind_dir_label = Label(root, text="Wind Direction: ", font=("arial", 15), fg="white", bg="#57adff")
    wind_dir_label.place(x=200, y=460, anchor="center")

    # rotate arrow image to show wind direction
    arrow_img = Image.open("icons/arrow.png")
    img_rotate = arrow_img.rotate(-wind['deg'])
    filename = "icons/arrow_rotated.png"
    img_rotate.save(filename)
    # Place rotated arrow on window
    wind_arrow = PhotoImage(file="icons/arrow_rotated.png")
    arrow = Label(root, image=wind_arrow, bg="#57adff")
    arrow.place(x=170, y=490)

    label_list = [city_label, temperature_label, icon, weather_label, High_low_label, wind_speed_label,
                  wind_dir_label, arrow]
    label_destroy = True

# store city name
city = ""

# Delete placeholder text in search bar
def delete_placeholder(e):
   city_input.delete(0,"end")

# Only display search bar and button until city name submitted
if city == "":
    # place rectangle under search bar
    searchbox_image = PhotoImage(file="icons/rounded_rectangle.png")
    rectangle = Label(image=searchbox_image, bg="#57adff")
    rectangle.place(x=20, y=22)
    # place cloud image over left side of search rectangle
    searchbox_logo = PhotoImage(file="icons/search_logo_img.png")
    searchbox_logo = searchbox_logo.subsample(2, 2)
    cloud = Label(image=searchbox_logo, bg="#149dc5", fg="#149dc5")
    cloud.place(x=32, y=32)
    # create search bar
    city_input = Entry(root, width=22, font=("Arial", 15, "bold"), bg="#149dc5", fg="white", border=0, justify="center")
    # Place holder text for search bar
    city_input.insert(0, 'Enter City Name')
    city_input.place(x=70, y=35)
    # when search bar is clicked, place holder text is deleted
    city_input.bind("<FocusIn>", delete_placeholder)

    # create button to submit search
    search_button_icon = PhotoImage(file="icons/search_icon.png")
    search_button_icon = search_button_icon.subsample(2, 2)
    search = Button(image=search_button_icon, border=0, cursor="hand2", bg="#149dc5", command=bClick)
    search.place(x=320, y=32)
    #Display logo on screen
    logo = PhotoImage(file="icons/main_logo.png")
    logo = logo.subsample(2, 2)
    main_logo = Label(image=logo, bg="#57adff")
    main_logo.place(x=80, y=170)


root.mainloop()
