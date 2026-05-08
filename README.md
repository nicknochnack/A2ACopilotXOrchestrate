# Calling CoPilot Agents from Watsonx Orchestrate using A2A
G'day, this is a full blown walkthrough on how to call collaborator agents in Copilot from your ole mate watsonx Orchestrate. It's configured to send the request to the sub agent and push notifications back into orchestratethis means...*drumroll please*...it supports long running tasks. Its been tested with RAG agents and tool calling and works reasonably well. 

## See it live and in action 📺 - Click the image!
<!-- <a href="https://youtu.be/D3pXSkGceY0"><img src="https://i.imgur.com/nEfrhIQ.png"/></a> -->
TBD - vid coming in hot.

# Setup 🪛
1. Install UV - `pip install uv`
2. Clone the repo - `git clone https://github.com/nicknochnack/A2ACopilotXOrchestrate .`
3. Install all the dependencies `uv sync`

# Configuring Your CoPilot Agent 🦾
1. Build whatever agent you want inside of copilot studio
2. Then publish it, using the button in the top right
3. Then go to Settings (in the top right) > Security > Web Channel Security 
4. Copy one of the secret keys - paste that into the .env as your `COPILOT_DIRECT_LINE_SECRET` value 

That's the authentication side from copilot side done.

# Setting up the Orchestrate Side  🚀 
1. Import the collaborator agent inside of orchestrate by running `uv run orchestrate agents import -f orchestratea2aagent.yaml` <b>P.s.</b> This step needs to be done inside of a watsonx orchestrate ADK instance. 
2. Get your watsonx orchestrate token value, this is from this location locally `root/.cache/orchestrate`, I'm not going to lie I can't remember how to get this on SaaS but as soon as someone asks me I'll go find it for you...promise. 
3. Chuck that token into your `.env` file under `WXO_TOKEN` <b>P.s.</b> If you're running a saas instance you WILL need to get an alternate push notifications end point, this can be retrieved from the A2A call that's returned from orchestrate, once you have that update `WXO_PUSH_NOTIFICATION_URL` with the value. 
4. Run the A2A server by running `uv run a2a_server.py`
5. Add the collaborator agent to your main agent inside of the orchestrate UI and test a prompt. You should see the request logged out to the server. Orchestrate will display <i>Your request is being processed. Please wait while the agent works on it.</i> while it's running, as soon as it's done you should see the pushed message back in the chat. 

# Who, When, Why?
👨🏾‍💻 Author: Nick Renotte <br />
📅 Version: 1.x<br />
📜 License: This project is licensed under the MIT License </br>
