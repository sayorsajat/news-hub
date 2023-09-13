import {sendCardsSave, fetchCardsSave, fetchRecentNews} from "./http.js";
import {getDashboardId} from "./getIdSearchParam.js";


// send html of dashboard to server in order to save all keywords settings
export function updateCardsSave() {
    // Clone the dashboard element to avoid modifying the displayed GUI
    const dashboard = document.getElementById('dashboard');
    const clonedDashboard = dashboard.cloneNode(true);

    // Remove text content from specific elements (e.g., <p> and <h3> tags)
    const elementsToRemoveTextFrom = clonedDashboard.querySelectorAll('p, #heading');
    elementsToRemoveTextFrom.forEach(element => {
        element.textContent = ''; // Remove the text content
    });
    // remove everything from a links
    clonedDashboard.querySelectorAll('a').forEach(element => {
        element.textContent = ''; // Remove the text content
        element.href = ''; // remove href
    });
    // delete remove-mode from class list before sending
    clonedDashboard.querySelectorAll('div .card').forEach(element => {
        element.classList = ["card"];
    });
    // clear indicator status before sending
    clonedDashboard.querySelectorAll('div #indicator').forEach(element => {
        element.classList = [];
    });
    clonedDashboard.querySelectorAll('div .clickable').forEach(element => {
        element.classList = element.classList[0];
    });

    // Get the HTML fragment from the cloned and modified dashboard
    const htmlFragment = clonedDashboard.innerHTML;

    const dashboardId = getDashboardId()

    sendCardsSave(htmlFragment, dashboardId)
}

// Preload already saved cards
export async function loadCardsSave(dashboardId) {
    try {
        const dashboard = document.getElementById('dashboard');

        const response = await fetchCardsSave(dashboardId);
        if(response === false) return false;
        dashboard.innerHTML = response;
        return true;
    } catch (error) {
        console.error('Error:', error);
        return false;
    }
}

// Preload the news data to cards
export async function updateCards() {
    const cards = document.querySelectorAll(".card")
    for (let i = 0; i < cards.length; i++) {
        const keywordsString = cards[i].getAttribute("keywords");
        const keywordsArray = parseKeywords(keywordsString);

        const news = await fetchRecentNews(keywordsArray);

        if(news.length === 0) {
            cards[i].getElementsByClassName("card-content")[0].innerHTML = "No news for now";
            // set indicator level to mundane
            const urgency = "mundane";
            cards[i].querySelector("#indicator").classList.add(urgency);
            continue;
        }

        let urgency = urgencyToColorClass(news[0].urgency)
        // set indicator level
        cards[i].querySelector("#indicator").classList.add(urgency);
        // set title and content of news for card
        cards[i].querySelector("#heading").innerHTML = news[0].title;
        cards[i].getElementsByClassName("card-content")[0].innerHTML = news[0].content;
        const link = cards[i].getElementsByTagName("a")[0];
        link.href = news[0].descriptionUrl;
        link.innerHTML = news[0].source;

        if(urgency !== "mundane") {
            cards[i].classList.add(urgency);
        }
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

function urgencyToColorClass(urgency){
    if (urgency < 2) {
        return "mundane"
    } else if (urgency < 4) {
        return "interesting"
    } else if (urgency < 6) {
        return "must-know-for-decision"
    } else if (urgency < 8) {
        return "must-react"
    } else if (urgency >= 8) {
        return "must-react-right-now"
    }
}
