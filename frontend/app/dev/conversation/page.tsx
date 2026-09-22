"use client";

import { AssistantMessage } from "@/components/AssistantMessage";
import { ChatComposer } from "@/components/ChatComposer";
import { ChatHeader } from "@/components/ChatHeader";
import { UserMessage } from "@/components/UserMessage";

/*
 * Development-only fixture: the chat shell in its conversation state,
 * populated with the exact content of the reference design, so the two
 * can be compared side by side. Mirrors the layout in app/page.tsx.
 *
 * Not linked from the app. Safe to delete.
 */
export default function DevConversationPage() {
  return (
    <main className="mx-auto flex h-dvh w-full max-w-[var(--column)] flex-col px-6">
      <ChatHeader hasMessages />
      <section className="flex min-h-0 flex-1 flex-col overflow-y-auto">
        <div className="mt-auto flex flex-col gap-2.5 pt-12 pb-5">
          <UserMessage text="What can I ask you to do?" />
          <AssistantMessage
            response={{
              type: "rag_response",
              answer:
                "Great question! You can ask for my help with the following:\n\n1. Anything to do with your reports in our software e.g. What is the last report we exported?\n2. Anything to do with your organisation e.g. how many employees are using our software?\n3. Anything to do with the features we have in our software e.g how can I change the colours of my report?",
              sources: [],
            }}
          />
        </div>
      </section>
      <ChatComposer value="" onChange={() => {}} onSubmit={() => {}} isLoading={false} />
    </main>
  );
}
