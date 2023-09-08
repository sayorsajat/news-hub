import {updateCardsSave} from "./cardsSaveUtils.js";

let removeMode = false; // Flag to enable or disable card removal

export function addCardsRemoval() {
    const removeCardBtn = document.getElementById("removeCardBtn");
    const dashboard = document.getElementById("dashboard");

    removeCardBtn.addEventListener("click", () => {
        removeMode = !removeMode; // Toggle the removeMode flag
        toggleRemoveIndicator(); // Toggle the removal indicator
    });

    dashboard.addEventListener("click", (event) => {
        if (removeMode && event.target.classList.contains("card")) {
            event.target.remove();
            updateCardsSave();
        }
    });

    function toggleRemoveIndicator() {
        const cards = document.querySelectorAll(".card");
        cards.forEach(card => {
            if (removeMode) {
                card.classList.add("removal-mode");
            } else {
                card.classList.remove("removal-mode");
            }
        });
    }


}

export function isRemoveMode() {
    return removeMode;
}
