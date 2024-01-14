-- MySQL dump 10.16  Distrib 10.1.48-MariaDB, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: tensorbot
-- ------------------------------------------------------
-- Server version	10.1.48-MariaDB-0ubuntu0.18.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `target_dict`
--

DROP TABLE IF EXISTS `target_dict`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `target_dict` (
  `id` mediumint(9) NOT NULL AUTO_INCREMENT,
  `target` varchar(50) NOT NULL,
  `coordinate` varchar(50) DEFAULT NULL,
  `info` varchar(500) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `target` (`target`)
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `target_dict`
--

LOCK TABLES `target_dict` WRITE;
/*!40000 ALTER TABLE `target_dict` DISABLE KEYS */;
INSERT INTO `target_dict` VALUES (1,'Tensorbot','[10, 69]',NULL),(2,'Quang','[4, 10]',NULL),(3,'E1304','[2,4]','This is the Manufacturing process automation lab. This room is for students to practice PLC (Programmable logic controller)'),(4,'Triet','[1,2]',NULL),(5,'Home','[0, 63]',NULL),(6,'E1310','[4, 90]','This is the teachers\' meeting room'),(7,'E1307','[1, 79]','This is the Servo Drive control system lab. In this room, you will learn to practice controlling servo motors and PLC machines (Programmable logic controller).'),(8,'E1311','[10, 69]','This is the advanced control lab. In this room, you will learn advanced practice about PLC (Programmable logic controller).'),(9,'E1306','[0, 65]','This is the Electrical and electronic engineering lab. In this room, you will learn practical subjects such as microprocessors, electricity, etc'),(10,'E1305','[1, 42]','This is the Process control and Scada lab. In this room, you will learn subjects about IoT (Internet of Things), SCADA (Supervisory Control And Data Acquisition)'),(11,'E1309','[1, 104]','This is the room to store projects'),(12,'E1302','[5,2]','This is the Mechatronics department office. A place for teachers to rest and do private work after class'),(13,'E1303','[0,4]','This is the Automation simulation lab. In this room, you will learn subjects such as embedded programming, microprocessors, robotics, etc'),(14,'Mechatronics',NULL,'Mechatronics is a multidisciplinary engineering field that combines mechanics, electronics and programming to develop and manufacture devices and systems. When studying at our school, you will learn three areas: electronics and programming (mainly Python and c). A total of 150 credits and three projects: mechanical (focusing on designing mechanical drawings properly), electromechanical project and graduation project, you can do the topics of your favorite'),(15,'PLC',NULL,'PLC stands for \"Programmable Logic Controller\". This is an electronic device widely used in industrial automation to control and monitor manufacturing systems and processes. Here you will learn a lot about Siemens'),(17,'IOT',NULL,'The Internet of Things (IoT) is a system that connects objects and devices via the Internet, allowing them to interact and share data to provide intelligent information and automate processes. Here you will learn mainly about web servers and wireless communication standards'),(18,'Embedded',NULL,'Regarding embedded marketing systems, you will learn programming mainly stm32 and raspberry'),(19,'SCADA',NULL,'SCADA stands for \"Supervisory Control and Data Acquisition\", and is an automation control and monitoring system widely used in industrial processes and facilities. Infrastructure.');
/*!40000 ALTER TABLE `target_dict` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-01-14 11:14:37
