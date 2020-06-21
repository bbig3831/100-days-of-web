import quart
from views import city_api, home
from config import settings
from services import weather_service, sun_service, location_service

app = quart.Quart(__name__)
is_debug = False

app.register_blueprint(home.blueprint)
app.register_blueprint(city_api.blueprint)

def configure_app():
    mode = 'dev' if is_debug else 'prod'
    data = settings.load(mode)
    weather_service.global_init(data.get('weather_key'))
    sun_service.use_cached_data = data.get('use_cached_data')
    location_service.use_cached_data = data.get('use_cached_data')

    print(f"Using cached data? {data.get('use_cached_data')}")


def run_web_app():
    app.run(debug=is_debug, port=5001)

configure_app()

if __name__ == '__main__':
    run_web_app()