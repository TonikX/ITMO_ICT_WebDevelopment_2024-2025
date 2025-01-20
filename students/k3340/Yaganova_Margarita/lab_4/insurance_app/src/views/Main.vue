<template>
    <div class="container">
    <h1>Insurance agency</h1>

    <ul>
        <li>
            <router-link :to="{name: 'enterprises'}">Enterprises</router-link>
        </li>
        <li>
            <router-link :to="{name: 'clients'}">Clients</router-link>
        </li>
        <li>
            <router-link :to="{name: 'contracts'}">Contracts</router-link>
        </li>
        <li>
            <router-link :to="{name: 'specialization'}">Specializations</router-link>
        </li>
        <li>
            <router-link :to="{name: 'payouts'}">Payouts</router-link>
        </li>
        <li>
            <router-link :to="{name: 'login'}">Login</router-link>
        </li>
        <li>
            <router-link :to="{name: 'reg'}">Registration</router-link>
        </li>
    </ul>
    </div>
</template>

<style>
.container {
    margin: 10px;
}
</style>