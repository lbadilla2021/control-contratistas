import { cookies } from "next/headers";

const AUTH_COOKIE = "token";

export function getSessionToken(): string | undefined {
  const cookieStore = cookies();
  const token = cookieStore.get(AUTH_COOKIE)?.value;
  return token;
}

export function isAuthenticated(): boolean {
  return Boolean(getSessionToken());
}
