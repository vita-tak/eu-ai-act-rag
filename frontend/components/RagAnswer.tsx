import Markdown from "react-markdown";
import type { RagResponse } from "@/types/chat";

interface RagAnswerProps {
  response: RagResponse;
}

export function RagAnswer({ response }: RagAnswerProps) {
  return (
    <div className="rounded-xl surface-ring border border-[var(--hairline)] bg-[var(--surface)] px-5 py-4">
      <div className="answer-prose text-[0.9375rem] leading-[1.4] text-ink">
        <Markdown>{response.answer}</Markdown>
      </div>

      {response.sources.length > 0 && (
        <div className="mt-4 border-t border-[var(--rule)] pt-3">
          <h3 className="label-micro font-semibold">
            {response.sources.length === 1 ? "Source" : "Sources"}
          </h3>
          <ul className="mt-2 flex flex-wrap gap-1.5">
            {response.sources.map((source, index) => (
              <li
                key={`${source}-${index}`}
                className="rounded border border-[var(--rule)] bg-[var(--surface-strong)] px-2 py-1 text-xs leading-none text-ink-muted"
              >
                {source.replace(/\s+/g, " ").trim()}
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}
