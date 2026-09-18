const TOKEN_KEY = "swp_token";

export function getToken() {
  return localStorage.getItem(TOKEN_KEY);
}

export function setSession(data) {
  localStorage.setItem(TOKEN_KEY, data.access_token);
  localStorage.setItem("swp_role", data.role);
  localStorage.setItem("swp_name", data.name);
  localStorage.setItem("swp_uid", String(data.user_id));
}

export function clearSession() {
  localStorage.removeItem(TOKEN_KEY);
  localStorage.removeItem("swp_role");
  localStorage.removeItem("swp_name");
  localStorage.removeItem("swp_uid");
}

export function session() {
  return {
    token: getToken(),
    role: localStorage.getItem("swp_role"),
    name: localStorage.getItem("swp_name"),
    userId: localStorage.getItem("swp_uid"),
  };
}

export async function api(path, options = {}) {
  const headers = { ...(options.headers || {}) };
  if (options.body && !(options.body instanceof FormData)) {
    headers["Content-Type"] = "application/json";
  }
  const token = getToken();
  if (token) headers.Authorization = `Bearer ${token}`;
  const res = await fetch(path, { ...options, headers });
  const text = await res.text();
  let data = null;
  try {
    data = text ? JSON.parse(text) : null;
  } catch {
    data = { detail: text };
  }
  if (!res.ok) {
    const msg = data?.detail
      ? typeof data.detail === "string"
        ? data.detail
        : JSON.stringify(data.detail)
      : res.statusText;
    throw new Error(msg);
  }
  return data;
}
