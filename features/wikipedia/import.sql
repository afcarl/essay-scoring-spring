DROP TABLE IF EXISTS wp2gram;
CREATE TABLE wp2gram (
   occur int
   ,w1 varchar NULL
   ,w2 varchar NULL
);

COPY wp2gram FROM '/tmp/wp_2gram.txt' DELIMITER E'\t' CSV quote E'\b';

CREATE UNIQUE INDEX wp2gram_ind1 ON wp2gram (w1,w2);

DROP TABLE IF EXISTS wp3gram;
CREATE TABLE wp3gram (
   occur int
   ,w1 varchar NULL
   ,w2 varchar NULL
   ,w3 varchar NULL
);

COPY wp3gram FROM '/tmp/wp_3gram.txt' DELIMITER E'\t' CSV quote E'\b';
CREATE UNIQUE INDEX wp3gram_ind1 ON wp3gram (w1,w2,w3);


