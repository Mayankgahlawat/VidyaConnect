document.addEventListener('DOMContentLoaded', function() {
    // Run both functions when the page loads
    fetchNews();
    fetchJobs();
});

// In app/static/main.js

function fetchNews() {
    const newsContainer = document.getElementById('news-container');
    fetch('/api/news/top-headlines')
        .then(response => response.json())
        .then(data => {
            newsContainer.innerHTML = '';
            if (data.data && data.data.length > 0) {
                data.data.forEach(article => {
                    // Check if an image exists and create the image tag only if it does
                    const imageTag = article.image 
                        ? `<img src="${article.image}" class="card-img-top" alt="Article image">` 
                        : ''; // Otherwise, create an empty string

                    const articleCard = `
                        <div class="col-md-4 mb-4">
                            <div class="card h-100">
                                ${imageTag}
                                <div class="card-body">
                                    <h5 class="card-title">${article.title}</h5>
                                    <p class="card-text">${article.description || 'No description available.'}</p>
                                    <a href="${article.url}" target="_blank" class="btn btn-primary">Read More</a>
                                </div>
                            </div>
                        </div>
                    `;
                    newsContainer.innerHTML += articleCard;
                });
            } else {
                newsContainer.innerHTML = '<p>No news articles found.</p>';
            }
        })
        .catch(error => {
            console.error('Error fetching news:', error);
            newsContainer.innerHTML = '<p>Sorry, there was an error fetching the news.</p>';
        });
}

function fetchJobs() {
    const jobContainer = document.getElementById('job-container');
    fetch('/api/jobs')
        .then(response => response.json())
        .then(jobs => {
            jobContainer.innerHTML = '';
            if (jobs && jobs.length > 0) {
                jobs.forEach(job => {
                    const jobCard = `
                        <div class="col-md-4 mb-4">
                            <div class="card h-100">
                                <div class="card-body">
                                    <h5 class="card-title">${job.title}</h5>
                                    <h6 class="card-subtitle mb-2 text-muted">${job.company}</h6>
                                    <p class="card-text">${job.location}</p>
                                    <a href="${job.url}" target="_blank" class="btn btn-secondary">View Job</a>
                                </div>
                            </div>
                        </div>
                    `;
                    jobContainer.innerHTML += jobCard;
                });
            } else {
                jobContainer.innerHTML = '<p>No jobs found. Run the scraper to populate the database.</p>';
            }
        })
        .catch(error => {
            console.error('Error fetching jobs:', error);
            jobContainer.innerHTML = '<p>Sorry, there was an error fetching jobs.</p>';
        });
}