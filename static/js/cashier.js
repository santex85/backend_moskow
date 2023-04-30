// отлавливаем все поля формы
const hotelField = document.querySelector('#id_hotel');
const dateField = document.querySelector('#id_date_service');
const employeeField = document.querySelector('#id_employee');
const guestField = document.querySelector('#id_guest');
const groupField = document.querySelector('#id_group');
const incomesField = document.querySelector('#id_incomes');
const outcomesField = document.querySelector('#id_outcomes');
const cashlessField = document.querySelector('#id_cashless');
const categoryOutcomeField = document.querySelector('#id_category_outcome');
const categoryIncomeField = document.querySelector('#id_category_income');
const commentField = document.querySelector('#id_comment');

// отключаем поля кроме выбора отеля
setDisabled()


// событие выбора отеля
hotelField.addEventListener('change', function () {
    // стартовое событие
    resetFields()
    sendRequest()
});


// события выбора даты
dateField.addEventListener('change', function () {
    employeeField.disabled = false;
    guestField.disabled = false;
    checkAvailableElement(incomesField, outcomesField, false)
});

// события выбора сотрудника
employeeField.addEventListener('click', function () {
    guestField.innerHTML = '';
    guestField.disabled = true;
    groupField.innerHTML = '';
    groupField.disabled = true;
    checkAvailableElement(categoryIncomeField,categoryOutcomeField, false);
    commentField.disabled = false;
    cashlessField.disabled = false;
});

// события выбора гостя
guestField.addEventListener('click', function () {
    employeeField.selectedIndex = 0;
    employeeField.disabled = true;
    groupField.disabled = false;
    cashlessField.disabled = false;
    checkAvailableElement(categoryIncomeField,categoryOutcomeField, false);
    commentField.disabled = false;
})


// --------functions--------------------

/**
 * Сбрасывает значения формы до исходных, и активирует поле даты.
 *
 * @return {void} Ничего не возвращает
 */
function resetFields() {
    // Отключаем все поля формы
    setDisabled();

    // Сбрасываем выбранные значения в полях формы
    employeeField.selectedIndex = 0;
    guestField.selectedIndex = 0;
    groupField.selectedIndex = 0;
    if (categoryIncomeField) {
        categoryIncomeField.selectedIndex = 0;

    } else {
        categoryOutcomeField.selectedIndex = 0;

    }

    // Активируем поле даты
    dateField.disabled = false;
}

/**
 * Отключает все поля формы.
 *
 * @return {void} Ничего не возвращает
 */
function setDisabled() {
    // Отключаем поля формы
    dateField.disabled = true;
    employeeField.disabled = true;
    guestField.disabled = true;
    groupField.disabled = true;
    checkAvailableElement(categoryIncomeField, categoryOutcomeField, true)
    checkAvailableElement(incomesField, outcomesField, true)
    commentField.disabled = true
    cashlessField.disabled = true
}

/**
 * Получает значение cookie по имени.
 *
 * @param {string} name - имя cookie, которое необходимо получить.
 * @return {string|null} Значение cookie или null, если cookie не найден.
 */
function getCookie(name) {
    let cookieValue = null;

    // Проверяем, есть ли какие-либо cookie на странице
    if (document.cookie && document.cookie !== '') {

        // Разбиваем cookie на массив
        const cookies = document.cookie.split(';');

        // Ищем cookie с указанным именем
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();

            // Если cookie с указанным именем найден, декодируем его значение и сохраняем его в переменную cookieValue
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }

    // Возвращаем значение cookie или null, если cookie не найден
    return cookieValue;
}

/**
 * Отправляет AJAX-запрос на сервер и обновляет соответствующие селекторы на странице.
 *
 * @return {void} Ничего не возвращает.
 */
function sendRequest() {
    // Получаем CSRF-токен
    const csrftoken = getCookie('csrftoken');

    // Получаем выбранное пользователем значение в селекторе отеля
    let selectValue = hotelField.value;

    // Отправляем POST-запрос на сервер, содержащий выбранное значение
    fetch(`/hotel/${selectValue}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': csrftoken,
        },
        body: `pk=${selectValue}`,
    })
        .then((response) => {
            // Если запрос не удался, выбрасываем ошибку
            if (!response.ok) {
                throw new Error(`Error: ${response.statusText}`);
            }
            // Преобразуем ответ в формат JSON
            return response.json();
        })
        .then((responseArray) => {
            // Обновляем селекторы на странице с помощью полученных данных
            addSelect(responseArray);
        })
        .catch((error) => {
            // Обрабатываем ошибку, если она произошла
            console.error(error);
        });
}

// Функция для добавления опций в селекторы на странице
function addSelect(responseArray) {
    // Очистка всех селекторов и задаем первый пустой селектор
    employeeField.innerHTML = '';
    addFirstSelection(employeeField)
    guestField.innerHTML = '';
    addFirstSelection(guestField)

    // Добавление опций в селектор для сотрудников
    for (const id in responseArray.employees) {
        const option = document.createElement('option');
        option.value = id;
        option.text = responseArray.employees[id];
        employeeField.add(option);
    }
    // Добавление опций в селектор для гостей
    for (const id in responseArray.customers) {
        const option = document.createElement('option');
        option.value = id;
        option.text = responseArray.customers[id];
        guestField.add(option);
    }
}

function addFirstSelection(field) {
    const option = document.createElement('option')
    option.value = ''
    option.text = '---------'
    field.add(option)
}

function checkAvailableElement(element1, element2, action) {
    if (element1) {
        element1.disabled = action;
    } else {
        element2.disabled = action;
    }
}