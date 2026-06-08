# Travel tools worker

This Cloudflare Worker exposes two simple endpoints for the travel assistant:

- GET /weather?city=Kampala
- GET /itinerary?city=Kampala&days=3

## Run locally

npm install
npm run dev

Then open the local URL shown by Wrangler.

## Deploy

npm run deploy

## Connect this in Azure AI Foundry

1. Open your Azure AI Foundry project.
2. Open the agent you want to use.
3. Add a custom tool / REST tool and point it to the deployed Worker URL.
4. Use the OpenAPI file in this folder as the contract:
   - openapi.yaml
5. The two tool calls will be:
   - GET /weather?city={city}
   - GET /itinerary?city={city}&days={days}

This is the portal path because the Foundry chat can call the public Cloudflare URL; it cannot execute your local Python functions directly.
