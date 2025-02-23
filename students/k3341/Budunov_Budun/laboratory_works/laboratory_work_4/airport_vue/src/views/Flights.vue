<template>
    <div>
      <DataList
        :fields="flightFields"
        itemType="flights"
        apiUrl="/flight/"
      />
    </div>
  </template>
  
  <script>
  import DataList from "@/components/DataList.vue";
  
  export default {
    name: "Flights",
    components: {
      DataList,
    },
    data() {
      return {
        flightFields: [
          { key: "flight_number", label: "Flight Number" },
          { key: "route", label: "Route" },
          { key: "departure_time", label: "Departure Time" },
          { key: "arrival_time", label: "Arrival Time" },
          { key: "airplane", label: "Airplane"},
          { key: "crews", label: "Crews"},
        ],
      };
    },
  };
  </script>
  