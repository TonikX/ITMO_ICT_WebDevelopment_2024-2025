<template>
    <v-dialog
    :model-value="dialog"
    @update:model-value="emitDialogUpdate"
    max-width="500"
  >
    <v-card>
      <v-card-title>Добавление нового самолёта</v-card-title>
      <v-card-text>
        <v-form ref="form">
          <v-text-field
            v-model="newPlane.number"
            label="Номер самолёта"
            required
          ></v-text-field>
          <v-select
            v-model="newPlane.model"
            :items="availableModels"
            label="Модель самолёта"
            item-value="id"
            item-title="name"
            required
          ></v-select>
        </v-form>
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn variant="text" @click="closeDialog">Отмена</v-btn>
        <v-btn color="primary" @click="createPlane">Сохранить</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
export default {
props: {
  dialog: {
    type: Boolean,
    required: true,
  },
  availableModels: {
    type: Array,
    required: true,
  },
},
emits: ['update:dialog', 'plane-created'],

  data() {
    return {
      newPlane: {
        number: '',
        model: null,
      },
    };
  },

  methods: {

    emitDialogUpdate(value) {
      this.$emit('update:dialog', value);
    },

    closeDialog() {
      this.$emit('update:dialog', false);
    },
    async createPlane() {
      if (!this.newPlane.number || !this.newPlane.model) {
        alert('Заполните все поля');
        return;
      }

      console.log('Модель:', this.newPlane.model);


      this.$emit('plane-created', {
        number: this.newPlane.number,
        model: this.newPlane.model,
      });

      this.closeDialog();
      this.newPlane = { number: '', model: null };
      }
    },
  watch: {
  dialog(val) {
    console.log('Состояние диалога:', val);
  },
},
};
</script>
