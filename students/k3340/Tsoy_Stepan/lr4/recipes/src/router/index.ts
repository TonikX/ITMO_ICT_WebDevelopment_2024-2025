import {createRouter, createWebHistory} from 'vue-router'
import HomeView from '../views/HomeView.vue'
import LoginView from "@/views/LoginView.vue";
import RegisterView from "@/views/RegisterView.vue";
import RecipeListView from "@/views/RecipeListView.vue";
import RecipePage from "@/views/RecipePage.vue";
import RecipeEditView from "@/views/RecipeEditView.vue";
import RecipeDeleteView from "@/views/RecipeDeleteView.vue";
import AccountView from "@/views/AccountView.vue";
import CreateView from "@/views/CreateView.vue";
import FavouriteRecipes from "@/views/FavouriteRecipes.vue";

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [
        {
            path: '/',
            name: 'home',
            component: HomeView,
        },

        {path: '/recipes', name: "recipesList", component: RecipeListView},
        {path: "/recipes/:id", component: RecipePage, props: true, name: "recipeDetails"},
        {path: "/recipes/:id/delete", component: RecipeDeleteView, props: true, name: "recipeDelete"},
        {path: "/recipes/:id/edit", component: RecipeEditView, props: true, name: "recipeEdit"},
        {path: '/login', name: "login", component: LoginView},
        {path: '/register', name: "register", component: RegisterView},
        {path: '/account', name: "account", component: AccountView},
        {path: '/account/new', name: "recipeCreate", component: CreateView},
        {path: '/favourites', name: "favouriteRecipe", component: FavouriteRecipes},

    ],
})

export default router
