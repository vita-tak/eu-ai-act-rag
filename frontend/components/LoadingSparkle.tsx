import { SparkleIcon } from "./SparkleIcon";

/*
 * The reference shows the assistant card arriving immediately with a
 * sparkle pulsing inside it, rather than a text status. The reference
 * sparkle is white; a pale slate is used so it still reads when the card
 * sits on plain white rather than over the gradient.
 */
export function LoadingSparkle() {
  return (
    <div className="flex flex-col items-end">
      <div className="w-full sm:max-w-[65%]">
        <p className="label-micro pb-2">Compliance assistant</p>
        <div className="flex items-center gap-2.5 rounded-xl surface-ring border border-[var(--hairline)] bg-[var(--surface)] px-5 py-4">
          <SparkleIcon className="sparkle-pulse size-6 text-[var(--sparkle-loading)]" />
          <span className="text-[0.9375rem] text-[var(--ink-muted)]">
            Thinking...
          </span>
        </div>
      </div>
    </div>
  );
}
