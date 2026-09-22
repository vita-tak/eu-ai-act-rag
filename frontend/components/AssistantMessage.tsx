import type { ChatResponse } from "@/types/chat";
import { ClassificationCard } from "./ClassificationCard";
import { FollowUp } from "./FollowUp";
import { RagAnswer } from "./RagAnswer";

interface AssistantMessageProps {
  response: ChatResponse;
}

function AssistantBody({ response }: AssistantMessageProps) {
  switch (response.type) {
    case "rag_response":
      return <RagAnswer response={response} />;
    case "follow_up":
      return <FollowUp response={response} />;
    case "classification":
      return <ClassificationCard response={response} />;
  }
}

/*
 * The assistant block is right-aligned and ends flush with the composer's
 * right edge, at roughly 65% of the column, per the reference. Each
 * response type supplies its own card chrome.
 */
export function AssistantMessage({ response }: AssistantMessageProps) {
  return (
    <div className="flex flex-col items-end">
      <div className="w-full sm:max-w-[65%]">
        <p className="label-micro pb-2">Compliance assistant</p>
        <AssistantBody response={response} />
      </div>
    </div>
  );
}
