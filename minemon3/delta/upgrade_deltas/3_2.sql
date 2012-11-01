-- Generation Time: Nov 01, 2012 at 09:20 PM

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";

--
-- Run this in your MM database to add any mysql-changes since last MM version
--

-- --------------------------------------------------------

--
-- Table structure for table `worlds`
--

CREATE TABLE IF NOT EXISTS `worlds` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `world_name` varchar(20) NOT NULL,
  `active` tinyint(1) NOT NULL,
  `path` varchar(50) NOT NULL,
  `used` int(11) NOT NULL,
  `timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=0 ;

-- Insert !world command

INSERT INTO `commands` (`id`, `name`, `enabled`, `op`) VALUES
(30, '!world', 1, 1);
