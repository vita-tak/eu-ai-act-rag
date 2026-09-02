import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import anthropic
from config import ANTHROPIC_API_KEY
from tools import tools, execute_tool

client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)


def run_agent(product_description, max_steps=12):
    messages = [
        {"role": "user", "content": product_description}
    ]

    for step in range(max_steps):
        print(f"Step {step + 1}")

        response = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=1000,
            tools=tools,
            messages=messages
        )

        print(f"stop_reason: {response.stop_reason}")

        if response.stop_reason == "end_turn":
            return response

        if response.stop_reason == "tool_use":
            # Append Claudes response as plain dicts, not SDK objects.
            messages.append({"role": "assistant", "content": [
                block.model_dump() for block in response.content
            ]})

            # Claude may call multiple tools in one response.
            # Every tool_use block must have a matching tool_result.
            tool_results = []
            for block in response.content:
                if block.type == "tool_use":
                    print(f"Tool: {block.name}, Input: {block.input}")
                    tool_result = execute_tool(block.name, block.input)
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": tool_result
                    })

            # Feed all results back in a single message.
            messages.append({
                "role": "user",
                "content": tool_results
            })

    # Safety exit: fires only if the agent never called generate_report.
    raise RuntimeError("Agent reached max_steps without completing")


if __name__ == "__main__":
    run_agent("An AI that screens job applications and ranks candidates")