document.addEventListener('DOMContentLoaded', () => {
    const addMovieForm = document.getElementById('addMovieForm');
    const searchMovieBtn = document.getElementById('searchMovieBtn');
    const searchMovieInput = document.getElementById('searchMovie');
    const movieLogsTableBody = document.getElementById('movieLogsTableBody');

    // Event listener for Add Movie form submission
    addMovieForm.addEventListener('submit', event => {
        event.preventDefault();
        const name = document.getElementById('name').value;
        const director = document.getElementById('director').value;
        const genreInput = document.getElementById('genre').value;
        const genreList = genreInput.split(',').map(genre => genre.trim().charAt(0).toUpperCase() + genre.trim().slice(1).toLowerCase());
        const popularity = document.getElementById('popularity').value;
        const imdbScore = document.getElementById('imdbScore').value;

        // Send a POST request to add a movie
        axios.post('/api/movies', {
            name: name,
            director: director,
            genre: genreList,
            popularity: parseFloat(popularity),
            imdb_score: parseFloat(imdbScore)
        }, {
            withCredentials: true
        })
        .then(response => {
            if (response.status === 201) {
                // After successful addition, add a new row to the table
                alert('Movie added successfully!');
                fetchMovieLogs();
                document.getElementById('addMovieForm').reset();
            }
        })
        .catch(error => {
            console.error(error);
        });
    });

    // Event listener for Search Movie button click
    searchMovieBtn.addEventListener('click', () => {
        const movieID = parseInt(searchMovieInput.value);
        // Send a GET request to search for the movie
        axios.get(`/api/movies/${movieID}`, {
            withCredentials: true
        })
        .then(response => {
            const movie = response.data;
            // Display movie info and manage buttons dynamically
            displayMovieInfo(movie);
        })
        .catch(error => {
            console.error(error);
        });
    });

    // Function to display movie info in the movieInfo section with edit and delete buttons
    function displayMovieInfo(movie) {
        const movieInfo = document.getElementById('movieInfo');
        // Clear previous movie info
        movieInfo.innerHTML = '';

        // Create movie card dynamically with edit, save, and delete buttons
        const card = document.createElement('div');
        card.className = 'card';
        card.innerHTML = `
            <div class="card-body">
                <h5 class="card-title" id="movieName">${movie.name}</h5>
                <p class="card-text">
                    <strong>ID:</strong> <span id="movieId">${movie.id}</span><br>
                    <strong>Director:</strong> <span id="director">${movie.director}</span><br>
                    <strong>Genre:</strong> <span id="genre">${movie.genre.join(', ')}</span><br>
                    <strong>Popularity:</strong> <span id="popularity">${movie.popularity}</span><br>
                    <strong>IMDB Score:</strong> <span id="imdbScore">${movie.imdb_score}</span>
                </p>
                <button class="btn btn-warning btn-sm" id="editBtn">Edit</button>
                <button class="btn btn-danger btn-sm" id="deleteBtn">Delete</button>
                <button class="btn btn-success btn-sm" id="saveBtn" style="display: none;">Save</button>
            </div>
        `;

        // Append the movie card to movieInfo
        movieInfo.appendChild(card);

        // Add event listeners to edit, save, and delete buttons
        const editBtn = card.querySelector('#editBtn');
        const saveBtn = card.querySelector('#saveBtn');
        const deleteBtn = card.querySelector('#deleteBtn');

        editBtn.addEventListener('click', () => {
            // Enable editing of movie content
            enableEditing(card);
        });

        saveBtn.addEventListener('click', () => {
            // Save edited movie content
            saveEditedMovie(card);
        });

        deleteBtn.addEventListener('click', () => {
            // Delete the movie and update the table
            deleteMovie(movie.id);
        });
    }

    // Function to enable editing of movie content
    function enableEditing(card) {
        card.querySelector('#movieName').contentEditable = true;
        card.querySelector('#director').contentEditable = true;
        card.querySelector('#genre').contentEditable = true;
        card.querySelector('#popularity').contentEditable = true;
        card.querySelector('#imdbScore').contentEditable = true;
       
        // Show the save button and hide the edit button
        card.querySelector('#saveBtn').style.display = 'inline-block';
        card.querySelector('#editBtn').style.display = 'none';
    }

    // Function to save edited movie content
    function saveEditedMovie(card) {
        const movieId = parseInt(card.querySelector('#movieId').innerText);
        const editedMovie = {
            id: movieId,
            name: card.querySelector('#movieName').innerText,
            director: card.querySelector('#director').innerText,
            genre: card.querySelector('#genre').innerText.split(',').map(genre => genre.trim().charAt(0).toUpperCase() + genre.trim().slice(1).toLowerCase()),
            popularity: parseFloat(card.querySelector('#popularity').innerText),
            imdb_score: parseFloat(card.querySelector('#imdbScore').innerText)
        };

        // Send a PUT request to update the movie
        axios.put(`/api/movies/${movieId}`, editedMovie, {
            withCredentials: true
        })
        .then(response => {
            if(response.status === 200) {
                // Disable editing and show the edit button
                disableEditing(card);
                alert('Movie updated successfully!');
                const movieInfo = document.getElementById('movieInfo');
                searchMovieInput.value = '';
                // Update the logs
                fetchMovieLogs();
            }
        })
        .catch(error => {
            console.error(error);
        });
    }

    // Function to disable editing of movie content
    function disableEditing(card) {
        card.querySelector('#movieName').contentEditable = false;
        card.querySelector('#director').contentEditable = false;
        card.querySelector('#genre').contentEditable = false;
        card.querySelector('#popularity').contentEditable = false;
        card.querySelector('#imdbScore').contentEditable = false;

        // Show the edit button and hide the save button
        card.querySelector('#saveBtn').style.display = 'none';
        card.querySelector('#editBtn').style.display = 'inline-block';
    }

    // Function to delete a movie and update the table
    function deleteMovie(movieId) {
        // Send a DELETE request to delete the movie
        axios.delete(`/api/movies/${movieId}`, {
            withCredentials: true
        })
        .then((response) => {
            if(response.status === 200) {
                alert('Movie deleted successfully!');
                const movieInfo = document.getElementById('movieInfo');
                // Clear previous movie info
                movieInfo.innerHTML = '';
                searchMovieInput.value = '';
                // Update the logs
                fetchMovieLogs();
            }
        })
        .catch(error => {
            console.error(error);
        });
    }

    // Function to fetch movie logs from the API and display them in the table
    function fetchMovieLogs() {
        axios.get('/api/movie_logs', {
            withCredentials: true
        })
        .then(response => {
            const logs = response.data.logs;
            // Clear previous logs
            movieLogsTableBody.innerHTML = '';
            logs.forEach(log => {
                // Add a new row to the table for each log
                addRowToTable(log);
            });
        })
        .catch(error => {
            console.error(error);
        });
    }

    // Function to add a new row to the table with movie log info
    function addRowToTable(log) {
        const row = document.createElement('tr');
    // Convert UTC timestamp to local time
    const utcDate = new Date(log.timestamp);
    const options = {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit',
        hour12: true, // Use 12-hour clock
        timeZoneName: 'short'
    };
    
    const localDate = new Intl.DateTimeFormat('en-US', options).format(utcDate);

    row.innerHTML = `
        <td>${log.id}</td>
        <td>${log.movie_id}</td>
        <td>${log.movie_name}</td>
        <td>${log.action}</td>
        <td>${localDate}</td>
    `;

        // Append the row to the table
        movieLogsTableBody.appendChild(row);
    }

    // Fetch movie logs when the page loads
    fetchMovieLogs();
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
