import { generateId } from "ai";
import { genSaltSync, hashSync } from "bcrypt-ts";

export const isProductionEnvironment = process.env.NODE_ENV === "production";
export const isDevelopmentEnvironment = process.env.NODE_ENV === "development";
export const isTestEnvironment = Boolean(
  process.env.PLAYWRIGHT_TEST_BASE_URL ||
  process.env.PLAYWRIGHT ||
  process.env.CI_PLAYWRIGHT
);

export const guestRegex = /^guest-\d+$/;

// Inlined from db/utils to remove database dependency
function generateDummyPassword() {
  const password = generateId();
  const salt = genSaltSync(10);
  return hashSync(password, salt);
}

export const DUMMY_PASSWORD = generateDummyPassword();
