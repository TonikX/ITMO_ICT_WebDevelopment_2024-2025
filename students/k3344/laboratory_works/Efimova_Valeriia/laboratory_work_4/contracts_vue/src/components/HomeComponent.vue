<script setup>
import {onMounted, ref} from 'vue';

import { fetchWrapper } from '@/helpers';
import {useAuthStore} from "@/stores";

const baseUrl = `${import.meta.env.VITE_API_URL}`;

const numEmployees = ref(0);
const numContracts = ref(0);
const contractId = ref(''); // Переменная для ввода ID контракта пользователем
const report = ref('');
const username = ref('');
const errorMsg = ref('');

const formatReportForDataTable = report => {
  const formattedReport = [];
  for (const name in report) {
    if (typeof report[name] !== 'object') {
      formattedReport.push({ name, value: report[name] });
    } else {
      for (const subName in report[name]) {
        formattedReport.push({ name: `${name}.${subName}`, value: report[name][subName] });
      }
    }
  }
  return formattedReport;
};

const loadReport = async () => {
  // Получить отчет по контракту
  try {
    const res = await fetchWrapper.get(`${baseUrl}/contracts/report/${contractId.value}/`);
    if (res) {
      if (res === "Not Found") {
        report.value = "";
        errorMsg.value = res || 'Unexpected error occurred.';
      }
      else {
        report.value = res;
        errorMsg.value = "";
      }
    }
  } catch (err) {
    errorMsg.value = err.message || 'Unexpected error occurred.';
    console.error(err);
  }
};

const logout = async () => {
  const authStore = useAuthStore();

  return await authStore.logout()
};

onMounted(async () => {
  const user = await fetchWrapper.get(`${baseUrl}/auth/users/me/`)
  if (user) {
    username.value = user.username;
  }

  // Получение списка сотрудников
  const employees = await fetchWrapper.get(`${baseUrl}/employees/`);
  if (employees) {
    numEmployees.value = employees.length;
  }

  // Получение списка контрактов
  const contracts = await fetchWrapper.get(`${baseUrl}/contracts/`);
  if (contracts) {
    numContracts.value = contracts.length;
  }
});
</script>

<template>
  <v-container>
    <v-row align="center" justify="center">
      <v-col cols="12" md="10" lg="8">
        <v-card>
          <v-card-title class="justify-center">
            <h2 style="white-space: normal">Welcome to our Insurance Management System</h2>
          </v-card-title>

          <v-card-actions class="justify-end">
            <span v-if="username" class="mr-4">Logged in as: {{ username }}</span>
            <v-btn color="error" outlined @click="logout">Logout</v-btn>
          </v-card-actions>

          <v-card-text>
            <p>
              This system allows us to properly manage insurance contracts with both physical and legal entities.
            </p>
            <p>We currently manage contracts for {{ numEmployees }} employees and {{ numContracts }} contracts.</p>

            <v-text-field v-model="contractId" label="Enter contract ID" type="number"></v-text-field>
            <v-btn :disabled="!contractId" color="primary" @click="loadReport" class="mr-2">Load Contract Report</v-btn>

            <v-btn color="success" to="/add_contract">Add New Contract</v-btn>

            <v-alert v-if="errorMsg" type="error" class="mt-5">{{ errorMsg }}</v-alert>
          </v-card-text>

          <!-- Отчет об контракте -->
          <v-card v-if="report" class="mx-auto my-5">
            <v-card-title>Contract Report</v-card-title>
            <v-card-text>
              <div>
                <h3>Contract Details:</h3>
                <p><strong>ID:</strong> {{ report.id }}</p>
                <p><strong>Type:</strong> {{ report.contract_type }}</p>
                <p><strong>Start Date:</strong> {{ report.start_date }}</p>
                <p><strong>End Date:</strong> {{ report.end_date }}</p>
                <p><strong>Insurance Cost:</strong> {{ report.insurance_cost }}</p>
                <p><strong>Total Payout:</strong> {{ report.total_payout }}</p>
              </div>

              <div v-if="report.organization">
                <h3>Organization Details:</h3>
                <p><strong>ID:</strong> {{ report.organization.id }}</p>
                <p><strong>Code:</strong> {{ report.organization.code }}</p>
                <p><strong>Full Name:</strong> {{ report.organization.full_name }}</p>
                <p><strong>Short Name:</strong> {{ report.organization.short_name }}</p>
                <p><strong>Address:</strong> {{ report.organization.address }}</p>
                <p><strong>Bank Account Number:</strong> {{ report.organization.bank_account_number }}</p>
                <p><strong>Specialization:</strong> {{ report.organization.specialization }}</p>
              </div>

              <div v-if="report.agent">
                <h3>Agent Details:</h3>
                <p><strong>ID:</strong> {{ report.agent.id }}</p>
                <p><strong>Full Name:</strong> {{ report.agent.full_name }}</p>
                <p><strong>Passport Details:</strong> {{ report.agent.passport_details }}</p>
                <p><strong>Contact Details:</strong> {{ report.agent.contact_details }}</p>
                <p><strong>Employment Contract ID:</strong> {{ report.agent.employment_contract_id }}</p>
                <p><strong>Contract IDs:</strong> {{ report.agent.contract_ids.join(', ') }}</p>
              </div>

              <div v-if="report.cases && report.cases.length">
                <h3>Insurance Cases:</h3>
                <div v-for="(caseItem, index) in report.cases" :key="index">
                  <p><strong>Date:</strong> {{ caseItem.date }}</p>
                  <p><strong>Cause:</strong> {{ caseItem.cause }}</p>
                  <p><strong>Decision:</strong> {{ caseItem.decision }}</p>
                  <p><strong>Amount:</strong> {{ caseItem.amount }}</p>
                </div>
              </div>
            </v-card-text>
          </v-card>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<style scoped>
.report-card {
  background-color: white;
  color: black;
}

.report-card .v-card-title,
.report-card .v-card-text {
  color: black;
}
</style>
