-- SQL query to list the titles of the five highest rated mocies (in order)
-- that Chadwick Boseman starred in, starting the highest rated
SELECT title FROM movies
JOIN ratings ON movies.id = ratings.movie_id
JOIN stars ON movies.id = stars.movie_id
JOIN people ON stars.person_id = people.id
WHERE name = "Chadwick Boseman" ORDER BY rating DESC LIMIT 5;