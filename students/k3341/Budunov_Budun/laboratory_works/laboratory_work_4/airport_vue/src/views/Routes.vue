<template>
    <div>
      <DataList :fields="routeFields" itemType="routes" apiUrl="/route/" />
    </div>
  </template>
  
  <script>
  import DataList from "@/components/DataList.vue";
  
  export default {
    name: "Routes",
    components: {
      DataList,
    },
    data() {
      return {
        routeFields: [
          { key: "airline", label: "Airline" , type: 'foreign', foreign_key: 'airline'},
          { key: "departure_airport", label: "Departure Airport", type: 'foreign', foreign_key: 'airport' },
          { key: "arrival_airport", label: "Arrival Airport", type: 'foreign', foreign_key: 'airport' },
          { key: "distance", label: "Distance" },
        ],
      };
    },
  };
  </script>
  