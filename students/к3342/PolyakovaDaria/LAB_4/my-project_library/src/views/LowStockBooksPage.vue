<template>
  <v-container>
    <!-- Заголовок страницы -->
    <v-row>
      <v-col cols="12">
        <v-card class="pa-5 mb-5" elevation="5">
          <v-card-title class="text-h5 text-center">
            📚 Книги с низким количеством экземпляров
          </v-card-title>
          <v-card-text>
            <!-- Сообщение об ошибке -->
            <v-alert v-if="errorMessage" type="error" class="mb-4">
              {{ errorMessage }}
            </v-alert>

            <!-- Таблица книг -->
            <v-data-table
              :headers="headers"
              :items="books"
              item-value="id"
              class="elevation-1"
            >
              <!-- Кастомное отображение строк таблицы -->
              <template #item="{ item }">
                <tr>
                  <!-- Название книги и авторы -->
                  <td>
                    <strong>{{ item.book.title }}</strong>
                    <div>{{ item.book.authors || "Авторы не указаны" }}</div>
                  </td>

                  <!-- Текущий код книги -->
                  <td>
                    {{ item.book.current_code || "Не указан" }}
                  </td>

                  <!-- Читатели книги -->
                  <td>
                    <ul v-if="item.readers && item.readers.length">
                      <li v-for="reader in item.readers" :key="reader.id">
                        Читатель: {{ reader.full_name }} (№ билета: {{ reader.ticket_number }})
                      </li>
                    </ul>
                    <span v-else>Нет данных о читателях</span>
                  </td>
                </tr>
              </template>
            </v-data-table>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Индикатор загрузки -->
    <v-row v-if="isLoading" justify="center" class="mt-5">
      <v-progress-circular
        indeterminate
        color="primary"
        size="50"
      ></v-progress-circular>
    </v-row>
  </v-container>
</template>

<script>
import axiosBooks from "@/axiosBooks";

export default {
  name: "LowStockBooksPage",
  data() {
    return {
      headers: [
        { text: "Название книги", value: "book.title" },
        { text: "Текущий код", value: "book.current_code" },
        { text: "Читатели", value: "readers" },
      ],
      books: [],
      errorMessage: "",
      isLoading: false,
    };
  },
  created() {
    this.fetchBooks();
  },
  methods: {
    async fetchBooks() {
      try {
        this.isLoading = true;
        const response = await axiosBooks.get("/books/low_stock/");
        this.books = response.data.map((item) => ({
          ...item,
          book: item.book || { title: "Неизвестная книга", authors: "Не указаны", current_code: "Не указан" },
          readers: item.readers || [],
        }));
      } catch (error) {
        console.error("Ошибка при загрузке книг:", error);
        this.errorMessage = "Ошибка при загрузке данных книг";
      } finally {
        this.isLoading = false;
      }
    },
  },
};
</script>

<style scoped>
.v-data-table tr td {
  vertical-align: middle;
  text-align: center;
}
</style>
