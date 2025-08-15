from flask import Flask, render_template, request
from waitress import serve

from weather import WeatherResponse, get_current_weather

app = Flask(__name__)


@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")


@app.route("/weather")
def get_weather():
    city = request.args.get("city")
    if not city:
        city = "London"
    weather_data = get_current_weather(city.strip())

    if (isinstance(weather_data, WeatherResponse)):
        return render_template(
            "weather.html",
            title=weather_data.name,
            status=weather_data.weather[0].description.capitalize(),
            temp=f"{weather_data.main.temp:.1f}",
            feels_like=f"{weather_data.main.feels_like:.1f}"
        )
    return render_template("city-not-found.html")


if __name__ == "__main__":
    # app.run(host="0.0.0.0", port=8000)
    serve(app, host="0.0.0.0", port=8000)
