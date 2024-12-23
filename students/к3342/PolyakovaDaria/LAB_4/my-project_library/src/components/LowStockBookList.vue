<template>
  <v-container>
    <!-- Заголовок страницы -->
    <v-row>
      <v-col cols="12">
        <v-card class="pa-5 mb-5" elevation="5">
          <v-card-title class="text-h5 text-center">📚 Книги с низким количеством экземпляров</v-card-title>
        </v-card>
      </v-col>
    </v-row>

    <!-- Таблица с книгами -->
    <v-row>
      <v-col cols="12">
        <v-data-table
          :headers="headers"
          :items="books"
          item-value="book.id"
          class="elevation-1"
        >
          <!-- Ячейка: Название книги -->
          <template v-slot:item.title="{ item }">
            <strong>{{ item.book.title }}</strong>
            <div>{{ item.book.authors || "Авторы не указаны" }}</div>
          </template>

          <!-- Ячейка: Код книги -->
          <template v-slot:item.current_code="{ item }">
            {{ item.book.current_code || "Не указан" }}
          </template>

          <!-- Ячейка: Читатели -->
          <template v-slot:item.readers="{ item }">
            <ul>
              <li v-for="reader in item.readers" :key="reader.id">
                Читатель: {{ reader.full_name }} (№ билета: {{ reader.ticket_number }})
              </li>
            </ul>
            <span v-if="!item.readers.length">Нет читателей</span>
          </template>
        </v-data-table>
      </v-col>
    </v-row>

    <!-- Сообщение при отсутствии данных -->
    <v-row v-if="!books.length">
      <v-col cols="12" class="text-center">
        <v-alert type="info">Нет книг с низким количеством экземпляров.</v-alert>
      </v-col>
    </v-row>
  </v-container>
</template>
