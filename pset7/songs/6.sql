-- SQL query that lists the names of songs that are by post malone
SELECT name FROM songs WHERE artist_id IN (SELECT id FROM artists WHERE name = "Post Malone");