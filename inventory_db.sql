-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3306
-- Generation Time: Nov 19, 2025 at 06:18 AM
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
) ENGINE=MyISAM AUTO_INCREMENT=55 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `activity_log`
--

INSERT INTO `activity_log` (`id`, `user_id`, `username`, `action`, `product_name`, `timestamp`) VALUES
(1, 1, 'qwerty213', 'Deleted product', 'car', '2025-11-08 04:44:06'),
(2, 1, 'qwerty213', 'Added new product', 'Sketchers', '2025-11-08 05:35:00'),
(3, 5, 'piercevaldez213', 'Staff added new product', 'Sketchers2', '2025-11-08 18:05:14'),
(4, 5, 'piercevaldez213', 'Staff added new product', 'Sketchers3', '2025-11-08 20:12:22'),
(5, 3, 'qwerty', 'Staff edited product details', 'Wmns Cortez', '2025-11-08 21:07:26'),
(6, 3, 'qwerty', 'Deducted 1 stock units', 'Wmns Cortez', '2025-11-08 21:07:38'),
(7, 1, 'qwerty213', 'Added 1 units', 'Wmns Cortez', '2025-11-09 22:31:14'),
(8, 6, 'harvey213', 'Deducted 1 units', 'Wmns Cortez', '2025-11-09 22:31:45'),
(9, 6, 'harvey213', 'Added 1 units', 'Wmns Cortez', '2025-11-09 22:31:49'),
(10, 1, 'qwerty213', 'Admin added product', 'shoe', '2025-11-09 22:42:11'),
(11, 1, 'qwerty213', 'Admin edited product', 'shoe', '2025-11-09 22:43:38'),
(12, 6, 'harvey213', 'Staff edited product', 'shoe', '2025-11-09 23:08:58'),
(13, 1, 'qwerty213', 'Admin edited product', 'Bread', '2025-11-09 23:20:59'),
(14, 6, 'harvey213', 'Deducted 3 units', 'Sketchers', '2025-11-09 23:29:50'),
(15, 1, 'qwerty213', 'Added 10 units', 'Sketchers', '2025-11-09 23:30:36'),
(16, 1, 'qwerty213', 'Admin edited product', 'shoe', '2025-11-09 23:36:32'),
(17, 1, 'qwerty213', 'Deducted 1 units', 'Wmns Cortez', '2025-11-11 18:14:07'),
(18, 1, 'qwerty213', 'Admin edited product', 'Hotdog', '2025-11-11 18:14:28'),
(19, 3, 'qwerty', 'Staff edited product', 'Wmns Cortez', '2025-11-11 18:15:36'),
(20, 1, 'qwerty213', 'Admin added product', 'Wmns Cortez', '2025-11-11 18:52:40'),
(21, 1, 'qwerty213', 'Admin edited product', 'Cortez', '2025-11-11 18:53:07'),
(22, 1, 'qwerty213', 'Admin edited product', 'Bread', '2025-11-11 18:53:20'),
(23, 1, 'qwerty213', 'Admin edited product', 'Bread', '2025-11-11 18:53:27'),
(24, 1, 'qwerty213', 'Admin edited product', 'Wmns Cortez', '2025-11-11 18:58:44'),
(25, 1, 'qwerty213', 'Admin added product', 'sandal', '2025-11-11 19:47:34'),
(26, 1, 'qwerty213', 'Admin edited product', 'sandal', '2025-11-11 19:48:01'),
(27, 1, 'qwerty213', 'Admin edited product', 'sandal', '2025-11-11 19:50:15'),
(28, 1, 'qwerty213', 'Admin edited product', 'shoe', '2025-11-11 19:50:52'),
(29, 6, 'harvey213', 'Staff added product', 'shoeshoe', '2025-11-11 20:35:26'),
(30, 1, 'qwerty213', 'Deducted 1 units', 'Wmns Cortez', '2025-11-11 20:41:08'),
(31, 1, 'qwerty213', 'Added 1 units', 'Wmns Cortez', '2025-11-11 20:41:28'),
(32, 1, 'qwerty213', 'Admin edited product', 'Wmns Cortez', '2025-11-11 20:41:38'),
(33, 1, 'qwerty213', 'Admin added product', 'reebook2', '2025-11-15 22:01:51'),
(34, 1, 'qwerty213', 'Admin edited product', 'sandal', '2025-11-15 22:03:37'),
(35, 1, 'qwerty213', 'Added 1 units', 'reebook2', '2025-11-15 22:04:03'),
(36, 1, 'qwerty213', 'Admin edited product', 'reebook2', '2025-11-15 22:04:25'),
(37, 3, 'qwerty', 'Deducted 1 units', 'reebook2', '2025-11-15 22:05:15'),
(38, 1, 'qwerty213', 'Admin registered new staff: harveyvaldez', 'harveyvaldez (Inventory)', '2025-11-15 22:46:32'),
(39, 3, 'qwerty', 'Staff edited product', 'Hotdog', '2025-11-17 01:42:41'),
(40, 3, 'qwerty', 'Staff edited product', 'Vans Men\'s Old Skool', '2025-11-17 01:43:31'),
(41, 3, 'qwerty', 'Staff edited product', 'shoe', '2025-11-17 01:43:44'),
(42, 3, 'qwerty', 'Staff edited product', 'tocino', '2025-11-17 01:44:10'),
(43, 3, 'qwerty', 'Deducted 50 units', 'Wmns Cortez', '2025-11-17 01:44:32'),
(44, 3, 'qwerty', 'Staff edited product', 'Hotdog', '2025-11-17 01:44:56'),
(45, 3, 'qwerty', 'Deducted 1000 units', 'Hotdog', '2025-11-17 01:45:06'),
(46, 3, 'qwerty', 'Deducted 8000 units', 'Hotdog', '2025-11-17 01:45:21'),
(47, 3, 'qwerty', 'Deducted 800 units', 'Hotdog', '2025-11-17 01:45:33'),
(48, 3, 'qwerty', 'Deducted 100 units', 'Hotdog', '2025-11-17 02:10:23'),
(49, 3, 'qwerty', 'Deducted 50 units', 'Hotdog', '2025-11-17 02:10:33'),
(50, 1, 'qwerty213', 'Admin edited product: stock adjustment', 'Wmns Cortez', '2025-11-17 04:20:17'),
(51, 1, 'qwerty213', 'Added 1 units', 'Wmns Cortez', '2025-11-17 05:32:19'),
(52, 1, 'qwerty213', 'Added 1 units', 'Wmns Cortez', '2025-11-17 10:59:43'),
(53, 1, 'qwerty213', 'Admin edited product', 'Wmns Cortez', '2025-11-17 11:00:08'),
(54, 1, 'qwerty213', 'Admin edited product', 'Wmns Cortez', '2025-11-17 11:00:29');

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
) ENGINE=MyISAM AUTO_INCREMENT=187 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

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
(40, 5, 'piercevaldez213', 'Login', '2025-11-07 21:55:34', '127.0.0.1'),
(41, 1, 'qwerty213', 'Login', '2025-11-08 10:04:31', '127.0.0.1'),
(42, 1, 'qwerty213', 'Logout', '2025-11-08 10:04:38', '127.0.0.1'),
(43, 5, 'piercevaldez213', 'Login', '2025-11-08 10:04:45', '127.0.0.1'),
(44, 5, 'piercevaldez213', 'Logout', '2025-11-08 10:05:18', '127.0.0.1'),
(45, 1, 'qwerty213', 'Login', '2025-11-08 10:05:23', '127.0.0.1'),
(46, 1, 'qwerty213', 'Logout', '2025-11-08 10:06:03', '127.0.0.1'),
(47, 5, 'piercevaldez213', 'Login', '2025-11-08 10:06:07', '127.0.0.1'),
(48, 1, 'qwerty213', 'Login', '2025-11-08 11:57:43', '127.0.0.1'),
(49, 1, 'qwerty213', 'Logout', '2025-11-08 11:58:08', '127.0.0.1'),
(50, 5, 'piercevaldez213', 'Login', '2025-11-08 11:58:26', '127.0.0.1'),
(51, 5, 'piercevaldez213', 'Logout', '2025-11-08 12:07:11', '127.0.0.1'),
(52, 1, 'qwerty213', 'Login', '2025-11-08 12:07:14', '127.0.0.1'),
(53, 1, 'qwerty213', 'Login', '2025-11-08 12:11:58', '127.0.0.1'),
(54, 1, 'qwerty213', 'Logout', '2025-11-08 12:12:03', '127.0.0.1'),
(55, 5, 'piercevaldez213', 'Login', '2025-11-08 12:12:09', '127.0.0.1'),
(56, 5, 'piercevaldez213', 'Logout', '2025-11-08 12:17:33', '127.0.0.1'),
(57, 5, 'piercevaldez213', 'Login', '2025-11-08 12:17:49', '127.0.0.1'),
(58, 5, 'piercevaldez213', 'Login', '2025-11-08 12:22:40', '127.0.0.1'),
(59, 5, 'piercevaldez213', 'Logout', '2025-11-08 12:31:23', '127.0.0.1'),
(60, 1, 'qwerty213', 'Login', '2025-11-08 12:31:30', '127.0.0.1'),
(61, 1, 'qwerty213', 'Logout', '2025-11-08 12:38:44', '127.0.0.1'),
(62, 5, 'piercevaldez213', 'Login', '2025-11-08 12:38:48', '127.0.0.1'),
(63, 5, 'piercevaldez213', 'Logout', '2025-11-08 12:38:55', '127.0.0.1'),
(64, 3, 'qwerty', 'Login', '2025-11-08 12:39:00', '127.0.0.1'),
(65, 3, 'qwerty', 'Logout', '2025-11-08 12:46:05', '127.0.0.1'),
(66, 1, 'qwerty213', 'Login', '2025-11-08 12:46:16', '127.0.0.1'),
(67, 1, 'qwerty213', 'Logout', '2025-11-08 12:50:55', '127.0.0.1'),
(68, 5, 'piercevaldez213', 'Login', '2025-11-08 12:51:00', '127.0.0.1'),
(69, 5, 'piercevaldez213', 'Logout', '2025-11-08 12:51:57', '127.0.0.1'),
(70, 1, 'qwerty213', 'Login', '2025-11-08 12:52:07', '127.0.0.1'),
(71, 1, 'qwerty213', 'Logout', '2025-11-08 12:55:49', '127.0.0.1'),
(72, 3, 'qwerty', 'Login', '2025-11-08 12:56:13', '127.0.0.1'),
(73, 1, 'qwerty213', 'Login', '2025-11-09 21:33:14', '127.0.0.1'),
(74, 1, 'qwerty213', 'Login', '2025-11-09 21:39:11', '127.0.0.1'),
(75, 1, 'qwerty213', 'Logout', '2025-11-09 21:41:53', '127.0.0.1'),
(76, 5, 'piercevaldez213', 'Login', '2025-11-09 21:42:16', '127.0.0.1'),
(77, 5, 'piercevaldez213', 'Logout', '2025-11-09 21:45:44', '127.0.0.1'),
(78, 1, 'qwerty213', 'Login', '2025-11-09 21:45:54', '127.0.0.1'),
(79, 1, 'qwerty213', 'Login', '2025-11-09 22:17:34', '127.0.0.1'),
(80, 1, 'qwerty213', 'Logout', '2025-11-09 22:19:33', '127.0.0.1'),
(81, 8, 'qwerty21332', 'Login', '2025-11-09 22:19:45', '127.0.0.1'),
(82, 1, 'qwerty213', 'Login', '2025-11-09 22:25:00', '127.0.0.1'),
(83, 1, 'qwerty213', 'Login', '2025-11-09 22:29:20', '127.0.0.1'),
(84, 1, 'qwerty213', 'Login', '2025-11-09 22:30:54', '127.0.0.1'),
(85, 1, 'qwerty213', 'Logout', '2025-11-09 22:31:27', '127.0.0.1'),
(86, 6, 'harvey213', 'Login', '2025-11-09 22:31:38', '127.0.0.1'),
(87, 6, 'harvey213', 'Logout', '2025-11-09 22:35:27', '127.0.0.1'),
(88, 1, 'qwerty213', 'Login', '2025-11-09 22:35:43', '127.0.0.1'),
(89, 1, 'qwerty213', 'Logout', '2025-11-09 22:42:50', '127.0.0.1'),
(90, 8, 'qwerty21332', 'Login', '2025-11-09 22:42:55', '127.0.0.1'),
(91, 8, 'qwerty21332', 'Logout', '2025-11-09 22:43:00', '127.0.0.1'),
(92, 1, 'qwerty213', 'Login', '2025-11-09 22:43:03', '127.0.0.1'),
(93, 1, 'qwerty213', 'Logout', '2025-11-09 22:49:04', '127.0.0.1'),
(94, 6, 'harvey213', 'Login', '2025-11-09 22:49:10', '127.0.0.1'),
(95, 6, 'harvey213', 'Logout', '2025-11-09 23:09:45', '127.0.0.1'),
(96, 1, 'qwerty213', 'Login', '2025-11-09 23:09:55', '127.0.0.1'),
(97, 1, 'qwerty213', 'Logout', '2025-11-09 23:29:35', '127.0.0.1'),
(98, 6, 'harvey213', 'Login', '2025-11-09 23:29:40', '127.0.0.1'),
(99, 6, 'harvey213', 'Logout', '2025-11-09 23:29:54', '127.0.0.1'),
(100, 1, 'qwerty213', 'Login', '2025-11-09 23:30:06', '127.0.0.1'),
(101, 1, 'qwerty213', 'Login', '2025-11-11 15:47:56', '127.0.0.1'),
(102, 1, 'qwerty213', 'Logout', '2025-11-11 15:53:39', '127.0.0.1'),
(103, 5, 'piercevaldez213', 'Login', '2025-11-11 15:53:48', '127.0.0.1'),
(104, 5, 'piercevaldez213', 'Logout', '2025-11-11 15:55:23', '127.0.0.1'),
(105, 1, 'qwerty213', 'Login', '2025-11-11 15:55:37', '127.0.0.1'),
(106, 1, 'qwerty213', 'Logout', '2025-11-11 16:14:53', '127.0.0.1'),
(107, 1, 'qwerty213', 'Login', '2025-11-11 16:14:58', '127.0.0.1'),
(108, 1, 'qwerty213', 'Login', '2025-11-11 16:19:39', '127.0.0.1'),
(109, 1, 'qwerty213', 'Logout', '2025-11-11 16:46:13', '127.0.0.1'),
(110, 5, 'piercevaldez213', 'Login', '2025-11-11 16:46:39', '127.0.0.1'),
(111, 5, 'piercevaldez213', 'Logout', '2025-11-11 16:48:30', '127.0.0.1'),
(112, 1, 'qwerty213', 'Login', '2025-11-11 16:48:36', '127.0.0.1'),
(113, 1, 'qwerty213', 'Logout', '2025-11-11 16:59:19', '127.0.0.1'),
(114, 1, 'qwerty213', 'Login', '2025-11-11 16:59:24', '127.0.0.1'),
(115, 1, 'qwerty213', 'Logout', '2025-11-11 16:59:40', '127.0.0.1'),
(116, 1, 'qwerty213', 'Login', '2025-11-11 16:59:46', '127.0.0.1'),
(117, 1, 'qwerty213', 'Logout', '2025-11-11 18:11:53', '127.0.0.1'),
(118, 3, 'qwerty', 'Login', '2025-11-11 18:12:09', '127.0.0.1'),
(119, 3, 'qwerty', 'Logout', '2025-11-11 18:12:24', '127.0.0.1'),
(120, 1, 'qwerty213', 'Login', '2025-11-11 18:13:35', '127.0.0.1'),
(121, 1, 'qwerty213', 'Logout', '2025-11-11 18:14:39', '127.0.0.1'),
(122, 3, 'qwerty', 'Login', '2025-11-11 18:14:47', '127.0.0.1'),
(123, 3, 'qwerty', 'Logout', '2025-11-11 18:16:21', '127.0.0.1'),
(124, 1, 'qwerty213', 'Login', '2025-11-11 18:16:28', '127.0.0.1'),
(125, 1, 'qwerty213', 'Logout', '2025-11-11 18:27:55', '127.0.0.1'),
(126, 1, 'qwerty213', 'Login', '2025-11-11 18:31:33', '127.0.0.1'),
(127, 1, 'qwerty213', 'Logout', '2025-11-11 18:31:34', '127.0.0.1'),
(128, 1, 'qwerty213', 'Login', '2025-11-11 18:32:27', '127.0.0.1'),
(129, 1, 'qwerty213', 'Logout', '2025-11-11 18:32:29', '127.0.0.1'),
(130, 12, 'anne213', 'Login', '2025-11-11 18:32:40', '127.0.0.1'),
(131, 12, 'anne213', 'Logout', '2025-11-11 18:50:43', '127.0.0.1'),
(132, 1, 'qwerty213', 'Login', '2025-11-11 18:50:55', '127.0.0.1'),
(133, 1, 'qwerty213', 'Logout', '2025-11-11 18:50:58', '127.0.0.1'),
(134, 1, 'qwerty213', 'Login', '2025-11-11 18:51:09', '127.0.0.1'),
(135, 1, 'qwerty213', 'Logout', '2025-11-11 19:11:21', '127.0.0.1'),
(136, 3, 'qwerty', 'Login', '2025-11-11 19:11:31', '127.0.0.1'),
(137, 3, 'qwerty', 'Logout', '2025-11-11 19:11:57', '127.0.0.1'),
(138, 1, 'qwerty213', 'Login', '2025-11-11 19:12:04', '127.0.0.1'),
(139, 1, 'qwerty213', 'Login', '2025-11-11 19:15:24', '192.168.1.2'),
(140, 1, 'qwerty213', 'Logout', '2025-11-11 19:16:11', '192.168.1.2'),
(141, 1, 'qwerty213', 'Login', '2025-11-11 19:18:10', '127.0.0.1'),
(142, 1, 'qwerty213', 'Logout', '2025-11-11 19:18:28', '127.0.0.1'),
(143, 3, 'qwerty', 'Login', '2025-11-11 19:18:42', '127.0.0.1'),
(144, 3, 'qwerty', 'Logout', '2025-11-11 19:20:39', '127.0.0.1'),
(145, 1, 'qwerty213', 'Login', '2025-11-11 19:20:49', '127.0.0.1'),
(146, 1, 'qwerty213', 'Logout', '2025-11-11 19:51:10', '127.0.0.1'),
(147, 3, 'qwerty', 'Login', '2025-11-11 19:51:18', '127.0.0.1'),
(148, 3, 'qwerty', 'Logout', '2025-11-11 19:55:26', '127.0.0.1'),
(149, 1, 'qwerty213', 'Login', '2025-11-11 19:55:37', '127.0.0.1'),
(150, 1, 'qwerty213', 'Logout', '2025-11-11 20:05:45', '127.0.0.1'),
(151, 3, 'qwerty', 'Login', '2025-11-11 20:05:51', '127.0.0.1'),
(152, 3, 'qwerty', 'Logout', '2025-11-11 20:24:54', '127.0.0.1'),
(153, 1, 'qwerty213', 'Login', '2025-11-11 20:25:13', '127.0.0.1'),
(154, 1, 'qwerty213', 'Logout', '2025-11-11 20:25:31', '127.0.0.1'),
(155, 3, 'qwerty', 'Login', '2025-11-11 20:25:36', '127.0.0.1'),
(156, 3, 'qwerty', 'Logout', '2025-11-11 20:26:11', '127.0.0.1'),
(157, 1, 'qwerty213', 'Login', '2025-11-11 20:26:15', '127.0.0.1'),
(158, 1, 'qwerty213', 'Logout', '2025-11-11 20:27:22', '127.0.0.1'),
(159, 3, 'qwerty', 'Login', '2025-11-11 20:27:30', '127.0.0.1'),
(160, 3, 'qwerty', 'Logout', '2025-11-11 20:32:24', '127.0.0.1'),
(161, 1, 'qwerty213', 'Login', '2025-11-11 20:32:29', '127.0.0.1'),
(162, 1, 'qwerty213', 'Logout', '2025-11-11 20:34:21', '127.0.0.1'),
(163, 6, 'harvey213', 'Login', '2025-11-11 20:34:42', '127.0.0.1'),
(164, 6, 'harvey213', 'Logout', '2025-11-11 20:34:46', '127.0.0.1'),
(165, 6, 'harvey213', 'Login', '2025-11-11 20:34:54', '127.0.0.1'),
(166, 6, 'harvey213', 'Logout', '2025-11-11 20:35:31', '127.0.0.1'),
(167, 1, 'qwerty213', 'Login', '2025-11-11 20:35:38', '127.0.0.1'),
(168, 1, 'qwerty213', 'Login', '2025-11-14 02:57:29', '127.0.0.1'),
(169, 1, 'qwerty213', 'Login', '2025-11-15 21:13:48', '127.0.0.1'),
(170, 1, 'qwerty213', 'Login', '2025-11-15 21:49:51', '127.0.0.1'),
(171, 1, 'qwerty213', 'Logout', '2025-11-15 22:04:56', '127.0.0.1'),
(172, 3, 'qwerty', 'Login', '2025-11-15 22:05:02', '127.0.0.1'),
(173, 3, 'qwerty', 'Logout', '2025-11-15 22:05:26', '127.0.0.1'),
(174, 1, 'qwerty213', 'Login', '2025-11-15 22:05:31', '127.0.0.1'),
(175, 1, 'qwerty213', 'Login', '2025-11-15 22:43:14', '127.0.0.1'),
(176, 3, 'qwerty', 'Login', '2025-11-17 01:42:17', '127.0.0.1'),
(177, 3, 'qwerty', 'Logout', '2025-11-17 04:08:08', '127.0.0.1'),
(178, 1, 'qwerty213', 'Login', '2025-11-17 04:08:14', '127.0.0.1'),
(179, 1, 'qwerty213', 'Logout', '2025-11-17 05:31:23', '127.0.0.1'),
(180, 1, 'qwerty213', 'Login', '2025-11-17 05:31:38', '127.0.0.1'),
(181, 3, 'qwerty', 'Login', '2025-11-17 05:40:16', '192.168.1.5'),
(182, 1, 'qwerty213', 'Login', '2025-11-17 10:58:13', '127.0.0.1'),
(183, 1, 'qwerty213', 'Logout', '2025-11-17 11:00:48', '127.0.0.1'),
(184, 3, 'qwerty', 'Login', '2025-11-17 11:01:00', '127.0.0.1'),
(185, 3, 'qwerty', 'Logout', '2025-11-17 11:43:29', '127.0.0.1'),
(186, 1, 'qwerty213', 'Login', '2025-11-17 11:43:47', '127.0.0.1');

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
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `size` varchar(20) DEFAULT NULL,
  `size_unit` varchar(10) DEFAULT NULL,
  `brand` varchar(50) DEFAULT NULL,
  `category` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=36 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `product`
