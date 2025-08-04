-- MySQL dump 10.13  Distrib 8.0.42, for Win64 (x86_64)
--
-- Host: localhost    Database: railway_mgmt
-- ------------------------------------------------------
-- Server version	8.0.42

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `bogie_capacity`
--

DROP TABLE IF EXISTS `bogie_capacity`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `bogie_capacity` (
  `train_id` int NOT NULL,
  `seats_per_bogie` int NOT NULL,
  PRIMARY KEY (`train_id`),
  CONSTRAINT `bogie_capacity_ibfk_1` FOREIGN KEY (`train_id`) REFERENCES `trains` (`train_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bogie_capacity`
--

LOCK TABLES `bogie_capacity` WRITE;
/*!40000 ALTER TABLE `bogie_capacity` DISABLE KEYS */;
INSERT INTO `bogie_capacity` VALUES (1,80),(2,80),(3,80),(4,80),(5,80),(6,80),(7,80),(8,80),(9,80),(10,80);
/*!40000 ALTER TABLE `bogie_capacity` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `passenger`
--

DROP TABLE IF EXISTS `passenger`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `passenger` (
  `passenger_id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `age` int DEFAULT NULL,
  `gender` varchar(10) DEFAULT NULL,
  `phone_number` varchar(15) DEFAULT NULL,
  PRIMARY KEY (`passenger_id`),
  CONSTRAINT `passenger_chk_1` CHECK ((`age` > 0))
) ENGINE=InnoDB AUTO_INCREMENT=28 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `passenger`
--

LOCK TABLES `passenger` WRITE;
/*!40000 ALTER TABLE `passenger` DISABLE KEYS */;
INSERT INTO `passenger` VALUES (1,'Jeffi',18,'Male','9000000001'),(2,'Nithin',19,'Male','9000000002'),(3,'Eldho',17,'Male','9000000003'),(4,'Asher',20,'Male','9000000004'),(5,'Johan',18,'Male','9000000005'),(6,'Ajmal',17,'M','238998566'),(7,'Ajmal',17,'M','12736584'),(8,'Ajmal',17,'M','132964563');
/*!40000 ALTER TABLE `passenger` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `reservations`
--

DROP TABLE IF EXISTS `reservations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `reservations` (
  `reservation_id` int NOT NULL AUTO_INCREMENT,
  `passenger_id` int DEFAULT NULL,
  `train_id` int DEFAULT NULL,
  `travel_date` date DEFAULT NULL,
  `seat_number` varchar(10) DEFAULT NULL,
  `booking_status` varchar(20) DEFAULT NULL,
  `bogie_number` varchar(2) NOT NULL,
  `coach_type` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`reservation_id`),
  KEY `fk_passenger_id` (`passenger_id`),
  KEY `fk_train_id` (`train_id`),
  CONSTRAINT `fk_passenger_id` FOREIGN KEY (`passenger_id`) REFERENCES `passenger` (`passenger_id`) ON DELETE CASCADE,
  CONSTRAINT `fk_train_id` FOREIGN KEY (`train_id`) REFERENCES `trains` (`train_id`) ON DELETE CASCADE,
  CONSTRAINT `reservations_ibfk_2` FOREIGN KEY (`train_id`) REFERENCES `trains` (`train_id`)
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `reservations`
--

LOCK TABLES `reservations` WRITE;
/*!40000 ALTER TABLE `reservations` DISABLE KEYS */;
INSERT INTO `reservations` VALUES (25,8,7,'2025-12-25','1','Confirmed','A',NULL);
/*!40000 ALTER TABLE `reservations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `station`
--

DROP TABLE IF EXISTS `station`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `station` (
  `station_id` int NOT NULL AUTO_INCREMENT,
  `station_name` varchar(100) NOT NULL,
  `location` varchar(100) NOT NULL,
  PRIMARY KEY (`station_id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `station`
--

LOCK TABLES `station` WRITE;
/*!40000 ALTER TABLE `station` DISABLE KEYS */;
INSERT INTO `station` VALUES (1,'Ernakulam Jn','Ernakulam'),(2,'Chennai Ctrl','Chennai'),(3,'Howrah','Kolkata'),(4,'Mumbai CST','Mumbai'),(5,'New Delhi','Delhi');
/*!40000 ALTER TABLE `station` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `trains`
--

DROP TABLE IF EXISTS `trains`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `trains` (
  `train_id` int NOT NULL AUTO_INCREMENT,
  `train_name` varchar(100) NOT NULL,
  `departure_time` time NOT NULL DEFAULT '00:00:00',
  `arrival_time` time NOT NULL DEFAULT '00:00:00',
  `route` varchar(100) DEFAULT NULL,
  `source` varchar(50) DEFAULT NULL,
  `destination` varchar(50) DEFAULT NULL,
  `coach_type` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`train_id`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `trains`
--

LOCK TABLES `trains` WRITE;
/*!40000 ALTER TABLE `trains` DISABLE KEYS */;
INSERT INTO `trains` VALUES (1,'Kerala Express','06:00:00','15:30:00','Kerala to Goa','Kerala','Goa','1A,2A,3A,SL,CC,2S'),(2,'Chennai Mail','08:00:00','17:00:00','Chennai to Mumbai','Chennai','Mumbai','1A,2A,3A,SL,CC,2S'),(3,'Rajdhani Express','10:00:00','20:00:00','Delhi to Bangalore','Delhi','Bangalore','1A,2A,3A,SL,CC,2S'),(4,'Duronto Express','12:30:00','21:30:00','Kolkata to Hyderabad','Kolkata','Hyderabad','1A,2A,3A,SL,CC,2S'),(5,'Shatabdi Express','05:45:00','14:15:00','Pune to Chennai','Pune','Chennai','1A,2A,3A,SL,CC,2S'),(6,'Ernakulam SF','07:15:00','19:00:00','Ernakulam to Chennai','Ernakulam','Chennai','1A,2A,3A,SL,CC,2S'),(7,'Garib Rath','09:00:00','18:45:00','Lucknow to Delhi','Lucknow','Delhi','1A,2A,3A,SL,CC,2S'),(8,'Jan Shatabdi','06:45:00','14:30:00','Goa to Mangalore','Goa','Mangalore','1A,2A,3A,SL,CC,2S'),(9,'Vande Bharat','07:30:00','13:00:00','Delhi to Varanasi','Delhi','Varanasi','1A,2A,3A,SL,CC,2S'),(10,'Humsafar Express','08:20:00','23:50:00','Jaipur to Bangalore','Jaipur','Bangalore','1A,2A,3A,SL,CC,2S');
/*!40000 ALTER TABLE `trains` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-08-04 20:41:10
