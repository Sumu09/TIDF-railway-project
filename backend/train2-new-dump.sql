-- MySQL dump 10.13  Distrib 8.0.42, for Win64 (x86_64)
--
-- Host: localhost    Database: train2
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
-- Table structure for table `casedetails`
--

DROP TABLE IF EXISTS `casedetails`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `casedetails` (
  `SI_No` int NOT NULL AUTO_INCREMENT,
  `Station_Code` varchar(20) DEFAULT NULL,
  `Case_ID` int DEFAULT NULL,
  `Case_Remark` text,
  `Close` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`SI_No`),
  KEY `casedetails_ibfk_1` (`Station_Code`),
  KEY `casedetails_ibfk_2` (`Case_ID`),
  CONSTRAINT `casedetails_ibfk_1` FOREIGN KEY (`Station_Code`) REFERENCES `station` (`Station_Code`) ON UPDATE CASCADE,
  CONSTRAINT `casedetails_ibfk_2` FOREIGN KEY (`Case_ID`) REFERENCES `report` (`Case_ID`) ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=37 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `casedetails`
--

LOCK TABLES `casedetails` WRITE;
/*!40000 ALTER TABLE `casedetails` DISABLE KEYS */;
INSERT INTO `casedetails` VALUES (1,'STN001',101,'Theft reported in coach A3',0),(2,'STN002',102,'Suspicious activity near platform 2',1),(3,'STN003',103,'Lost luggage reported',0),(4,'STN004',104,'Vandalism in waiting room',0),(5,'STN005',105,'Unauthorized vendor complaint',1),(6,'STN006',106,'Broken CCTV at gate',0),(7,'STN007',21,'Passenger fight reported',1),(8,'STN008',108,'Gate left open',0),(9,'STN009',109,'Lighting issue on platform 3',1),(10,'STN011',110,'Fire alarm triggered falsely',0),(26,'STN001',101,'Theft reported in coach A3',0),(28,'STN001',101,'Theft reported in coach A3',0),(29,'STN001',101,'Theft reported in coach A3',0),(31,'STN001',101,'Theft  in coach A3',0),(32,'STN001',101,'Theft  in coach A3',1),(33,'STN011',101,'Theft  in coach A3',1),(34,'STN021',101,'Theft  in coach A3',1);
/*!40000 ALTER TABLE `casedetails` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `final_report`
--

DROP TABLE IF EXISTS `final_report`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `final_report` (
  `SI_No` int NOT NULL DEFAULT '0',
  `Train_Name` varchar(50) DEFAULT NULL,
  `Report_ID` varchar(20) DEFAULT NULL,
  `Wagon_No` int DEFAULT NULL,
  `Coach_Position` int DEFAULT NULL,
  `Door_No` int DEFAULT NULL,
  `Camera_No` int DEFAULT NULL,
  `Date` date DEFAULT NULL,
  `Time` time DEFAULT NULL,
  `Status` tinyint(1) DEFAULT NULL,
  `Report_Remark` text,
  `Station_Code` varchar(20) DEFAULT NULL,
  `Station_Name` varchar(100) DEFAULT NULL,
  `Case_ID` int DEFAULT NULL,
  `Image_Link` varchar(255) DEFAULT NULL,
  `Ph_No` bigint DEFAULT NULL,
  `User_Name` varchar(100) DEFAULT NULL,
  `User_Age` int DEFAULT NULL,
  `User_Email` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `final_report`
--

LOCK TABLES `final_report` WRITE;
/*!40000 ALTER TABLE `final_report` DISABLE KEYS */;
INSERT INTO `final_report` VALUES (1,'Guwahati Express','RPT001',5,3,1,2,'2025-06-01','12:00:00',1,'Theft caught on cam','STN001','Kolkata Junction',101,'link1.jpg',9876543010,'Riya Sharma',25,'riya25@gmail.com'),(2,'Dibrugarh Rajdhani','RPT002',6,4,2,3,'2025-06-02','13:15:00',0,'Suspicious behavior','STN002','Delhi Central',102,'link2.jpg',9812345678,'Amit Das',28,'amitd28@yahoo.com'),(3,'Howrah Kamrup Express','RPT003',3,2,1,1,'2025-06-03','10:30:00',1,'Luggage reported missing','STN003','Mumbai Gateway',103,'link3.jpg',9900112233,'Sneha Paul',22,'sneha_paul@hotmail.com'),(4,'Brahmaputra Mail','RPT004',7,5,2,4,'2025-06-04','09:45:00',0,'Waiting room damaged','STN004','Chennai Park',104,'link4.jpg',9123456701,'Kabir Singh',30,'kabir.singh@outlook.com'),(5,'Kamakhya Intercity','RPT005',2,1,1,1,'2025-06-05','11:20:00',1,'Unauthorized vendor at gate','STN005','Guwahati Town',105,'link5.jpg',9009988776,'Neha Roy',24,'neha.roy@gmail.com'),(6,'Tezpur Passenger','RPT006',4,2,2,2,'2025-06-06','14:00:00',0,'CCTV broken','STN006','Bangalore East',106,'link6.jpg',8887766554,'Rohan Mehta',27,'rohanm27@gmail.com'),(7,'Silchar Express','RPT007',1,1,1,3,'2025-06-07','16:10:00',1,'Fight at platform','STN007','Hyderabad City',107,'link7.jpg',9665544332,'Ishita Verma',21,'ishita.v@gmail.com'),(8,'Intercity Express','RPT008',5,3,1,2,'2025-06-08','08:30:00',0,'Open gate alert','STN008','Pune Terminal',108,'link8.jpg',8776655443,'Nikhil Sen',26,'nikhilsen@ymail.com'),(9,'Jan Shatabdi Express','RPT009',3,2,2,1,'2025-06-09','17:50:00',1,'Low light on platform','STN009','Jaipur Metro',109,'link9.jpg',9345678901,'Priya Dey',23,'priyadey23@yahoo.in'),(10,'Kaziranga Express','RPT010',6,4,2,4,'2025-06-10','19:00:00',0,'False fire alarm','STN010','Ahmedabad Line',110,'link10.jpg',7890654321,'Manav Jain',29,'manavjain@protonmail.com');
/*!40000 ALTER TABLE `final_report` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `goodstrain`
--

DROP TABLE IF EXISTS `goodstrain`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `goodstrain` (
  `SI_No` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `status` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`SI_No`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `goodstrain`
--

LOCK TABLES `goodstrain` WRITE;
/*!40000 ALTER TABLE `goodstrain` DISABLE KEYS */;
/*!40000 ALTER TABLE `goodstrain` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `goodstrains`
--

DROP TABLE IF EXISTS `goodstrains`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `goodstrains` (
  `Sl_No` int NOT NULL AUTO_INCREMENT,
  `Train_Name` varchar(50) DEFAULT NULL,
  `Train_Status` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`Sl_No`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `goodstrains`
--

LOCK TABLES `goodstrains` WRITE;
/*!40000 ALTER TABLE `goodstrains` DISABLE KEYS */;
INSERT INTO `goodstrains` VALUES (1,'First Goods Train','Finished'),(2,'Second Goods Train','Finished'),(3,'Third Goods Train','Finished'),(4,'Fourth Goods Train','Unfinished'),(5,'Fifth Goods Train','Unfinished'),(6,'Sixth Goods Train','Finished'),(7,'Seventh Goods Train','Unfinished'),(8,'Eighth Goods Train','Unfinished'),(9,'Ninth Goods Train','Unfinished'),(10,'Tenth Goods Train','Finished'),(11,'Eleventh Goods Train','Unfinished'),(12,'Twelfth Goods Train','Finished'),(13,'Thirteenth Goods Train','Unfinished'),(14,'Fourteenth Goods Train','Unfinished'),(15,'Fifteenth Goods Train','Unfinished');
/*!40000 ALTER TABLE `goodstrains` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `report`
--

DROP TABLE IF EXISTS `report`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `report` (
  `SI_No` int NOT NULL AUTO_INCREMENT,
  `Train_Name` varchar(50) DEFAULT NULL,
  `Report_ID` varchar(20) DEFAULT NULL,
  `Wagon_No` int DEFAULT NULL,
  `Coach_Position` int DEFAULT NULL,
  `Door_No` int DEFAULT NULL,
  `Camera_No` int DEFAULT NULL,
  `Date` date DEFAULT NULL,
  `Time` time DEFAULT NULL,
  `Status` tinyint(1) DEFAULT NULL,
  `Report_Remark` text,
  `Station_Code` varchar(20) DEFAULT NULL,
  `Case_ID` int DEFAULT NULL,
  `Image_Link` varchar(255) DEFAULT NULL,
  `Ph_No` bigint DEFAULT NULL,
  PRIMARY KEY (`SI_No`),
  UNIQUE KEY `Report_ID` (`Report_ID`),
  UNIQUE KEY `Case_ID` (`Case_ID`),
  KEY `report_ibfk_1` (`Station_Code`),
  CONSTRAINT `report_ibfk_1` FOREIGN KEY (`Station_Code`) REFERENCES `station` (`Station_Code`) ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=42 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `report`
--

LOCK TABLES `report` WRITE;
/*!40000 ALTER TABLE `report` DISABLE KEYS */;
INSERT INTO `report` VALUES (1,'Guwahati Express','RPT001',5,3,1,2,'2025-06-01','12:00:00',1,'Theft caught on cam','STN001',101,'link1.jpg',9876543010),(2,'Dibrugarh Rajdhani','RPT002',6,4,2,3,'2025-06-02','13:15:00',0,'Suspicious behavior','STN002',102,'link2.jpg',9812345678),(3,'Howrah Kamrup Express','RPT003',3,2,1,1,'2025-06-03','10:30:00',1,'Luggage reported missing','STN003',103,'link3.jpg',9900112233),(4,'Brahmaputra Mail','RPT004',7,5,2,4,'2025-06-04','09:45:00',0,'Waiting room damaged','STN004',104,'link4.jpg',9123456701),(5,'Kamakhya Intercity','RPT005',2,1,1,1,'2025-06-05','11:20:00',1,'Unauthorized vendor at gate','STN005',105,'link5.jpg',9009988776),(6,'first express','RPT006',4,2,2,2,'2025-06-06','14:00:00',1,'CCTV broken','STN006',106,'link6.jpg',8887766554),(7,'Silchar Express','RPT007',1,1,1,3,'2025-06-07','16:10:00',1,'Fight at platform','STN007',21,'link7.jpg',9665544332),(8,'Intercity Express','RPT008',5,3,1,2,'2025-06-08','08:30:00',0,'Open gate alert','STN008',108,'link8.jpg',8776655443),(9,'Jan Shatabdi Express','RPT009',3,2,2,1,'2025-06-09','17:50:00',1,'Low light on platform','STN009',109,'link9.jpg',9345678901),(10,'Kaziranga Express','RPT010',6,4,2,4,'2025-06-10','19:00:00',0,'False fire alarm','STN011',110,'link10.jpg',7890654321),(11,'Rajdhani Superfast','RPT011',7,4,1,5,'2025-07-01','10:00:00',1,'Security breach in coach','STN001',111,'link11.jpg',9876500011),(12,'Bongaigaon Intercity','RPT012',2,1,2,6,'2025-07-02','11:30:00',0,'Vendor denied entry','STN001',112,'link12.jpg',9876500022),(13,'Assam Link Express','RPT013',5,3,1,7,'2025-07-03','12:45:00',1,'Suspicious package found','STN001',113,'link13.jpg',9876500033),(14,'North East Express','RPT014',6,4,2,8,'2025-07-04','14:20:00',0,'Fire extinguisher missing','STN001',114,'link14.jpg',9876500044),(15,'Rajdhani Night Rider','RPT015',4,2,1,1,'2025-07-05','08:00:00',1,'Delay due to track issue','STN002',115,'link15.jpg',9812345600),(16,'Dibrugarh Mail','RPT016',5,3,2,2,'2025-07-06','09:15:00',0,'Lost luggage reported','STN002',116,'link16.jpg',9812345601),(17,'Ledo Passenger','RPT017',6,4,1,3,'2025-07-07','10:30:00',1,'Gate malfunction','STN002',117,'link17.jpg',9812345602),(18,'debo selfie express','RPT018',3,1,1,2,'2025-07-05','11:45:00',0,'Unauthorized filming','STN003',118,'link18.jpg',9900112200),(19,'Howrah Night Express','RPT019',4,2,2,3,'2025-07-06','13:00:00',1,'Broken CCTV found','STN003',119,'link19.jpg',9900112201),(20,'blah blah express','RPT020',5,3,1,4,'2025-07-07','14:15:00',1,'Power failure in coach','STN003',120,'link20.jpg',9900112202),(21,'Brahmaputra Local','RPT021',2,1,2,2,'2025-07-05','07:30:00',1,'Vendor without ID','STN004',121,'link21.jpg',9123456700),(22,'Mail Runner Express','RPT022',3,2,1,3,'2025-07-06','08:45:00',0,'Passenger got injured','STN004',122,'link22.jpg',9123456702),(23,'Assam Heritage Line','RPT023',4,3,2,4,'2025-07-07','10:00:00',1,'Alert raised at gate','STN004',123,'link23.jpg',9123456703),(24,'Kamakhya Special','RPT024',1,1,1,1,'2025-07-05','06:20:00',0,'Train delayed 3 hours','STN005',124,'link24.jpg',9009988700),(25,'City Shuttle','RPT025',2,2,2,2,'2025-07-06','07:30:00',1,'CCTV tampering','STN005',125,'link25.jpg',9009988701),(26,'Guwahati Passenger','RPT026',3,3,1,3,'2025-07-07','08:40:00',0,'Unidentified item found','STN005',126,'link26.jpg',9009988702),(27,'Tezpur Local','RPT027',4,2,2,2,'2025-07-05','07:50:00',1,'Overcrowded platform','STN006',127,'link27.jpg',8887766500),(28,'debo express','RPT028',5,3,1,3,'2025-07-06','09:00:00',1,'False alarm triggered','STN006',128,'link28.jpg',8887766501),(29,'Passenger Link','RPT029',6,4,2,4,'2025-07-07','10:10:00',1,'Rail crossing issue','STN006',129,'link29.jpg',8887766502),(30,'Silchar City Connect','RPT030',1,1,1,1,'2025-07-05','06:40:00',0,'Track inspection pending','STN007',130,'link30.jpg',9665544300),(31,'Barak Valley Express','RPT031',2,2,2,2,'2025-07-06','07:50:00',1,'Security camera stolen','STN007',131,'link31.jpg',9665544301),(32,'South Assam Passenger','RPT032',3,3,1,3,'2025-07-07','09:00:00',0,'Train stuck at signal','STN007',132,'link32.jpg',9665544302),(33,'Intercity Shuttle','RPT033',4,2,1,1,'2025-07-05','08:10:00',1,'Suspicious bag reported','STN008',133,'link33.jpg',8776655400),(34,'Kaziranga Special','RPT034',5,3,2,2,'2025-07-06','09:20:00',0,'Signal failure alert','STN008',134,'link34.jpg',8776655401),(35,'Brahmaputra Connect','RPT035',6,4,1,3,'2025-07-07','10:30:00',1,'Train staff reported missing','STN008',135,'link35.jpg',8776655402),(36,'Jan Shatabdi Link','RPT036',1,1,2,4,'2025-07-05','07:30:00',0,'Smoke detected in coach','STN009',136,'link36.jpg',9345678900),(37,'Highway Rider Express','RPT037',2,2,1,1,'2025-07-06','08:40:00',1,'Gate left open','STN009',137,'link37.jpg',9345678902),(38,'Evening Star Express','RPT038',3,3,2,2,'2025-07-07','10:00:00',0,'Emergency alarm pressed','STN009',138,'link38.jpg',9345678903),(39,'Kaziranga Morning','RPT039',4,2,1,3,'2025-07-05','09:00:00',1,'Unauthorized vendor','STN011',139,'link39.jpg',7890654300),(40,'Kaziranga Rapid','RPT040',5,3,2,4,'2025-07-06','10:30:00',0,'Light flickering alert','STN011',140,'link40.jpg',7890654301),(41,'Guwahati Local Link','RPT041',6,4,1,1,'2025-07-07','12:00:00',1,'Stretcher request on train','STN011',141,'link41.jpg',7890654302);
/*!40000 ALTER TABLE `report` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `signup`
--

DROP TABLE IF EXISTS `signup`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `signup` (
  `SI_No` int NOT NULL AUTO_INCREMENT,
  `Ph_No` bigint DEFAULT NULL,
  `Station_Code` varchar(20) DEFAULT NULL,
  `Type_of_User` varchar(50) DEFAULT NULL,
  `Password` varchar(100) DEFAULT NULL,
  `Name` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`SI_No`),
  UNIQUE KEY `Ph_No` (`Ph_No`),
  KEY `signup_ibfk_1` (`Station_Code`),
  CONSTRAINT `signup_ibfk_1` FOREIGN KEY (`Station_Code`) REFERENCES `station` (`Station_Code`) ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=42 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `signup`
--

LOCK TABLES `signup` WRITE;
/*!40000 ALTER TABLE `signup` DISABLE KEYS */;
INSERT INTO `signup` VALUES (1,9876543010,'STN001','GroundStaff','45b69182434c1ad1c2c03850702e20254e33c76d','Riya Sharma'),(2,9812345678,'STN002','GroundStaff','1a097e632ebfd6a0247e9dd4806f1339f4a0e081','Amit Das'),(3,9900112233,'STN003','GroundStaff','ba25612cd0dc40690a01999af2b0ca4ca38cf649','Sneha Paul'),(4,9123456701,'STN004','GroundStaff','8842e473276aa7486fab85e19047313b10a05e75','Kabir Singh'),(5,9009988776,'STN005','StationAdmin','b671bcade0e711f766bb510b93b42fac7562860b','Neha Roy'),(6,8887766554,'STN006','StationAdmin','b564adf3b991f32ca7b862fd0f6b4ddd7f053fde','Rohan Mehta'),(7,9665544332,'STN007','StationAdmin','753b59c8cc4e53206deb6fcd8b369f23c53d3ff4','Ishita Verma'),(8,8776655443,'STN008','ZonalHead','0967165ae286ee7bfb1c91d2069b58dd13af62ee','Nikhil Sen'),(9,9345678901,'STN009','ZonalHead','9637a999b775ce0754e9c5f93fbaf0b3a55a81c7','Priya Dey'),(10,7890654321,'STN011','ZonalHead','45b69182434c1ad1c2c03850702e20254e33c76d','Manav Jain'),(39,1234123412,'STN003','GroundStaff','018e19f099fb69b646c76224b04a2333e67725c8','milinda barua'),(41,1234567890,'STN006','GroundStaff','018e19f099fb69b646c76224b04a2333e67725c8','milinda barua');
/*!40000 ALTER TABLE `signup` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `station`
--

DROP TABLE IF EXISTS `station`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `station` (
  `SI_No` int NOT NULL AUTO_INCREMENT,
  `Station_Name` varchar(100) DEFAULT NULL,
  `Station_Code` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`SI_No`),
  UNIQUE KEY `Station_Code` (`Station_Code`)
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `station`
--

LOCK TABLES `station` WRITE;
/*!40000 ALTER TABLE `station` DISABLE KEYS */;
INSERT INTO `station` VALUES (1,'Kolkata Junction','STN001'),(2,'Delhi Central','STN002'),(3,'Mumbai Gateway','STN003'),(4,'Chennai Park','STN004'),(5,'Guwahati Town','STN005'),(6,'Bangalore East','STN006'),(7,'Hyderabad City','STN007'),(8,'Pune Terminal','STN008'),(9,'Jaipur Metro','STN009'),(10,'Ahmedabad Line','STN011'),(21,'sibsagar junction','STN021');
/*!40000 ALTER TABLE `station` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `train`
--

DROP TABLE IF EXISTS `train`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `train` (
  `SI_No` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `time` varchar(20) DEFAULT NULL,
  `status` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`SI_No`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `train`
--

LOCK TABLES `train` WRITE;
/*!40000 ALTER TABLE `train` DISABLE KEYS */;
/*!40000 ALTER TABLE `train` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `userdetails`
--

DROP TABLE IF EXISTS `userdetails`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `userdetails` (
  `Name` varchar(100) DEFAULT NULL,
  `Age` int DEFAULT NULL,
  `Email` varchar(100) DEFAULT NULL,
  `Ph_No` bigint DEFAULT NULL,
  KEY `fk_phno` (`Ph_No`),
  CONSTRAINT `fk_phno` FOREIGN KEY (`Ph_No`) REFERENCES `signup` (`Ph_No`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `userdetails`
--

LOCK TABLES `userdetails` WRITE;
/*!40000 ALTER TABLE `userdetails` DISABLE KEYS */;
INSERT INTO `userdetails` VALUES ('Riya Sharma',25,'riya25@gmail.com',9876543010),('Amit Das',28,'amitd28@yahoo.com',9812345678),('Sneha Paul',22,'sneha_paul@hotmail.com',9900112233),('Kabir Singh',30,'kabir.singh@outlook.com',9123456701),('Neha Roy',24,'neha.roy@gmail.com',9009988776),('Rohan Mehta',27,'rohanm27@gmail.com',8887766554),('Ishita Verma',21,'ishita.v@gmail.com',9665544332),('Nikhil Sen',26,'nikhilsen@ymail.com',8776655443),('Priya Dey',23,'priyadey23@yahoo.in',9345678901),('Manav Jain',29,'manavjain@protonmail.com',7890654321);
/*!40000 ALTER TABLE `userdetails` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-07-18 11:30:43
