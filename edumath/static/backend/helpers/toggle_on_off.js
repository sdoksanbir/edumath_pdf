function toggleTable(iconElement, tableId) {
    let table = document.getElementById(tableId);

    if (table.style.display === "none" || table.style.display === "") {
        table.style.display = "table";
        iconElement.classList.replace("ti-eye", "ti-eye-off");
    } else {
        table.style.display = "none";
        iconElement.classList.replace("ti-eye-off", "ti-eye");
    }
}