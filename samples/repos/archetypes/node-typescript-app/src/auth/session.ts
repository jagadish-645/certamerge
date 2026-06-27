export function sessionLabel(userId: string): string {
  return `session:${userId.trim().toLowerCase()}`;
}
