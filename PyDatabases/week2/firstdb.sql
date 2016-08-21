# firstdb.sql

# "Our first database" assignment from "Using databases with python" coursera course (Week 2)

# create table
create table ages (
	name VARCHAR(128),
	age INTEGER
);

# add entries to table
delete from ages;
INSERT INTO Ages (name, age) VALUES ('Krystal', 20);
INSERT INTO Ages (name, age) VALUES ('Melisa', 17);
INSERT INTO Ages (name, age) VALUES ('Donnacha', 17);
INSERT INTO Ages (name, age) VALUES ('Farrah', 17);
INSERT INTO Ages (name, age) VALUES ('Donnacha', 22);
INSERT INTO Ages (name, age) VALUES ('Tane', 35);

# set the hexidecimal representation of the concatenation of name and age as the temporary variable x.
# get this temp var from the table ordered by that new temporary variablewi
select hex(concat(name,age)) as x from ages order by x;
