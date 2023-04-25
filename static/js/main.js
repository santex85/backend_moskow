
// заполняем поля по очереди
let startDate = document.getElementById("start-date");
let endDate = document.getElementById("end-date");
startDate.addEventListener("input", () => {
    endDate.disabled = false;
    endDate.addEventListener("input", () => {
        document.getElementById("submit-date").classList.remove("disabled")
    })
})


// работа с формами кассы

