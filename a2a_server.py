import uvicorn
from starlette.applications import Starlette
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware import Middleware

from a2a.server.routes import (
    create_agent_card_routes,
    create_jsonrpc_routes,
)
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore
from a2a_agent_executor import CopilotAgentExecutor 
from a2a.types import (
    AgentCapabilities,
    AgentCard,
    AgentInterface,
    AgentSkill,
)

if __name__ == '__main__': 
    skill = AgentSkill(
        id='copilot_agent',
        name='AIA Copilot Agent',
        description='Finds group rule details for AIA',
        tags=['copilot aia insurance'],
        examples=[
            'what are the age requirements for contributing based on the AIA rules?',
            'Whats the minimum contribution age as per the AIA group rules?', 
            'What changes do i need to notify AIA of?'
            ],
    )

    public_agent_card = AgentCard(
        name='Copilot Insurance Rules Agent.', 
        description='This agent retrieves insurance group policy rules.',
        version='0.0.1',
        default_input_modes=['text/plain'],
        default_output_modes=['text/plain'],
        capabilities=AgentCapabilities(
            streaming=False, extended_agent_card=False
        ),
        supported_interfaces=[
            AgentInterface(
                protocol_binding='JSONRPC',
                url='http://127.0.0.1:9997',
            )
        ],
        skills=[skill],  # Only the basic skill for the public card
    )

    request_handler = DefaultRequestHandler(
        agent_executor=CopilotAgentExecutor(), 
        task_store = InMemoryTaskStore(), 
        agent_card = public_agent_card
    )

routes = [*create_agent_card_routes(public_agent_card), *create_jsonrpc_routes(request_handler, '/', enable_v0_3_compat=True )] 

class LogRequestMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        body = await request.body()
        print(f"Incoming request: {body.decode()}")
        return await call_next(request)

app = Starlette(routes=routes, middleware=[
    Middleware(LogRequestMiddleware)
])
uvicorn.run(app, host="0.0.0.0", port=9997, access_log=True, log_level="debug")





