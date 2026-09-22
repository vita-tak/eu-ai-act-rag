interface UserMessageProps {
  text: string;
}

export function UserMessage({ text }: UserMessageProps) {
  return (
    <div className="flex flex-col items-start">
      <p className="label-micro pb-2">Me</p>
      <p className="max-w-[80%] rounded-xl surface-ring border border-[var(--hairline)] bg-[var(--surface-strong)] px-5 py-3 text-[0.9375rem] leading-[1.45] text-ink">
        {text}
      </p>
    </div>
  );
}
