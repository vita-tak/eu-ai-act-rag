/*
 * The six values the agent can emit, from the generate_report tool schema
 * in ai-service/src/agent/tools.py. Matched case-insensitively, with a
 * neutral fallback so an unrecognised value still renders legibly.
 *
 * Prohibited practice outranks High risk under the Act, so it is the only
 * tier rendered as a solid fill rather than a tint.
 */
const TIER_STYLES: Record<string, string> = {
  "prohibited practice":
    "bg-[var(--risk-prohibited-bg)] text-[var(--risk-prohibited-fg)] border-transparent",
  "high risk":
    "bg-[var(--risk-high-bg)] text-[var(--risk-high-fg)] border-[var(--risk-high-br)]",
  "limited risk":
    "bg-[var(--risk-limited-bg)] text-[var(--risk-limited-fg)] border-[var(--risk-limited-br)]",
  "minimal risk":
    "bg-[var(--risk-minimal-bg)] text-[var(--risk-minimal-fg)] border-[var(--risk-minimal-br)]",
  gpai:
    "bg-[var(--risk-info-bg)] text-[var(--risk-info-fg)] border-[var(--risk-info-br)]",
  "not an ai system":
    "bg-[var(--risk-neutral-bg)] text-[var(--risk-neutral-fg)] border-[var(--risk-neutral-br)]",
};

const NEUTRAL =
  "bg-[var(--risk-neutral-bg)] text-[var(--risk-neutral-fg)] border-[var(--risk-neutral-br)]";

interface RiskBadgeProps {
  classification: string;
}

export function RiskBadge({ classification }: RiskBadgeProps) {
  const tier = TIER_STYLES[classification.trim().toLowerCase()] ?? NEUTRAL;

  return (
    <span
      className={`inline-flex items-center rounded-md border px-3 py-1.5 text-[1.0625rem] leading-none font-semibold tracking-[-0.005em] ${tier}`}
    >
      {classification}
    </span>
  );
}
