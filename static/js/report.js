const custom_params = new URLSearchParams(window.location.search);
let start_date = custom_params.get('start_date_report');
let finish_date = custom_params.get('finish_date_report');
if (start_date && finish_date) {
    // Устанавливаем значения для полей
    document.getElementById('finish-date-report').value = finish_date;
    document.getElementById('start-date-report').value = start_date;
}
