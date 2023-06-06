-- SQL query to list the titles of all movies in which both Johnny Depp and
-- Helena Bonham Carter srarred
SELECT title FROM movies
JOIN stars ON movies.id = stars.movie_id
JOIN people ON stars.person_id = people.id
WHERE name IN ('Johnny Depp','Helena Bonham Carter')
GROUP BY title
HAVING COUNT(title) = 2;