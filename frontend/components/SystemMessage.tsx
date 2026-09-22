interface SystemMessageProps {
  text: string;
}

export function SystemMessage({ text }: SystemMessageProps) {
  return (
    <div className="flex flex-col items-end">
      <div className="w-full sm:max-w-[65%]">
        <p className="label-micro pb-2 text-[var(--risk-high-fg)]">Error</p>
        <p className="rounded-xl border border-[var(--risk-high-br)] bg-[var(--risk-high-bg)] px-5 py-3.5 text-[0.9375rem] leading-[1.5] text-[var(--risk-high-fg)]">
          {text}
        </p>
      </div>
    </div>
  );
}
