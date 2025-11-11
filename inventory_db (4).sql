-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3306
-- Generation Time: Nov 07, 2025 at 09:58 PM
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
-- Table structure for table `activity_log`
--

DROP TABLE IF EXISTS `activity_log`;
CREATE TABLE IF NOT EXISTS `activity_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int DEFAULT NULL,
  `username` varchar(50) DEFAULT NULL,
  `action` varchar(100) DEFAULT NULL,
  `product_name` varchar(100) DEFAULT NULL,
  `timestamp` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`)
) ENGINE=MyISAM AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `activity_log`
--

INSERT INTO `activity_log` (`id`, `user_id`, `username`, `action`, `product_name`, `timestamp`) VALUES
(1, 1, 'qwerty213', 'Deleted product', 'car', '2025-11-08 04:44:06'),
(2, 1, 'qwerty213', 'Added new product', 'Sketchers', '2025-11-08 05:35:00');

-- --------------------------------------------------------

--
-- Table structure for table `login_activity`
--

DROP TABLE IF EXISTS `login_activity`;
CREATE TABLE IF NOT EXISTS `login_activity` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int DEFAULT NULL,
  `username` varchar(50) DEFAULT NULL,
  `action` varchar(50) DEFAULT NULL,
  `timestamp` datetime DEFAULT CURRENT_TIMESTAMP,
  `ip_address` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`)
) ENGINE=MyISAM AUTO_INCREMENT=41 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `login_activity`
--

INSERT INTO `login_activity` (`id`, `user_id`, `username`, `action`, `timestamp`, `ip_address`) VALUES
(1, 1, 'qwerty213', 'Login', '2025-11-07 20:41:35', '127.0.0.1'),
(2, 1, 'qwerty213', 'Logout', '2025-11-07 20:44:14', '127.0.0.1'),
(3, 5, 'piercevaldez213', 'Login', '2025-11-07 20:44:18', '127.0.0.1'),
(4, 5, 'piercevaldez213', 'Logout', '2025-11-07 20:45:12', '127.0.0.1'),
(5, 1, 'qwerty213', 'Login', '2025-11-07 20:45:17', '127.0.0.1'),
(6, 5, 'piercevaldez213', 'Login', '2025-11-07 20:59:32', '127.0.0.1'),
(7, 5, 'piercevaldez213', 'Logout', '2025-11-07 21:00:07', '127.0.0.1'),
(8, 1, 'qwerty213', 'Login', '2025-11-07 21:00:14', '127.0.0.1'),
(9, 1, 'qwerty213', 'Logout', '2025-11-07 21:06:23', '127.0.0.1'),
(10, 5, 'piercevaldez213', 'Login', '2025-11-07 21:06:28', '127.0.0.1'),
(11, 1, 'qwerty213', 'Login', '2025-11-07 21:12:55', '127.0.0.1'),
(12, 5, 'piercevaldez213', 'Login', '2025-11-07 21:20:15', '127.0.0.1'),
(13, 5, 'piercevaldez213', 'Logout', '2025-11-07 21:20:19', '127.0.0.1'),
(14, 1, 'qwerty213', 'Login', '2025-11-07 21:20:24', '127.0.0.1'),
(15, 1, 'qwerty213', 'Logout', '2025-11-07 21:20:45', '127.0.0.1'),
(16, 5, 'piercevaldez213', 'Login', '2025-11-07 21:20:50', '127.0.0.1'),
(17, 5, 'piercevaldez213', 'Logout', '2025-11-07 21:20:55', '127.0.0.1'),
(18, 1, 'qwerty213', 'Login', '2025-11-07 21:21:05', '127.0.0.1'),
(19, 1, 'qwerty213', 'Login', '2025-11-07 21:22:08', '127.0.0.1'),
(20, 1, 'qwerty213', 'Login', '2025-11-07 21:23:03', '127.0.0.1'),
(21, 1, 'qwerty213', 'Login', '2025-11-07 21:24:15', '127.0.0.1'),
(22, 1, 'qwerty213', 'Logout', '2025-11-07 21:25:51', '127.0.0.1'),
(23, 1, 'qwerty213', 'Login', '2025-11-07 21:25:58', '127.0.0.1'),
(24, 1, 'qwerty213', 'Logout', '2025-11-07 21:31:36', '127.0.0.1'),
(25, 1, 'qwerty213', 'Login', '2025-11-07 21:31:42', '127.0.0.1'),
(26, 1, 'qwerty213', 'Logout', '2025-11-07 21:32:08', '127.0.0.1'),
(27, 5, 'piercevaldez213', 'Login', '2025-11-07 21:32:14', '127.0.0.1'),
(28, 5, 'piercevaldez213', 'Logout', '2025-11-07 21:32:15', '127.0.0.1'),
(29, 1, 'qwerty213', 'Login', '2025-11-07 21:32:20', '127.0.0.1'),
(30, 1, 'qwerty213', 'Login', '2025-11-07 21:49:47', '127.0.0.1'),
(31, 1, 'qwerty213', 'Logout', '2025-11-07 21:49:58', '127.0.0.1'),
(32, 5, 'piercevaldez213', 'Login', '2025-11-07 21:50:03', '127.0.0.1'),
(33, 5, 'piercevaldez213', 'Logout', '2025-11-07 21:50:05', '127.0.0.1'),
(34, 1, 'qwerty213', 'Login', '2025-11-07 21:50:09', '127.0.0.1'),
(35, 1, 'qwerty213', 'Logout', '2025-11-07 21:52:26', '127.0.0.1'),
(36, 5, 'piercevaldez213', 'Login', '2025-11-07 21:52:33', '127.0.0.1'),
(37, 5, 'piercevaldez213', 'Logout', '2025-11-07 21:52:46', '127.0.0.1'),
(38, 1, 'qwerty213', 'Login', '2025-11-07 21:52:50', '127.0.0.1'),
(39, 1, 'qwerty213', 'Logout', '2025-11-07 21:55:30', '127.0.0.1'),
(40, 5, 'piercevaldez213', 'Login', '2025-11-07 21:55:34', '127.0.0.1');

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
  `size` varchar(20) DEFAULT NULL,
  `size_unit` varchar(10) DEFAULT NULL,
  `brand` varchar(50) DEFAULT NULL,
  `category` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=29 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `product`
--

INSERT INTO `product` (`id`, `name`, `stock`, `price`, `image`, `date_added`, `time_added`, `size`, `size_unit`, `brand`, `category`) VALUES
(21, 'Wmns Cortez', 10, 4171.98, 'nike.jpg', '2025-11-05', '07:02:06', '10', 'US', 'Nike', 'Sneakers'),
(27, 'Bread', 21, 123, NULL, '2025-11-05', '08:24:32', '100', 'EU', 'dike', 'Sneakers'),
(22, 'Vans Men\'s Old Skool', 12312, 12312, 'vans.jpg', '2025-11-05', '07:04:07', '10', 'EU', 'Vans', 'Sneakers'),
(23, 'Hotdog', 12312, 12312, NULL, '2025-11-05', '07:04:22', NULL, NULL, NULL, NULL),
(24, 'Butter', 13, 1311, NULL, '2025-11-05', '07:05:07', NULL, NULL, NULL, NULL),
(25, 'tocino', 100, 1000, NULL, '2025-11-05', '07:05:56', '10', 'UK', 'Jordan', 'Sneakers'),
(28, 'Sketchers', 6, 1234, NULL, '2025-11-08', '05:35:00', '10', 'UK', 'sketchers', 'Sneakers');

-- --------------------------------------------------------

--
-- Table structure for table `stock_alert`
--

DROP TABLE IF EXISTS `stock_alert`;
CREATE TABLE IF NOT EXISTS `stock_alert` (
  `id` int NOT NULL AUTO_INCREMENT,
  `product_id` int DEFAULT NULL,
  `product_name` varchar(100) DEFAULT NULL,
  `stock` int DEFAULT NULL,
  `alert_type` varchar(50) DEFAULT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `product_id` (`product_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

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
) ENGINE=MyISAM AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `user`
--

INSERT INTO `user` (`id`, `username`, `password`, `role`) VALUES
(1, 'qwerty213', '$2b$12$Ilz1CdONSA1iinBbeshw..i3yQ4mJuEAzPhdYyMbaprA2FsmXhfgi', 'admin'),
(5, 'piercevaldez213', '$2b$12$yU3zI/OtCYOjCXoIKQHdbupVn7Ck77mX/5x5sZliGNIewRtgkwC/G', 'staff'),
(3, 'qwerty', '$2b$12$8bTe8RELI/ysh6mKFZDhrugW17GCX4BApxzc.uPJGAhJLnqy14wJu', 'staff'),
(6, 'harvey213', '$2b$12$OqjzaDJeaV9NmE0d.xKE6Ol.X4gtfHw2V9ASRzBGW52UdQNCtHSV2', 'staff');
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
