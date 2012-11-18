-- phpMyAdmin SQL Dump
-- version 3.4.10.1deb1
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Nov 18, 2012 at 12:18 PM
-- Server version: 5.5.28
-- PHP Version: 5.3.10-1ubuntu3.4

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";

--
-- Database: `mmuser`
--

-- --------------------------------------------------------

--
-- Table structure for table `gateways`
--

CREATE TABLE IF NOT EXISTS `gateways` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(20) NOT NULL,
  `coords` varchar(25) NOT NULL,
  `user_id` int(11) NOT NULL,
  `world_id` int(11) NOT NULL,
  `type` varchar(10) NOT NULL,
  `created` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `used` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`,`world_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;


ALTER TABLE `gateways` ADD INDEX ( `user_id` ) ;
ALTER TABLE `gateways` ADD INDEX ( `world_id` ) ;



ALTER TABLE `gateways` ADD FOREIGN KEY ( `user_id` ) REFERENCES `users` (
`id`
) ON DELETE NO ACTION ON UPDATE NO ACTION ;

ALTER TABLE `gateways` ADD FOREIGN KEY ( `world_id` ) REFERENCES `worlds` (
`id`
) ON DELETE NO ACTION ON UPDATE NO ACTION ;


INSERT INTO `commands` (
`id` ,
`name` ,
`desc` ,
`syntax`
)
VALUES (
NULL , '!gateway', 'Registers public or private gateway used for teleportation', '!gateway MODE NAME COORDS 
MODE = public or private
NAME = name of gateway
COORDS = coordinates to save, x y z 
example: !gateway public centrum 100 100 100'
);

INSERT INTO `commands` (
`id` ,
`name` ,
`desc` ,
`syntax`
)
VALUES (
NULL , '!dial', 'Teleports player to private registerd gateway.', '!dial GATEWAY 
Use !help !gateway to get instructions on how to register new gateways.'
);

INSERT INTO `commands` (
`id` ,
`name` ,
`desc` ,
`syntax`
)
VALUES (
NULL , '!travel', 'Teleports player to public registerd gateway.', '!travel GATEWAY 
Use !help !gateway to get instructions on how to register new gateways.'
);
