-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3306
-- Generation Time: Nov 03, 2025 at 09:06 PM
-- Server version: 9.1.0
-- PHP Version: 8.3.14

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `inventory_db`
--

-- --------------------------------------------------------

--
-- Table structure for table `product`
--

DROP TABLE IF EXISTS `product`;
CREATE TABLE IF NOT EXISTS `product` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `stock` int DEFAULT NULL,
  `price` float NOT NULL,
  `image` varchar(255) DEFAULT NULL,
  `date_added` date DEFAULT NULL,
  `time_added` time DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=19 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `product`
--

INSERT INTO `product` (`id`, `name`, `stock`, `price`, `image`, `date_added`, `time_added`) VALUES
(17, 'qwe', 45, 123, NULL, '2025-11-04', '04:55:46'),
(8, 'Hotdog', 100, 500, NULL, NULL, NULL),
(16, 'Hotdog', 100, 500, NULL, '2025-11-04', '04:55:34'),
(11, 'Butter', 20, 100, NULL, NULL, NULL),
(13, 'Butter', 20, 100, NULL, NULL, NULL),
(14, 'Honey', 20, 3000, NULL, NULL, NULL),
(15, 'nike', 50, 1000, NULL, '2025-11-04', '04:45:33'),
(18, 'bike', 213, 200, 'WIN_20250612_18_39_54_Pro.jpg', '2025-11-04', '05:03:03');

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
CREATE TABLE IF NOT EXISTS `user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(50) NOT NULL,
  `password` varchar(255) NOT NULL,
  `role` varchar(10) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=MyISAM AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `user`
--

INSERT INTO `user` (`id`, `username`, `password`, `role`) VALUES
(1, 'qwerty213', '$2b$12$Ilz1CdONSA1iinBbeshw..i3yQ4mJuEAzPhdYyMbaprA2FsmXhfgi', 'admin'),
(5, 'piercevaldez213', '$2b$12$yU3zI/OtCYOjCXoIKQHdbupVn7Ck77mX/5x5sZliGNIewRtgkwC/G', 'staff'),
(3, 'qwerty', '$2b$12$8bTe8RELI/ysh6mKFZDhrugW17GCX4BApxzc.uPJGAhJLnqy14wJu', 'staff'),
(4, 'harvey213', '$2b$12$uKwhGYRzhhRIBcDtEsZ0cOxO9JfD5KjxFGaQewZPeIoZoI9SgoDzq', 'staff');
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
