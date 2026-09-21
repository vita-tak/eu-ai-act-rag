const DEFAULT_API_URL = 'http://localhost:8000';
const BACKEND_TIMEOUT_MS = 70000;

interface ChatRequestBody {
  conversation_id: string;
  message: string;
}

function isValidChatRequestBody(body: unknown): body is ChatRequestBody {
  if (typeof body !== 'object' || body === null) {
    return false;
  }

  const candidate = body as Record<string, unknown>;

  return (
    typeof candidate.conversation_id === 'string' &&
    candidate.conversation_id.trim().length > 0 &&
    typeof candidate.message === 'string' &&
    candidate.message.trim().length > 0
  );
}

export async function POST(request: Request): Promise<Response> {
  let body: unknown;

  try {
    body = await request.json();
  } catch {
    return Response.json({ error: 'Invalid JSON body' }, { status: 400 });
  }

  if (!isValidChatRequestBody(body)) {
    return Response.json(
      {
        error:
          "Request body must include non-empty string fields 'conversation_id' and 'message'",
      },
      { status: 400 },
    );
  }

  const apiUrl = process.env.NEXT_PUBLIC_API_URL ?? DEFAULT_API_URL;

  let backendResponse: Response;

  try {
    backendResponse = await fetch(`${apiUrl}/chat`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        conversation_id: body.conversation_id,
        message: body.message,
      }),
      signal: AbortSignal.timeout(BACKEND_TIMEOUT_MS),
    });
  } catch (error) {
    if (error instanceof Error && error.name === 'TimeoutError') {
      console.error('Chat proxy: backend request timed out', error);
      return Response.json({ error: 'AI service timed out' }, { status: 504 });
    }

    console.error('Chat proxy: backend unreachable', error);
    return Response.json(
      { error: 'Unable to reach the AI service. Please try again shortly.' },
      { status: 502 },
    );
  }

  if (!backendResponse.ok) {
    const details = await backendResponse
      .clone()
      .json()
      .catch(() => backendResponse.text().catch(() => null));

    return Response.json(
      { error: 'AI service error', details },
      { status: backendResponse.status },
    );
  }

  try {
    const data = await backendResponse.json();
    return Response.json(data, { status: 200 });
  } catch (error) {
    console.error('Chat proxy: backend returned invalid JSON', error);
    return Response.json(
      { error: 'AI service returned an unexpected response' },
      { status: 502 },
    );
  }
}
