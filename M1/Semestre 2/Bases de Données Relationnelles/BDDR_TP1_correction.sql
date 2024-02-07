-- ########################################################
-- BDDR TP 1
-- 13/01/2023
--
-- Sakila (BD), SQLite (SGBD)
-- ########################################################


-- ------------------------------------------------------------------
-- 1- Récupérez la liste de tous les films, avec l’année de sortie et 
-- la durée, triés par année de sortie (ordre descendant) et 
-- nom (ordre ascendant).
-- ------------------------------------------------------------------

SELECT release_year, title, length 
FROM film 
ORDER BY release_year DESC, title ASC;

-- ------------------------------------------------------------------
-- 2- Quels sont les acteurs qui ont pour nom ‘JACKMAN’ ? 
-- R: Warren et Jane
-- ------------------------------------------------------------------

SELECT * 
FROM actor 
WHERE last_name='JACKMAN';


-- ------------------------------------------------------------------
-- 3- Combien de catégories de films il y a dans la bdd ?
-- R: 16
-- ------------------------------------------------------------------

SELECT count(*) FROM category;


-- ------------------------------------------------------------------
-- 4- Quelle est la durée moyenne des films disponibles au video-club.
-- R: 4.985 (avg), 3 (min), 7 (max)
-- ------------------------------------------------------------------

SELECT AVG(rental_duration) moyenne, MIN(rental_duration) min, MAX(rental_duration) max
FROM film;


-- ------------------------------------------------------------------
-- 5- Combien de films sont sortis chaque année ? 
-- R: 1000 films en 2006 (il n'y a pas d'autres années dans la bdd)
-- ------------------------------------------------------------------

SELECT release_year, COUNT(*) 
FROM film 
GROUP BY release_year;

-- ------------------------------------------------------------------
-- 6- Listez toutes les adresses enregistrés en format 
-- “<adresse>, <code_postal>” (l’adresse est concaténé avec le code 
-- postal). Triez la liste par code postal puis adresse.
-- ------------------------------------------------------------------

SELECT address || ", " || postal_code 
FROM address 
ORDER BY postal_code, address;


-- ------------------------------------------------------------------
-- 7- A partir de la requête de la question précédente, supprimez les 
-- adresses qui ont un valeur NULL.
-- ------------------------------------------------------------------

SELECT address || ", " || postal_code 
FROM address 
WHERE postal_code IS NOT NULL 
ORDER BY postal_code, address;

-- ------------------------------------------------------------------
-- 8- Quels sont les référencement cinématographiques des films dans 
-- la bdd? Obtenez une liste sans doublons.
-- R: G, NC-17, PG, PG-13, R (5 en total)
-- ------------------------------------------------------------------

SELECT DISTINCT rating FROM film;


-- ------------------------------------------------------------------
-- 9- Affichez une liste de films avec le nom de la langue de 
-- la version originale (VO).
-- ------------------------------------------------------------------

SELECT L.language_id, L.name, title
FROM film F, language L
WHERE F.language_id = L.language_id;


-- ------------------------------------------------------------------
-- 10- Combien de films il y a par langue ? 
-- Dans votre tableau de résultat, affichez l’identifiant de la 
-- langue, le nom et le nombre de films.
-- R: 1000 films en anglais (pas d'autres langues)
-- ------------------------------------------------------------------

SELECT language.language_id, language.name, COUNT(title) 
FROM   film, language
WHERE  film.language_id = language.language_id
GROUP BY film.language_id 
ORDER BY film.language_id;

