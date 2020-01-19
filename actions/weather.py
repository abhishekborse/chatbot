from typing import Any, Text, Dict, List
import json
import requests
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

API_KEY = '<your API key>'
API_URL = 'http://api.openweathermap.org/data/2.5/weather'


class ActionCheckWeather(Action):
    def name(self) -> Text:
        return "action_check_weather"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        latest_message_entities = tracker.latest_message.get('entities', [])
        if latest_message_entities:
            city_name = latest_message_entities[0].get('value')
            details_text = self.get_weather_details(city_name)
            dispatcher.utter_message(details_text)
        else:
            dispatcher.utter_message("I haven't found any city name")
        return []

    @staticmethod
    def get_weather_details(city_name):
        try:
            querystring = {"q": city_name, "units": "metric", "appid": API_KEY}
            response = requests.request("GET", API_URL, params=querystring)
            response = json.loads(response.text)
        except Exception as e:
            pass
        if response.get('cod') in [200, 201]:
            return 'In {}({}) temperature is {}°C with {}% humidity'.format(
                response.get('name'), response.get('sys').get('country'), 
                response.get('main').get('temp'), response.get('main').get('humidity'))
        else:
            return "I haven't found any city named {}".format(city_name)


