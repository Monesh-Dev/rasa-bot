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

        # 🔄 Replace this with real data later
        expense_summary = "Food ₹5000, Education ₹3000, Entertainment ₹2000"

        prompt = (f"You are a personal finance assistant. "
                  f"Here is the user's expense summary: {expense_summary}.\n"
                  f"User's question: {user_message}")

        try:
            client = OpenAI(base_url="https://openrouter.ai/api/v1",
                api_key=OPENROUTER_API_KEY)
            completion = client.chat.completions.create(
                model="meta-llama/llama-4-maverick:free",
                messages=[{"role": "user", "content": prompt}])

            reply = completion.choices[0].message.content
        except Exception as e:
            reply = f"Sorry, I couldn't fetch the answer: {str(e)}"

        dispatcher.utter_message(text=reply)
        return []
