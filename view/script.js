import { createApp } from 'vue';

createApp({
    data: function() {
        return {
            items: [],
            currentItem: 0,
        };
    },
    methods: {
        fetchRecentNews() {
            fetch('http://localhost:25000/news/getRecent')
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! Status: ${response.status}`);
                }
                return response.json(); // Get raw response as text
            })
            .then(data => {
                console.log('Raw response:', data); // Log the raw response

                try {
                    //const jsonData = JSON.parse(data); // Attempt to parse the response
                    this.items = data; // Assign parsed news data
                } catch (error) {
                    console.error('Error parsing JSON:', error);
                }
            })
            .catch(error => {
                console.error('Error fetching news:', error);
            });

        },
        scrollUp() {
            if (this.currentItem > 0) {
                this.currentItem -= 1;
            }
        },
        scrollDown() {
            if (this.currentItem < this.items.length - 1) {
                this.currentItem += 1;
            }
        },
    },
    mounted() {
        this.fetchRecentNews();
    },
}).mount("#app");
