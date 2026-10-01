const TOKEN_KEY = "acess_token";

export function salvarToken(token: string) {
  localStorage.setItem(TOKEN_KEY, token);
}

export function obterToken(): string | null {
  return localStorage.getItem(TOKEN_KEY);
}

export function logout() {
  localStorage.removeItem(TOKEN_KEY);
  window.location.href = "login.html"
}
