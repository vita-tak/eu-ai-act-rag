import anthropic
from src.config import ANTHROPIC_API_KEY
from src.agent.tools import tools, execute_tool, FollowUpRequired

client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

SYSTEM_PROMPT = (
    "You are an EU AI Act compliance classifier. "
    "You must ALWAYS use one of the provided tools to respond. "
    "Never respond with plain text. "
    "Use search_eu_ai_act to find relevant articles, "
    "ask_user to clarify missing information, "
    "and generate_report to deliver the final classification. "
    "You must always end by calling generate_report."
)


def print_report(report):
    print("\n=== EU AI Act Compliance Report ===")
    print(f"Classification: {report['classification']}\n")
    print(f"Reasoning:\n{report['reasoning']}\n")
    print("Cited articles:")
    for article in report['cited_articles']:
        print(f"  - {article}")
    print("===================================\n")


def run_agent(messages, max_steps=12, interactive=False):
    for step in range(max_steps):
        print(f"Step {step + 1}")

        response = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=1000,
            tools=tools,
            system=SYSTEM_PROMPT,
            messages=messages
        )

        print(f"stop_reason: {response.stop_reason}")

        if response.stop_reason == "end_turn":
            return {"status": "done", "messages": messages}

        if response.stop_reason == "tool_use":
            messages.append({"role": "assistant", "content": [
                block.model_dump() for block in response.content
            ]})

            tool_results = []

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
                        return {
                            "status": "follow_up",
                            "question": e.question,
                            "tool_use_id": block.id,
                            "messages": messages
                        }

                    # Return immediately when generate_report is called.
                    # Do not feed the result back to Claude.
                    if block.name == "generate_report":
                        return {"status": "done", "report": tool_result, "messages": messages}

                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": str(tool_result)
                    })

            messages.append({
                "role": "user",
                "content": tool_results
            })

    raise RuntimeError("Agent reached max_steps without completing")


if __name__ == "__main__":
    messages = [
        {"role": "user", "content": "An AI that screens job applications and ranks candidates"}
    ]
    result = run_agent(messages, interactive=True)
    if result.get("report"):
        print_report(result["report"])