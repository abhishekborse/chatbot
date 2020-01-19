from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import datetime as dt
import logging
import json

logger = logging.getLogger(__name__)


class ActionTimeGreeting(Action):

    def __init__(self):
        self.now = dt.datetime.now()

    def name(self) -> Text:
        return "action_time_greeting"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        user_message = tracker.latest_message.get('text')
        message = self.check_message_for_time(user_message)
        dispatcher.utter_message(message)
        return []

    def check_message_for_time(self, user_message):
        today00am = self.now.replace(hour=00, minute=0, second=0, microsecond=0)
        today12pm = self.now.replace(hour=12, minute=0, second=0, microsecond=0)
        today04pm = self.now.replace(hour=16, minute=0, second=0, microsecond=0)

        if today00am < self.now < today12pm:
            bot_message = 'Good Morning'
        elif today12pm < self.now < today04pm:
            bot_message = 'Good Afternoon'
        else:
            bot_message = 'Good Evening'

        if bot_message.replace(' ', '_').lower() not in user_message.replace(' ', '_').lower():
            return "Hey, It's {}. By the way!".format(bot_message)

        return bot_message
