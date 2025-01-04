<template>
  <form @submit.prevent>
    <div class="pet-form">
      <h2>{{ isEditing ? 'Обновить информацию о питомце' : 'Добавить нового питомца' }}</h2>

        <div>
          <label for="number" v-if="!isEditing">Номер:
            <input type="number" v-model="pet.number"  required />
          </label>
        </div>

        <div>
          <label for="name">Имя:
          <input type="text" v-model="pet.name" required /></label>
        </div>

        <div>
          <label for="sex">Пол:
          <select v-model="pet.sex" required>
            <option value="самец">Самец</option>
            <option value="самка">Самка</option>
          </select></label>
        </div>

        <div>
          <label for="animal_type">Тип животного:
          <input type="text" v-model="pet.animal_type" required /></label>
        </div>

        <div v-if="pet.animal_type == 'bird'">
            <p>Заметка о птице:</p>

            <label for="note_bird_pet.is_wintering">Зимует?
            <input type="checkbox" v-model="pet.note_bird_pet.is_wintering" /></label>

            <div class="wintering-info" v-if="pet.note_bird_pet.is_wintering">
                <label for="note_bird_pet.country_wintering">Страна зимовки:
                  <input type="text" v-model="pet.note_bird_pet.country_wintering" required />
                </label>

                <label for="note_bird_pet.start_wintering">Дата начала зимовки:
                <input type="date" v-model="pet.note_bird_pet.start_wintering" required /></label>

                <label for="note_bird_pet.finish_wintering">Окончание зимовки:
                <input type="date" v-model="pet.note_bird_pet.finish_wintering" required /></label>
            </div>
        </div>

        <div v-else-if="pet.animal_type == 'reptile'">
            <p>Заметка о рептилии:</p>
            <div class="wintering-info">
                <label for="note_reptile_pet.normal_temperature">Нормальная температура
                <input type="number" v-model="pet.note_reptile_pet.normal_temperature" required /></label>

                <label for="note_reptile_pet.begin_wintering">Дата начала зимовки:
                <input type="date" v-model="pet.note_reptile_pet.begin_wintering" required /></label>
            </div>
        </div>

        <div>
          <label for="birtday">Дата рождения:
          <input type="date" v-model="pet.birtday" /></label>
        </div>

        <div>
            <label for="is_buy">Куплен?
              <input type="checkbox" v-model="pet.is_buy" />
            </label>
        </div>

        <div class="buy_pet" v-if="pet.is_buy">
            <label for="buy_pet.seller">Продавец:
            <input type="text" v-model="pet.buy_pet.seller" required /></label>

            <label for="buy_pet.date_buy">Дата покупки:
            <input type="date" v-model="pet.buy_pet.date_buy" required /></label>
        </div>

        <div>
            <label for="is_rented">Арендован ли?
            <select v-model="pet.is_rented">
                <option value="">Не арендован</option>
                <option value="out">Сдан</option>
                <option value="in">Взят</option>
            </select></label>
        </div>

        <div class="buy_rent" v-if="pet.is_rented">
            <label for="rent_pet.zoo">Продавец:
            <input type="text" v-model="pet.rent_pet.zoo" required /></label>

            <label for="rent_pet.price">Цена:
            <input type="number" v-model="pet.rent_pet.price" required /></label>
            
            <label for="rent_pet.start_rent">Начало аренды:
            <input type="date" v-model="pet.rent_pet.start_rent" required /></label>

            <label for="rent_pet.finish_rent">Конец аренды:
            <input type="date" v-model="pet.rent_pet.finish_rent" required /></label>
        </div>

        <div>
          <label for="valliere">Вольер:
          <input type="number" v-model="pet.valliere" required /></label>
        </div>

        <div>
          <label for="habited">Зона обитания:
          <input type="number" v-model="pet.habited" /></label>
        </div>

        <div>
          <label for="diet">Рацион:
          <input type="number" v-model="pet.diet" required /></label>
        </div>

        <button type="submit" @click="submitForm(pet, isEditing)">{{ isEditing ? 'Обновить' : 'Добавить' }}</button>
        <button type="button" @click="cancel">Отменить</button>
    </div>
  </form>
</template>

