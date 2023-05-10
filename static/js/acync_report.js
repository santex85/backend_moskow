function getReportAsync() {
    let startDate = document.getElementById("start-date-report").value;
    let finishDate = document.getElementById("finish-date-report").value;
    let categoryIncome = document.getElementById("inlineFormSelectIncomeCategory").value;
    let categoryOutcome = document.getElementById("inlineFormSelectOutcomeCategory").value;
    let group = document.getElementById("inlineFormSelectGroup").value;
    let hotel = document.getElementById("inlineFormSelectObjets").value;

    // Отправьте асинхронный запрос к серверу
    fetch("/report-async/?start_date=" + startDate + "&finish_date=" + finishDate + "&category_income=" + categoryIncome + "&category_outcome=" + categoryOutcome + "&group=" + group + "&hotel=" + hotel)
        .then(function (response) {
            if (!response.ok) {
                throw new Error("HTTP error " + response.status);
            }
            return response.json();
        })
        .then(function (data) {
            updateReportTable(data);
        })
        .catch(function (error) {
            console.error("Failed to fetch data:", error);
        });
}

function updateReportTable(data) {

    let oldTable = document.querySelector(".table");
    if (oldTable) {
        oldTable.remove();
    }
    // Создаем элементы таблицы
    let table = document.createElement("table");
    table.classList.add("table");

    // Создаем заголовок таблицы
    let thead = document.createElement("thead");
    let headerRow = document.createElement("tr");
    let dateHeader = document.createElement("th");
    dateHeader.textContent = "Дата";
    let hotelNameHeader = document.createElement("th");
    hotelNameHeader.textContent = "Название отеля";
    let balanceHeader = document.createElement("th");
    balanceHeader.textContent = "Баланс";
    headerRow.appendChild(dateHeader);
    headerRow.appendChild(hotelNameHeader);
    headerRow.appendChild(balanceHeader);
    thead.appendChild(headerRow);
    table.appendChild(thead);

    // Создаем тело таблицы
    let tbody = document.createElement("tbody");
    for (let item of data) {
        let row = document.createElement("tr");

        let dateCell = document.createElement("td");
        dateCell.textContent = item.date_service;
        row.appendChild(dateCell);

        let hotelNameCell = document.createElement("td");
        hotelNameCell.textContent = item.hotel_name;  // Предполагается, что имя отеля приходит с сервера
        row.appendChild(hotelNameCell);

        let balanceCell = document.createElement("td");
        balanceCell.textContent = item.balance;
        row.appendChild(balanceCell);

        tbody.appendChild(row);
    }
    table.appendChild(tbody);

    // Добавляем таблицу в div
    let reportTableDiv = document.getElementById("reportTableDiv");
    reportTableDiv.innerHTML = '';  // Очищаем div, если в нем уже была таблица
    reportTableDiv.appendChild(table);
}