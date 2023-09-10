// for every modal window
export function openModal(content, overlay, modal_content) {
    if(content) {
        modal_content.innerHTML = content;
    }
    overlay.style.display = 'flex';
}

export function closeModal(overlay, modal_content) {
    overlay.style.display = 'none';
    if(modal_content) {
      modal_content.innerHTML = "";
    }
}


export function setUpModalClosing(overlay, modal_content) {
    overlay.addEventListener('click', (event) => {
        if (event.target === overlay) {
            closeModal(overlay, modal_content);
        }
    });

    document.addEventListener('keydown', (event) => {
        if (event.key === 'Escape' && overlay.style.display !== "none") {
            closeModal(overlay, modal_content);
        }
    });
}

export function createCard(keywords, topic) {
    let _keywords = "";
    keywords.map((keyword) => _keywords += `${Object.keys(keyword)[0]}: ${Object.values(keyword)[0]};`)

    const card = document.createElement('div');
    card.className = 'card';
    card.id = `cardWith${_keywords}`;

    // insert keywords to html
    card.setAttribute('keywords', _keywords);

    card.innerHTML = `
    <div id="indicator"></div>
    <h3 id="topicContainer">
        <span id="topic">${topic}</span>
    </h3>
    <div class="clickable">
        <h3 id="heading"></h3>
        <p class="card-content"></p>
    </div>
    <a></a>
    `

    return card;
}