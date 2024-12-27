<template>
  <div class="insurance-cases">
    <h1>Страховые случаи</h1>

    <!-- Header with button for employees to report a new insurance case -->
    <div class="header">
      <button
          v-if="!isAgent"
          @click="newCaseModal = true"
          class="primary-btn"
      >
        Заявить о новом страховом случае
      </button>
    </div>


    <!-- Фильтры -->
    <div class="filters">
      <label for="statusFilter">Фильтр по статусу:</label>
      <select v-model="selectedStatus" @change="filterByStatus">
        <option value="">Все статусы</option>
        <option value="pending">Ожидает</option>
        <option value="approved">Одобрено</option>
        <option value="rejected">Отклонено</option>
        <option value="closed">Закрыто</option>
      </select>

      <label for="sortDate">Сортировка по дате:</label>
      <select v-model="sortOptions.date" @change="applySorting">
        <option value="">Без сортировки</option>
        <option value="asc">По возрастанию</option>
        <option value="desc">По убыванию</option>
      </select>

      <label for="sortPayout">Сортировка по выплатам:</label>
      <select v-model="sortOptions.payout" @change="applySorting">
        <option value="">Без сортировки</option>
        <option value="asc">По возрастанию</option>
        <option value="desc">По убыванию</option>
      </select>
    </div>

    <!-- Таблица страховых случаев -->
    <table>
      <thead>
      <tr>
        <th>Дата</th>
        <th>Причина</th>
        <th>Сумма выплаты</th>
        <th>Статус</th>
        <th v-if="isAgent">Действия</th>
      </tr>
      </thead>
      <tbody>
      <tr v-for="insuranceCase in paginatedCases" :key="insuranceCase.id">
        <td>{{ insuranceCase.date }}</td>
        <td>{{ insuranceCase.reason }}</td>
        <td>{{ insuranceCase.payout_amount || '—' }}</td>
        <td>{{ insuranceCase.status }}</td>
        <td v-if="isAgent">
          <button @click="openEditModal(insuranceCase)">Рассмотреть</button>
          <button @click="openContractModal(insuranceCase.contract)">
            Информация по контракту
          </button>
        </td>
      </tr>
      </tbody>
    </table>

    <!-- Пагинация -->
    <div v-if="pageCount > 1" class="pagination">
      <button @click="prevPage" :disabled="currentPage === 1">Назад</button>
      <span>Страница {{ currentPage }} из {{ pageCount }}</span>
      <button @click="nextPage" :disabled="currentPage === pageCount">
        Вперед
      </button>
    </div>

    <!-- Модалка редактирования -->
    <div v-if="editModal" class="modal">
      <div class="modal-content">
        <h2>Рассмотрение страхового случая</h2>
        <form @submit.prevent="submitCaseReview">
          <div>
            <label>Дата:</label>
            <input v-model="selectedCase.date" type="date" disabled/>
          </div>
          <div>
            <label>Причина:</label>
            <textarea v-model="selectedCase.reason" disabled></textarea>
          </div>
          <div>
            <label>Статус:</label>
            <select v-model="selectedCase.status" required>
              <option value="pending">Ожидает</option>
              <option value="approved">Одобрено</option>
              <option value="rejected">Отклонено</option>
              <option value="closed">Закрыто</option>
            </select>
          </div>
          <div v-if="selectedCase.status === 'approved'">
            <label>Сумма выплаты:</label>
            <input
                v-model="selectedCase.payout_amount"
                type="number"
                min="0"
                required
            />
          </div>
          <div>
            <label>Решение по выплате:</label>
            <textarea v-model="selectedCase.payout_decision" required></textarea>
          </div>
          <button type="submit">Сохранить</button>
          <button @click="editModal = false">Отмена</button>
        </form>
      </div>
    </div>

    <!-- Модалка с информацией по контракту -->
    <div v-if="contractModal" class="modal">
      <div class="modal-content">
        <h2>Информация по контракту</h2>
        <div v-if="contractInfo">
          <p><strong>Контракт ID:</strong> {{ contractInfo.id }}</p>
          <p><strong>Тип:</strong> {{ contractInfo.contract_type }}</p>
          <p><strong>Дата начала:</strong> {{ contractInfo.start_date }}</p>
          <p><strong>Дата окончания:</strong> {{ contractInfo.end_date }}</p>
          <p><strong>Статус:</strong> {{ contractInfo.status }}</p>
          <p><strong>Сумма:</strong> {{ contractInfo.total_sum }}</p>
          <p><strong>Описание:</strong> {{ contractInfo.contract_info }}</p>
        </div>
        <button @click="contractModal = false">Закрыть</button>
      </div>
    </div>

    <!-- Модалка для нового страхового случая -->
    <div v-if="newCaseModal" class="modal">
      <div class="modal-content">
        <h2>Новый страховой случай</h2>
        <form @submit.prevent="submitNewCase">
          <div>
            <label>Дата:</label>
            <input v-model="newCase.date" type="date" required/>
          </div>
          <div>
            <label>Причина:</label>
            <textarea v-model="newCase.reason" required></textarea>
          </div>
          <button type="submit">Отправить</button>
          <button @click="newCaseModal = false">Отмена</button>
        </form>
        <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
      </div>
    </div>
  </div>
</template>

<script>
import InsuranceService from "@/services/InsuranceService";
import UserService from "@/services/UserService";

