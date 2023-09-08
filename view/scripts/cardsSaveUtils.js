import {sendCardsSave, fetchCardsSave, fetchRecentNews} from "./http.js";


// send html of dashboard to server in order to save all keywords settings
export function updateCardsSave() {
    // Clone the dashboard element to avoid modifying the displayed GUI
    const dashboard = document.getElementById('dashboard');
    const clonedDashboard = dashboard.cloneNode(true);

    // Remove text content from specific elements (e.g., <p> and <h3> tags)
    const elementsToRemoveTextFrom = clonedDashboard.querySelectorAll('p, h3');
    elementsToRemoveTextFrom.forEach(element => {
        element.textContent = ''; // Remove the text content
    });
    // remove everything from a links
    clonedDashboard.querySelectorAll('a').forEach(element => {
        element.textContent = ''; // Remove the text content
        element.href = ''; // remove href
    });
    // delete remove-mode from class list before sending
    clonedDashboard.querySelectorAll('div').forEach(element => {
        element.classList.remove("removal-mode");
    });

    // Get the HTML fragment from the cloned and modified dashboard
    const htmlFragment = clonedDashboard.innerHTML;

    sendCardsSave(htmlFragment)
}

// Preload already saved cards
export async function loadCardsSave() {
    try {
        const dashboard = document.getElementById('dashboard');
        dashboard.innerHTML = await fetchCardsSave();
    } catch (error) {
        console.error('Error:', error);
        return null;
    }
}

// Preload the news data to cards
export async function updateCards() {
    const cards = document.getElementsByClassName("card")
    for (let i = 0; i < cards.length; i++) {
        const keywordsString = cards[i].getAttribute("keywords");
        const keywordsArray = parseKeywords(keywordsString);

        const news = await fetchRecentNews(keywordsArray);

        if(news.length === 0) {
            cards[i].getElementsByTagName("h3")[0].innerHTML = "No news for now";
            continue;
        }

        // set title and content of news for card
        cards[i].getElementsByTagName("h3")[0].innerHTML = news[0].title;
        cards[i].getElementsByClassName("card-content")[0].innerHTML = news[0].content;
        const link = cards[i].getElementsByTagName("a")[0];
        link.href = news[0].descriptionUrl;
        link.innerHTML = news[0].descriptionUrl;
    }
}

// get keywords from html attribute "keywords" of cards
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