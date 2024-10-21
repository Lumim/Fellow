-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Oct 22, 2024 at 01:14 AM
-- Server version: 10.4.22-MariaDB
-- PHP Version: 8.1.2

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `fellow_1`
--

-- --------------------------------------------------------

--
-- Table structure for table `customers`
--

CREATE TABLE `customers` (
  `id` int(11) NOT NULL,
  `user_name` varchar(200) NOT NULL,
  `type` varchar(200) DEFAULT NULL,
  `card_number` varchar(200) DEFAULT NULL,
  `mobile_number` varchar(11) NOT NULL,
  `number_of_visits` int(11) DEFAULT NULL,
  `password` varchar(255) DEFAULT NULL,
  `profile_img` blob DEFAULT NULL,
  `created_at` int(11) NOT NULL DEFAULT current_timestamp(),
  `updated_at` int(11) NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `customers`
--

INSERT INTO `customers` (`id`, `user_name`, `type`, `card_number`, `mobile_number`, `number_of_visits`, `password`, `profile_img`, `created_at`, `updated_at`) VALUES
(1, 'gekki sad', NULL, NULL, '4456778', NULL, NULL, NULL, 2147483647, 2147483647);

-- --------------------------------------------------------

--
-- Table structure for table `customer_offer_calculate_table`
--

CREATE TABLE `customer_offer_calculate_table` (
  `id` int(11) NOT NULL,
  `customer_id` int(11) NOT NULL,
  `offer_id` int(11) NOT NULL,
  `restaurant_id` int(11) NOT NULL,
  `condition_met` int(1) NOT NULL,
  `offer_taken` int(1) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `offer_table`
--

CREATE TABLE `offer_table` (
  `id` int(11) NOT NULL,
  `restaurant_id` varchar(200) NOT NULL,
  `type` varchar(200) DEFAULT NULL,
  `details` varchar(200) DEFAULT NULL,
  `condition_type` varchar(200) DEFAULT NULL,
  `condition_value` int(11) DEFAULT NULL,
  `offer_name` varchar(200) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `created_by` varchar(200) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `points`
--

CREATE TABLE `points` (
  `id` int(11) NOT NULL,
  `customer_id` int(11) NOT NULL,
  `available_points` int(11) DEFAULT NULL,
  `mobile_number` varchar(11) NOT NULL,
  `used_points` int(11) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `restaurant`
--

CREATE TABLE `restaurant` (
  `id` int(11) NOT NULL,
  `logo_img` blob DEFAULT NULL,
  `banner_img` mediumblob DEFAULT NULL,
  `owner_img` blob DEFAULT NULL,
  `rest_name` varchar(200) NOT NULL,
  `type` varchar(200) DEFAULT NULL,
  `rest_mobile_number` varchar(11) NOT NULL,
  `backup_number` varchar(11) DEFAULT NULL,
  `cvr` int(9) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `customers`
--
ALTER TABLE `customers`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `customer_offer_calculate_table`
--
ALTER TABLE `customer_offer_calculate_table`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `offer_table`
--
ALTER TABLE `offer_table`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `points`
--
ALTER TABLE `points`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `restaurant`
--
ALTER TABLE `restaurant`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `customers`
--
ALTER TABLE `customers`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `customer_offer_calculate_table`
--
ALTER TABLE `customer_offer_calculate_table`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `offer_table`
--
ALTER TABLE `offer_table`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `points`
--
ALTER TABLE `points`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `restaurant`
--
ALTER TABLE `restaurant`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
