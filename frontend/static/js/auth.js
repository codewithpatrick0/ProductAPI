import { call_fetch } from "./api.js";

async function register() {
    const FormRegister = document.getElementById('auth-form-register')
    FormRegister.addEventListener('submit', async function(event) {
        event.preventDefault();

        const data_form = new FormData(FormRegister)
        const object_register = Object.fromEntries(data_form)

        const response = await call_fetch('POST', 'http://127.0.0.1:8000/auth/register', {}, object_register)
        
        if (!response.ok) {
            alert('Algo falló!')
        } else {
            alert('Loged in')
        }
        console.log(response)
        
    })
}

async function login() {
    const FormLogin = document.getElementById('auth-form-login')
    FormLogin.addEventListener('submit', async function (event) {
        event.preventDefault();

        const data_form = new FormData(FormLogin)
        const object_login = Object.fromEntries(data_form)

        const response = await call_fetch('POST', 'http://127.0.0.1:8000/auth/login', {}, object_login)

        if (!response.ok) {
            alert('Algo falló!')
        } else {
            alert('Loged in')
            schedule_refresh()
        }
        console.log(response)
    })
}

async function refresh() {
    const response = await call_fetch('POST', 'http://127.0.0.1:8000/auth/refresh', {}, null)
    console.log(response)
    return response
}

const ACCESS_TOKEN_LIFETIME_MS = 14 * 60 * 1000 // 1 min antes de que expire el access token (15 min)
let refresh_interval_id = null

function schedule_refresh() {
    if (refresh_interval_id) {
        clearInterval(refresh_interval_id)
    }
    refresh_interval_id = setInterval(async function () {
        const response = await refresh()
        if (!response.ok) {
            clearInterval(refresh_interval_id)
        }
    }, ACCESS_TOKEN_LIFETIME_MS)
}

register()
login()