import {loadCardsSave, updateCards} from "./scripts/cardsSaveUtils.js"
import {setExpandingCardsUp} from "./scripts/modals/expandingCards.js";
import {setAddingCardsUp} from "./scripts/modals/addingCardsModal.js";
import {addCardsRemoval} from "./scripts/deletingCards.js";


// execution of preloading
loadCardsSave().then(() => updateCards())

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
    },
});