export default {
  data() {
    return {
      insuranceCases: [],
      contracts: [],
      selectedCase: null,
      editModal: false,
      contractModal: false,
      contractInfo: null,
      newCaseModal: false,
      newCase: {
        date: '',
        reason: ''
      },
      isAgent: false,
      selectedStatus: "",
      sortOptions: {
        date: "",
        payout: "",
      },
      currentPage: 1,
      itemsPerPage: 5,
      errorMessage: ''
    };
  },
  computed: {
    filteredCases() {
      let cases = this.insuranceCases;

      if (this.selectedStatus) {
        cases = cases.filter((item) => item.status === this.selectedStatus);
      }

      return cases;
    },
    sortedCases() {
      let cases = [...this.filteredCases];

      if (this.sortOptions.date) {
        cases.sort((a, b) => {
          const dateA = new Date(a.date);
          const dateB = new Date(b.date);
          return this.sortOptions.date === "asc" ? dateA - dateB : dateB - dateA;
        });
      }

      if (this.sortOptions.payout) {
        cases.sort((a, b) => {
          const payoutA = a.payout_amount || 0;
          const payoutB = b.payout_amount || 0;
          return this.sortOptions.payout === "asc" ? payoutA - payoutB : payoutB - payoutA;
        });
      }

      return cases;
    },
    paginatedCases() {
      const start = (this.currentPage - 1) * this.itemsPerPage;
      const end = start + this.itemsPerPage;
      return this.sortedCases.slice(start, end);
    },
    pageCount() {
      return Math.ceil(this.sortedCases.length / this.itemsPerPage);
    },
  },
  async mounted() {
    console.log("--- Компонент загружен ---");
    await this.loadInsuranceCases();
    await this.loadContracts();
    const user = await UserService.getProfile();
    this.isAgent = user.role === "agent";
  },
  methods: {
  async loadInsuranceCases() {
    this.insuranceCases = await InsuranceService.getInsuranceCases();
  },
  async loadContracts() {
    this.contracts = await InsuranceService.getContracts();
  },
  openEditModal(insuranceCase) {
    this.selectedCase = {...insuranceCase};
    this.editModal = true;
  },
  async submitCaseReview() {
    await InsuranceService.updateInsuranceCase(this.selectedCase);
    this.editModal = false;
    await this.loadInsuranceCases();
  },
  openContractModal(contractId) {
    this.contractInfo = this.contracts.find((c) => c.id === contractId);
    this.contractModal = true;
  },
  applySorting() {
    this.currentPage = 1;
  },
  async submitNewCase() {
    try {
      const contract = this.contracts.find(c => c.start_date <= this.newCase.date && c.end_date >= this.newCase.date);
      if (!contract) {
        this.errorMessage = 'Нет контрактов на выбранную дату';
        return;
      }
      const newCaseWithContract = {...this.newCase, contract: contract.id};
      await InsuranceService.submitInsuranceCase(newCaseWithContract);
      this.newCaseModal = false;
      this.newCase = {date: '', reason: ''};
      await this.loadInsuranceCases();
    } catch (error) {
      console.error('Ошибка подачи страхового случая:', error);
    }
  },
  prevPage() {
    if (this.currentPage > 1) {
      this.currentPage--;
    }
  },
  nextPage() {
    if (this.currentPage < this.pageCount) {
      this.currentPage++;
    }
  }
},
};
</script>

<style scoped>
.insurance-cases {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 40px;
  background-color: #f4f7f6;
  min-height: 100vh;
}

h1 {
  margin-bottom: 30px;
  font-size: 2.5rem;
  color: #333;
}

.header {
  width: 100%;
  display: flex;
  justify-content: center;
  margin-bottom: 30px;
}

.primary-btn {
  background-color: #007bff;
  color: white;
  padding: 12px 25px;
  font-size: 1rem;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.primary-btn:hover {
  background-color: #0056b3;
}

.filters {
  display: flex;
  gap: 20px;
  margin-bottom: 30px;
  justify-content: center;
  flex-wrap: wrap;
  width: 100%;
}

.filters label {
  font-weight: 500;
  color: #555;
}

.filters select {
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 8px;
  width: 100%;
  max-width: 300px;
}

table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
}

table th, table td {
  padding: 15px;
  border: 1px solid #ddd;
  text-align: left;
}

table th {
  background-color: #f4f4f4;
  color: #555;
}

table tr:hover {
  background-color: #f9f9f9;
}

button {
  padding: 10px 20px;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  margin: 5px;
  font-weight: 500;
  transition: background-color 0.3s ease, transform 0.2s ease;
}

/* Стиль для кнопки "Рассмотреть" */
button:first-of-type {
  background-color: #28a745;
  color: white;
}

button:first-of-type:hover {
  background-color: #218838;
  transform: scale(1.05);
}

/* Стиль для кнопки "Информация по контракту" */
button:last-of-type {
  background-color: #17a2b8;
  color: white;
}

button:last-of-type:hover {
  background-color: #138496;
  transform: scale(1.05);
}


.pagination {
  margin-top: 30px;
  display: flex;
  justify-content: center;
  gap: 15px;
  align-items: center;
}

.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}

.modal-content {
  background: white;
  padding: 30px;
  border-radius: 10px;
  width: 600px;
  max-width: 90%;
}

.modal-content h2 {
  margin-bottom: 20px;
  font-size: 1.8rem;
  color: #333;
}

.modal-content form div {
  margin-bottom: 20px;
}

.modal-content label {
  display: block;
  margin-bottom: 8px;
  font-weight: 500;
  color: #555;
}

.modal-content input,
.modal-content textarea,
.modal-content select {
  width: 100%;
  padding: 12px;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-size: 1rem;
}

.modal-content button {
  padding: 12px 25px;
  font-size: 1rem;
  margin-right: 10px;
}

.error {
  color: red;
  margin-top: 10px;
  font-weight: 500;
}
</style>
