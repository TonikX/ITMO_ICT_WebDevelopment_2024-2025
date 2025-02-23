<template>
    <v-container>
      <v-form ref="form" v-model="valid" @submit.prevent="onSubmit">
        <v-card>
          <v-card-title class="headline">
            {{ isEditing ? "Edit" : "Create" }} {{ itemType }}
          </v-card-title>
          <v-card-text>
            <v-row>
              <v-col v-for="field in fields" :key="field.key" cols="12">
                <v-text-field
                  v-if="
                    field.type !== 'select' &&
                    field.key !== 'crews' &&
                    field.type != 'foreign' &&
                    field.key != 'user'
                  "
                  v-model="formData[field.key]"
                  :label="field.label"
                  :type="field.type || 'text'"
                  outlined
                  required
                ></v-text-field>
                <v-select
                  v-else-if="
                    field.key !== 'crews' &&
                    field.type == 'select' &&
                    field.type != 'foreign' &&
                      field.key != 'user'
                  "
                  v-model="formData[field.key]"
                  :items="field.items"
                  :label="field.label"
                  item-text="name"
                  item-value="id"
                  outlined
                  required
                ></v-select>
                <v-select
                  v-else-if="field.type === 'crews'"
                  v-model="formData[field.key]"
                  :items="crews"
                  item-text="full_name"
                  item-value="id"
                  :label="field.label"
                  multiple
                  outlined
                >
                </v-select>
                <v-select
                  v-else-if="field.type == 'foreign'"
                  v-model="formData[field.key]"
                  :items="foreignItems[field.key]"
                  :label="field.label"
                  item-text="name"
                  item-value="id"
                  outlined
                  required
                >
                </v-select>
                  <v-select
                          v-else-if="field.key == 'user'"
                          v-model="formData[field.key]"
                          :items="employees"
                          :label="field.label"
                          item-text="full_name"
                          item-value="id"
                          outlined
                          required>
                  </v-select>
              </v-col>
            </v-row>
          </v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn color="blue darken-1" text @click="$emit('close')">
              Cancel
            </v-btn>
            <v-btn color="blue darken-1" text type="submit" :disabled="!valid">
              Save
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-form>
    </v-container>
  </template>
  
  <script>
  import api from "@/api";
  
  export default {
    name: "DataForm",
    props: {
      itemType: {
        type: String,
        required: true,
      },
      itemId: {
        type: Number,
        default: null,
      },
      fields: {
        type: Array,
        required: true,
      },
    },
    data() {
      return {
        valid: false,
        formData: {},
        crews: [],
        foreignItems: {},
          employees: [],
      };
    },
    computed: {
      isEditing() {
        return !!this.itemId;
      },
      apiUrl() {
        return `/${this.itemType}/`;
      },
    },
    watch: {
      itemId: {
        handler() {
          this.loadItem();
        },
        immediate: true,
      },
    },
    methods: {
      async loadItem() {
        if (this.itemId) {
          try {
            const response = await api.get(`${this.apiUrl}${this.itemId}/`);
            this.formData = response.data;
            if (this.formData.crews) {
              this.formData.crews = this.formData.crews.map((crew) => crew.id);
            }
          } catch (error) {
            console.error(error);
          }
        } else {
          this.resetForm();
        }
        try {
          if (this.itemType == "flight") {
            const response = await api.get("/crew/");
            this.crews = response.data;
          }
          this.fields.forEach(async (f) => {
            if (f.type === "foreign") {
              const res = await api.get(`/${f.foreign_key}/`);
              this.$set(this.foreignItems, f.key, res.data);
            }
            if (f.key == 'user'){
                const response = await api.get("/employee/")
                this.employees = response.data
            }
          });
        } catch (error) {
          console.error(error);
        }
      },
      resetForm() {
        this.formData = {};
        this.fields.forEach((f) => {
          if (f.key == "crews") {
            this.formData[f.key] = [];
          }
        });
      },
      async onSubmit() {
        if (this.$refs.form.validate()) {
          try {
            const response = this.isEditing
              ? await api.put(`${this.apiUrl}${this.itemId}/`, this.formData)
              : await api.post(this.apiUrl, this.formData);
            if (this.isEditing) {
              this.$emit("item-updated", response.data);
            } else {
              this.$emit("item-created", response.data);
            }
          } catch (error) {
            console.error(error);
          }
        }
      },
    },
  };
  </script>
  