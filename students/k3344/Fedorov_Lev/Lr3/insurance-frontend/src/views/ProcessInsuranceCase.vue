<template>
  <div class="process-case">
    <h1>Обработка страхового случая</h1>

    <form @submit.prevent="processCase">
      <div class="form-group">
        <label for="date">Дата:</label>
        <input
          type="date"
          v-model="insuranceCase.date"
          class="form-control"
          disabled
        />
      </div>

      <div class="form-group">
        <label for="reason">Причина:</label>
        <textarea
          v-model="insuranceCase.reason"
          class="form-control"
          disabled
        ></textarea>
      </div>

      <div class="form-group">
        <label for="status">Статус:</label>
        <select v-model="insuranceCase.status" class="form-control" required>
          <option value="approved">Одобрено</option>
          <option value="rejected">Отклонено</option>
        </select>
      </div>

      <div class="form-group">
        <label for="payout_amount">Сумма выплаты:</label>
        <input
          type="number"
          v-model="insuranceCase.payout_amount"
          class="form-control"
          required
        />
      </div>

      <div class="form-group">
        <label for="payout_decision">Описание решения:</label>
        <textarea
            v-model="insuranceCase.payout_decision"
            class="form-control"
            required
        ></textarea>
      </div>

      <div class="button-group">
        <button type="submit" class="primary-btn">Сохранить изменения</button>
        <button
            @click.prevent="$router.push('/insurance-cases')"
            class="secondary-btn"
        >
          Отмена
        </button>
      </div>
    </form>
  </div>
</template>

<script>
import apiClient from "@/services/apiClient";

export default {
  data() {
    return {
      insuranceCase: {
        id: "",
        date: "",
        reason: "",
        payout_amount: 0,
        payout_decision: "",
        status: "pending",
      },
    };
  },
  async mounted() {
    const caseId = this.$route.params.id;
    const response = await apiClient.get(
        `/insurance/insurance_cases/${caseId}/`
    );
    this.insuranceCase = response.data;
  },
  methods: {
    async processCase() {
      try {
        await apiClient.patch(
            `/insurance/insurance_cases/${this.insuranceCase.id}/`,
            this.insuranceCase
        );
        alert("Страховой случай обновлён");
        this.$router.push("/insurance-cases");
      } catch (error) {
        console.error("Ошибка при обновлении:", error);
        alert("Ошибка обновления страхового случая");
      }
    },
  },
};
</script>

<style scoped>
.process-case {
  max-width: 700px;
  margin: 60px auto;
  background-color: white;
  padding: 40px;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

h1 {
  text-align: center;
  margin-bottom: 30px;
  font-size: 2rem;
  color: #333;
}

.form-group {
  margin-bottom: 25px;
}

label {
  display: block;
  margin-bottom: 8px;
  font-weight: 500;
  color: #555;
}

.form-control {
  width: 100%;
  padding: 14px;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-size: 1rem;
  box-sizing: border-box;
  transition: border-color 0.3s ease;
}

.form-control:focus {
  border-color: #007bff;
  outline: none;
  box-shadow: 0 0 8px rgba(0, 123, 255, 0.25);
}

textarea {
  min-height: 120px;
  resize: vertical;
}

.button-group {
  display: flex;
  justify-content: space-between;
  margin-top: 30px;
}

.primary-btn {
  background-color: #007bff;
  color: white;
  padding: 14px 30px;
  font-size: 1rem;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.primary-btn:hover {
  background-color: #0056b3;
}

.secondary-btn {
  background-color: #6c757d;
  color: white;
  padding: 14px 30px;
  font-size: 1rem;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.secondary-btn:hover {
  background-color: #5a6268;
}
</style>
