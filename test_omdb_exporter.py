import pytest
from unittest.mock import patch, mock_open
from omdb_exporter import (
    load_imdb_ids,
    fetch_movie,
    sql_escape,
    generate_sql,
    generate_rating_sql
)

# -----------------------------
# Test: load_imdb_ids
# -----------------------------
def test_load_imdb_ids():
    mock_data = "tt0111161\n\ntt0068646\n"
    with patch("builtins.open", mock_open(read_data=mock_data)):
        ids = load_imdb_ids("dummy.txt")
        assert ids == ["tt0111161", "tt0068646"]

# -----------------------------
# Test: sql_escape
# -----------------------------
@pytest.mark.parametrize("input_val,expected", [
    ("Some Title", "'Some Title'"),
    ("O'Hara", "'O''Hara'"),
    ("N/A", "NULL"),
    ("", "NULL"),
    (None, "NULL")
])
def test_sql_escape(input_val, expected):
    assert sql_escape(input_val) == expected

# -----------------------------
# Test: fetch_movie (mocked API)
# -----------------------------
@patch("omdb_exporter.requests.get")
def test_fetch_movie(mock_get):
    mock_get.return_value.json.return_value = {"Title": "Test Movie", "Response": "True"}
    result = fetch_movie("tt1234567")
    assert result["Title"] == "Test Movie"

# -----------------------------
# Test: generate_sql (mocked fetch and file write)
# -----------------------------
@patch("omdb_exporter.fetch_movie")
@patch("builtins.open", new_callable=mock_open)
@patch("omdb_exporter.time.sleep", return_value=None)  # skip delay
def test_generate_sql(mock_sleep, mock_file, mock_fetch):
    mock_fetch.return_value = {
        "Response": "True",
        "imdbID": "tt1234567",
        "Title": "Test",
        "Year": "2020",
        "Rated": "PG",
        "Released": "01 Jan 2020",
        "Runtime": "120 min",
        "Genre": "Drama",
        "Director": "Someone",
        "Writer": "Someone Else",
        "Actors": "Actor A, Actor B",
        "Plot": "A test plot.",
        "Language": "English",
        "Country": "USA",
        "Awards": "None",
        "Poster": "http://example.com",
        "Metascore": "70",
        "imdbRating": "8.0",
        "imdbVotes": "10,000",
        "Type": "movie",
        "DVD": "N/A",
        "BoxOffice": "N/A",
        "Production": "Studio",
        "Website": "N/A",
        "Response": "True"
    }
    generate_sql(["tt1234567"], "output.sql")
    mock_file().write.assert_called()  # ensure file was written

# -----------------------------
# Test: generate_rating_sql (mocked fetch and file write)
# -----------------------------
@patch("omdb_exporter.fetch_movie")
@patch("builtins.open", new_callable=mock_open)
@patch("omdb_exporter.time.sleep", return_value=None)  # skip delay
def test_generate_rating_sql(mock_sleep, mock_file, mock_fetch):
    mock_fetch.return_value = {
        "Response": "True",
        "Ratings": [
            {"Source": "Internet Movie Database", "Value": "8.5/10"},
            {"Source": "Rotten Tomatoes", "Value": "95%"}
        ]
    }
    generate_rating_sql(["tt1234567"], "ratings.sql")
    mock_file().write.assert_called()
