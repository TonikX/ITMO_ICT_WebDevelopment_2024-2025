<template>
  <div class="contract-page">
    <div class="header">
      <h1>Контракты</h1>
      <button
          v-if="isDirector"
          class="primary-btn"
          @click="toggleCreateContract"
      >
        Создать контракт
      </button>
    </div>

    <table class="styled-table">
      <thead>
      <tr>
        <th>ID</th>
        <th>Организация</th>
        <th>Агент</th>
        <th>Дата начала</th>
        <th>Дата окончания</th>
        <th>Статус</th>
        <th v-if="isDirector">Действия</th>
      </tr>
      </thead>
      <tbody>
      <tr v-for="contract in filteredContracts" :key="contract.id">
        <td>{{ contract.id }}</td>
        <td>{{ getOrganizationName(contract.organization) }}</td>
        <td>{{ getAgentName(contract.agent) || '—' }}</td>
        <td>{{ contract.start_date }}</td>
        <td>{{ contract.end_date }}</td>
        <td>
            <span :class="statusClass(contract.status)">
              {{ contract.status }}
            </span>
        </td>
        <td v-if="isDirector">
          <button
              class="danger-btn"
              @click="terminateContract(contract.id)"
          >
            Удалить
          </button>
        </td>
      </tr>
      </tbody>
    </table>

    <!-- Модальное окно для создания контракта -->
    <div v-if="showCreateForm" class="modal-overlay">
      <div class="modal">
        <h2>Создать контракт</h2>
        <form @submit.prevent="createContract">
          <div class="form-group">
            <label>Организация:</label>
            <select v-model="contract.organization" required>
              <option
                  v-for="org in organizations"
                  :key="org.id"
                  :value="org.id"
              >
                {{ org.full_name }}
              </option>
            </select>
          </div>

          <div class="form-group">
            <label>Агент:</label>
            <select v-model="contract.agent" required>
              <option
                  v-for="agent in agents"
                  :key="agent.id"
                  :value="agent.id"
              >
                {{ agent.first_name }} {{ agent.last_name }}
              </option>
            </select>
          </div>

          <div class="form-group">
            <label>Дата начала:</label>
            <input v-model="contract.start_date" type="date" required/>
          </div>

          <div class="form-group">
            <label>Дата окончания:</label>
            <input v-model="contract.end_date" type="date" required/>
          </div>

          <div class="form-group">
            <label>Сумма:</label>
            <input
                v-model="contract.total_sum"
                type="number"
                required
                min="1"
            />
          </div>

          <div class="form-group">
            <label>Описание:</label>
            <textarea v-model="contract.contract_info" required></textarea>
          </div>

          <div class="modal-actions">
            <button type="submit" class="primary-btn">Создать</button>
            <button
                @click.prevent="toggleCreateContract"
                class="secondary-btn"
            >
              Отмена
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

---

### **Script (логика):**
```javascript
<script>
import InsuranceService from "@/services/InsuranceService";
import EmployeeService from "@/services/EmployeeService";
import UserService from "@/services/UserService";

export default {
  data() {
    return {
      contracts: [],
      organizations: [],
      agents: [],
      employees: [],
      userProfile: {},
      showCreateForm: false,
      contract: {
        agent: "",
        organization: "",
        employees: [],
        contract_type: 1,
        start_date: "",
        end_date: "",
        total_sum: "",
        contract_info: "",
      },
    };
  },
  computed: {
    filteredContracts() {
      if (this.isDirector) {
        // Директор видит все контракты организации
        return this.contracts.filter(
            (contract) => contract.organization === this.userProfile.organization_id
        );
      }
      // Агент видит только свои контракты
      if (this.userProfile.role === 'agent') {
        return this.contracts;
      }

      return [];
    },
    isDirector() {
      return this.userProfile.position?.is_staff === true;
    },
  },
  methods: {
    getOrganizationName(orgId) {
      const org = this.organizations.find((org) => org.id === orgId);
      return org ? org.full_name : "—";
    },
    getAgentName(agentId) {
      const agent = this.agents.find((agent) => agent.id === agentId);
      return agent ? `${agent.first_name} ${agent.last_name}` : "—";
    },
    async fetchData() {
      const [contracts, organizations, agents] = await Promise.all([
        InsuranceService.getContracts(),
        EmployeeService.getOrganizations(),
        InsuranceService.getAgents(),
      ]);
      this.contracts = contracts;
      this.organizations = organizations;
      this.agents = agents;
    },
    async getUserProfile() {
      this.userProfile = await UserService.getProfile();
      console.log('User Profile:', this.userProfile);
    },
    async createContract() {
      try {
        await InsuranceService.createContract(this.contract);
        alert("Контракт успешно создан!");
        this.fetchData();
        this.showCreateForm = false;
      } catch (error) {
        console.error("Ошибка создания контракта:", error.response?.data || error);
        if (
            error.response &&
            error.response.data.error &&
            error.response.data.error.includes("Контракт уже существует")
        ) {
          alert("Ошибка: Контракт с таким агентом, организацией и датой уже существует.");
        } else {
          alert("Ошибка при создании контракта.");
        }
      }
    },
    async terminateContract(contractId) {
      if (confirm("Удалить контракт?")) {
        await InsuranceService.terminateContract(contractId);
        alert("Контракт удален");
        this.fetchData();
      }
    },
    toggleCreateContract() {
      this.showCreateForm = !this.showCreateForm;
    },
    statusClass(status) {
      return {
        "status-active": status === "active",
        "status-pending": status === "pending",
        "status-closed": status === "closed",
      };
    },
  },
  async created() {
    await this.fetchData();
    await this.getUserProfile();
  },
};
</script>
<style scoped>
.contract-page {
  padding: 30px;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
}

.primary-btn {
  background-color: #007bff;
  color: white;
  border: none;
  padding: 12px 24px;
  cursor: pointer;
  border-radius: 5px;
}

.danger-btn {
  background-color: #dc3545;
  color: white;
  padding: 5px 10px;
  border: none;
  border-radius: 5px;
}

.styled-table {
  width: 100%;
  border-collapse: collapse;
}

.styled-table th,
.styled-table td {
  padding: 12px;
  border: 1px solid #ddd;
}

.modal {
  background: white;
  padding: 30px;
  border-radius: 12px;
  width: 500px;
  max-width: 95%;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}
</style>