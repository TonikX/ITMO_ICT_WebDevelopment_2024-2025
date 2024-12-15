import {defineStore} from 'pinia'
import {ref} from "vue";

export const TokenStore = defineStore('TokenStore', () => {
    let token = ref(null)

    function setToken(newToken){
        token.value = newToken
    }

    function deleteToken(){
        token.value = null
    }

    return {token, setToken, deleteToken}
}, {persist: true})
