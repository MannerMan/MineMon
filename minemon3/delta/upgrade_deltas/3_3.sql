-- Generation Time: Nov 04, 2012 at 09:20 PM


SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";

--
-- Run this in MM database
--

-- --------------------------------------------------------

--
-- Table structure for table `enabled_commands`
--

CREATE TABLE IF NOT EXISTS `enabled_commands` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `world_id` int(11) NOT NULL,
  `command_id` int(11) NOT NULL,
  `enabled` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `world_id` (`world_id`),
  KEY `command_id` (`command_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;


ALTER TABLE `enabled_commands` ADD FOREIGN KEY ( `world_id` ) REFERENCES `worlds` (
`id`
) ON DELETE NO ACTION ON UPDATE NO ACTION ;

ALTER TABLE `enabled_commands` ADD FOREIGN KEY ( `command_id` ) REFERENCES `commands` (
`id`
) ON DELETE NO ACTION ON UPDATE NO ACTION ;
