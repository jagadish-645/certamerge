export function canViewWorkspace(role: string): boolean {
  return role === "admin" || role === "reviewer";
}
