import { createRouter, createWebHistory } from 'vue-router'
import Login from "@/components/LoginPage.vue";
import RegisterPage from "@/components/RegisterPage.vue";

import AddCategory from "@/components/Category/AddCategory.vue";
import CategoryList from "@/components/Category/CategoryList.vue";
import CategoryPage from "@/components/Category/CategoryPage.vue";
import AddAuthor from "@/components/Author/AddAuthor.vue";
import AuthorList from "@/components/Author/AuthorList.vue";
import AuthorPage from "@/components/Author/AuthorPage.vue";
import AddReadingRoom from "@/components/ReadingRoom/AddReadingRoom.vue";
import ReadingRoomList from "@/components/ReadingRoom/ReadingRoomList.vue";
import ReadingRoomPage from "@/components/ReadingRoom/RedingRoomPage.vue";
import ShowReaders from "@/components/ReadingRoom/ShowReaders.vue";
import AddBook from "@/components/Book/AddBook.vue";
import BookList from "@/components/Book/BookList.vue";
import BookPage from "@/components/Book/BookPage.vue";
import AddBookCopy from "@/components/BookCopy/AddBookCopy.vue";
import BookCopyList from "@/components/BookCopy/BookCopyList.vue";
import BookCopyPage from "@/components/BookCopy/BookCopyPage.vue";
import AddReader from "@/components/Reader/AddReader.vue";
import ReaderList from "@/components/Reader/ReaderList.vue";
import ReaderPage from "@/components/Reader/ReaderPage.vue";
import YongestReader from "@/components/Reader/YongestReader.vue";
import ShowBookTaken from "@/components/Reader/ShowBookTaken.vue";
import AddBookTake from "@/components/BookTake/AddBooktake.vue";
import BookTakeList from "@/components/BookTake/BookTakeList.vue";
import BookTakePage from "@/components/BookTake/BookTakePage.vue";
import LastMonth from "@/components/BookTake/LastMonth.vue";




const routes =[
    {path: '/login', component: Login},
    {path: '/register', component: RegisterPage},

    {path: '/add-category', component: AddCategory},
    {path: '/categories', component: CategoryList},
    {path: '/categories/:id', component: CategoryPage},

    {path: '/add-author', component: AddAuthor},
    {path: '/authors', component: AuthorList},
    {path: '/authors/:id', component: AuthorPage},

    {path: '/add-readingroom', component: AddReadingRoom},
    {path: '/readingrooms', component: ReadingRoomList},
    {path: '/readingrooms/:id', component: ReadingRoomPage},

    {path: '/add-book', component: AddBook},
    {path: '/books', component: BookList},
    {path: '/books/:id', component: BookPage},

    {path: '/add-book-copy', component: AddBookCopy},
    {path: '/book-copies', component: BookCopyList},
    {path: '/book-copies/:id', component: BookCopyPage},

    {path: '/add-reader', component: AddReader},
    {path: '/readers', component: ReaderList},
    {path: '/readers/youngest', component: YongestReader},
    {path: '/readers/:id', component: ReaderPage},
    {path: '/readers/:id/show-books-taken', component: ShowBookTaken},

    {path: '/add-book-take', component: AddBookTake},
    {path: '/book-takes', component: BookTakeList},
    {path: '/book-takes/:id', component: BookTakePage},
    {path: '/book-takes/last_month', component: LastMonth},
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

export default router
