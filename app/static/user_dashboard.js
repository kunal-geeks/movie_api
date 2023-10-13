document.addEventListener('DOMContentLoaded', function () {
    // Fetch genres and populate dropdown
    fetch('/api/get_genres')
        .then(response => response.json())
        .then(data => {
            const genreDropdown = document.getElementById('genreFilter');
            // Clear existing options
            genreDropdown.innerHTML = '';
            // Add the default "All Genres" option
            const allGenresOption = document.createElement('option');
            allGenresOption.value = '';
            allGenresOption.textContent = 'All Genres';
            genreDropdown.appendChild(allGenresOption);

            // Add genres fetched from the API
            data.genres.forEach(genre => {
                const option = document.createElement('option');
                option.value = genre;
                option.textContent = genre;
                genreDropdown.appendChild(option);
            });
        })
        .catch(error => console.error('Error loading genres:', error));

    let page = 1;
    let isLoading = false;

    function loadMovies() {
        if (isLoading) {
            return;
        }

        isLoading = true;
        document.getElementById('loadingIndicator').style.display = 'block';

        const genreFilter = document.getElementById('genreFilter').value;
        const sortBy = document.getElementById('sortBy').value;
        const sortOrder = document.getElementById('sortOrder').value;
        const searchQuery = document.getElementById('searchInput').value.toLowerCase();

        fetch(`/api/get_movies?page=${page}&genre=${genreFilter}&sort=${sortBy}&order=${sortOrder}&search=${searchQuery}`)
            .then(response => response.json())
            .then(data => {
                const moviesList = document.getElementById('moviesList');
                const movies = data.movies;

                if (page === 1) {
                    moviesList.innerHTML = ''; // Clear moviesList if it's the first page
                }

                movies.forEach(movie => {
                    const cardHtml = `
                        <div class="movie-card">
                            <h5 class="card-title">${movie.name}</h5>
                            <p class="card-text">ID: ${movie.id}</p>
                            <p class="card-text">Director: ${movie.director}</p>
                            <p class="card-text">Popularity: ${movie.popularity}</p>
                            <p class="card-text">IMDb Score: ${movie.imdb_score}</p>
                            <p class="card-text">Genres: ${movie.genre.join(', ')}</p>
                        </div>
                    `;
                    moviesList.insertAdjacentHTML('beforeend', cardHtml);
                });

                isLoading = false;
                document.getElementById('loadingIndicator').style.display = 'none';
                page++;
            })
            .catch(error => console.error('Error loading movies:', error));
    }

    function handleScroll() {
        const { scrollTop, scrollHeight, clientHeight } = document.documentElement;
        if (scrollTop + clientHeight >= scrollHeight - 100) {
            loadMovies();
        }
    }

    // Event listeners for genre, sort, and order changes
    document.getElementById('genreFilter').addEventListener('change', () => resetAndLoadMovies());
    document.getElementById('sortBy').addEventListener('change', () => resetAndLoadMovies());
    document.getElementById('sortOrder').addEventListener('change', () => resetAndLoadMovies());

    // Event listener for Search button click
    document.getElementById('searchButton').addEventListener('click', () => resetAndLoadMovies());

    // Event listener for Reset button click
    document.getElementById('resetButton').addEventListener('click', () => {
        document.getElementById('genreFilter').value = '';
        document.getElementById('sortBy').value = 'imdb_score';
        document.getElementById('sortOrder').value = 'desc';
        document.getElementById('searchInput').value = '';
        resetAndLoadMovies();
    });

    // Event listener for Enter key in the search input field
    document.getElementById('searchInput').addEventListener('keypress', event => {
        if (event.key === 'Enter') {
            resetAndLoadMovies();
        }
    });

    // Function to reset page and load movies
    function resetAndLoadMovies() {
        page = 1;
        const moviesList = document.getElementById('moviesList');
        moviesList.innerHTML = '';
        loadMovies();
    }

    // Initial load
    loadMovies();
    window.addEventListener('scroll', handleScroll);
});


// Function to handle logout
function handleLogout() {
    fetch('/auth/logout', {
        method: 'POST',
        credentials: 'include', // include cookies in the request
    })
    .then(response => {
        if (response.ok) {
            // Successfully logged out
            window.location.href = '/login'; // Redirect to login page
        } else {
            // Failed to log out, handle the error
            console.error('Failed to logout');
        }
    })
    .catch(error => console.error(error));
}
// Function to handle edit account
function handleEditAccount() {
    window.location.href = '/edit-account'; // Redirect to edit account page
}

// Example: Add event listeners to the logout and edit account links/buttons
document.getElementById('logoutBtn').addEventListener('click', handleLogout);
document.getElementById('editAccountBtn').addEventListener('click', handleEditAccount);
