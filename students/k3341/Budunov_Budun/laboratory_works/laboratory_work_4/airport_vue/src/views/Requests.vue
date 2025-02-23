<template>
    <div>
      <DataList :fields="requestFields" itemType="requests" apiUrl="/profile_change_request/" />
    </div>
  </template>
  
  <script>
  import DataList from "@/components/DataList.vue";
  
  export default {
    name: "Requests",
    components: {
      DataList,
    },
    data() {
      return {
        requestFields: [
          { key: "user", label: "User", type: "foreign", foreign_key: "user" },
          { key: "full_name", label: "Full Name" },
          { key: "position", label: "Position" },
          { key: "airline", label: "Airline", type: "foreign", foreign_key: "airline" },
          { key: "status", label: "Status" },
        ],
      };
    },
  };
  </script>
  