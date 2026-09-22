interface SendIconProps {
  className?: string;
}

/*
 * Outlined paper plane. The notch at x=9 on the left edge is what gives
 * the silhouette its crease; traced from the reference, where the notch
 * sits at roughly 35% of the icon's width.
 */
export function SendIcon({ className }: SendIconProps) {
  return (
    <svg
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth={1.9}
      strokeLinecap="round"
      strokeLinejoin="round"
      aria-hidden="true"
      focusable="false"
      className={className}
    >
      <path d="M2.4 2.2 22 12 2.4 21.8 9 12Z" />
    </svg>
  );
}
