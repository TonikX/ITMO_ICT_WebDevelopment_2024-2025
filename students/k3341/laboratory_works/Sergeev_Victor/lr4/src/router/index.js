import { createRouter, createWebHistory } from 'vue-router'
import Register from '@/components/Register.vue'
import Login from '@/components/Login.vue'
import Home from '@/components/Home.vue'
import AuthorListPage from '@/pages/Author/AuthorListPage.vue'
import AuthorCreatePage from '@/pages/Author/AuthorCreatePage.vue'
import AuthorDetailPage from '@/pages/Author/AuthorDetailPage.vue'
import GenreListPage from '@/pages/Genre/GenreListPage.vue'
import GenreCreatePage from '@/pages/Genre/GenreCreatePage.vue'
import GenreDetailPage from '@/pages/Genre/GenreDetailPage.vue'
import ReadingRoomListPage from '@/pages/ReadingRoom/ReadingRoomListPage.vue'
import ReadingRoomCreatePage from '@/pages/ReadingRoom/ReadingRoomCreatePage.vue'
import ReadingRoomDetailPage from '@/pages/ReadingRoom/ReadingRoomDetailPage.vue'
import BookListPage from '@/pages/Book/BookListPage.vue'
import BookDetailPage from '@/pages/Book/BookDetailPage.vue'
import BookCreatePage from '@/pages/Book/BookCreatePage.vue'
import BookGenreCreatePage from '@/pages/Book/BookGenreCreatePage.vue'
import BookAuthorCreatePage from '@/pages/Book/BookAuthorCreatePage.vue'
import BookCopyListPage from '@/pages/BookCopy/BookCopyListPage.vue'
import BookCopyCreatePage from '@/pages/BookCopy/BookCopyCreatePage.vue'
import BookCopyDetailPage from '@/pages/BookCopy/BookCopyDetailPage.vue'
import ReaderListPage from '@/pages/Reader/ReaderListPage.vue'
import ReaderCreatePage from '@/pages/Reader/ReaderCreatePage.vue'
import ReaderDetailPage from '@/pages/Reader/ReaderDetailPage.vue'
import BookTakeListPage from '@/pages/BookTake/BookTakeListPage.vue'
import BookTakeCreatePage from '@/pages/BookTake/BookTakeCreatePage.vue'
import BookTakeDetailPage from '@/pages/BookTake/BookTakeDetailPage.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {path: '/', name: 'home', component: Home},
    {path: '/login', name: 'login', component: Login},
    {path: '/register', name: 'register', component: Register},

    {path: '/author', name: 'author-list', component: AuthorListPage},
    {path: '/author/create', name: 'author-create', component: AuthorCreatePage},
    {path: '/author/:id', name: 'author-detail', component: AuthorDetailPage},

    {path: '/genre', name: 'genre-list', component: GenreListPage},
    {path: '/genre/create', name: 'genre-create', component: GenreCreatePage},
    {path: '/genre/:id', name: 'genre-detail', component: GenreDetailPage},

    {path: '/room', name: 'reading-room-list', component: ReadingRoomListPage},
    {path: '/room/create', name: 'reading-room-create', component: ReadingRoomCreatePage},
    {path: '/room/:id', name: 'reading-room-detail', component: ReadingRoomDetailPage},

    {path: '/book', name: 'book-list', component: BookListPage},
    {path: '/book/:id', name: 'book-detail', component: BookDetailPage},
    {path: '/book/create', name: 'book-create', component: BookCreatePage},
    {path: '/book/:id/add_genre', name: 'add-book-genre', component: BookGenreCreatePage},
    {path: '/book/:id/add_author', name: 'add-book-author', component: BookAuthorCreatePage},

    {path: '/book_copy', name: 'book-copy-list', component: BookCopyListPage},
    {path: '/book_copy/create', name: 'book-copy-create', component: BookCopyCreatePage},
    {path: '/book_copy/:id', name: 'book-copy-detail', component: BookCopyDetailPage},
    
    {path: '/reader', name: 'reader-list', component: ReaderListPage},
    {path: '/reader/create', name: 'reader-create', component: ReaderCreatePage},
    {path: '/reader/:id', name: 'reader-detail', component: ReaderDetailPage},
    
    {path: '/reader/book_take/:id', name: 'reader-book-takes', component: BookTakeListPage},
    {path: '/book_take/:id', name: 'book-take-detail', component: BookTakeDetailPage},
    {path: '/book_take/create', name: 'book-take-create', component: BookTakeCreatePage},
  ],
})


export default router
