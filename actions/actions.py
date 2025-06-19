import os
from typing import Any, Dict, List

import requests
from openai import OpenAI
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

# Set your OpenRouter API key here or use an environment variable
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")


class ActionOpenRouterResponse(Action):
    def name(self) -> str:
        return "action_openrouter_response"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[str, Any]) -> List[Dict[str, Any]]:

        user_message = tracker.latest_message.get('text', '')

        metadata = tracker.latest_message.get("metadata", {})
        summary = metadata.get("summary", "")
        budget = metadata.get("budget", 0)
        remaining = metadata.get("remaining", 0)
        timestamp = metadata.get("timestamp", "")

        prompt = (
            f"You are a personal finance assistant.\n"
            f"Time: {timestamp}\n"
            f"Monthly budget: ₹{budget}\n"
            f"Remaining: ₹{remaining}\n"
            f"Expenses by category: {summary}\n"
            f"User query: {user_message}"
        )

        try:
            client = OpenAI(base_url="https://openrouter.ai/api/v1",
                api_key=OPENROUTER_API_KEY)
            completion = client.chat.completions.create(
                model="deepseek/deepseek-chat-v3-0324:free",
                messages=[{"role": "user", "content": prompt}])

            reply = completion.choices[0].message.content
        except Exception as e:
            reply = f"Sorry, I couldn't fetch the answer: {str(e)}"

        dispatcher.utter_message(text=reply)
        return []
