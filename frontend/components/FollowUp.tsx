import type { FollowUpResponse } from "@/types/chat";
import { SparkleIcon } from "./SparkleIcon";

interface FollowUpProps {
  response: FollowUpResponse;
}

/*
 * A follow-up is a prompt, not an answer, so it gets its own chrome: a
 * warm accent rule down the leading edge and a label that says the
 * classification is waiting on the user.
 */
export function FollowUp({ response }: FollowUpProps) {
  return (
    <div className="rounded-xl rounded-l-sm surface-ring border border-[var(--hairline)] border-l-2 border-l-[var(--accent-attention)] bg-[var(--surface)] px-5 py-4">
      <h3 className="label-micro flex items-center gap-1.5 font-semibold text-[var(--risk-limited-fg)]">
        <SparkleIcon className="size-3 text-[var(--accent-attention)]" />
        Needs your input
      </h3>
      <p className="mt-2 text-[0.9375rem] leading-[1.55] text-ink">
        {response.question}
      </p>
    </div>
  );
}
