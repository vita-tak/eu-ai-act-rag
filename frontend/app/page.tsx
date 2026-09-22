"use client";

import { useCallback, useEffect, useRef, useState } from "react";
import type { ChatResponse } from "@/types/chat";
import { AssistantMessage } from "@/components/AssistantMessage";
import { ChatComposer } from "@/components/ChatComposer";
import { ChatHeader, FixedHeaderTitle } from "@/components/ChatHeader";
import { LoadingSparkle } from "@/components/LoadingSparkle";
import { SparkleIcon } from "@/components/SparkleIcon";
import { SuggestionChips } from "@/components/SuggestionChips";
import { SystemMessage } from "@/components/SystemMessage";
import { UserMessage } from "@/components/UserMessage";
import { roleLabel, type UiMessage } from "@/components/messages";

interface ErrorBody {
  error?: string;
  details?: unknown;
}

async function extractErrorMessage(response: Response): Promise<string> {
  try {
    const body = (await response.json()) as ErrorBody;
    if (typeof body.error === "string" && body.error.length > 0) {
      return body.error;
    }
  } catch {
    // Response body was not valid JSON; fall through to the generic message.
  }
  return `Request failed with status ${response.status}`;
}

export default function Home() {
  // The backend keys server-side conversation state (including CLASSIFYING)
  // by this id, so it must be generated once per page session.
  const [conversationId] = useState(() => crypto.randomUUID());
  const [messages, setMessages] = useState<UiMessage[]>([]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const endRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    endRef.current?.scrollIntoView({ block: "end", behavior: "smooth" });
  }, [messages, isLoading]);

  const sendMessage = useCallback(
    async (raw: string) => {
      const trimmed = raw.trim();
      if (trimmed.length === 0 || isLoading) {
        return;
      }

      setMessages((prev) => [
        ...prev,
        { id: crypto.randomUUID(), role: "user", text: trimmed },
      ]);
      setInput("");
      setIsLoading(true);

      try {
        const response = await fetch("/api/chat", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            conversation_id: conversationId,
            message: trimmed,
          }),
        });

        if (!response.ok) {
          const errorMessage = await extractErrorMessage(response);
          setMessages((prev) => [
            ...prev,
            { id: crypto.randomUUID(), role: "system", text: errorMessage },
          ]);
          return;
        }

        const data = (await response.json()) as ChatResponse;
        setMessages((prev) => [
          ...prev,
          { id: crypto.randomUUID(), role: "assistant", response: data },
        ]);
      } catch {
        setMessages((prev) => [
          ...prev,
          {
            id: crypto.randomUUID(),
            role: "system",
            text: "Unable to reach the chat service. Please try again.",
          },
        ]);
      } finally {
        setIsLoading(false);
      }
    },
    [conversationId, isLoading],
  );

  const hasMessages = messages.length > 0;

  return (
    <main
      aria-label="Chat"
      className="mx-auto flex h-dvh w-full max-w-[var(--column)] flex-col px-6"
    >
      {hasMessages && <FixedHeaderTitle />}
      <ChatHeader hasMessages={hasMessages} />

      <div
        className="relative flex min-h-0 flex-1 flex-col"
        style={hasMessages ? { marginTop: "var(--header-height)" } : undefined}
      >
        {hasMessages && (
          <div
            aria-hidden="true"
            className="pointer-events-none absolute inset-x-0 top-0 z-10 h-14 bg-gradient-to-b from-[var(--page)] to-transparent"
          />
        )}

        <section
          aria-live="polite"
          aria-label="Conversation"
          className="scrollbar-on-hover flex min-h-0 flex-1 flex-col overflow-y-auto"
        >
          <div
            className={`mt-auto flex flex-col gap-2.5 pb-5 ${hasMessages ? "pt-20" : "pt-12"}`}
          >
            {hasMessages && (
              <SparkleIcon className="mb-2 size-[52px] text-ink" />
            )}

            {messages.map((message) => (
              <article key={message.id} aria-label={roleLabel(message.role)}>
                {message.role === "user" && (
                  <UserMessage text={message.text} />
                )}
                {message.role === "assistant" && (
                  <AssistantMessage response={message.response} />
                )}
                {message.role === "system" && (
                  <SystemMessage text={message.text} />
                )}
              </article>
            ))}

            {isLoading && <LoadingSparkle />}
            <div ref={endRef} />
          </div>
        </section>
      </div>

      {!hasMessages && (
        <SuggestionChips onSelect={sendMessage} disabled={isLoading} />
      )}

      <ChatComposer
        value={input}
        onChange={setInput}
        onSubmit={() => sendMessage(input)}
        isLoading={isLoading}
      />
    </main>
  );
}
