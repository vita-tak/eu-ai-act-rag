import type { ChatResponse } from "@/types/chat";

/*
 * The UI keeps the backend's structured response intact so each of the
 * three response types can render itself, rather than flattening
 * everything into one string.
 *
 * This composes the exported types from types/chat.ts instead of
 * modifying them.
 */
export type UiMessage =
  | { id: string; role: "user"; text: string }
  | { id: string; role: "assistant"; response: ChatResponse }
  | { id: string; role: "system"; text: string };

export function roleLabel(role: UiMessage["role"]): string {
  switch (role) {
    case "user":
      return "Me";
    case "assistant":
      return "Compliance assistant";
    case "system":
      return "Error";
  }
}
