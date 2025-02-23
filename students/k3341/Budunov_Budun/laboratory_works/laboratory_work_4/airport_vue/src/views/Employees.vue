<template>
    <div>
      <DataList :fields="employeeFields" itemType="employees" apiUrl="/employee/" />
    </div>
  </template>
  
  <script>
  import DataList from "@/components/DataList.vue";
  
  export default {
    name: "Employees",
    components: {
      DataList,
    },
    data() {
      return {
        employeeFields: [
          { key: "full_name", label: "Full Name" },
          { key: "position", label: "Position" },
          { key: "airline", label: "Airline", type: 'foreign', foreign_key: 'airline' },
          { key: 'user', label: 'User', type: 'foreign', foreign_key: 'user'},
        ],
      };
    },
  };
  </script>
  