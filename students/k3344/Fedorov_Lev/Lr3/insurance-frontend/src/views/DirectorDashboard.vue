<template>
  <div class="dashboard">
    <h1>Личный кабинет директора</h1>

    <div class="company-info">
      <h2>Информация о компании</h2>
      <p><strong>Компания:</strong> {{ organization.full_name || 'Не указана' }}</p>
      <p><strong>Должность:</strong> {{ user.position?.name || 'Не указана' }}</p>
      <p><strong>Роль:</strong> {{ user.role }}</p>
      <p><strong>Имя пользователя:</strong> {{ user.username }}</p>
      <p><strong>Email:</strong> {{ user.email }}</p>
      <button class="primary-btn" @click="$router.push('/profile/edit')">Редактировать профиль</button>

    </div>


  </div>
</template>

<script>
import apiClient from '@/services/apiClient';

export default {
  data() {
    return {
      user: {},
      agents: [],
      employees: [],
      organizations: [],
      activeContracts: [],
      contract: {
        agent: '',
        organization: '',
        employees: [],
        contract_type: 1,
        start_date: '',
        end_date: '',
        total_sum: '',
        contract_info: '',
      },
      showCreateForm: false,
      organization: {}
    };
  },
  computed: {
  },
  async created() {
    await this.fetchUser();
    await this.fetchAgents();
    await this.fetchOrganizations();
    await this.fetchEmployees();
  },
  methods: {
    async fetchUser() {
      try {
        const response = await apiClient.get('/insurance/user/profile/');
        this.user = response.data;
        this.contract.organization = this.user.organization_id;
        this.fetchOrganizationDetails(this.user.organization_id);
      } catch (error) {
        console.error('Ошибка загрузки профиля:', error.response?.data || error);
      }
    },
    async fetchAgents() {
      try {
        const response = await apiClient.get('/insurance/agents/');
        this.agents = response.data;
      } catch (error) {
        console.error('Ошибка загрузки агентов:', error.response?.data || error);
      }
    },
    async fetchOrganizations() {
      try {
        const response = await apiClient.get('/insurance/organizations/');
        this.organizations = response.data;
      } catch (error) {
        console.error('Ошибка загрузки организаций:', error.response?.data || error);
      }
    },
    async fetchEmployees() {
      try {
        const response = await apiClient.get('/insurance/employees/');
        this.employees = response.data;
      } catch (error) {
        console.error('Ошибка загрузки сотрудников:', error.response?.data || error);
      }
    },
    async fetchOrganizationDetails(organizationId) {
      try {
        const response = await apiClient.get(`/insurance/organizations/${organizationId}/`);
        this.organization = response.data;
      } catch (error) {
        console.error('Ошибка загрузки информации о компании:', error.response?.data || error);
      }
    },
    toggleCreateContract() {
      this.showCreateForm = !this.showCreateForm;
    },
    async createContract() {
      try {
        await apiClient.post('/insurance/contracts/', this.contract);
        alert('Контракт успешно создан!');
        this.fetchEmployees();
        this.showCreateForm = false;
      } catch (error) {
        console.error('Ошибка создания контракта:', error.response?.data || error);
        alert('Ошибка при создании контракта.');
      }
    },
  },
};
</script>

<style scoped>
.dashboard {
  padding: 40px;
  max-width: 800px;
  margin: 0 auto;
}
.company-info {
  margin-bottom: 30px;
  padding: 20px;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.05);
}
.primary-btn {
  background-color: #007bff;
  color: white;
  border: none;
  padding: 12px 24px;
  border-radius: 5px;
  cursor: pointer;
}
.primary-btn:hover {
  background-color: #0056b3;
}

textarea,
select,
input {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 5px;
}
</style>