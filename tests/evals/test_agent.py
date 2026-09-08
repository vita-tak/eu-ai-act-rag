import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from deepeval import assert_test
from deepeval.test_case import LLMTestCase, SingleTurnParams
from deepeval.metrics import GEval
from agent.agent import run_agent


# A product description that is unambiguous enough for the agent to classify
# without follow-up questions. Explicitly states that humans make the final
# decision and that no biometric data is used, since those are the two
# follow-up questions the agent typically asks for recruitment systems.
PRODUCT_DESCRIPTION = (
    "An AI system that screens and ranks job applications for recruitment purposes. "
    "It analyses CVs and ranks candidates based on their qualifications. "
    "Human recruiters make the final hiring decision. "
    "The system does not use biometric data."
)


def test_high_risk_classification():
    # Run the full agent pipeline against the product description.
    # This is an end-to-end eval: it exercises the real ReAct loop,
    # RAG retrieval, and report generation rather than mocking any component.
    messages = [{"role": "user", "content": PRODUCT_DESCRIPTION}]
    result = run_agent(messages)

    # Guard against incomplete runs. If the agent still needs follow-up
    # information it returns status "follow_up" instead of "done", which
    # means the product description was not specific enough.
    assert result["status"] == "done", (
        f"Agent did not complete classification. Asked: {result.get('question')}"
    )

    classification = result["report"]["classification"]
    cited_articles = " ".join(result["report"]["cited_articles"])

    # Combine classification and sources into one string so GEval can
    # evaluate both in a single pass. A simple string assertion would
    # suffice for the classification label, but verifying that the legal
    # basis is correct (Annex III, not just any article) requires semantic
    # judgment, which is why GEval is used here instead.
    actual_output = f"{classification}. Sources: {cited_articles}"

    # GEval uses an LLM as judge to evaluate whether the output meets the
    # criteria. Threshold 0.7 rather than 0.5 because this is a compliance
    # context where a wrong classification has real consequences.
    classification_metric = GEval(
        name="High Risk Classification",
        criteria=(
            "Determine if the actual output correctly classifies the product as "
            "'High risk' and references Annex III as a cited source."
        ),
        evaluation_params=[
            SingleTurnParams.ACTUAL_OUTPUT,
            SingleTurnParams.EXPECTED_OUTPUT
        ],
        threshold=0.7
    )

    test_case = LLMTestCase(
        input=PRODUCT_DESCRIPTION,
        actual_output=actual_output,
        expected_output="High risk. Annex III should be cited as a source."
    )

    assert_test(test_case, [classification_metric])