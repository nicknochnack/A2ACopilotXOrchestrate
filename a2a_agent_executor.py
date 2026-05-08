from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.helpers import (
    new_task_from_user_message,
    new_text_artifact,
    new_text_message,
)
from a2a.types.a2a_pb2 import (
    TaskArtifactUpdateEvent,
    TaskState,
    TaskStatus,
    TaskStatusUpdateEvent,
)

from a2a_copilot import CopilotAgent
from a2a_pusher import pushNotification
from colorama import Fore
import time 
import asyncio 

class CopilotAgentExecutor(AgentExecutor): 
    def __init__(self) -> None: 
            self.agent = CopilotAgent() 
    
    def _agent_flow(self, task, context, event_queue): 
        print('triggering flow') 
        result = self.agent.invoke(str(task.history))
        response = pushNotification(task.id, context.task_id, context.context_id, context.metadata['corr_id'], 'completed', message=result)
    
    def _run_agent(self, task, context, event_queue): 
        self._agent_flow(task, context, event_queue)
    
    async def execute(self, context, event_queue) -> None:
        task = context.current_task or new_task_from_user_message(context.message)
        await event_queue.enqueue_event(task)
        await event_queue.enqueue_event(TaskStatusUpdateEvent(
                task_id = context.task_id, 
                context_id = context.context_id, 
                status = TaskStatus(
                    state = TaskState.TASK_STATE_WORKING, 
                )
            ) )
        self._bg_task = asyncio.create_task(asyncio.to_thread(self._run_agent, task, context, event_queue))

    async def cancel(self, context, event_queue) -> None: 
        raise Exception('cancel not supported') 








