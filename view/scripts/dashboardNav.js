const dashboardNameInput = document.getElementById("nameInput");
let inputValue = "";
let allowSubmit = false;

function validateName(name) {
    if(name.length <= 128 && name.length > 0)
       return /^[a-zA-Z0-9_]*$/.test(name);
    else return false;
}

dashboardNameInput.addEventListener("input", (event) => {
    inputValue = event.target.value;
    const label = document.querySelector("label");

    if(validateName(inputValue)) {
        label.style.color = "#56F000";
        allowSubmit = true;
        console.log(allowSubmit)
    } else {
        label.style.color = "#D52941";
        allowSubmit = false;
    }
})

const form = document.getElementById("form");

form.addEventListener("submit", (event) => {
    event.preventDefault();
    if(allowSubmit === false) return;

    window.location.replace(`http://localhost:25000/view/view.html?id=${inputValue}`);
})