import {openModal, setUpModalClosing} from "./modalWindows.js";
import {isRemoveMode} from "../deletingCards.js";

export function setExpandingCardsUp() {
    // cards modals (expanding full text)
    const modalOverlay = document.getElementById('modalOverlay');
    const modalContent = document.getElementById('modalContent');

    const dashboard = document.getElementById('dashboard');

    setUpModalClosing(modalOverlay);

    dashboard.addEventListener('click', (event) => {
        if(isRemoveMode()) return;
        if(event.target.closest(".clickable")) {
        const card = event.target.closest('.card');

        const heading = card.querySelector('#heading').textContent;
        const content = card.querySelector('.card-content').textContent;
        const source = card.querySelector('a');
        const sourceUrl = source.href;
        const sourceBaseUrl = source.textContent;

        const modalHtml = `
            <h3>${heading}</h3>
            <p>${content}</p>
            <a href=${sourceUrl}>${sourceBaseUrl}</a>
        `
        if (card) {
            openModal(modalHtml, modalOverlay, modalContent);
        }
        }

    });
}