from typing import Any

import pytest
from unittest.mock import patch, mock_open
from src.movie.omdb_exporter import (
    load_imdb_ids,
    fetch_movie,
    sql_escape,
    generate_sql,
    generate_rating_sql
)
@pytest.fixture
def dune_json() -> dict[str | Any, str | Any]:
    return {
        "Title": "Dune",
        "Year": "1984",
        "Rated": "PG-13",
        "Released": "14 Dec 1984",
        "Runtime": "137 min",
        "Genre": "Action, Adventure, Sci-Fi",
        "Director": "David Lynch",
        "Writer": "Frank Herbert, David Lynch",
        "Actors": "Kyle MacLachlan, Virginia Madsen, Francesca Annis",
        "Plot": "A Duke's son leads desert warriors against the galactic emperor and his father's evil nemesis to free their desert world from the emperor's rule.",
        "Language": "English",
        "Country": "United States, Mexico",
        "Awards": "Nominated for 1 Oscar. 2 wins & 7 nominations total",
        "Poster": "https://m.media-amazon.com/images/M/MV5BMGJlMGM3NDAtOWNhMy00MWExLWI2MzEtMDQ0ZDIzZDY5ZmQ2XkEyXkFqcGc@._V1_SX300.jpg",
        "Ratings": [
            {"Source": "Internet Movie Database", "Value": "6.3/10"},
            {"Source": "Rotten Tomatoes", "Value": "36%"},
            {"Source": "Metacritic", "Value": "41/100"}
        ],
        "Metascore": "41",
        "imdbRating": "6.3",
        "imdbVotes": "188,960",
        "imdbID": "tt0087182",
        "Type": "movie",
        "DVD": "N/A",
        "BoxOffice": "$31,439,560",
        "Production": "N/A",
        "Website": "N/A",
        "Response": "True"
    }
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
def test_fetch_movie_dune(mock_get, dune_json):

    mock_get.return_value.json.return_value = dune_json

    result = fetch_movie("tt0087182")

    assert result["Title"] == "Dune"
    assert result["Year"] == "1984"
    assert result["Rated"] == "PG-13"
    assert result["Released"] == "14 Dec 1984"
    assert result["Runtime"] == "137 min"
    assert result["Genre"] == "Action, Adventure, Sci-Fi"
    assert result["Director"] == "David Lynch"
    assert result["Writer"] == "Frank Herbert, David Lynch"
    assert result["Actors"] == "Kyle MacLachlan, Virginia Madsen, Francesca Annis"
    assert result["Plot"] == (
        "A Duke's son leads desert warriors against the galactic emperor and his father's evil nemesis "
        "to free their desert world from the emperor's rule."
    )
    assert result["Language"] == "English"
    assert result["Country"] == "United States, Mexico"
    assert result["Awards"] == "Nominated for 1 Oscar. 2 wins & 7 nominations total"
    assert result["Poster"] == "https://m.media-amazon.com/images/M/MV5BMGJlMGM3NDAtOWNhMy00MWExLWI2MzEtMDQ0ZDIzZDY5ZmQ2XkEyXkFqcGc@._V1_SX300.jpg"
    assert result["Ratings"] == [
        {"Source": "Internet Movie Database", "Value": "6.3/10"},
        {"Source": "Rotten Tomatoes", "Value": "36%"},
        {"Source": "Metacritic", "Value": "41/100"}
    ]
    assert result["Metascore"] == "41"
    assert result["imdbRating"] == "6.3"
    assert result["imdbVotes"] == "188,960"
    assert result["imdbID"] == "tt0087182"
    assert result["Type"] == "movie"
    assert result["DVD"] == "N/A"
    assert result["BoxOffice"] == "$31,439,560"
    assert result["Production"] == "N/A"
    assert result["Website"] == "N/A"
    assert result["Response"] == "True"


# -----------------------------
# Test: generate_sql (mocked fetch and file write)
# -----------------------------
@patch("omdb_exporter.fetch_movie")
@patch("builtins.open", new_callable=mock_open)
@patch("omdb_exporter.time.sleep", return_value=None)  # skip delay
def test_generate_sql(mock_sleep, mock_file, mock_fetch, dune_json):
    mock_fetch.return_value = dune_json
    generate_sql(["tt0087182"], "output.sql")
    mock_file().write.assert_called()  # ensure file was written

# -----------------------------
# Test: generate_rating_sql (mocked fetch and file write)
# -----------------------------
@patch("omdb_exporter.fetch_movie")
@patch("builtins.open", new_callable=mock_open)
@patch("omdb_exporter.time.sleep", return_value=None)  # skip delay
def test_generate_rating_sql(mock_sleep, mock_file, mock_fetch, dune_json):
    mock_fetch.return_value = dune_json
    generate_rating_sql(["tt0087182"], "ratings.sql")
    mock_file().write.assert_called()
