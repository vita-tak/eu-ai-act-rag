import type { ClassificationResponse } from "@/types/chat";
import { RiskBadge } from "./RiskBadge";

interface ClassificationCardProps {
  response: ClassificationResponse;
}

/*
 * The report is the product of the whole classification flow, so it gets
 * the most structure of the three response types: a titled card, the tier
 * badge as the headline, then reasoning and citations as labelled
 * sections separated by hairlines.
 */
export function ClassificationCard({ response }: ClassificationCardProps) {
  const { classification, reasoning, cited_articles } = response.report;

  return (
    <article className="rounded-xl border border-[var(--hairline)] bg-[var(--surface-strong)] px-5 py-4 surface-ring">
      <h3 className="label-micro font-semibold">Risk classification</h3>

      <div className="mt-2.5">
        <RiskBadge classification={classification} />
      </div>

      <div className="mt-4 border-t border-[var(--rule)] pt-3.5">
        <h4 className="label-micro font-semibold">Reasoning</h4>
        <p className="mt-2 text-[0.9375rem] leading-[1.55] whitespace-pre-line text-ink">
          {reasoning}
        </p>
      </div>

      {cited_articles.length > 0 && (
        <div className="mt-4 border-t border-[var(--rule)] pt-3.5">
          <h4 className="label-micro font-semibold">Cited articles</h4>
          <ul className="mt-2 flex flex-wrap gap-1.5">
            {cited_articles.map((article, index) => (
              <li
                key={`${article}-${index}`}
                className="rounded border border-[var(--rule)] bg-[var(--surface-solid)] px-2 py-1 text-xs leading-none text-ink-soft"
              >
                {article}
              </li>
            ))}
          </ul>
        </div>
      )}
    </article>
  );
}