--

INSERT INTO `product` (`id`, `name`, `stock`, `price`, `image`, `created_at`, `size`, `size_unit`, `brand`, `category`) VALUES
(21, 'Wmns Cortez', 12, 4171.98, 'hospitality-cruise-ship-management_1763377229.jpg', '2025-11-05 07:02:06', '10', 'US', 'Nike', 'Sneakers'),
(27, 'Bread', 21, 123, NULL, '2025-11-05 08:24:32', '10', 'EU', 'dike', 'Sneakers'),
(22, 'Vans Men\'s Old Skool', 16, 12312, 'vans.jpg', '2025-11-05 07:04:07', '10', 'EU', 'Vans', 'Sneakers'),
(23, 'Hotdog', 50, 12312, NULL, '2025-11-05 07:04:22', '10', 'US', 'None', 'Sneakers'),
(24, 'Butter', 13, 1311, NULL, '2025-11-05 07:05:07', NULL, NULL, NULL, NULL),
(25, 'tocino', 100, 1000, NULL, '2025-11-05 07:05:56', '10', 'UK', 'Jordan', 'Sneakers'),
(28, 'Sketchers', 13, 1234, NULL, '2025-11-08 05:35:00', '10', 'UK', 'sketchers', 'Sneakers'),
(29, 'Sketchers2', 61, 12343, NULL, '2025-11-08 18:05:14', '11', 'US', 'sketchers', 'Sneakers'),
(30, 'Sketchers3', 5, 12343, NULL, '2025-11-08 20:12:22', '11', 'US', 'sketchers3', 'Sneakers'),
(31, 'shoe', 100, 1300, 'shoe_1762731391.jfif', '2025-11-09 22:42:11', '9', 'UK', '', 'Formal'),
(32, 'Cortez', 10, 4171.98, 'logo_1762887160.png', '2025-11-11 18:52:40', '10', 'US', 'Nike', 'Sneakers'),
(33, 'sandal', 12, 121313, NULL, '2025-11-11 19:47:34', '9', 'US', '', 'Sandals'),
(34, 'shoeshoe', 10, 1233, NULL, '2025-11-11 20:35:26', '90', 'US', 'Jordan', 'Boots'),
(35, 'reebook2', 49, 1234, NULL, '2025-11-15 22:01:51', '9.5', 'UK', 'reebook', 'Running');

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
) ENGINE=MyISAM AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `stock_alert`
--

