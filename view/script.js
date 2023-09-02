// Define the fetchRecentNews function
async function fetchRecentNews(keywords) {
    const url = 'http://localhost:25000/news/getRecent';
    const response = await fetch(url, {
        method: "POST",
        mode: "cors",
        cache: "no-cache",
        credentials: "same-origin",
        headers: {
          "Content-Type": "application/json",
        },
        redirect: "follow",
        referrerPolicy: "no-referrer",
        body: JSON.stringify(keywords), // body data type must match "Content-Type" header
      });

    return response.json();
}

// Preload the news data
function parseKeywords(inputString) {
    const objectArray = [];
    const keyValuePairs = inputString.split(';').filter(Boolean);
  
    for (const pair of keyValuePairs) {
        const [key, value] = pair.split(':');
        const obj = {};
        obj[key.trim()] = Number(value.trim());
        objectArray.push(obj);
    }
  
    return objectArray;
}
  

async function updateCards() {
    const cards = document.getElementsByClassName("card")
    for (var i = 0; i < cards.length; i++) {
        const keywordsString = cards[i].getAttribute("keywords");
        const keywordsArray = parseKeywords(keywordsString);

        const news = await fetchRecentNews(keywordsArray);
        console.log(JSON.stringify(keywordsArray));

        console.log(news);

        // set title and content of news for card
        cards[i].getElementsByTagName("h3")[0].innerHTML = news[1].title;
        cards[i].getElementsByClassName("card-content")[0].innerHTML = news[1].content;
    }
}

// execution of preloading
updateCards();

let index = 0;

// part for adding cards
const addCardBtn = document.getElementById('addCardBtn');
const dashboard = document.getElementById('dashboard');
let cardCounter = 1;

function createCard(keywords) {
    const card = document.createElement('div');
    card.className = 'card';
    card.id = `card${cardCounter}`;

    // insert keywords to html
    let _keywords = "";
    keywords.map((keyword) => _keywords += `${Object.keys(keyword)[0]}: ${Object.values(keyword)[0]};`)
    card.setAttribute('keywords', _keywords);

    card.innerHTML = `
    <h3>Card ${cardCounter}</h3>
    <p class="card-content">lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum </p>
    `;
    cardCounter++;
    return card;
}

// for every modal
function openModal(content, overlay, modal_content) {
    if(content) {
        modal_content.innerHTML = content;
    }
    overlay.style.display = 'flex';
}

// overload decides whether content is being erased or not
// same for "setUpModalClosing"
function closeModal(overlay) {
    overlay.style.display = 'none';
}
function closeModal(overlay, modal_content) {
    overlay.style.display = 'none';
    if(modal_content) {
      modal_content.innerHTML = "";  
    }
}

function setUpModalClosing(overlay) {
    overlay.addEventListener('click', (event) => {
        if (event.target === overlay) {
            closeModal(overlay);
        }
    });
    
    document.addEventListener('keydown', (event) => {
        if (event.key === 'Escape' && overlay.style.display != "none") {
            closeModal(overlay);
        }
    });
}
function setUpModalClosing(overlay, modal_content) {
    overlay.addEventListener('click', (event) => {
        if (event.target === overlay) {
            closeModal(overlay, modal_content);
        }
    });
    
    document.addEventListener('keydown', (event) => {
        if (event.key === 'Escape' && overlay.style.display != "none") {
            closeModal(overlay, modal_content);
        }
    });
}

// adding cards modal form
const newCardModalOverlay = document.getElementById("newCardModalOverlay");
const newCardModalContent = document.getElementById("newCardModalContent");
const newKeywordBtn = document.getElementById("newKeywordBtn");
const keywordsList = document.getElementById("keywordsList");
const newCardForm = document.getElementById("newCardForm");

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
        </input>
        <input
            placeholder="urgency"
            type="text"
        >
        </input><br/>
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
    // and then this keywords are used to create card
    for (var i = 0; i < inputs.length; i++) {
        if((i+1)%2==1){
            keyword = inputs[i].value;
            urgency = inputs[i+1].value;
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
})



// cards modals (expanding full text)
const modalOverlay = document.getElementById('modalOverlay');
const modalContent = document.getElementById('modalContent');

setUpModalClosing(modalOverlay);

dashboard.addEventListener('click', (event) => {
    const card = event.target.closest('.card');
    if (card) {
        const content = card.querySelector('.card-content').textContent;
        openModal(`<p>${content}</p>`, modalOverlay, modalContent);
    }
});

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