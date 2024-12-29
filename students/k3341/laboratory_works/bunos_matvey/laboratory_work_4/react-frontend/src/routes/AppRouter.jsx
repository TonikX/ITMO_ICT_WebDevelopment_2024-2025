// src/routes/AppRouter.jsx
import React from 'react';
import { Routes, Route } from 'react-router-dom';

import MainLayout from '../layout/MainLayout';
import HomePage from '../pages/HomePage';
import LoginPage from '../pages/LoginPage';
import RegisterPage from '../pages/RegisterPage';
// Author
import AuthorsListPage from '../pages/authors/AuthorsListPage';
import AuthorFormPage from '../pages/authors/AuthorFormPage';
// ReadingRoom
import ReadingRoomsListPage from '../pages/readingRooms/ReadingRoomsListPage';
import ReadingRoomFormPage from '../pages/readingRooms/ReadingRoomFormPage';
// Book
import BooksListPage from '../pages/books/BooksListPage';
import BookFormPage from '../pages/books/BookFormPage';
// Reader
import ReadersListPage from '../pages/readers/ReadersListPage';
import ReaderFormPage from '../pages/readers/ReaderFormPage';
import ReaderAssignedBooksPage from '../pages/readers/ReaderAssignedBooksPage';
import ReaderAvailableBooksPage from '../pages/readers/ReaderAvailableBooksPage';
import BooksReportPage from '../pages/books/BooksReportPage';


function AppRouter() {
  return (
    <Routes>
      <Route 
        path="/" 
        element={
          <MainLayout>
            <HomePage />
          </MainLayout>
        } 
      />
      <Route 
        path="/login" 
        element={
          <MainLayout>
            <LoginPage />
          </MainLayout>
        } 
      />
      <Route 
        path="/register" 
        element={
          <MainLayout>
            <RegisterPage />
          </MainLayout>
        } 
      />
      {/* Author */}
      <Route
        path="/authors"
        element={
          <MainLayout>
            <AuthorsListPage />
          </MainLayout>
        }
      />
      <Route
        path="/authors/create"
        element={
          <MainLayout>
            <AuthorFormPage />
          </MainLayout>
        }
      />
      <Route
        path="/authors/:id"
        element={
          <MainLayout>
            <AuthorFormPage />
          </MainLayout>
        }
      />

      {/* ReadingRoom */}
      <Route
        path="/reading-rooms"
        element={
          <MainLayout>
            <ReadingRoomsListPage />
          </MainLayout>
        }
      />
      <Route
        path="/reading-rooms/create"
        element={
          <MainLayout>
            <ReadingRoomFormPage />
          </MainLayout>
        }
      />
      <Route
        path="/reading-rooms/:id"
        element={
          <MainLayout>
            <ReadingRoomFormPage />
          </MainLayout>
        }
      />

      {/* Book */}
      <Route
        path="/books"
        element={
          <MainLayout>
            <BooksListPage />
          </MainLayout>
        }
      />
      <Route
        path="/books/create"
        element={
          <MainLayout>
            <BookFormPage />
          </MainLayout>
        }
      />
      <Route
        path="/books/:id"
        element={
          <MainLayout>
            <BookFormPage />
          </MainLayout>
        }
      />

      {/* Reader */}
      <Route
        path="/readers"
        element={
          <MainLayout>
            <ReadersListPage />
          </MainLayout>
        }
      />
      <Route
        path="/readers/create"
        element={
          <MainLayout>
            <ReaderFormPage />
          </MainLayout>
        }
      />
      <Route
        path="/readers/:id"
        element={
          <MainLayout>
            <ReaderFormPage />
          </MainLayout>
        }
      />

<Route
        path="/readers/:id/books-assigned"
        element={
          <MainLayout>
            <ReaderAssignedBooksPage />
          </MainLayout>
        }
      />

      <Route
        path="/readers/:id/books-available"
        element={
          <MainLayout>
            <ReaderAvailableBooksPage />
          </MainLayout>
        }
      />

      <Route
        path="/books/report"
        element={
          <MainLayout>
            <BooksReportPage />
          </MainLayout>
        }
      />
    </Routes>
  );
}

export default AppRouter;