<script setup>
    import { ref } from 'vue';

    const props = defineProps({
        petData: Object,
        isEditing: Boolean
    })

    const pet = ref(
        {
            number: props.petData.number,
            name: props.petData.name,
            sex: props.petData.sex,
            animal_type: props.petData.animal_type,

            note_reptile_pet: (props.petData.note_reptile_pet != null) ? {
                normal_temperature: props.petData.note_reptile_pet.normal_temperature,
                begin_wintering: props.petData.note_reptile_pet.begin_wintering
            } : {
                normal_temperature: null,
                begin_wintering: ""
            },

            note_bird_pet: (props.petData.note_bird_pet != null) ? {
                is_wintering: props.petData.note_bird_pet.is_wintering,
                country_wintering: props.petData.note_bird_pet.country_wintering,
                start_wintering: props.petData.note_bird_pet.start_wintering,
                finish_wintering: props.petData.note_bird_pet.finish_wintering
            } : {
                is_wintering: false,
                country_wintering: "",
                start_wintering: "",
                finish_wintering: ""
            },

            birtday: "",
            is_buy: props.petData.is_buy,
            buy_pet: (props.petData.is_buy) ? {
                seller: props.petData.buy_pet.seller,
                date_buy: props.petData.buy_pet.date_buy
            } : {
                seller: "",
                date_buy: ""
            },

            is_rented: (props.petData.is_rented == null) ? "" : props.petData.is_rented,
            rent_pet: (props.petData.is_rented != null) ? {
                zoo: props.petData.rent_pet.zoo,
                price: props.petData.rent_pet.price,
                start_rent: props.petData.rent_pet.start_rent,
                finish_rent: props.petData.rent_pet.finish_rent
            } : {
                zoo: "",
                price: null,
                start_rent: null,
                finish_rent: null
            },

            valliere: props.petData.valliere.id,
            habited: props.petData.habited.id,
            diet: props.petData.diet.number
    });

    const emit = defineEmits(['submit', 'cancel'])

    function falidateForm() {
        return  Boolean(pet.value.number &&
                pet.value.name &&
                pet.value.sex &&
                pet.value.animal_type &&
                (pet.value.animal_type != 'bird' || 
                    (!pet.value.note_bird_pet.is_wintering || 
                        (pet.value.note_bird_pet.country_wintering && 
                          pet.value.note_bird_pet.start_wintering && 
                          pet.value.note_bird_pet.finish_wintering))) &&
                (pet.value.animal_type != 'reptile' || 
                    (pet.value.note_reptile_pet.normal_temperature && 
                    pet.value.note_reptile_pet.begin_wintering)) &&
                (!pet.value.is_buy || 
                    (pet.value.buy_pet.seller && 
                    pet.value.buy_pet.date_buy)) &&
                (pet.value.is_rented == "" || 
                    (pet.value.rent_pet.zoo && 
                    pet.value.rent_pet.price && 
                    pet.value.rent_pet.start_rent && 
                    pet.value.rent_pet.finish_rent)) &&
                pet.value.valliere && 
                pet.value.diet)
    }
    function submitForm() {
        if (!falidateForm()){return}
        emit('submit', pet.value, props.isEditing);
    }

    function cancel() {
        emit('cancel');
    }
</script>

<style scoped>
  /* Общий стиль для формы */
  .pet-form {
    border: 1px solid #ddd; /* Граница формы */
    border-radius: 8px; /* Скругленные углы */
    padding: 20px; /* Внутренние отступы */
    background-color: #f9f9f9; /* Цвет фона для формы */
    margin-bottom: 20px; /* Отступ снизу формы */
    transition: box-shadow 0.3s; /* Плавный переход для тени */
  }

  /* Эффект тени при наведении на форму */
  .pet-form:hover {
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2); /* Тень при наведении */
  }

  /* Стили для заголовков формы */
  .pet-form h2 {
    color: #333; /* Цвет заголовка */
    font-size: 1.5em; /* Размер шрифта для заголовка */
    margin-bottom: 15px; /* Отступ снизу заголовка */
  }

  /* Стили для полей ввода и выбора */
  input[type="text"],
  input[type="number"],
  input[type="date"],
  select {
    width: 100%; /* Ширина полей ввода */
    padding: 8px; /* Внутренние отступы полей ввода */
    margin-bottom: 15px; /* Отступ снизу для полей ввода */
    border: 1px solid #ccc; /* Граница полей ввода */
    border-radius: 4px; /* Скругленные углы */
    font-size: 1em; /* Размер шрифта для полей ввода */
  }

  /* Эффект на полях ввода при фокусе */
  input:focus,
  select:focus {
    border-color: #007BFF; /* Цвет границы при фокусе */
    outline: none; /* Убираем стандартный контур */
  }

  /* Стиль для чекбоксов */
  input[type="checkbox"] {
    margin-right: 8px; /* Отступ справа */
  }

  /* Кнопки в конце формы */
  button {
    background-color: #007BFF; /* Цвет фона кнопок */
    color: white; /* Цвет текста кнопок */
    border: none; /* Убираем границу */
    border-radius: 5px; /* Скругленные углы для кнопок */
    padding: 10px 15px; /* Внутренние отступы */
    cursor: pointer; /* Курсор при наведении */
    transition: background-color 0.3s; /* Плавный переход цвета фона */
    margin-right: 10px; /* Отступ между кнопками */
  }

  /* Эффект при наведении на кнопки */
  button:hover {
    background-color: #0056b3; /* Темнее при наведении */
  }

  /* Стили для разделителей */
  .wintering-info {
    margin: 15px 0; /* Отступы для разделителей */
    padding: 10px;
    border-left: 4px solid #007BFF; /* Левый разделитель */
    background-color: #f1f1f1; /* Светлый фон разделителя */
  }

  /* Адаптивные стили */
  @media (max-width: 768px) {
    .pet-form {
      padding: 15px; /* Уменьшение отступов на мобильных устройствах */
    }

    button {
      width: 100%; /* Кнопки занимают всю ширину на мобильных устройствах */
      margin: 5px 0; /* Выровненные отступы между кнопками */
    }
  }
</style>