import "server-only";

import type {
    User,
    Chat,
    DBMessage,
    Vote,
    Document,
    Suggestion,
    Stream,
} from "@/lib/types/db-types";
import type { AppUsage } from "@/lib/usage";

/**
 * Mock database queries - These are no-op or mock implementations
 * that replace the PostgreSQL/Drizzle ORM queries.
 * 
 * All functions return empty data or perform no operations.
 * This allows the application to run without a database connection.
 */

// ============================================================================
// User Functions
// ============================================================================

export async function getUser(email: string): Promise<User[]> {
    // No database - return empty array (user not found)
    return [];
}

export async function createUser(email: string, password: string): Promise<User[]> {
    // Create a mock user with a random ID
    return [{
        id: crypto.randomUUID(),
        email,
        password,
    }];
}

export async function createGuestUser(): Promise<User[]> {
    // Create a guest user with a random ID and email
    return [{
        id: crypto.randomUUID(),
        email: `guest-${Date.now()}@guest.local`,
        password: null,
    }];
}

// ============================================================================
// Chat Functions
// ============================================================================

export async function saveChat({
    id,
    userId,
    title,
    visibility,
}: {
    id: string;
    userId: string;
    title: string;
    visibility: "public" | "private";
}): Promise<void> {
    // No-op: Chat would be saved to database
}

export async function deleteChatById({ id }: { id: string }): Promise<{ id: string }> {
    // Return the deleted chat ID (mock)
    return { id };
}

export async function deleteAllChatsByUserId({ userId }: { userId: string }): Promise<void> {
    // No-op: All chats for user would be deleted
}

export async function getChatsByUserId({
    id,
    limit,
    startingAfter,
    endingBefore,
}: {
    id: string;
    limit: number;
    startingAfter: string | null;
    endingBefore: string | null;
}): Promise<{ chats: Chat[]; hasMore: boolean }> {
    // No database - return empty chat list
    return { chats: [], hasMore: false };
}

export async function getChatById({ id }: { id: string }): Promise<Chat | null> {
    // No database - chat not found
    return null;
}

// ============================================================================
// Message Functions
// ============================================================================

export async function saveMessages({ messages }: { messages: DBMessage[] }): Promise<void> {
    // No-op: Messages would be saved to database
}

export async function getMessagesByChatId({ id }: { id: string }): Promise<DBMessage[]> {
    // No database - return empty message list
    return [];
}

export async function getMessageById({ id }: { id: string }): Promise<DBMessage[]> {
    // No database - message not found
    return [];
}

export async function deleteMessagesByChatIdAfterTimestamp({
    chatId,
    timestamp,
}: {
    chatId: string;
    timestamp: Date;
}): Promise<void> {
    // No-op: Messages would be deleted
}

// ============================================================================
// Vote Functions
// ============================================================================

export async function voteMessage({
    chatId,
    messageId,
    type,
}: {
    chatId: string;
    messageId: string;
    type: "up" | "down";
}): Promise<void> {
    // No-op: Vote would be saved
}

export async function getVotesByChatId({ id }: { id: string }): Promise<Vote[]> {
    // No database - return empty votes list
    return [];
}

// ============================================================================
// Document Functions
// ============================================================================

export async function saveDocument({
    id,
    title,
    content,
    userId,
}: {
    id: string;
    title: string;
    content: string;
    userId: string;
}): Promise<void> {
    // No-op: Document would be saved
}

export async function getDocumentsById({ id }: { id: string }): Promise<Document[]> {
    // No database - return empty document list
    return [];
}

export async function getDocumentById({ id }: { id: string }): Promise<Document | null> {
    // No database - document not found
    return null;
}

export async function deleteDocumentsByIdAfterTimestamp({
    id,
    timestamp,
}: {
    id: string;
    timestamp: Date;
}): Promise<void> {
    // No-op: Documents would be deleted
}

// ============================================================================
// Suggestion Functions
// ============================================================================

export async function saveSuggestions({
    suggestions,
}: {
    suggestions: Suggestion[];
}): Promise<void> {
    // No-op: Suggestions would be saved
}

export async function getSuggestionsByDocumentId({
    documentId,
}: {
    documentId: string;
}): Promise<Suggestion[]> {
    // No database - return empty suggestions list
    return [];
}

// ============================================================================
// Chat Update Functions
// ============================================================================

export async function updateChatVisiblityById({
    chatId,
    visibility,
}: {
    chatId: string;
    visibility: "private" | "public";
}): Promise<void> {
    // No-op: Chat visibility would be updated
}

export async function updateChatLastContextById({
    chatId,
    context,
}: {
    chatId: string;
    context: AppUsage;
}): Promise<void> {
    // No-op: Chat context would be updated
}

// ============================================================================
// Rate Limiting Functions
// ============================================================================

export async function getMessageCountByUserId({
    id,
    differenceInHours,
}: {
    id: string;
    differenceInHours: number;
}): Promise<number> {
    // No database - return 0 (no rate limiting)
    return 0;
}

// ============================================================================
// Stream Functions
// ============================================================================

export async function createStreamId({
    streamId,
    chatId,
}: {
    streamId: string;
    chatId: string;
}): Promise<void> {
    // No-op: Stream ID would be created
}

export async function getStreamIdsByChatId({ chatId }: { chatId: string }): Promise<Stream[]> {
    // No database - return empty stream list
    return [];
}
