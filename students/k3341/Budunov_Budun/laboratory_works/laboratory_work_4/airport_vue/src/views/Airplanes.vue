<template>
    <div>
      <DataList :fields="airplaneFields" itemType="airplanes" apiUrl="/airplane/" />
    </div>
  </template>
  
  <script>
  import DataList from "@/components/DataList.vue";
  
  export default {
    name: "Airplanes",
    components: {
      DataList,
    },
    data() {
      return {
        airplaneFields: [
          { key: "registration_number", label: "Registration Number" },
          { key: "airplane_model", label: "Model", type: 'foreign', foreign_key: 'airplane_model' },
          { key: "airline", label: "Airline", type: 'foreign', foreign_key: 'airline' },
        ],
      };
    },
  };
  </script>
  