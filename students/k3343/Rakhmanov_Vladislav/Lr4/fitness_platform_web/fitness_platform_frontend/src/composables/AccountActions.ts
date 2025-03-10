import {ClearAuthToken, SetAuthToken} from "@/composables/tokenActions.ts";
import api from "@/services/axios.ts";

interface RegisterResponse {
    email: string;
    username: string;
    id: number;
}

interface LoginResponse {
    auth_token: string;
}

interface LoginError {
    username?: string[];
    password?: string[];
    non_field_errors?: string[];
    detail?: string;
}

export interface UserInfo{
    id: 1,
    email: string
    username: string
    first_name: string
    last_name: string
    is_superuser: boolean
}

export function logout() {
    ClearAuthToken()
}

export async function login(username: string, password: string): Promise<void> {
    try {
        const response = await api.post<LoginResponse>('auth/token/login', {
            username: username,
            password: password,
        })

        SetAuthToken(response.data.auth_token)
    } catch (error: any) {
        const errorData = error.response?.data as LoginError | undefined;
        if (errorData) {
            console.log("Login failed", errorData)
        } else {
            console.log("Unexpected error", error)
        }
    }
}

export async function register(email: string,
                               password: string,
                               re_password: string,
                               username: string): Promise<void> {
    const response = await api.post<RegisterResponse>('auth/users/', {
        email: email,
        password: password,
        re_password: re_password,
        username: username
    })
    if (response.status === 201) {
        await login(username, password)
    } else {
        throw new Error("Unexpected error")
    }
}

export async function isAdmin(): Promise<boolean> {
    try {
        const response = await api.get<UserInfo>('fitness/current-user/')
        return response.data.is_superuser
    } catch (e) {
        return false
    }
}