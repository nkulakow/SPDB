import { constant } from "../constant.ts"

type Method = "GET" | "POST" | "PUT" | "DELETE"

export class APIError extends Error {
    constructor(
        message: string,
        public status: number,
        public api_error_code?: string
    ) {
        super(message)
        this.api_error_code = api_error_code
    }
}

export default async function fetchAPI(
    method: Method,
    uri: string,
    body?: object
) {
    const response = await fetch(`${constant("VITE_APP_API_URL")}${uri}`, {
        method,
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(body),
    })
    let data: any = null
    try {
        data = await response.json()
    } catch (e) {}
    if (!response.ok) {
        const message = data?.error || data?.message || response.statusText
        const apiErrorCode = data?.api_error_code
        throw new APIError(message, response.status, apiErrorCode)
    }
    return await data
}
