"use client";

import { SendIcon } from "./SendIcon";

interface ChatComposerProps {
  value: string;
  onChange: (value: string) => void;
  onSubmit: () => void;
  isLoading: boolean;
}

export function ChatComposer({
  value,
  onChange,
  onSubmit,
  isLoading,
}: ChatComposerProps) {
  const canSend = value.trim().length > 0 && !isLoading;

  return (
    <form
      onSubmit={(event) => {
        event.preventDefault();
        onSubmit();
      }}
      aria-busy={isLoading}
      className="pb-10"
    >
      <div className="flex h-14 items-center gap-2 rounded-[10px] border border-[var(--field-border)] bg-[var(--surface-solid)] pr-3 pl-[18px] focus-within:border-ink/35">
        <label htmlFor="chat-input" className="sr-only">
          Ask about the EU AI Act or describe your AI system
        </label>
        <input
          id="chat-input"
          type="text"
          value={value}
          onChange={(event) => onChange(event.target.value)}
          placeholder="Ask about the EU AI Act or describe your AI system..."
          autoComplete="off"
          className="h-full min-w-0 flex-1 bg-transparent text-[0.9375rem] text-ink outline-none placeholder:text-[var(--ink-placeholder)]"
        />
        <button
          type="submit"
          disabled={!canSend}
          className="grid size-10 shrink-0 place-items-center rounded-md text-[var(--send)] transition-colors hover:text-ink focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-ink disabled:cursor-default disabled:hover:text-[var(--send)]"
        >
          <span className="sr-only">{isLoading ? "Sending" : "Send"}</span>
          <SendIcon className="size-[32px]" />
        </button>
      </div>
    </form>
  );
}
