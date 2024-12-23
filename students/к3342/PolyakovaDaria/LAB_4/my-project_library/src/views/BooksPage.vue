<template>
  <div>
    <h1>Управление книгами</h1>

    <!-- Форма добавления новой книги -->
    <form @submit.prevent="addBook">
      <input v-model="newBook.title" placeholder="Название" required />
      <input v-model="newBook.authors" placeholder="Авторы через запятую" required />
      <input v-model="newBook.publisher" placeholder="Издательство" required />
      <input v-model.number="newBook.publication_year" placeholder="Год издания" type="number" required />
      <input v-model="newBook.section" placeholder="Раздел" required />
      <input v-model="newBook.code" placeholder="Шифр книги" required />

      <!-- Добавление экземпляров книги -->
      <h3>Экземпляры книги</h3>
      <div v-for="(copy, index) in newBook.copies" :key="index" class="copy-item">
        <select v-model.number="copy.room_id" required>
          <option disabled value="">Выберите зал</option>
          <option v-for="room in availableRooms" :key="room.id" :value="room.id">
            {{ room.name }}
          </option>
        </select>
        <input v-model.number="copy.quantity" type="number" placeholder="Количество" min="1" required />
        <button type="button" @click="removeCopy(index)">Удалить</button>
      </div>
      <button type="button" @click="addCopy">Добавить экземпляр</button>
      <button type="submit" :disabled="isLoading">Добавить книгу</button>
    </form>

    <!-- Сообщение об ошибке -->
    <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>

    <!-- Компонент для отображения списка книг -->
    <book-list
      v-if="books.length && availableRooms.length"
      :books="books"
      :available-rooms="availableRooms"
      @delete="deleteBook"
      @discard="discardBook"
      @updateBookCode="handleUpdateBookCode"
      @transfer="transferBook"
      @addCopies="addCopies"
      @removeCopies="removeCopies"
    ></book-list>

    <!-- Индикатор загрузки -->
    <div v-if="isLoading" class="loading-indicator">Загрузка...</div>
  </div>
</template>

<script>
import axiosBooks from "@/axiosBooks";
import BookList from "@/components/BookList.vue";

export default {
  components: { BookList },
  data() {
    return {
      books: [],
      newBook: {
        title: "",
        authors: "",
        publisher: "",
        publication_year: null,
        section: "",
        code: "",
        copies: [],
      },
      availableRooms: [],
      errorMessage: "",
      isLoading: false,
    };
  },
  methods: {
    async fetchBooks() {
      this.isLoading = true;
      try {
        const response = await axiosBooks.get("/books/");
        this.books = response.data.map((book) => ({
          ...book,
          copies: [],
        }));

        const copyPromises = this.books.map((book) =>
          axiosBooks.get(`/books/${book.id}/manage_copies/`).then((copiesResponse) => {
            book.copies = copiesResponse.data.copies || [];
          })
        );
        await Promise.all(copyPromises);
      } catch (error) {
        this.handleApiError(error, "Ошибка загрузки книг.");
      } finally {
        this.isLoading = false;
      }
    },

    async fetchRooms() {
      try {
        const response = await axiosBooks.get("/reading_rooms/");
        this.availableRooms = response.data;
      } catch (error) {
        this.handleApiError(error, "Ошибка загрузки залов.");
      }
    },

    async addBook() {
      this.isLoading = true;
      try {
        const payload = {
          title: this.newBook.title,
          authors: this.newBook.authors, // Передаем строку напрямую
          publisher: this.newBook.publisher,
          publication_year: this.newBook.publication_year,
          section: this.newBook.section,
          code: this.newBook.code,
          copies: this.newBook.copies.filter((copy) => copy.room_id && copy.quantity > 0),
        };

        console.log("Отправляем данные:", payload);

        await axiosBooks.post("/books/", payload);
        await this.fetchBooks();
        this.clearForm();
      } catch (error) {
        console.error("Ошибка при добавлении книги:", error.response?.data);
        this.handleApiError(error, "Ошибка при добавлении книги.");
      } finally {
        this.isLoading = false;
      }
    },

    async transferBook({ bookId, sourceRoomId, targetRoomId, quantity }) {
      this.isLoading = true;
      try {
        await axiosBooks.patch(`/books/${bookId}/transfer/`, {
          source_room_id: sourceRoomId,
          target_room_id: targetRoomId,
          quantity,
        });
        await this.fetchBooks();
      } catch (error) {
        this.handleApiError(error, "Ошибка при перемещении экземпляров книги.");
      } finally {
        this.isLoading = false;
      }
    },

    async addCopies({ bookId, roomId, quantity }) {
      this.isLoading = true;
      try {
        await axiosBooks.post(`/books/${bookId}/manage_copies/`, {
          room_id: roomId,
          quantity,
        });
        await this.fetchBooks();
      } catch (error) {
        this.handleApiError(error, "Ошибка добавления экземпляров книги.");
      } finally {
        this.isLoading = false;
      }
    },

    async removeCopies({ bookId, roomId, quantity }) {
      this.isLoading = true;
      try {
        await axiosBooks.delete(`/books/${bookId}/manage_copies/`, {
          data: { room_id: roomId, quantity },
        });
        await this.fetchBooks();
      } catch (error) {
        this.handleApiError(error, "Ошибка удаления экземпляров книги.");
      } finally {
        this.isLoading = false;
      }
    },

    addCopy() {
      this.newBook.copies.push({ room_id: null, quantity: 1 });
    },

    removeCopy(index) {
      this.newBook.copies.splice(index, 1);
    },

    handleApiError(error, message) {
      console.error("Детали ошибки:", error.response?.data || error.message);
      this.errorMessage = error.response?.data?.detail || message;
    },

    clearForm() {
      this.newBook = {
        title: "",
        authors: "",
        publisher: "",
        publication_year: null,
        section: "",
        code: "",
        copies: [],
      };
    },

    async deleteBook(bookId) {
      this.isLoading = true;
      try {
        await axiosBooks.delete(`/books/${bookId}/`);
        await this.fetchBooks();
      } catch (error) {
        this.handleApiError(error, "Ошибка удаления книги.");
      } finally {
        this.isLoading = false;
      }
    },

    handleUpdateBookCode({ id, new_code }) {
      const book = this.books.find((b) => b.id === id);
      if (book) book.code = new_code;
    },
  },
  mounted() {
    this.fetchRooms();
    this.fetchBooks();
  },
};
</script>

<style scoped>
form {
  margin-bottom: 20px;
}

form input,
form select {
  margin: 5px 0;
  padding: 8px;
  display: block;
  width: 100%;
  max-width: 400px;
}

.copy-item {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 10px;
}

.copy-item select,
.copy-item input {
  flex: 1;
}

copy-item button {
  background-color: #dc3545;
}

button {
  padding: 8px 16px;
  margin: 5px 0;
  background-color: #007bff;
  color: white;
  border: none;
  cursor: pointer;
  border-radius: 4px;
}

button:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
}

button:hover:not(:disabled) {
  background-color: #0056b3;
}

h1 {
  margin-bottom: 20px;
}

.error-message {
  color: red;
  margin-top: 10px;
}

.loading-indicator {
  font-size: 16px;
  color: #007bff;
  margin-top: 20px;
  text-align: center;
}
</style>
