import {closeModal, createCard, openModal, setUpModalClosing} from "./modalWindows.js";
import {updateCards, updateCardsSave} from "../cardsSaveUtils.js";

export function setAddingCardsUp() {
    // adding cards modal form
    const newCardModalOverlay = document.getElementById("newCardModalOverlay");
    const newCardModalContent = document.getElementById("newCardModalContent");
    const newKeywordBtn = document.getElementById("newKeywordBtn");
    const keywordsList = document.getElementById("keywordsList");
    const newCardForm = document.getElementById("newCardForm");
    const addCardBtn = document.getElementById('addCardBtn');
    const dashboard = document.getElementById('dashboard');

    setUpModalClosing(newCardModalOverlay, keywordsList);

    addCardBtn.addEventListener('click', (event) => {
        openModal("", newCardModalOverlay, newCardModalContent);
    });

    newKeywordBtn.addEventListener('click', (event) => {
        const keywordInputs = document.createElement('div');
        keywordInputs.innerHTML +=
        `
            <input
                placeholder="keyword"
                type="text"
            >
            <input
                placeholder="urgency"
                type="text"
            ><br/>
        `;

        keywordsList.appendChild(keywordInputs)
    })

    newCardForm.addEventListener("submit", async (event) => {
        event.preventDefault();

        let cardKeywords = []

        let inputs = keywordsList.getElementsByTagName('input');

        // form is based on key-value pairs
        // checking for the parity of i+1 is because of that
        // (i+1 because indexes start from zero)
        // and key-value paris are put into array of objects cardKeywords
        // and then these keywords are used to create card
        let keyword;
        let urgency;
        for (let i = 0; i < inputs.length; i++) {
            if ((i + 1) % 2 === 1) {
                keyword = inputs[i].value;
                urgency = inputs[i + 1].value;
                let keywordObject = {}
                keywordObject[keyword] = urgency;
                cardKeywords.push(keywordObject)
            }
        }

        closeModal(newCardModalOverlay);
        keywordsList.innerHTML = "";

        let newCard = createCard(cardKeywords);
        dashboard.appendChild(newCard);

        await updateCards();
        updateCardsSave();
    })
}