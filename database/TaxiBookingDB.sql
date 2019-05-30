-- phpMyAdmin SQL Dump
-- version 3.3.9
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Mar 26, 2019 at 06:18 AM
-- Server version: 5.5.8
-- PHP Version: 5.3.5

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `Taxi Booking Service`
--

-- --------------------------------------------------------

--
-- Table structure for table `cab`
--

CREATE TABLE IF NOT EXISTS `cab` (
  `regNo` varchar(4) NOT NULL,
  `capacity` int(2) NOT NULL,
  `company` varchar(15) NOT NULL,
  `driverid` int(4) NOT NULL,
  `insuranceNo` varchar(15) NOT NULL,
  PRIMARY KEY (`regNo`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `cab`
--


-- --------------------------------------------------------

--
-- Table structure for table `driver`
--

CREATE TABLE IF NOT EXISTS `driver` (
  `driverid` int(4) NOT NULL,
  `name` varchar(15) NOT NULL,
  `age` int(2) NOT NULL,
  `regNo` varchar(4) NOT NULL,
  `licenceNo` varchar(10) NOT NULL,
  PRIMARY KEY (`driverid`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `driver`
--


-- --------------------------------------------------------

--
-- Table structure for table `passenger`
--

CREATE TABLE IF NOT EXISTS `passenger` (
  `passengerid` int(4) NOT NULL,
  `name` varchar(15) NOT NULL,
  `contact` int(10) NOT NULL,
  `source` varchar(10) NOT NULL,
  `destination` varchar(10) NOT NULL,
  `driverid` int(4) NOT NULL,
  PRIMARY KEY (`passengerid`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `passenger`
--


-- --------------------------------------------------------

--
-- Table structure for table `route`
--

CREATE TABLE IF NOT EXISTS `route` (
  `routeid` int(4) NOT NULL,
  `passengerid` int(4) NOT NULL,
  `distance` int(4) NOT NULL,
  `fare` int(5) NOT NULL,
  PRIMARY KEY (`routeid`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `route`
--


-- --------------------------------------------------------

--
-- Table structure for table `transaction`
--

CREATE TABLE IF NOT EXISTS `transaction` (
  `transactionid` varchar(4) NOT NULL,
  `routeid` int(4) NOT NULL,
  `cardDetails` int(15) NULL,
  `eWalletName` varchar(10) NULL,
  PRIMARY KEY (`transactionid`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `transaction`
--
ALTER TABLE `cab`
  ADD CONSTRAINT `cab_fk` FOREIGN KEY (`driverid`) REFERENCES `driver` (`driverid`);


ALTER TABLE `driver`
  ADD CONSTRAINT `driver_fk` FOREIGN KEY (`regNo`) REFERENCES `cab` (`regNo`);
  
ALTER TABLE `passenger`
  ADD CONSTRAINT `pass_fk` FOREIGN KEY (`driverid`) REFERENCES `driver` (`driverid`);
  
ALTER TABLE `route`
  ADD CONSTRAINT `route_fk` FOREIGN KEY (`passengerid`) REFERENCES `passenger` (`passengerid`);
  
ALTER TABLE `transaction`
  ADD CONSTRAINT `tran_fk` FOREIGN KEY (`routeid`) REFERENCES `route` (`routeid`);




