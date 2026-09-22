import type { Metadata } from "next";
import localFont from "next/font/local";
import "./globals.css";

/*
 * Switzer is not published on Google Fonts or Bunny Fonts, so it is
 * self-hosted here from the Fontshare variable release. One 43 KB file
 * covers weights 100-900, which keeps the request count at zero and
 * avoids layout shift.
 */
const switzer = localFont({
  src: "./fonts/Switzer-Variable.woff2",
  weight: "100 900",
  variable: "--font-switzer",
  display: "swap",
});

export const metadata: Metadata = {
  title: "EU AI Act Compliance Assistant",
  description:
    "Ask questions about EU AI Act regulations or classify your AI system's risk level.",
};

export default function RootLayout({ children }: LayoutProps<"/">) {
  return (
    <html
      lang="en"
      className={`${switzer.variable} h-full antialiased`}
      style={{ colorScheme: "light" }}
    >
      <body className="flex min-h-full flex-col">{children}</body>
    </html>
  );
}
