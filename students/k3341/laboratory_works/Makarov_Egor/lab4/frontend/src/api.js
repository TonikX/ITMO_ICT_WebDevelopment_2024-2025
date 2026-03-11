const BASE = 'http://localhost:8000'

export function api(token) {
  const h = () => ({
    'Content-Type': 'application/json',
    Authorization: `Token ${token}`,
  })

  async function request(method, path, body) {
    const res = await fetch(`${BASE}${path}`, {
      method,
      headers: h(),
      body: body ? JSON.stringify(body) : undefined,
    })
    const data = res.status === 204 ? null : await res.json()
    if (!res.ok) {
      const msg = data ? Object.values(data).flat().join(' ') : res.statusText
      throw new Error(msg)
    }
    return data
  }

  return {
    get:  (path)       => request('GET',    path),
    post: (path, body) => request('POST',   path, body),
    patch:(path, body) => request('PATCH',  path, body),
    put:  (path, body) => request('PUT',    path, body),
    del:  (path)       => request('DELETE', path),
  }
}