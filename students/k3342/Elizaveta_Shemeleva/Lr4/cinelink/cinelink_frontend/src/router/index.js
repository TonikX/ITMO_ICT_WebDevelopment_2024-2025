import {createRouter, createWebHistory} from "vue-router";
import MainPage from "@/components/MainPage.vue";
import FriendsPage from "@/components/FriendsPage.vue";
import FriendProfile from "@/components/FriendProfile.vue";
import EditProfile from "@/components/EditProfile.vue";
import FriendsActivity from "@/components/FriendsActivity.vue";
import ListPage from "@/components/ListPage.vue";
import LoginPage from "@/components/LoginPage.vue";
import MovieDetails from "@/components/MovieDetails.vue";
import SearchResults from "@/components/SearchResults.vue";
import SignUp from "@/components/SignUp.vue";
import UserProfile from "@/components/UserProfile.vue";

const routes = [
    {path: "/", name: "MainPage", component: MainPage},
    {path: "/friends", name: "FriendsPage", component: FriendsPage},
    {path: "/friend/:userId", name: "FriendProfile", component: FriendProfile},
    {path: "/edit-profile", name: "EditProfile", component: EditProfile},
    {path: "/friends-activity", name: "FriendsActivity", component: FriendsActivity},
    {path: "/list", name: "ListPage", component: ListPage},
    {path: "/login", name: "LoginPage", component: LoginPage},
    {path: "/movie/:id", name: "MovieDetails", component: MovieDetails},
    {path: "/profile", name: "UserProfile", component: UserProfile},
    {path: "/search", name: "SearchResults", component: SearchResults},
    {path: "/signup", name: "SignUp", component: SignUp},
];

const router = createRouter({
    history: createWebHistory(),
    routes,
});

export default router;