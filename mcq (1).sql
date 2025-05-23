-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3306
-- Generation Time: Mar 14, 2024 at 04:28 PM
-- Server version: 8.2.0
-- PHP Version: 8.2.13

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `mcq`
--

-- --------------------------------------------------------

--
-- Table structure for table `answer`
--

DROP TABLE IF EXISTS `answer`;
CREATE TABLE IF NOT EXISTS `answer` (
  `uid` int NOT NULL,
  `qnid` int NOT NULL,
  `ans` text NOT NULL,
  PRIMARY KEY (`uid`,`qnid`),
  KEY `qnid` (`qnid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `question`
--

DROP TABLE IF EXISTS `question`;
CREATE TABLE IF NOT EXISTS `question` (
  `QuestionID` int NOT NULL AUTO_INCREMENT,
  `QuestionTitle` varchar(500) NOT NULL,
  `OptionA` varchar(200) DEFAULT NULL,
  `OptionB` varchar(200) DEFAULT NULL,
  `OptionC` varchar(200) DEFAULT NULL,
  `OptionD` varchar(200) DEFAULT NULL,
  `Answer` varchar(200) NOT NULL,
  `QuizID` int NOT NULL,
  PRIMARY KEY (`QuestionID`),
  KEY `QuizID` (`QuizID`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `question`
--

INSERT INTO `question` (`QuestionID`, `QuestionTitle`, `OptionA`, `OptionB`, `OptionC`, `OptionD`, `Answer`, `QuizID`) VALUES
(2, 'enter your name ', 'veeru', NULL, 'punneth', 'dsfsdf', 'option3', 0),
(3, 'sdf', 'sdfsd', 'sdfsdf', 'sdfsd', 'sdfsdf', 'option2', 0),
(6, 'Python variables are', 'variable type', NULL, 'neutral', 'good', 'A', 10);

-- --------------------------------------------------------

--
-- Table structure for table `quiz`
--

DROP TABLE IF EXISTS `quiz`;
CREATE TABLE IF NOT EXISTS `quiz` (
  `QuizID` int NOT NULL AUTO_INCREMENT,
  `QuizTitle` varchar(100) NOT NULL,
  PRIMARY KEY (`QuizID`)
) ENGINE=MyISAM AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `quiz`
--

INSERT INTO `quiz` (`QuizID`, `QuizTitle`) VALUES
(1, 'Java'),
(2, ''),
(3, 'hello'),
(4, 'hellofsd'),
(5, 'sdsad'),
(6, 'sdsad'),
(10, 'Python');

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
CREATE TABLE IF NOT EXISTS `user` (
  `UserID` int NOT NULL AUTO_INCREMENT,
  `Username` varchar(30) NOT NULL,
  `Email` varchar(40) NOT NULL,
  `UPassword` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  PRIMARY KEY (`UserID`),
  UNIQUE KEY `Email` (`Email`)
) ENGINE=InnoDB AUTO_INCREMENT=37 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `user`
--

INSERT INTO `user` (`UserID`, `Username`, `Email`, `UPassword`) VALUES
(36, 'chetan', 'ckr@gmail.com', '3047e89fd6c75ff535487f279f08435c');

--
-- Constraints for dumped tables
--

--
-- Constraints for table `answer`
--
ALTER TABLE `answer`
  ADD CONSTRAINT `answer_ibfk_1` FOREIGN KEY (`uid`) REFERENCES `user` (`UserID`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  ADD CONSTRAINT `answer_ibfk_2` FOREIGN KEY (`qnid`) REFERENCES `question` (`QuestionID`) ON DELETE RESTRICT ON UPDATE RESTRICT;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
