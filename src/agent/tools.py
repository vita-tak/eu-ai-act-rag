import requests

tools = [
    {
        "name": "search_eu_ai_act",
        "description": (
            "Search the EU AI Act for relevant articles and provisions. "
            "Use this to find passages relevant to the product being classified. "
            "Formulate the query as a specific, narrow phrase rather than a broad or "
            "vague one, so the search returns the most relevant passages."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The search query"
                }
            },
            "required": ["query"]
        }
    },
    {
        "name": "ask_user",
        "description": (
            "Ask the user a clarifying follow-up question when the product description "
            "lacks information that is decisive for the EU AI Act risk classification. "
            "Use this only when the missing information could change which risk category "
            "applies, for example: whether the system is used for employment or hiring "
            "decisions, whether it processes biometric data, whether it operates in real "
            "time in public spaces, or who the end users are. Ask one focused question "
            "at a time. Do NOT use this tool for information that is already stated or "
            "clearly implied in the product description, and do NOT ask about details "
            "that would not affect the classification outcome."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "question": {
                    "type": "string",
                    "description": "The clarifying question to ask the user"
                }
            },
            "required": ["question"]
        }
    },
    {
        "name": "generate_report",
        "description": (
            "Generate the final EU AI Act risk classification report with reasoning "
            "and cited articles. Use this only when the necessary searches in the EU "
            "AI Act have been made and any classification-relevant uncertainties have "
            "been resolved through follow-up questions, so the classification rests on "
            "actual articles and facts rather than guesswork. Do NOT call this tool "
            "while decisive information is still missing or unverified."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "classification": {
                    "type": "string",
                    "enum": [
                        "Ej ett AI-system",
                        "Minimal risk",
                        "Begränsad risk",
                        "Hög risk",
                        "GPAI",
                        "Förbjuden praktik"
                    ]
                },
                "reasoning": {
                    "type": "string",
                    "description": "Explanation of why this classification applies"
                },
                "cited_articles": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "List of EU AI Act articles that support the classification"
                }
            },
            "required": ["classification", "reasoning", "cited_articles"]
        }
    }
]


def search_eu_ai_act(query):
    response = requests.post(
        "http://localhost:8000/query",
        json={"question": query}
    )
    data = response.json()
    return data.get("answer", "No results found")


def ask_user(question):
    # Pauses the loop and waits for user input.
    print(f"\nFollow-up question: {question}")
    return input("Your answer: ")


def generate_report(findings):
    # Returns structured dict so the caller can format it.
    return findings


def execute_tool(tool_name, tool_input):
    # Dispatches to the right function based on Claudes choice.
    if tool_name == "search_eu_ai_act":
        return search_eu_ai_act(tool_input["query"])
    elif tool_name == "ask_user":
        return ask_user(tool_input["question"])
    elif tool_name == "generate_report":
        return generate_report(tool_input)
    else:
        return f"Unknown tool: {tool_name}"