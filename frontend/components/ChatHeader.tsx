import { SparkleIcon } from "./SparkleIcon";

const TITLE = "EU AI Act Compliance Assistant";
const SUBTITLE =
  "Ask questions about EU AI Act regulations or classify your AI system’s risk level.";

interface ChatHeaderProps {
  /*
   * The reference treats the title and the subtitle as alternates: the
   * empty state leads with the invitation, and once a conversation is
   * under way the header falls back to the product name.
   */
  hasMessages: boolean;
}

export function ChatHeader({ hasMessages }: ChatHeaderProps) {
  return (
    <header
      className={`flex flex-col items-center text-center ${hasMessages ? "pt-[155px]" : "pt-[124px]"} [@media(max-height:720px)]:pt-10`}
    >
      <SparkleIcon className="size-[52px] text-ink" />
      {hasMessages ? (
        <h1 className="mt-10 text-[1.625rem] leading-[1.22] font-normal tracking-[-0.011em] text-ink">
          {TITLE}
        </h1>
      ) : (
        <>
          <h1 className="sr-only">{TITLE}</h1>
          <p className="mt-10 max-w-[344px] text-[1.625rem] leading-[1.22] font-normal tracking-[-0.011em] text-ink">
            {SUBTITLE}
          </p>
        </>
      )}
    </header>
  );
}
