import type { ClassificationResponse } from "@/types/chat";
import { AssistantMessage } from "@/components/AssistantMessage";
import { LoadingSparkle } from "@/components/LoadingSparkle";
import { SystemMessage } from "@/components/SystemMessage";
import { UserMessage } from "@/components/UserMessage";

/*
 * Development-only fixture gallery. Renders every message state from
 * static data so the three response types and all six risk tiers can be
 * reviewed without driving the agent into each branch.
 *
 * Not linked from the app. Safe to delete.
 */

const ALL_TIERS = [
  "Prohibited practice",
  "High risk",
  "Limited risk",
  "Minimal risk",
  "GPAI",
  "Not an AI system",
  "Something unexpected",
] as const;

function classificationFixture(tier: string): ClassificationResponse {
  return {
    type: "classification",
    report: {
      classification: tier,
      reasoning:
        "The system performs automated screening of job applications and ranks candidates for human reviewers. Annex III point 4(a) covers AI intended to be used for recruitment or selection of natural persons, which places it in the high-risk category regardless of the provider's intent. The presence of a human reviewer does not remove the classification, because Article 6(3) only exempts systems that perform a narrow procedural task or improve the result of a previously completed human activity.",
      cited_articles: ["Article 6(2)", "Article 6(3)", "Annex III, 4(a)"],
    },
  };
}

function Row({ label, children }: { label: string; children: React.ReactNode }) {
  return (
    <section className="flex flex-col gap-3 border-t border-[var(--rule)] pt-6">
      <h2 className="font-mono text-[11px] tracking-wide text-ink-muted">
        {label}
      </h2>
      {children}
    </section>
  );
}

export default function DevMessagesPage() {
  return (
    <main className="mx-auto flex w-full max-w-[var(--column)] flex-col gap-6 px-6 py-16">
      <h1 className="text-2xl">Message fixtures</h1>

      <Row label="user message">
        <UserMessage text="What can I ask you to do?" />
      </Row>

      <Row label="rag_response (real backend payload, captured 2026-09-22)">
        <AssistantMessage
          response={{
            type: "rag_response",
            answer: "# What is a High-Risk AI System?\n\nAccording to the EU AI Act, a high-risk AI system is defined through multiple classification criteria outlined in **Article 6**:\n\n## Primary Classification Routes\n\n### 1. **Safety Components in Regulated Products (Article 6(1))**\nAn AI system is high-risk when **both** conditions are met:\n- The AI system is intended to be used as a safety component of a product, or is itself a product, covered by Union harmonisation legislation listed in Annex I; **AND**\n- The product or AI system is required to undergo third-party conformity assessment before being placed on the market or put into service\n\n### 2. **Specific Use Cases (Article 6(2))**\nAI systems listed in **Annex III** are considered high-risk, which cover applications such as:\n- Biometric identification systems\n- Evaluation of natural persons in critical contexts\n- Employment and education decisions\n- And other specified high-impact use cases\n\n## Important Exceptions (Article 6(3))\n\nAn AI system in Annex III is **not** considered high-risk if it does not pose significant risk of harm to health, safety, or fundamental rights, such as when:\n- It performs a narrow procedural task\n- It improves results of previously completed human activity\n- It detects patterns without replacing human assessment\n- It performs preparatory tasks\n\n**However**, an Annex III system is **always** high-risk if it performs profiling of natural persons.\n\n## Compliance Requirements\n\nHigh-risk AI systems must comply with extensive requirements including risk management systems (Article 8), human oversight (Article 14), quality management, documentation, conformity assessment, and other safeguards outlined in **Section 2 of Chapter III**.",
            sources: ["Article  20", "Article  16", "Article  12", "Article  8", "Article  9", "Article  14", "Article  6", "Article  49"],
          }}
        />
      </Row>

      <Row label="rag_response (no sources)">
        <AssistantMessage
          response={{
            type: "rag_response",
            answer:
              "Classification could not be completed. Please try again with more details about your AI system.",
            sources: [],
          }}
        />
      </Row>

      <Row label="follow_up">
        <AssistantMessage
          response={{
            type: "follow_up",
            question:
              "Does the system make or materially influence the hiring decision, or does it only sort applications for a human who independently reviews each one?",
          }}
        />
      </Row>

      <Row label="loading">
        <LoadingSparkle />
      </Row>

      <Row label="system / error">
        <SystemMessage text="Unable to reach the AI service. Please try again shortly." />
      </Row>

      {ALL_TIERS.map((tier) => (
        <Row key={tier} label={`classification - ${tier}`}>
          <AssistantMessage response={classificationFixture(tier)} />
        </Row>
      ))}
    </main>
  );
}
