<template>
  <v-container>
    <!-- Управление транзакциями -->
    <v-row>
      <v-col cols="12">
        <v-card class="pa-5 mb-5" elevation="5">
          <v-card-title class="text-h5 text-center">🔄 Управление транзакциями</v-card-title>
          <v-card-text>
            <!-- Форма для добавления транзакции -->
            <v-form @submit.prevent="addTransaction">
              <v-select
                v-model="newTransaction.reader_id"
                :items="readers"
                item-title="full_name"
                item-value="id"
                label="Выберите читателя"
                required
              ></v-select>
              <v-select
                v-model="newTransaction.book_id"
                :items="books"
                item-title="title"
                item-value="id"
                label="Выберите книгу"
                required
              ></v-select>
              <v-select
                v-model="newTransaction.transaction_type"
                :items="['Выдача', 'Возврат']"
                label="Тип транзакции"
                required
              ></v-select>
              <v-btn
                type="submit"
                color="primary"
                block
                class="mt-3"
                :disabled="isLoading"
              >
                Добавить транзакцию
              </v-btn>
            </v-form>

            <!-- Сообщение об ошибке -->
            <v-alert v-if="errorMessage" type="error" class="mt-3">
              {{ errorMessage }}
            </v-alert>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Форма для выбора транзакций читателя -->
    <v-row>
      <v-col cols="12">
        <v-card class="pa-5 mb-5" elevation="3">
          <v-card-title class="text-h6">📚 Транзакции читателя</v-card-title>
          <v-card-text>
            <v-select
              v-model="selectedReaderId"
              :items="readers"
              item-title="full_name"
              item-value="id"
              label="Выберите читателя"
            ></v-select>
            <v-btn
              color="primary"
              block
              class="mt-3"
              :disabled="!selectedReaderId || isLoading"
              @click="fetchReaderTransactions"
            >
              Получить транзакции
            </v-btn>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Список транзакций выбранного читателя -->
    <v-row v-if="readerTransactions.length > 0">
      <v-col cols="12">
        <v-card elevation="3">
          <v-card-title>
            📖 Транзакции читателя: {{ getReaderName(selectedReaderId) }}
          </v-card-title>
          <v-data-table
            :headers="readerTransactionsHeaders"
            :items="readerTransactions"
            class="elevation-1"
          ></v-data-table>
        </v-card>
      </v-col>
    </v-row>
    <v-row v-else-if="selectedReaderId && readerTransactions.length === 0">
      <v-col cols="12" class="text-center">
        <v-alert type="info">У выбранного читателя нет транзакций.</v-alert>
      </v-col>
    </v-row>

    <!-- Список всех транзакций -->
    <v-row>
      <v-col cols="12">
        <v-card elevation="3" class="mb-5">
          <v-card-title>📊 Все транзакции</v-card-title>
          <v-data-table
            :headers="transactionsHeaders"
            :items="transactions"
            class="elevation-1"
          ></v-data-table>
        </v-card>
      </v-col>
    </v-row>

    <!-- Список просроченных транзакций -->
    <v-row>
      <v-col cols="12">
        <v-card elevation="3">
          <v-card-title>⏳ Просроченные транзакции</v-card-title>
          <v-data-table
            :headers="overdueTransactionsHeaders"
            :items="overdueTransactions"
            class="elevation-1"
          ></v-data-table>
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
import axiosBooks from '@/axiosBooks';

export default {
  name: 'TransactionsPage',
  data() {
    return {
      newTransaction: {
        reader_id: '',
        book_id: '',
        transaction_type: '',
      },
      selectedReaderId: null,
      readers: [],
      books: [],
      transactions: [],
      readerTransactions: [],
      transactionsHeaders: [
        { text: 'Читатель', value: 'reader.full_name' },
        { text: 'Книга', value: 'book.title' },
        { text: 'Тип транзакции', value: 'transaction_type' },
        { text: 'Дата', value: 'transaction_date' },
      ],
      readerTransactionsHeaders: [
        { text: 'Книга', value: 'book.title' },
        { text: 'Тип транзакции', value: 'transaction_type' },
        { text: 'Дата транзакции', value: 'transaction_date' },
      ],
      overdueTransactions: [],
      overdueTransactionsHeaders: [
        { text: 'Читатель', value: 'reader.full_name' },
        { text: 'Книга', value: 'book.title' },
        { text: 'Дата выдачи', value: 'transaction_date' },
      ],
      errorMessage: '',
      isLoading: false,
    };
  },
  methods: {
    async fetchReaders() {
      try {
        const response = await axiosBooks.get('/readers/');
        this.readers = response.data;
      } catch (error) {
        console.error('Ошибка загрузки читателей:', error);
        this.errorMessage = 'Ошибка загрузки читателей.';
      }
    },
    async fetchBooks() {
      try {
        const response = await axiosBooks.get('/books/');
        this.books = response.data;
      } catch (error) {
        console.error('Ошибка загрузки книг:', error);
        this.errorMessage = 'Ошибка загрузки книг.';
      }
    },
    async fetchTransactions() {
      try {
        const response = await axiosBooks.get('/book_transactions/');
        this.transactions = response.data.map(transaction => ({
          ...transaction,
          reader: this.readers.find(reader => reader.id === transaction.reader) || { full_name: 'Неизвестный читатель' },
          book: this.books.find(book => book.id === transaction.book) || { title: 'Неизвестная книга' },
        }));
        this.filterOverdueTransactions();
      } catch (error) {
        console.error('Ошибка загрузки транзакций:', error);
        this.errorMessage = 'Ошибка загрузки транзакций.';
      }
    },
    async fetchReaderTransactions() {
      this.readerTransactions = [];
      if (!this.selectedReaderId) return;
      try {
        this.readerTransactions = this.transactions.filter(
          transaction => transaction.reader.id === this.selectedReaderId
        );
      } catch (error) {
        console.error('Ошибка загрузки транзакций читателя:', error);
        this.errorMessage = 'Ошибка загрузки транзакций читателя.';
      }
    },
    filterOverdueTransactions() {
      const oneMonthAgo = new Date();
      oneMonthAgo.setMonth(oneMonthAgo.getMonth() - 1);
      this.overdueTransactions = this.transactions.filter(
        transaction =>
          transaction.transaction_type === 'Выдача' &&
          !transaction.returned &&
          new Date(transaction.transaction_date) < oneMonthAgo
      );
    },
    async addTransaction() {
      try {
        const transactionData = {
          reader: this.newTransaction.reader_id,
          book: this.newTransaction.book_id,
          transaction_type: this.newTransaction.transaction_type,
          transaction_date: new Date().toISOString().split('T')[0],
        };
        await axiosBooks.post('/book_transactions/', transactionData);
        await this.fetchTransactions();
        this.newTransaction = { reader_id: '', book_id: '', transaction_type: '' };
      } catch (error) {
        console.error('Ошибка добавления транзакции:', error);
        this.errorMessage = 'Ошибка добавления транзакции.';
      }
    },
    getReaderName(id) {
      return this.readers.find(reader => reader.id === id)?.full_name || 'Неизвестный читатель';
    },
  },
  async mounted() {
    this.isLoading = true;
    try {
      await Promise.all([this.fetchReaders(), this.fetchBooks()]);
      await this.fetchTransactions();
    } catch (error) {
      console.error('Ошибка инициализации страницы:', error);
    } finally {
      this.isLoading = false;
    }
  },
};
</script>

<style scoped>
.v-data-table tr td {
  vertical-align: middle;
  text-align: center;
}
</style>
