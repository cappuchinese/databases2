/* Script for week3 assignment 2: Create database according to provided information */

/* Drop the tables before creating them */
DROP TABLE IF EXISTS organisms;
DROP TABLE IF EXISTS chromosomes;
DROP TABLE IF EXISTS gene_identifier;
DROP TABLE IF EXISTS genes;
DROP TABLE IF EXISTS oligonucleotides;
DROP TABLE IF EXISTS microarrays;
DROP TABLE IF EXISTS probe;

/* Create the tables */
CREATE TABLE organisms(
    id      INT         AUTO_INCREMENT,
    genus   VARCHAR(30) NOT NULL,
    species VARCHAR(30) NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE chromosomes(
    id          INT         AUTO_INCREMENT,
    organism    INT         NOT NULL,
    chromosome  VARCHAR(7)  NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (organism) REFERENCES organisms(id)
);

CREATE TABLE genes(
    id          INT         AUTO_INCREMENT,
    chromosome  INT         NOT NULL,
    sequence    LONGTEXT    NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (chromosome) REFERENCES chromosomes(id)
);

CREATE TABLE gene_identifier(
    id          INT         AUTO_INCREMENT,
    gene        INT         NOT NULL,
    identifier  MEDIUMTEXT  ,
    PRIMARY KEY (id),
    FOREIGN KEY (gene) REFERENCES genes(id)
);

CREATE TABLE oligonucleotides(
    id          INT         AUTO_INCREMENT,
    gene        INT         NOT NULL,
    sequence    CHAR(15)    NOT NULL,
    gc_perc     FLOAT       ,
    melt_temp   FLOAT       ,
    unique_seq  BOOL        DEFAULT FALSE,
    4_nucs_rep  BOOL        DEFAULT FALSE,
    max_dinucs  BOOL        DEFAULT FALSE,
    hairpin     BOOL        DEFAULT FALSE,
    PRIMARY KEY (id),
    FOREIGN KEY (gene) REFERENCES genes(id)
);

CREATE TABLE microarrays(
    id          INT         AUTO_INCREMENT,
    incub_temp  FLOAT       NOT NULL,
    quality     FLOAT       NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE probe(
    id          INT         AUTO_INCREMENT,
    microarray  INT         NOT NULL,
    oligo       INT         NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (microarray) REFERENCES microarrays(id),
    FOREIGN KEY (oligo) REFERENCES oligonucleotides(id)
);
