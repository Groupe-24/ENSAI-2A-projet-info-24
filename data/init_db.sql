-----------------------------------------------------
-- Joueur
-----------------------------------------------------
DROP TABLE IF EXISTS joueur CASCADE ;
CREATE TABLE joueur(
    id_joueur    SERIAL PRIMARY KEY,
    date       VARCHAR(50),
    event          VARCHAR(256),
    blue_team           VARCHAR(50),
    blue_players1          INVARCHAR(50)TEGER,
    blue_players2         VARCHAR(50),
    blue_players3  VARCHAR(50),
    orange_team    VARCHAR(50),
    orange_players1       VARCHAR(50),
    orange_players2          VARCHAR(50),
    orange_players3          VARCHAR(50)
);
