import {loadCardsSave, updateCards, updateCardsSave} from "./scripts/cardsSaveUtils.js"
import {setExpandingCardsUp} from "./scripts/modals/expandingCards.js";
import {setAddingCardsUp} from "./scripts/modals/addingCardsModal.js";
import {addCardsRemoval} from "./scripts/deletingCards.js";
import {getDashboardId} from "./scripts/getIdSearchParam.js";


document.addEventListener("DOMContentLoaded", () => {

if(getDashboardId() == "") {
    window.location.replace("http://localhost:25000/");
    return;
}

// execution of preloading
loadCardsSave(getDashboardId())
    .then((isOk) => {
        if(isOk) {
            updateCards()
        } else {
            updateCardsSave(getDashboardId())
        }
    })


setAddingCardsUp();

addCardsRemoval();

setExpandingCardsUp();

const dashboard = document.getElementById('dashboard');
const sortable = new Sortable(dashboard, {
    animation: 150,
    handle: '.card',
    draggable: '.card',
    ghostClass: 'ghost',
    onUpdate: (event) => {
        const draggedCard = event.item;
        dashboard.insertBefore(draggedCard, event.to.children[event.newIndex]);
        updateCardsSave(getDashboardId())
    },
});
});
