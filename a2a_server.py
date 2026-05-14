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
        name='Outlook Copilot Agent',
        description='This agent is able to create draft emails and send those draft emails via Outlook.',
        tags=['copilot', 'outlook', 'send email', 'draft email'],
        examples=[
            'Send this email ...',
            'Draft this email ...', 
            ],
    )

    public_agent_card = AgentCard(
        name='Outlook Copilot Agent', 
        description='This agent is able to create draft emails and send those draft emails via Outlook.',
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
        skills=[skill], 
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





