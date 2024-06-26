document.getElementById('searchForm').addEventListener('submit', function(event) {
    event.preventDefault();
    var searchQuery = document.getElementById('searchInput').value;
    fetch('http://localhost:9200/files/_search?q=' + encodeURIComponent(searchQuery))
        .then(response => response.json())
        .then(data => {
            var resultsDiv = document.getElementById('results');
            resultsDiv.innerHTML = '';
            data.hits.hits.forEach(hit => {
                var resultDiv = document.createElement('div');
                resultDiv.textContent = hit._source.content;
                resultsDiv.appendChild(resultDiv);
            });
        });
});