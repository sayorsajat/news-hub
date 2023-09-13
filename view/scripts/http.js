
export async function fetchRecentNews(keywords) {
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

export function sendCardsSave(htmlFragment, dashboardId) {
    // Make a PUT request to server endpoint
    const requestOptions = {
        method: "PUT",
        body: htmlFragment,
        headers: {
            "Content-Type": "text/html",
        },
    };

    fetch(`http://localhost:25000/user/viewSettings/${dashboardId}`, requestOptions)
    .then(response => {
        if (!response.ok) {
            console.error("Error uploading HTML fragment:", response.statusText);
        }
    })
    .catch(error => {
        console.error("Error:", error);
    });
}

export async function fetchCardsSave(dashboardId) {
    const url = `http://localhost:25000/view/custom_dashboards/${dashboardId}_dashboard.html`;

    const response = await fetch(url, {
        cache: 'no-store', // Disable caching
    });

    if (response.ok) {
        return await response.text()
    } else {
        console.error('Error retrieving HTML fragment:', response.statusText);
        return false;
    }
}