INSERT INTO `stock_alert` (`id`, `product_id`, `product_name`, `stock`, `alert_type`, `created_at`) VALUES
(1, 30, 'Sketchers3', 5, 'Low Stock', '2025-11-08 20:12:22'),
(2, 28, 'Sketchers', 3, 'Low Stock', '2025-11-09 23:29:50');

-- --------------------------------------------------------

--
-- Table structure for table `stock_history`
--

DROP TABLE IF EXISTS `stock_history`;
CREATE TABLE IF NOT EXISTS `stock_history` (
  `id` int NOT NULL AUTO_INCREMENT,
  `product_id` int NOT NULL,
  `product_name` varchar(100) NOT NULL,
  `old_stock` int NOT NULL,
  `new_stock` int NOT NULL,
  `change_reason` varchar(200) DEFAULT NULL,
  `user_id` int DEFAULT NULL,
  `username` varchar(50) DEFAULT NULL,
  `timestamp` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `product_id` (`product_id`),
  KEY `user_id` (`user_id`)
) ENGINE=MyISAM AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `stock_history`
--

INSERT INTO `stock_history` (`id`, `product_id`, `product_name`, `old_stock`, `new_stock`, `change_reason`, `user_id`, `username`, `timestamp`) VALUES
(1, 21, 'Wmns Cortez', 10, 9, 'Deducted 1 units', 1, 'qwerty213', '2025-11-11 20:41:08'),
(2, 21, 'Wmns Cortez', 9, 10, 'Added 1 units', 1, 'qwerty213', '2025-11-11 20:41:28'),
(3, 35, 'reebook2', 7, 8, 'Added 1 units', 1, 'qwerty213', '2025-11-15 22:04:03'),
(4, 35, 'reebook2', 50, 49, 'Deducted 1 units', 3, 'qwerty', '2025-11-15 22:05:15'),
(5, 21, 'Wmns Cortez', 100, 50, 'Deducted 50 units', 3, 'qwerty', '2025-11-17 01:44:32'),
(6, 23, 'Hotdog', 10000, 9000, 'Deducted 1000 units', 3, 'qwerty', '2025-11-17 01:45:06'),
(7, 23, 'Hotdog', 9000, 1000, 'Deducted 8000 units', 3, 'qwerty', '2025-11-17 01:45:21'),
(8, 23, 'Hotdog', 1000, 200, 'Deducted 800 units', 3, 'qwerty', '2025-11-17 01:45:33'),
(9, 23, 'Hotdog', 200, 100, 'Deducted 100 units', 3, 'qwerty', '2025-11-17 02:10:23'),
(10, 23, 'Hotdog', 100, 50, 'Deducted 50 units', 3, 'qwerty', '2025-11-17 02:10:33'),
(11, 21, 'Wmns Cortez', 50, 10, 'Stock edited via update: stock adjustment', 1, 'qwerty213', '2025-11-17 04:20:17'),
(12, 21, 'Wmns Cortez', 10, 11, 'Added 1 units', 1, 'qwerty213', '2025-11-17 05:32:19'),
(13, 21, 'Wmns Cortez', 11, 12, 'Added 1 units', 1, 'qwerty213', '2025-11-17 10:59:43');

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
CREATE TABLE IF NOT EXISTS `user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(50) NOT NULL,
  `password` varchar(255) NOT NULL,
  `full_name` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `phone` varchar(20) DEFAULT NULL,
  `department` varchar(50) DEFAULT 'General',
  `is_active` tinyint(1) DEFAULT '1',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `role` varchar(10) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `unique_email` (`email`)
) ENGINE=MyISAM AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `user`
--

INSERT INTO `user` (`id`, `username`, `password`, `full_name`, `email`, `phone`, `department`, `is_active`, `created_at`, `role`) VALUES
(1, 'qwerty213', '$2b$12$hxtfngLXVZrlC93xp6nZM.xj.UVOrPodO/m8AHUGcdTeGjvEKmSXK', 'System Administrator', 'admin@system.local', NULL, 'General', 1, '2025-11-16 06:39:20', 'admin'),
(5, 'piercevaldez213', '$2b$12$gZd2vxhh.YwbX6w77BDDN.m61vtp3CZVOIwATMrHOGK2uPLDKHAfy', 'piercevaldez213', 'staff_5@temp.local', NULL, 'General', 1, '2025-11-16 06:39:20', 'staff'),
(3, 'qwerty', '$2b$12$4NYurfl4D12E0r9lkjGNveieXuI9IExQjlILtJVWXAs1CihV0Q2N2', 'qwerty', 'staff_3@temp.local', NULL, 'General', 1, '2025-11-16 06:39:20', 'staff'),
(6, 'harvey213', '$2b$12$OqjzaDJeaV9NmE0d.xKE6Ol.X4gtfHw2V9ASRzBGW52UdQNCtHSV2', 'harvey213', 'staff_6@temp.local', NULL, 'General', 1, '2025-11-16 06:39:20', 'staff'),
(7, 'valdez213', '$2b$12$Ypa0SNAXaQSbpbMEC571Ae0e4wXApnpGIDnM/y2S84uT.IzQrSOLW', 'valdez213', 'staff_7@temp.local', NULL, 'General', 1, '2025-11-16 06:39:20', 'staff'),
(8, 'qwerty21332', '$2b$12$QsENxGMgJG9G4Sh6oqIq0e/rVjOn/B8Mhbk5rmxoSMZ/LTEGdnlua', 'qwerty21332', 'staff_8@temp.local', NULL, 'General', 1, '2025-11-16 06:39:20', 'staff'),
(12, 'anne213', '$2b$12$1uFu.KgR3Wlf37WJIn35aOiyNMhPbjkq8mNiLXkJZNP4erofnwAZG', 'anne213', 'staff_12@temp.local', NULL, 'General', 1, '2025-11-16 06:39:20', 'staff'),
(13, 'asdfgh', '$2b$12$t0I.G6G2g5BAJP8Rpzi5W.iujxUkhZIYEQX4MXpu7TMHtfCkhg/.q', 'asdfgh', 'staff_13@temp.local', NULL, 'General', 1, '2025-11-16 06:39:20', 'staff'),
(14, 'harveyvaldez', '$2b$12$zbq6pA60VT..NK/TmUGH6umrsPnD24cMR0YyYQzbh5SUHDv1oLmCe', 'harveyvaldez', 'harvey@gmail.com', '0931231523431', 'Inventory', 1, '2025-11-15 22:46:32', 'staff');
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
