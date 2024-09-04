/* In this SQL file, write (and comment!) the schema of your database,
including the CREATE TABLE IF NOT EXISTS, CREATE INDEX, CREATE VIEW, etc. statements that compose it */

/*
to connect mysql database: mysql -h 127.0.0.1 -P 3306 -u root -p
password: crimson

to create database-
CREATE DATABASE database_name;

to delete database-
DROP DATABASE database_name;

SHOW DATABASES;
USE [DATABASE NAME];

to create database from .sql file
source [database_creation_file].sql

alter any column data
ALTER TABLE table_name
MODIFY COLUMN column_name datatype;

*/

-- use this to CREATE TABLE IF NOT EXISTS only if not exist
-- CREATE TABLE IF NOT EXISTS IF NOT EXISTS 'table_name' ();


-- table to store user informations

CREATE TABLE IF NOT EXISTS `users` (
    `id` INT AUTO_INCREMENT,
    `username` VARCHAR(32) UNIQUE NOT NULL,
    `password` VARCHAR(128) NOT NULL,
    `first_name` VARCHAR(32) NOT NULL,
    `last_name` VARCHAR(32) NOT NULL,
    `email` VARCHAR(128) UNIQUE NOT NULL,
    `acc_created` DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
    `last_login` DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
    PRIMARY KEY(`id`)
);


-- table to store category informations

CREATE TABLE IF NOT EXISTS `categories` (
    `id` INT AUTO_INCREMENT,
    `category` VARCHAR(32) UNIQUE NOT NULL,
    PRIMARY KEY(`id`)
);


-- table to store listing informations

CREATE TABLE IF NOT EXISTS `listings` (
    `id` INT AUTO_INCREMENT,
    `category_id` INT NOT NULL,
    `title` VARCHAR(225) UNIQUE NOT NULL,
    `description` TEXT NOT NULL,
    `listing_price` DECIMAL(5, 2) CHECK(`listing_price` > 0) NOT NULL,
    `datetime_added` DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
    `added_by_user_id` INT NOT NULL,
    `status` ENUM('active', 'closed', 'deleted') DEFAULT 'active' NOT NULL,
    PRIMARY KEY(`id`),
    FOREIGN KEY(`category_id`) REFERENCES `categories`(`id`),
    FOREIGN KEY(`added_by_user_id`) REFERENCES `users`(`id`)
);


-- table to store images

CREATE TABLE IF NOT EXISTS `images` (
    `listing_id` INT NOT NULL,
    `image` BLOB NOT NULL,
    FOREIGN KEY(`listing_id`) REFERENCES `listings`(`id`)
);


-- table to store comments posted on listings

CREATE TABLE IF NOT EXISTS `comments` (
    `user_id` INT NOT NULL,
    `listing_id` INT NOT NULL,
    `comment` TEXT NOT NULL,
    `timestamp` DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
    FOREIGN KEY(`user_id`) REFERENCES `users`(`id`),
    FOREIGN KEY(`listing_id`) REFERENCES `listings`(`id`)
);


-- table to store listing bids

CREATE TABLE IF NOT EXISTS `bids` (
    `id` INT AUTO_INCREMENT,
    `user_id` INT NOT NULL,
    `listing_id` INT NOT NULL,
    `action` ENUM('added', 'bid_placed') NOT NULL,
    `price` DECIMAL(5, 2) CHECK(`price` > 0) NOT NULL,
    `timestamp` DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
    PRIMARY KEY(`id`, `user_id`, `listing_id`, `price`),
    FOREIGN KEY(`user_id`) REFERENCES `users`(`id`),
    FOREIGN KEY(`listing_id`) REFERENCES `listings`(`id`)
);


-- table to store bid winner

CREATE TABLE IF NOT EXISTS `winners` (
    `listing_id` INT NOT NULL,
    `user_id` INT NOT NULL,
    `timestamp` DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
    PRIMARY KEY(`listing_id`, `user_id`),
    FOREIGN KEY(`listing_id`) REFERENCES `listings`(`id`),
    FOREIGN KEY(`user_id`) REFERENCES `users`(`id`)
);


-- table to store listings into user's watchlist

CREATE TABLE IF NOT EXISTS `watchlists` (
    `user_id` INT NOT NULL,
    `listing_id` INT NOT NULL,
    FOREIGN KEY(`user_id`) REFERENCES `users`(`id`),
    FOREIGN KEY(`listing_id`) REFERENCES `listings`(`id`)
);

-- triggers

-- trigger for adding first bid as a listing added

CREATE TRIGGER initial_bid
AFTER INSERT ON listings
FOR EACH ROW
BEGIN
    INSERT INTO bids
    SET user_id = NEW.added_by_user_id,
        listing_id = NEW.id,
        price = NEW.listing_price;
END;


-- trigger for adding winner in winners table when listing is closed

CREATE TRIGGER bid_winner
AFTER UPDATE ON listings
FOR EACH ROW
BEGIN
    IF NEW.status = 'closed' THEN
        INSERT INTO winners
        SET listing_id = NEW.id,
            user_id = (SELECT bids.user_id FROM bids WHERE bids.listing_id = NEW.id AND bids.action = 'bid_placed' ORDER BY bids.timestamp, bids.price DESC LIMIT 1);
    END IF;
END;


-- indexes

-- index for listing

CREATE INDEX find_listings_title ON listings(title);
CREATE INDEX find_listings_category ON listings(category_id);
CREATE INDEX find_listings_status ON listings(status);
CREATE INDEX bid_by_listings ON bids (listing_id);
CREATE INDEX bid_by_price ON bids (price);

