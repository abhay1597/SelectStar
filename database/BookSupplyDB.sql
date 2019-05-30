-- phpMyAdmin SQL Dump
-- version 3.3.9
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Mar 27, 2019 at 05:04 AM
-- Server version: 5.5.8
-- PHP Version: 5.3.5

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `books supply`
--

-- --------------------------------------------------------

--
-- Table structure for table `author`
--

CREATE TABLE IF NOT EXISTS `author` (
  `authorid` varchar(5) NOT NULL,
  `name` varchar(15) NOT NULL,
  `age` int(2) NOT NULL,
  `language` varchar(10) NOT NULL,
  PRIMARY KEY (`authorid`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `author`
--


-- --------------------------------------------------------

--
-- Table structure for table `book`
--

CREATE TABLE IF NOT EXISTS `book` (
  `bookid` varchar(5) NOT NULL,
  `name` varchar(15) NOT NULL,
  `year` int(4) NOT NULL,
  `noOfPages` int(4) NOT NULL,
  `authorid` varchar(5) NOT NULL,
  `price` int(5) NOT NULL,
  PRIMARY KEY (`bookid`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `book`
--


-- --------------------------------------------------------

--
-- Table structure for table `printingpress`
--

CREATE TABLE IF NOT EXISTS `printingpress` (
  `bookid` varchar(5) NOT NULL,
  `noOfCopies` int(5) NOT NULL,
  `warehouseLocation` varchar(15) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `printingpress`
--


-- --------------------------------------------------------

--
-- Table structure for table `store`
--

CREATE TABLE IF NOT EXISTS `store` (
  `location` varchar(15) NOT NULL,
  `bookid` varchar(5) NOT NULL,
  `shelfNo` int(4) NOT NULL,
  UNIQUE KEY `location` (`location`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `store`
--

ALTER TABLE `book`
  ADD CONSTRAINT `book_fk` FOREIGN KEY (`authorid`) REFERENCES `author` (`authorid`);
  
ALTER TABLE `store`
  ADD CONSTRAINT `store_fk` FOREIGN KEY (`bookid`) REFERENCES `book` (`bookid`);
  
ALTER TABLE `printingpress`
  ADD CONSTRAINT `pp_fk` FOREIGN KEY (`bookid`) REFERENCES `book` (`bookid`);
