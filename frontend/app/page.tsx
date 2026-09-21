"use client";

import { useState } from "react";
import type { ChatMessage, ChatResponse } from "@/types/chat";

function formatAssistantContent(response: ChatResponse): string {
  switch (response.type) {
    case "rag_response": {
      if (response.sources.length === 0) {
        return response.answer;
      }
      return `${response.answer}\n\nSources: ${response.sources.join(", ")}`;
    }
    case "follow_up":
      return response.question;
    case "classification": {
      const { classification, reasoning, cited_articles } = response.report;
      return [
        `Classification: ${classification}`,
        `Reasoning: ${reasoning}`,
        `Cited articles: ${cited_articles.join(", ")}`,
      ].join("\n\n");
    }
  }
}

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
  const [conversationId] = useState(() => crypto.randomUUID());
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  async function handleSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();

    const trimmed = input.trim();
    if (trimmed.length === 0 || isLoading) {
      return;
    }

    const userMessage: ChatMessage = {
      id: crypto.randomUUID(),
      role: "user",
      content: trimmed,
    };

    setMessages((prev) => [...prev, userMessage]);
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
          { id: crypto.randomUUID(), role: "system", content: errorMessage },
        ]);
        return;
      }

      const data = (await response.json()) as ChatResponse;
      setMessages((prev) => [
        ...prev,
        {
          id: crypto.randomUUID(),
          role: "assistant",
          content: formatAssistantContent(data),
          type: data.type,
        },
      ]);
    } catch {
      setMessages((prev) => [
        ...prev,
        {
          id: crypto.randomUUID(),
          role: "system",
          content: "Unable to reach the chat service. Please try again.",
        },
      ]);
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <main aria-label="Chat" className="flex flex-1 flex-col">
      <section
        aria-live="polite"
        aria-label="Conversation"
        className="flex flex-1 flex-col gap-4 overflow-y-auto p-4"
      >
        {messages.map((message) => (
          <article key={message.id} aria-label={roleLabel(message.role)}>
            <p>
              <strong>{roleLabel(message.role)}:</strong>{" "}
              <span style={{ whiteSpace: "pre-wrap" }}>{message.content}</span>
            </p>
          </article>
        ))}
      </section>

      <form
        onSubmit={handleSubmit}
        aria-busy={isLoading}
        className="mt-auto flex gap-2 p-4"
      >
        <label htmlFor="chat-input" className="sr-only">
          Message
        </label>
        <input
          id="chat-input"
          type="text"
          value={input}
          onChange={(event) => setInput(event.target.value)}
          disabled={isLoading}
          className="flex-1"
        />
        <button type="submit" disabled={isLoading || input.trim().length === 0}>
          {isLoading ? "Sending..." : "Send"}
        </button>
      </form>
    </main>
  );
}

function roleLabel(role: ChatMessage["role"]): string {
  switch (role) {
    case "user":
      return "You";
    case "assistant":
      return "Assistant";
    case "system":
      return "Error";
  }
}
