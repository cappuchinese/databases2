SET foreign_key_checks=0;

/* Drop the tables before creating them */
DROP TABLE IF EXISTS organisms;
DROP TABLE IF EXISTS chromosomes;
DROP TABLE IF EXISTS gene_identifier;
DROP TABLE IF EXISTS genes;
DROP TABLE IF EXISTS oligonucleotides;
DROP TABLE IF EXISTS microarrays;
DROP TABLE IF EXISTS probe;

/* Drop the procedures before creating them */
DROP PROCEDURE IF EXISTS sp_get_genes;
DROP PROCEDURE IF EXISTS sp_get_tm_vs_probes;
DROP PROCEDURE IF EXISTS sp_mark_duplicate_oligos;
DROP PROCEDURE IF EXISTS sp_get_oligos_by_tm;
DROP PROCEDURE IF EXISTS sp_get_matrices_by_quality;
DROP PROCEDURE IF EXISTS sp_create_probe;

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
    melt_temp   FLOAT       NOT NULL,
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
#
# /* Import the data from the files: Header line is ignored and fields are split by comma */
# LOAD DATA LOCAL INFILE 'data/organisms.txt'
#     INTO TABLE organisms
#     FIELDS TERMINATED BY ','
#     LINES TERMINATED BY '\n'
#     IGNORE 1 LINES;
#
# LOAD DATA LOCAL INFILE 'data/chromosomes.txt'
#     INTO TABLE chromosomes
#     FIELDS TERMINATED BY ','
#     LINES TERMINATED BY '\n'
#     IGNORE 1 LINES;
#
# LOAD DATA LOCAL INFILE 'data/genes.txt'
#     INTO TABLE genes
#     FIELDS TERMINATED BY ','
#     LINES TERMINATED BY '\n'
#     IGNORE 1 LINES;
#
# LOAD DATA LOCAL INFILE 'data/oligonucleotides.txt'
#     INTO TABLE oligonucleotides
#     FIELDS TERMINATED BY ','
#     LINES TERMINATED BY '\n'
#     IGNORE 1 LINES;

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

/* Procedure to mark every duplicate sequence entry in oligonucleotides */
CREATE PROCEDURE sp_mark_duplicate_oligos()
BEGIN
    UPDATE oligonucleotides SET unique_seq = 1 WHERE id IN (SELECT o.id
                                                     FROM oligonucleotides o
                                                     JOIN (SELECT id, sequence, count(*)
                                                           FROM oligonucleotides
                                                           GROUP BY sequence
                                                           HAVING COUNT(sequence)<2) AS cnt
                                                     ON o.sequence = cnt.sequence);
END -

/* Procedure to show oligo id's between a min and max */
CREATE PROCEDURE sp_get_oligos_by_tm(IN min FLOAT, IN max FLOAT)
    BEGIN
        /* Set variables and query*/
        SET @max = max;
        SET @min = min;
        SET @query = 'INSERT INTO oligo_ids SELECT id FROM oligonucleotides WHERE melt_temp BETWEEN ? AND ? ORDER BY melt_temp';

        /* Drop temporary table if it exists */
        DROP TABLE IF EXISTS oligo_ids;

        /* Create temporary table to store id's */
        CREATE TEMPORARY TABLE oligo_ids (
            oligo_id    INT
        );

        /* Prepare the query and execute it using the given values */
        PREPARE QUERY FROM @query;
        EXECUTE QUERY USING @min, @max;

        SELECT * FROM oligo_ids;
    END -

/* Procedure to show matrices ordered by genes without probes*/
CREATE PROCEDURE sp_get_matrices_by_quality()
    BEGIN
        SELECT m.id, m.quality, m.incub_temp,
        (SELECT MAX(id) FROM genes g) - COUNT(DISTINCT g.id) AS 'probeless_gene',
        COUNT(DISTINCT p.id) / COUNT(DISTINCT g.id) AS 'average_probes_per_gene'
        FROM genes g JOIN oligonucleotides o ON g.id = o.gene
        JOIN probe p ON o.id = p.oligo
        JOIN microarrays m ON p.microarray = m.id
        GROUP BY m.id ORDER BY probeless_gene, average_probes_per_gene DESC;
    END -

/* Procedure to create a new probe*/
CREATE PROCEDURE sp_create_probe(IN matrix_id INT, IN oligo_id INT)
    BEGIN
        SET @matrix_id = matrix_id;
        SET @oligo_id = oligo_id;
        SET @query = 'INSERT INTO probe(microarray, oligo) values(?, ?)';

        PREPARE QUERY FROM  @query;
        EXECUTE QUERY USING @matrix_id, @oligo_id;
    END -

/* Set delimiter back to default */
DELIMITER ;

/* Create indices */
CREATE FULLTEXT INDEX oligo_seq_index ON oligonucleotides(sequence);
CREATE FULLTEXT INDEX gene_name_index ON gene_identifier(identifier);
CREATE UNIQUE INDEX gene_id_index ON gene_identifier(id);
CREATE INDEX quality_index ON microarrays(quality);
CREATE INDEX incubation_index ON microarrays(incub_temp);
