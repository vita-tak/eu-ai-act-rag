import { SparkleIcon } from "./SparkleIcon";

export const TITLE = "EU AI Act Compliance Assistant";
const SUBTITLE =
  "Ask questions about EU AI Act regulations or classify your AI system’s risk level.";

interface ChatHeaderProps {
  /*
   * The reference treats the title and the subtitle as alternates: the
   * empty state leads with the invitation, and once a conversation is
   * under way the header falls back to the product name. Once a
   * conversation is under way, the title moves to a fixed top-left bar
   * (rendered separately, see FixedHeaderTitle) and the sparkle moves
   * into the scrollable conversation, so this component only renders the
   * empty-state block in that case.
   */
  hasMessages: boolean;
}

export function ChatHeader({ hasMessages }: ChatHeaderProps) {
  if (hasMessages) {
    return <h1 className="sr-only">{TITLE}</h1>;
  }

  return (
    <header className="flex flex-col items-center pt-[124px] text-center [@media(max-height:720px)]:pt-10">
      <SparkleIcon className="size-[52px] text-ink" />
      <h1 className="sr-only">{TITLE}</h1>
      <p className="mt-10 max-w-[344px] text-[1.625rem] leading-[1.22] font-normal tracking-[-0.011em] text-ink">
        {SUBTITLE}
      </p>
    </header>
  );
}

/*
 * Fixed top-left title shown once a conversation is active. Lives outside
 * the scrollable conversation area, unlike the sparkle mark, which scrolls
 * away with the rest of the content it introduces.
 */
export function FixedHeaderTitle() {
  return (
    <div className="fixed top-0 left-0 z-10 px-6 pt-6">
      <p className="text-[0.9375rem] font-medium text-ink">{TITLE}</p>
    </div>
  );
}
