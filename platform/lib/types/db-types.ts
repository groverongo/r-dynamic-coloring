/**
 * Database types - Standalone type definitions that don't depend on Drizzle ORM.
 * These replace the types previously inferred from the Drizzle schema.
 */

import type { AppUsage } from "../usage";

export interface User {
    id: string;
    email: string;
    password: string | null;
}

export interface Chat {
    id: string;
    createdAt: Date;
    title: string;
    userId: string;
    visibility: "public" | "private";
    lastContext: AppUsage | null;
}

export interface DBMessage {
    id: string;
    chatId: string;
    role: string;
    parts: any;
    attachments: any;
    createdAt: Date;
}

export interface Vote {
    chatId: string;
    messageId: string;
    isUpvoted: boolean;
}

export interface Document {
    id: string;
    createdAt: Date;
    title: string;
    content: string | null;
    kind: "text" | "code" | "image" | "sheet";
    userId: string;
}

export interface Suggestion {
    id: string;
    documentId: string;
    documentCreatedAt: Date;
    originalText: string;
    suggestedText: string;
    description: string | null;
    isResolved: boolean;
    userId: string;
    createdAt: Date;
}

export interface Stream {
    id: string;
    chatId: string;
    createdAt: Date;
}

// Re-export for backwards compatibility
export type { AppUsage };
