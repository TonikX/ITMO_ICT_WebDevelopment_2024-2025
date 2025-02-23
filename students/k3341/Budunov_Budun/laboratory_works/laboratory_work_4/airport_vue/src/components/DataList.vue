<template>
    <v-container>
      <v-row>
        <v-col cols="12">
          <v-text-field
            v-model="searchQuery"
            label="Search"
            outlined
            clearable
          ></v-text-field>
        </v-col>
      </v-row>
      <v-row>
        <v-col cols="12">
          <v-select
            v-model="selectedFilter"
            :items="filterOptions"
            label="Filter By"
            outlined
            @change="applyFilters"
          ></v-select>
        </v-col>
      </v-row>
      <v-row>
        <v-col cols="12">
          <v-btn @click="openForm('create')">Add</v-btn>
        </v-col>
      </v-row>
      <v-row>
        <v-col cols="12">
          <v-table fixed-header height="500px">
            <thead>
              <tr>
                <th
                  v-for="field in fields"
                  :key="field.key"
                  @click="sortBy(field.key)"
                  style="cursor: pointer"
                >
                  {{ field.label }}
                  <v-icon v-if="sortKey === field.key">
                    {{
                      sortDirection === "asc" ? "mdi-arrow-up" : "mdi-arrow-down"
                    }}
                  </v-icon>
                </th>
                <th v-if="isAdmin">Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="item in paginatedItems" :key="item.id">
                <td v-for="field in fields" :key="field.key">
                  <template v-if="field.key === 'crews'">
                    <span v-for="crew in item.crews" :key="crew.id">
                      {{ crew.employee }}
                    </span>
                  </template>
                  <template v-else-if="field.key.includes('airport')">
                    {{ item[field.key].name }}
                  </template>
                  <template v-else-if="field.key == 'airline'">
                    {{ item[field.key].name }}
                  </template>
                  <template v-else>
                    {{ item[field.key] }}
                  </template>
                </td>
                <td v-if="isAdmin">
                  <v-btn @click="viewItem(item.id)" icon="mdi-eye"></v-btn>
                  <v-btn @click="openForm('edit', item.id)" icon="mdi-pencil"></v-btn>
                  <v-btn @click="deleteItem(item.id)" icon="mdi-delete"></v-btn>
                </td>
              </tr>
            </tbody>
          </v-table>
        </v-col>
      </v-row>
      <v-row>
        <v-col cols="12">
          <v-pagination
            v-model="page"
            :length="totalPages"
            @input="onPageChange"
          />
        </v-col>
      </v-row>
      <v-dialog v-model="dialog" max-width="800px">
        <DataForm
          v-if="dialog"
          :itemType="itemType"
          :itemId="itemId"
          :fields="fields"
          @close="closeForm"
          @item-created="addItem"
          @item-updated="updateItem"
        />
      </v-dialog>
      <Loading v-if="isLoading" />
    </v-container>
  </template>
  
  <script>
  import api from "@/api";
  import { mapState } from "vuex";
  import DataForm from "@/components/DataForm.vue";
  import Loading from "@/components/Loading.vue";
  
  export default {
    name: "DataList",
    components: {
      DataForm,
      Loading,
    },
    props: {
      fields: {
        type: Array,
        required: true,
      },
      itemType: {
        type: String,
        required: true,
      },
      apiUrl: {
        type: String,
        required: true,
      },
    },
    data() {
      return {
        items: [],
        dialog: false,
        itemId: null,
        formType: null,
        page: 1,
        perPage: 5,
        searchQuery: "",
        sortKey: null,
        sortDirection: "asc",
        selectedFilter: null,
        isLoading: false,
      };
    },
    computed: {
      ...mapState("auth", ["isAuthenticated", "token", "user"]),
      isAdmin() {
        return this.user && this.user.is_admin;
      },
      totalPages() {
        return Math.ceil(this.items.length / this.perPage);
      },
      paginatedItems() {
        const start = (this.page - 1) * this.perPage;
        const end = start + this.perPage;
        return this.filteredItems.slice(start, end);
      },
      filteredItems() {
        let items = this.items.filter((item) => {
          return Object.values(item).some((value) => {
            if (typeof value === "string") {
              return value.toLowerCase().includes(this.searchQuery.toLowerCase());
            } else if (typeof value === "object" && value !== null) {
              for (const key in value) {
                if (typeof value[key] === "string") {
                  if (
                    value[key]
                      .toLowerCase()
                      .includes(this.searchQuery.toLowerCase())
                  ) {
                    return true;
                  }
                }
              }
            }
            return false;
          });
        });
        if (this.selectedFilter) {
          items = items.filter((item) => {
            return item[this.selectedFilter.key] === this.selectedFilter.value;
          });
        }
        return items.sort((a, b) => {
          if (this.sortKey) {
            const valA = a[this.sortKey];
            const valB = b[this.sortKey];
            if (valA < valB) {
              return this.sortDirection === "asc" ? -1 : 1;
            }
            if (valA > valB) {
              return this.sortDirection === "asc" ? 1 : -1;
            }
          }
          return 0;
        });
      },
      filterOptions() {
        const options = [];
        if (this.selectedFilter) {
          options.push({
            key: this.selectedFilter.key,
            label: `Current: ${this.selectedFilter.value}`,
            value: this.selectedFilter.value,
          });
        }
        const uniqueValues = new Set();
        this.fields.forEach((field) => {
          this.items.forEach((item) => {
            if (item[field.key] && !uniqueValues.has(item[field.key])) {
              let value = item[field.key];
              if (typeof item[field.key] === "object") {
                value = item[field.key].name;
              }
              options.push({
                key: field.key,
                label: `${field.label}: ${value}`,
                value: item[field.key],
              });
              uniqueValues.add(item[field.key]);
            }
          });
        });
        return options;
      },
    },
    watch: {
      "$route.query": {
        handler(query) {
          this.fetchData(query);
        },
        deep: true,
        immediate: true,
      },
    },
    created() {
      this.fetchData();
    },
    methods: {
      async fetchData(query = {}) {
        try {
          this.isLoading = true;
          const response = await api.get(this.apiUrl, { params: query });
          this.items = response.data;
        } catch (error) {
          console.error(error);
        } finally {
          this.isLoading = false;
        }
      },
      openForm(type, id = null) {
        this.itemId = id;
        this.formType = type;
        this.dialog = true;
      },
      closeForm() {
        this.dialog = false;
        this.itemId = null;
        this.formType = null;
      },
      async deleteItem(id) {
        try {
          await api.delete(`${this.apiUrl}${id}/`);
          this.items = this.items.filter((item) => item.id !== id);
        } catch (error) {
          console.error(error);
        }
      },
      addItem(item) {
        this.items.push(item);
        this.closeForm();
      },
      updateItem(item) {
        const index = this.items.findIndex((i) => i.id === item.id);
        if (index !== -1) {
          this.items.splice(index, 1, item);
        }
        this.closeForm();
      },
      viewItem(id) {
        this.$router.push(`/${this.itemType}/${id}`);
      },
      onPageChange(newPage) {
        this.page = newPage;
      },
      sortBy(key) {
        if (this.sortKey === key) {
          this.sortDirection = this.sortDirection === "asc" ? "desc" : "asc";
        } else {
          this.sortKey = key;
          this.sortDirection = "asc";
        }
      },
      applyFilters() {
        this.page = 1;
      },
    },
  };
  </script>
  