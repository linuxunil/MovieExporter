## Program Walkthrough: Movie & Ratings SQL Exporter

### Objective
Build a program that:
1. Reads a list of IMDb IDs from a file.
2. Queries the OMDb API for each movie using the IMDb ID.
3. Extracts movie details and ratings.
4. Saves this information into two separate SQL files — one for movies, one for ratings.

---

### Setup & Configuration

- The program should load a private API key from a `.env` file using an environment variable.
- It must be able to access:
  - A file containing IMDb IDs (one per line).
  - An API endpoint that returns movie data based on an IMDb ID.

---

### Required Files

1. **IMDb ID file**: A plain text file with one IMDb ID per line.
2. **SQL output file for movies**: Contains all the movie details formatted as an SQL `INSERT` statement.
3. **SQL output file for ratings**: Contains the rating data (source and value) for each movie, also as SQL `INSERT` statements.

---

### Program Workflow

#### 1. Load Environment Variables
- Load an API key from the environment (not hardcoded).
- This key is required to make requests to the OMDb API.

#### 2. Load IMDb IDs
- Open the input file with IMDb IDs.
- Read all non-empty lines.
- Strip leading/trailing whitespace from each line.
- Store the cleaned list of IDs in memory.

#### 3. Fetch Movie Data
- For each IMDb ID:
  - Construct a URL with the API key and ID.
  - Send an HTTP GET request to fetch movie data.
  - Parse the response (JSON format).

#### 4. Generate Movie SQL Output
- Create an SQL `INSERT INTO` statement for a `movies` table.
- For each movie:
  - If the API response is valid, extract key fields such as:
    - Title, year, rating, release date, runtime, genre, director, actors, etc.
  - Escape all text values to ensure they are safe for SQL.
  - If a field is missing or marked as "N/A", insert `NULL`.
  - Construct a value row for each movie.
  - After each request, pause briefly (e.g., 200ms) to avoid rate-limiting.
- Write all rows to the SQL file, ending the statement with a semicolon.

#### 5. Generate Ratings SQL Output
- Create an SQL `INSERT INTO` statement for a `ratings` table.
- For each movie:
  - If the API response is valid and includes a `Ratings` section:
    - Loop through each rating source and its value.
    - Escape both fields for SQL.
    - Add a new value row linking the IMDb ID with its rating source and value.
  - Pause between API requests to respect rate limits.
- Write all rating rows to the SQL file, ending the statement with a semicolon.

---

### Additional Notes

- The program should print status updates or warnings when a movie isn’t found.
- Make sure both SQL files are UTF-8 encoded and properly formatted.
- Treat the entire operation as batch processing — no real-time UI required.
- Focus on reliability, escaping input, and respecting API limits.

---

### Output

- **movies_insert.sql**: An SQL file with all movies and their metadata, ready to be imported into a `movies` table.
- **ratings_insert.sql**: An SQL file with all rating source/value pairs, linked to each IMDb ID.

