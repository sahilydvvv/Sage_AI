from dotenv import load_dotenv
load_dotenv()

from langchain_groq import ChatGroq
from langchain_core.messages import (SystemMessage,HumanMessage,ToolMessage)
from tools.calendar_tools import create_calendar_event,get_upcoming_events,delete_calendar_event

llm = ChatGroq(model="llama-3.3-70b-versatile")
tools = [create_calendar_event,get_upcoming_events,delete_calendar_event]
llm_with_tools = llm.bind_tools(tools)

tools_dict = {
    "create_calendar_event": create_calendar_event,
    "get_upcoming_events": get_upcoming_events,
    "delete_calendar_event": delete_calendar_event
}

messages = [
    SystemMessage(
        content=(
            '''You are a helpful assistant that can check the user's calendar for upcoming events and create new events if needed.'''
        )
    ),

    HumanMessage(
        content=(
            '''check my calendar and delete any event present.'''
        )
    )
]

while True:

    ai_msg = llm_with_tools.invoke(messages)

    messages.append(ai_msg)
    print(ai_msg.tool_calls)
    if not ai_msg.tool_calls:
        print(ai_msg.content)
        break

    for tool_call in ai_msg.tool_calls:
        tool_name = tool_call["name"]
        print(f"\nTool name: {tool_name}")
        tool_args = tool_call["args"]
        print(f"Tool args: {tool_args}")

        if tool_name in tools_dict:
            tool_func = tools_dict[tool_name]
            result = tool_func.invoke(tool_args)
            print(f"Tool result: {result}")

            messages.append(
                ToolMessage(
                    content=str(result),
                    tool_call_id=tool_call["id"]
                )
            )

        else:
            print(f"Tool {tool_name} not found in tools_dict.")