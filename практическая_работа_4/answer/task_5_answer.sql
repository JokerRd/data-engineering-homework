CREATE TABLE clubs (
	club_id INTEGER NOT NULL,
	club_code VARCHAR NOT NULL,
	name VARCHAR NOT NULL,
	squad_size INTEGER NOT NULL,
	average_age FLOAT,
	foreigners_number INTEGER NOT NULL,
	national_team_players INTEGER NOT NULL,
	stadium_name VARCHAR NOT NULL,
	stadium_seats INTEGER NOT NULL,
	net_transfer_record VARCHAR NOT NULL,
	last_season INTEGER NOT NULL,
	PRIMARY KEY (club_id)
)

CREATE TABLE club_games (
	id INTEGER NOT NULL,
	game_id INTEGER NOT NULL,
	club_id INTEGER NOT NULL,
	own_goals INTEGER NOT NULL,
	own_position INTEGER,
	own_manager_name VARCHAR NOT NULL,
	opponent_id INTEGER NOT NULL,
	opponent_goals INTEGER NOT NULL,
	opponent_position INTEGER,
	opponent_manager_name VARCHAR NOT NULL,
	hosting VARCHAR NOT NULL,
	is_win BOOLEAN NOT NULL,
	PRIMARY KEY (id)
)

CREATE TABLE players (
	player_id INTEGER NOT NULL,
	first_name VARCHAR,
	last_name VARCHAR NOT NULL,
	name VARCHAR NOT NULL,
	last_season INTEGER NOT NULL,
	current_club_id INTEGER NOT NULL,
	country_of_birth VARCHAR,
	city_of_birth VARCHAR,
	date_of_birth DATE,
	position VARCHAR NOT NULL,
	foot VARCHAR,
	height_in_cm INTEGER,
	market_value_in_eur INTEGER,
	PRIMARY KEY (player_id)
)

SELECT clubs.club_id, clubs.club_code, clubs.name, clubs.squad_size, clubs.average_age, clubs.foreigners_number, clubs.national_team_players, clubs.stadium_name, clubs.stadium_seats, clubs.net_transfer_record, clubs.last_season
FROM clubs
WHERE clubs.squad_size > 25 ORDER BY clubs.squad_size
 LIMIT 30 OFFSET 0

SELECT clubs.club_id, clubs.club_code, clubs.name, clubs.squad_size, clubs.average_age, clubs.foreigners_number, clubs.national_team_players, clubs.stadium_name, clubs.stadium_seats, clubs.net_transfer_record, clubs.last_season
FROM clubs JOIN players ON players.current_club_id = clubs.club_id
WHERE players.name = 'Rio Ferdinand'
 LIMIT 1 OFFSET 0

SELECT club_games.own_manager_name, count(club_games.own_manager_name) AS count, sum(club_games.own_goals) AS sum, min(club_games.own_goals) AS min, max(club_games.own_goals) AS max, avg(club_games.own_goals) AS mean
FROM club_games GROUP BY club_games.own_manager_name

SELECT players.player_id, players.first_name, players.last_name, players.name, players.last_season, players.current_club_id, players.country_of_birth, players.city_of_birth, players.date_of_birth, players.position, players.foot, players.height_in_cm, players.market_value_in_eur, anon_1.sum_goals
FROM clubs JOIN (SELECT club_games.club_id AS club_id, sum(club_games.own_goals) AS sum_goals
FROM club_games GROUP BY club_games.club_id ORDER BY sum_goals desc
 LIMIT 1 OFFSET 0) AS anon_1 ON clubs.club_id = anon_1.club_id JOIN players ON players.current_club_id = clubs.club_id
WHERE 1 = 1

SELECT players.player_id, players.first_name, players.last_name, players.name, players.last_season, players.current_club_id, players.country_of_birth, players.city_of_birth, players.date_of_birth, players.position, players.foot, players.height_in_cm, players.market_value_in_eur
FROM players
WHERE players.country_of_birth = 'England' ORDER BY players.date_of_birth DESC
 LIMIT 30 OFFSET 0

SELECT club_games.own_goals, count(club_games.own_goals) AS count
FROM club_games GROUP BY club_games.own_goals