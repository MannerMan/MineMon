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
example: !gateway public centrum 100 100 100
example: !gateway delete public centrum
example: !gateway list private
Tip: Press F3 to see your current coordinates'
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
NULL , '!warp', 'Teleports player to public registerd gateway.', '!warp GATEWAY 
Use !help !gateway to get instructions on how to register new gateways.'
);

UPDATE version v SET v.current = 0 WHERE v.current = 1;

INSERT INTO `version` (`id`, `version`, `current`, `changes`) VALUES (NULL, '3.4', '1', 'Coordination-based teleportation system added! 
You can register private coordinates unique to you, or public, for anyone to use.
!gateway - Used for registration, listing and deletion of coordinates 
!dial - Used for teleportation to private coordinates
!warp - Used for teleportation to public coordinates');
