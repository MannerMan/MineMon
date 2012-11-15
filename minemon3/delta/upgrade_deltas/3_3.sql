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
  `op` tinyint(1) NOT NULL,
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

ALTER TABLE `commands` DROP `enabled`;
ALTER TABLE `commands` DROP `op`;

ALTER TABLE `commands` ADD `desc` TEXT NOT NULL 
ALTER TABLE `commands` ADD `syntax` TEXT NOT NULL 

UPDATE `commands` SET `desc` = 'Prints random Charlie Sheen quote',
`syntax` = '!sheen' WHERE `commands`.`id` =1;
UPDATE `commands` SET `desc` = 'Give player creative mode.',
`syntax` = '!hax' WHERE `commands`.`id` =2;
UPDATE `commands` SET `desc` = 'Give player survival mode.',
`syntax` = '!unhax' WHERE `commands`.`id` =3;
UPDATE `commands` SET `desc` = 'Instantly turns the time into day, "time 10"',
`syntax` = '!day' WHERE `commands`.`id` =4;
UPDATE `commands` SET `desc` = 'Instantly turns the time into night, "time 14000"',
`syntax` = '!night' WHERE `commands`.`id` =5;
UPDATE `commands` SET `desc` = 'Teleports player to TARGET, where TARGET is other players nick.',
`syntax` = '!tp TARGET 
Example: !tp chucknorris 
Teleports player to the player with the nick chucknorris' WHERE `commands`.`id` =6;
UPDATE `commands` SET `desc` = 'Teleports TARGET to player, where TARGET is other players nick.',
`syntax` = '!pull TARGET
Example: !pull mange 
Teleports "mange" to player' WHERE `commands`.`id` =7;
UPDATE `commands` SET `desc` = 'Prints link to the nightly updated map',
`syntax` = '!map' WHERE `commands`.`id` =8;
UPDATE `commands` SET `desc` = 'Prints help and syntax for specific commands',
`syntax` = '!help !COMMAND' WHERE `commands`.`id` =9;
UPDATE `commands` SET `desc` = 'Player rolls 1-100, really high rolls can be rewarding!',
`syntax` = '!roll' WHERE `commands`.`id` =10;
UPDATE `commands` SET `desc` = 'Toggle rain/snow',
`syntax` = '!rain' WHERE `commands`.`id` =11;
UPDATE `commands` SET `desc` = 'Give player lots of XP',
`syntax` = '!xp' WHERE `commands`.`id` =12;
UPDATE `commands` SET `desc` = 'Give player a starter kit, mining-pick, axe, etc.',
`syntax` = '!kit' WHERE `commands`.`id` =13;
UPDATE `commands` SET `desc` = 'Give player full leather-armour and a wooden sword',
`syntax` = '!leatherset' WHERE `commands`.`id` =14;
UPDATE `commands` SET `desc` = 'Give player full diamond armour and sword.',
`syntax` = '!diamondset' WHERE `commands`.`id` =15;
UPDATE `commands` SET `desc` = 'Give player a bow and three stacks of arrows',
`syntax` = '!bow' WHERE `commands`.`id` =16;
UPDATE `commands` SET `desc` = 'Give player five minecarts',
`syntax` = '!train' WHERE `commands`.`id` =17;
UPDATE `commands` SET `desc` = 'Give player five beds',
`syntax` = '!sleep' WHERE `commands`.`id` =18;
UPDATE `commands` SET `desc` = 'Give player optimal railroad building set',
`syntax` = '!rail' WHERE `commands`.`id` =19;
UPDATE `commands` SET `desc` = 'Give player five grilled porks',
`syntax` = '!food' WHERE `commands`.`id` =20;
UPDATE `commands` SET `desc` = 'Give player a stack of specified item',
`syntax` = '!item NUMBER
Example: !item 12
Gives player a stack of item 12' WHERE `commands`.`id` =21
UPDATE `commands` SET `desc` = 'Restarts the server, takes about 15 seconds.',
`syntax` = '!restart' WHERE `commands`.`id` =22;
UPDATE `commands` SET `desc` = 'Download latest version of minecraft server and compares with the current installed version.',
`syntax` = '!update
If versions missmatch a auto-update will commence.' WHERE `commands`.`id` =23;
UPDATE `commands` SET `desc` = 'Send a message to the administrator about issues.',
`syntax` = '!report WRITE_YOUR_ISSUE_HERE' WHERE `commands`.`id` =24;
UPDATE `commands` SET `desc` = 'Activates/Deactivates monster.',
`syntax` = '!monsters 
Please note that it could take a day-cycle before the monsters appear/disappear' WHERE `commands`.`id` =25;
UPDATE `commands` SET `desc` = 'Give TARGET creative-mode until next login.',
`syntax` = '!temphax TARGET 
Upon next login TARGET will have ten seconds to get to safety before creative is removed.' WHERE `commands`.`id` =26;
UPDATE `commands` SET `desc` = 'Lists your current playtime, updated every 5 minutes',
`syntax` = '!played' WHERE `commands`.`id` =27;
UPDATE `commands` SET `desc` = 'Prints version information and changes.',
`syntax` = '!version' WHERE `commands`.`id` =28;
UPDATE `commands` SET `desc` = 'Give player Adventure mode',
`syntax` = '!adv' WHERE `commands`.`id` =29;
UPDATE `commands` SET `desc` = 'Restarts server and change world',
`syntax` = '!world WORLDNAME
Use !world without parameters to list available worlds.' WHERE `commands`.`id` =30;

CREATE TABLE IF NOT EXISTS `version` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `version` varchar(15) NOT NULL,
  `current` tinyint(1) NOT NULL,
  `changes` text NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

