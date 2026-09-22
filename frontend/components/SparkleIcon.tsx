interface Star {
  cx: number;
  cy: number;
  r: number;
}

/*
 * The mark is a cluster of three four-pointed stars: two stacked on the
 * left, meeting at their points, and one slightly smaller to the right at
 * mid-height. Traced from the reference design.
 */
const STARS: readonly Star[] = [
  { cx: 9, cy: 8.6, r: 6.2 },
  { cx: 9, cy: 20.2, r: 5.4 },
  { cx: 19.4, cy: 14.4, r: 5.2 },
];

/*
 * A four-pointed star with concave edges. Each cubic pulls its control
 * points close to the centre, which is what gives the points their taper.
 */
function starPath({ cx, cy, r }: Star): string {
  const c = r * 0.26;
  return [
    `M${cx} ${cy - r}`,
    `C${cx} ${cy - c} ${cx + c} ${cy} ${cx + r} ${cy}`,
    `C${cx + c} ${cy} ${cx} ${cy + c} ${cx} ${cy + r}`,
    `C${cx} ${cy + c} ${cx - c} ${cy} ${cx - r} ${cy}`,
    `C${cx - c} ${cy} ${cx} ${cy - c} ${cx} ${cy - r}`,
    "Z",
  ].join("");
}

interface SparkleIconProps {
  className?: string;
}

export function SparkleIcon({ className }: SparkleIconProps) {
  return (
    <svg
      viewBox="0 0 28 28"
      fill="currentColor"
      aria-hidden="true"
      focusable="false"
      className={className}
    >
      {STARS.map((star) => (
        <path key={`${star.cx}-${star.cy}`} d={starPath(star)} />
      ))}
    </svg>
  );
}
