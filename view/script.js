import {loadCardsSave, updateCards} from "./scripts/cardsSaveUtils.js"
import {setExpandingCardsUp} from "./scripts/modals/expandingCards.js";
import {setAddingCardsUp} from "./scripts/modals/addingCardsModal.js";


// execution of preloading
loadCardsSave().then(() => updateCards())

setAddingCardsUp();

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