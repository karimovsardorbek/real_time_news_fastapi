const shownArticleIds = new Set();

// Fetch articles from the API and render them in the DOM
async function fetchArticles() {
    try {
        const res = await fetch('http://localhost:8010/api/articles/');
        const articles = await res.json();
        articles.forEach(addArticleToDOM);
    } catch (err) {
        console.error("Failed to fetch articles:", err);
    }
}

// Add a new article to the DOM if it hasn't been shown yet
function addArticleToDOM(article) {
    if (shownArticleIds.has(article.id)) return;

    const card = renderArticle(article);
    document.getElementById('news-list').prepend(card);
    shownArticleIds.add(article.id);
}

// Render an article card
function renderArticle(article) {
    const card = document.createElement('div');
    card.className = 'news-card';

    if (article.image) {
        const img = document.createElement('img');
        img.src = article.image;
        img.alt = article.title;
        img.className = 'news-image';
        card.appendChild(img);
    }

    const title = document.createElement('div');
    title.className = 'news-title';
    title.textContent = article.title;
    card.appendChild(title);

    const meta = document.createElement('div');
    meta.className = 'news-meta';
    meta.textContent = new Date(article.publication_date).toLocaleString();
    card.appendChild(meta);

    const content = document.createElement('div');
    content.className = 'news-content';
    content.textContent = article.summary;
    card.appendChild(content);

    return card;
}

// WebSocket connection
const socket = new WebSocket('ws://localhost:8010/ws/news/');

socket.onopen = () => {
    console.log("✅ WebSocket connected");
};

socket.onmessage = (e) => {
    const data = JSON.parse(e.data);
    if (data.article) addArticleToDOM(data.article);
};

socket.onclose = () => {
    console.warn("⚠️ WebSocket closed. Attempting to reconnect in 3s...");
    setTimeout(() => location.reload(), 3000);
};

socket.onerror = (err) => {
    console.error("❌ WebSocket error:", err);
};

fetchArticles();