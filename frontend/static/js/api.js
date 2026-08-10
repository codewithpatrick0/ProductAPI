export async function call_fetch(method,
    url,
    headers = {},
    body = null
) {
    let config = {
        method: method,
        headers: headers,
        credentials: 'include'
    };

    if (body){
        config.headers = {'Content-Type': 'application/json'}
        config.body = JSON.stringify(body)
    }
    try {
        const response = await fetch(url, config)
        const data = response.status === 204 ? null : await response.json()
        return {
                ok: response.ok,
                status: response.status,
                data: data
                }
    } catch (error) {
        return {
            ok: false,
            status: null,
            data: { detail: error.message }
            }
    }
}
