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
    gene_name   VARCHAR(30) NOT NULL,
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

/* Import the data from the files: Header line is ignored and fields are split by comma */
LOAD DATA INFILE 'data/organisms.txt'
    INTO TABLE organisms
    FIELDS TERMINATED BY ','
    LINES TERMINATED BY '\n'
    IGNORE 1 LINES;

LOAD DATA INFILE 'data/chromosomes.txt'
    INTO TABLE chromosomes
    FIELDS TERMINATED BY ','
    LINES TERMINATED BY '\n'
    IGNORE 1 LINES;

LOAD DATA INFILE 'data/genes.txt'
    INTO TABLE genes
    FIELDS TERMINATED BY ','
    LINES TERMINATED BY '\n'
    IGNORE 1 LINES;

LOAD DATA INFILE 'data/oligonucleotides.txt'
    INTO TABLE oligonucleotides
    FIELDS TERMINATED BY ','
    LINES TERMINATED BY '\n'
    IGNORE 1 LINES;

/* Create stored procedure */
/* Set delimiter to dash for readability */
DELIMITER -

/* Procedure using SELECT to get the gene name, identifiers and sequence */
CREATE PROCEDURE sp_get_genes()
BEGIN
    SELECT g.gene_name, gi.identifier, o.sequence FROM gene_identifier gi
        JOIN genes g ON g.id = gi.gene
        JOIN oligonucleotides o on g.id = o.gene;
END -

/* Procedure gives amount of different melting temperature divided by the number of oligonucleotides */
CREATE PROCEDURE sp_get_tm_vs_probes()
BEGIN
    SELECT COUNT(DISTINCT melt_temp)/COUNT(id) FROM oligonucleotides;
END -

/*  */
CREATE PROCEDURE sp_mark_duplicate_oligos(IN oligo_seq char(25))
BEGIN
    UPDATE oligonucleotides SET unique_seq = 1 WHERE sequence = oligo_seq;
END -

/* Set delimiter back to default */
DELIMITER ;