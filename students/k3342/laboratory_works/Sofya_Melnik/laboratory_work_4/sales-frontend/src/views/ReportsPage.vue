<template>
  <div class="admin-reports-page">
    <h2 class="page-title">Отчёты</h2>

    <div class="reports-links">
      <ul>
        <li><router-link to="/reports/completed-orders" class="report-link">Выполненные работы</router-link></li>
        <li><router-link to="/reports/payments-by-period" class="report-link">Платежные поручения</router-link></li>
        <li><router-link to="/reports/services-list" class="report-link">Номенклатура рекламных услуг</router-link></li>
        <li><router-link to="/reports/orders-by-client" class="report-link">Заявки клиентов за период</router-link></li>
        <li><router-link to="/reports/employee-orders-completed" class="report-link">Сотрудники с выполненными заявками</router-link></li>
        <li><router-link to="/reports/quarterly" class="report-link">Отчет о стоимости работ за последний квартал</router-link></li>
      </ul>
    </div>
  </div>
</template>

<script setup>
</script>

<style scoped>

  .admin-reports-page {
    max-width: 1200px;
    margin: 40px auto;
    padding: 20px;
    background-color: #ffffff;
    border-radius: 10px;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  }


  .page-title {
    font-size: 2.2rem;
    font-weight: 700;
    color: #333;
    text-align: center;
    margin-bottom: 30px;
    border-bottom: 2px solid #4CAF50;
    padding-bottom: 10px;
  }


  .reports-links ul {
    list-style: none;
    padding: 0;
    margin: 0;
    text-align: center;
  }

  .reports-links li {
    margin: 15px 0;
  }


  .report-link {
    text-decoration: none;
    color: #fff;
    font-size: 18px;
    background-color: #4CAF50;
    padding: 12px 25px;
    border-radius: 8px;
    display: inline-block;
    min-width: 300px;
    text-align: center;
    margin: 5px 0;
    transition: background-color 0.3s ease, transform 0.3s ease;
  }


  .report-link:hover {
    background-color: #45a049;
    transform: translateY(-5px);
  }


  .report-link:focus {
    outline: none;
    background-color: #388e3c;
  }
</style>
