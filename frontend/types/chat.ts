export interface RagResponse {
  type: "rag_response";
  answer: string;
  sources: string[];
}

export interface FollowUpResponse {
  type: "follow_up";
  question: string;
}

export interface ClassificationReport {
  classification: string;
  reasoning: string;
  cited_articles: string[];
}

export interface ClassificationResponse {
  type: "classification";
  report: ClassificationReport;
}

export type ChatResponse =
  | RagResponse
  | FollowUpResponse
  | ClassificationResponse;

export type MessageRole = "user" | "assistant" | "system";

export interface ChatMessage {
  id: string;
  role: MessageRole;
  content: string;
  type?: ChatResponse["type"];
}
