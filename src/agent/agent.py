import anthropic
from src.config import ANTHROPIC_API_KEY
from src.agent.tools import tools, execute_tool, FollowUpRequired

client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)


def print_report(report):
    print("\n=== EU AI Act Compliance Report ===")
    print(f"Classification: {report['classification']}\n")
    print(f"Reasoning:\n{report['reasoning']}\n")
    print("Cited articles:")
    for article in report['cited_articles']:
        print(f"  - {article}")
    print("===================================\n")


def run_agent(messages, max_steps=12, interactive=False):
    # Accepts an existing messages list so sessions can be resumed.
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
            return {"status": "done", "messages": messages}

        if response.stop_reason == "tool_use":
            # Append Claudes response as plain dicts, not SDK objects.
            messages.append({"role": "assistant", "content": [
                block.model_dump() for block in response.content
            ]})

            # Claude may call multiple tools in one response.
            # Every tool_use block must have a matching tool_result.
            tool_results = []
            report = None

            for block in response.content:
                if block.type == "tool_use":
                    print(f"Tool: {block.name}, Input: {block.input}")

                    try:
                        tool_result = execute_tool(
                            block.name,
                            block.input,
                            interactive=interactive
                        )
                    except FollowUpRequired as e:
                        # Agent needs more information.
                        # Append partial tool results and return the question.
                        messages.append({
                            "role": "user",
                            "content": [{
                                "type": "tool_result",
                                "tool_use_id": block.id,
                                "content": "Waiting for user response."
                            }]
                        })
                        return {
                            "status": "follow_up",
                            "question": e.question,
                            "messages": messages
                        }

                    if block.name == "generate_report":
                        report = tool_result

                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": str(tool_result)
                    })

            # Feed all results back in a single message.
            messages.append({
                "role": "user",
                "content": tool_results
            })

            # If generate_report was called, return the structured report.
            if report:
                return {"status": "done", "report": report, "messages": messages}

    # Safety exit: fires only if the agent never called generate_report.
    raise RuntimeError("Agent reached max_steps without completing")


if __name__ == "__main__":
    messages = [
        {"role": "user", "content": "An AI that screens job applications and ranks candidates"}
    ]
    result = run_agent(messages, interactive=True)
    if result.get("report"):
        print_report(result["report"])