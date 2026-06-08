# Travel Assistant Demo

This folder contains a simple Microsoft Agent Framework demo for a travel assistant.

## What it does
- asks for a destination city
- asks for the number of travel days
- uses AI tools to provide weather and itinerary guidance

## How to run
1. Create a Python virtual environment
2. Install dependencies:
   pip install -r requirements.txt
3. Make sure your Foundry project has a deployed model name and update `.env` if needed
4. Run:
   python travel_assistant.py

The demo is already configured to use:
- PROJECT_ENDPOINT = https://samabrains-ai-lab-resource.services.ai.azure.com/api/projects/samabrains-ai-lab
- MODEL_DEPLOYMENT_NAME = gpt-4.1

## Notes
- This demo uses your Azure account via `AzureCliCredential`.
- Run `az login` before starting the app.
