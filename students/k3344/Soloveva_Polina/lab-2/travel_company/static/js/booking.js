document.addEventListener('DOMContentLoaded', () => {
    const form = document.querySelector('.booking-form');

    if (form) {
        // Получаем элементы формы
        const numPeopleInput = document.getElementById('id_num_people');
        const tariffSelect = document.getElementById('id_tariff');
        const mealSelect = document.getElementById('id_meal_option');
        const totalPriceSpan = document.getElementById('totalPrice');
        console.log(totalPriceSpan, tariffSelect, mealSelect)
        // Функция для получения данных о тарифах и вариантах питания
        function extractDataFromOptions(selectElement) {
            const options = selectElement.options;
            const data = {};

            for (let i = 0; i < options.length; i++) {
                const option = options[i];
                if (option.value) {
                    const priceText = option.textContent.match(/(\d+)\s*RUB/); // Извлекаем цену из текста
                    const price = priceText ? parseInt(priceText[1].replace(/\s/g, ''), 10) : 0;
                    data[option.value] = price; // Сопоставляем ID с ценой
                }
            }

            return data;
        }

        // Сбор данных о тарифах и вариантах питания
        const tariffs = extractDataFromOptions(tariffSelect);
        const mealOptions = extractDataFromOptions(mealSelect);

        // Функция для извлечения данных формы
        function getBookingDetails() {
            const numPeople = parseInt(numPeopleInput.value, 10) || 0; // Количество человек
            const tariffId = tariffSelect.value; // ID тарифа
            const mealId = mealSelect.value; // ID варианта питания

            return {
                numPeople,
                tariffId,
                mealId,
            };
        }

        // Функция для пересчета общей стоимости
        function updateTotalPrice() {
            const { numPeople, tariffId, mealId } = getBookingDetails();
            const tariffPrice = tariffs[tariffId] || 0;
            const mealPrice = mealOptions[mealId] || 0;

            const totalPrice = (tariffPrice + mealPrice) * numPeople;
            totalPriceSpan.textContent = `${totalPrice.toLocaleString()} ₽`;
        }

        // Обработчики событий
        numPeopleInput.addEventListener('input', updateTotalPrice);
        tariffSelect.addEventListener('change', updateTotalPrice);
        mealSelect.addEventListener('change', updateTotalPrice);

        // Первоначальный расчет
        updateTotalPrice();

        // Пример: логирование данных при изменении формы
        form.addEventListener('change', () => {
            const bookingDetails = getBookingDetails();
            console.log('Booking Details:', bookingDetails);
        });

    }
});
