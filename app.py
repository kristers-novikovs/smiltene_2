from flask import (
    Flask,
    render_template,
    request,
    redirect
)
from requests import get
from pprint import pprint

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("layout.html")

@app.route("/get_weather", methods=["POST", "GET"])
def get_weather():
    if request.method == "POST":
    #GLOBAL DATA
        city = request.form.get("city")
        type = request.form.get("type")

        # city -> coordinates
        api_key = "1327e0d41e6b3d10460508b6f0d9ba04"
        geo_url = f"""http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=5&appid={api_key}"""
    #TYPE DATA
        #weather data for one day
        if type == "1":

            req = get(geo_url)
            #print(req.json())
            if req.status_code != 200:
                return render_template(
                    "layout.html",
                    text="Neizdevās ielādēt datus!")

            if not req.json():
                return render_template(
                    "layout.html",
                    text="Pilsēta neeksistē!")

            #print(req.json())
            geo_data = req.json()[0]
            #print (geo_data)
            
            # declaring latitude and longitude
            lat = geo_data["lat"]
            lon = geo_data["lon"]

            #print(lat, lon)

            # coordinates -> weather
            weather_url = f"""http://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={api_key}&units=metric&lang=la"""

            req = get(weather_url)
            
            #pprint(req.json())

            if req.status_code != 200:
                return render_template(
                    "layout.html",
                    text="Neizdevās ielādēt datus!")
            
            weather_data = req.json()

            degrees = weather_data["list"][0]["main"]["temp"]
            description = weather_data["list"][0]["weather"][0]["description"]
            icon = weather_data["list"][0]["weather"][0]["icon"]

            #print(degrees, description, icon)

            weather = {
                    "degrees":degrees,
                    "description":description,
                    "icon":icon
                }

            icon_url = f"https://openweathermap.org/img/wn/{icon}@2x.png"
        
            return render_template(
                "layout.html",
                weather_day=weather,
                icon_url=icon_url)

        #weather data for 5 days
        elif type == "5":

            req = get(geo_url)
            #print(req.json())
            if req.status_code != 200:
                return render_template(
                    "layout.html",
                    text="Neizdevās ielādēt datus!")

            if not req.json():
                return render_template(
                    "layout.html",
                    text="Pilsēta neeksistē!")

            #print(req.json())
            geo_data = req.json()[0]
            #print (geo_data)
            
            # declaring latitude and longitude
            lat = geo_data["lat"]
            lon = geo_data["lon"]

            #print(lat, lon)

            # coordinates -> weather
            weather_url = f"""http://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={api_key}&units=metric&lang=la"""

            req = get(weather_url)
            
            #pprint(req.json())

            if req.status_code != 200:
                return render_template(
                    "layout.html",
                    text="Neizdevās ielādēt datus!")
            
            weather_data = req.json()

            time = weather_data["list"][0]["dt_txt"]
            split_time = time.split(" ")[1]
            #print(split_time)

            # degrees = weather_data["list"][0]["main"]["temp"]
            # description = weather_data["list"][0]["weather"][0]["description"]
            icon = weather_data["list"][0]["weather"][0]["icon"]
            #print(degrees, description, icon)
            
            item_list = []

            icon_url = f"https://openweathermap.org/img/wn/{icon}@2x.png"

            for item in weather_data["list"]:
                if split_time in item["dt_txt"]:
                    item_list.append({
                        "degrees" : item["main"]["temp"],
                        "description" : item["weather"][0]["description"],
                        "icon" : icon_url
                    })
            pprint(item_list)
                    
            return render_template(
                "layout.html",
                weather_week=item_list,
                icon_url=icon_url)
        
        else:
            return render_template(
                    "layout.html",
                    text="Netika noteikts prognozes veids!")

    else:
        ...

if __name__ == "__main__":
    app.run(debug=True)