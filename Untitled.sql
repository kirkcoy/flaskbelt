-- MySQL dump 10.13  Distrib 8.0.12, for macos10.13 (x86_64)
--
-- Host: localhost    Database: retake_python_quotesdb
-- ------------------------------------------------------
-- Server version	8.0.12

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
 SET NAMES utf8 ;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `likes`
--

DROP TABLE IF EXISTS `likes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `likes` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `quote_id` int(11) NOT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_likes_users1_idx` (`user_id`),
  KEY `fk_likes_qutoes1_idx` (`quote_id`),
  CONSTRAINT `fk_likes_qutoes1` FOREIGN KEY (`quote_id`) REFERENCES `quotes` (`id`),
  CONSTRAINT `fk_likes_users1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `likes`
--

LOCK TABLES `likes` WRITE;
/*!40000 ALTER TABLE `likes` DISABLE KEYS */;
INSERT INTO `likes` VALUES (1,1,8,'2018-09-26 15:22:30','2018-09-26 15:22:30'),(2,1,8,'2018-09-26 15:22:32','2018-09-26 15:22:32'),(3,1,8,'2018-09-26 15:22:33','2018-09-26 15:22:33'),(4,1,8,'2018-09-26 15:22:33','2018-09-26 15:22:33'),(5,1,7,'2018-09-26 15:23:23','2018-09-26 15:23:23'),(6,1,5,'2018-09-26 15:23:25','2018-09-26 15:23:25'),(7,1,2,'2018-09-26 15:23:27','2018-09-26 15:23:27'),(8,4,8,'2018-09-26 15:24:37','2018-09-26 15:24:37'),(9,4,2,'2018-09-26 15:24:47','2018-09-26 15:24:47'),(10,4,6,'2018-09-26 16:46:17','2018-09-26 16:46:17');
/*!40000 ALTER TABLE `likes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `quotes`
--

DROP TABLE IF EXISTS `quotes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `quotes` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `message` text,
  `author` varchar(255) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_qutoes_users_idx` (`user_id`),
  CONSTRAINT `fk_qutoes_users` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `quotes`
--

LOCK TABLES `quotes` WRITE;
/*!40000 ALTER TABLE `quotes` DISABLE KEYS */;
INSERT INTO `quotes` VALUES (1,1,'A1234567890','AAAA','2018-09-26 12:27:34','2018-09-26 12:27:34'),(2,2,'A1234567890sdfsdf','BBBB','2018-09-26 12:46:03','2018-09-26 12:46:03'),(3,2,'A1234567890fsdfs','AAAAsdfsdf','2018-09-26 12:46:10','2018-09-26 12:46:10'),(5,3,'A123456789sdfsdfdsf','CCCC','2018-09-26 12:46:59','2018-09-26 12:46:59'),(6,3,'sasdasdadA123456789asdas','DDDDsdas','2018-09-26 12:47:09','2018-09-26 12:47:09'),(7,4,'fsA123456789sdfs','AAAAsfsdf','2018-09-26 12:47:32','2018-09-26 12:47:32'),(8,4,'sdfsfA123456789','BBBBsdfsd','2018-09-26 12:47:39','2018-09-26 12:47:39'),(10,5,'To be or not to be.','William','2018-09-26 17:41:18','2018-09-26 17:41:18');
/*!40000 ALTER TABLE `quotes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `first_name` varchar(255) DEFAULT NULL,
  `last_name` varchar(255) DEFAULT NULL,
  `email` varchar(255) DEFAULT NULL,
  `password_hash` varchar(255) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'Kirkdfdf','Dojofdfd','K@c.cfd','$2b$12$GAE2K52x4Yq.j/F1IvpbJe7BGOTiS0CUhY1f4ZCe09qAEUaeTUKWK','2018-09-26 11:14:59','2018-09-26 11:14:59'),(2,'Justin','Dojo','j@c.c','$2b$12$Jx.a.H4UY.H/NgdFdd.d9ufte9.CDBNLCyoUS7If2.zbWM7We40se','2018-09-26 12:45:48','2018-09-26 12:45:48'),(3,'Michaelasda','Dojoasa','M@c.c','$2b$12$fBboKFE5O.AkcJQgVkUJTO0qIBBY3Ce0jB6P7xtixKhIuoWzIXVK2','2018-09-26 12:46:52','2018-09-26 12:46:52'),(4,'Gwenyyyy','Dojoyyyyy','G@c.cyyyyy','$2b$12$7DCs2UUED7/kg.YCwbQKveDga0Oy2qiAWi9bmGOY9bgJHqCIhPhL6','2018-09-26 12:47:27','2018-09-26 12:47:27'),(5,'Ninakirk','Dojo','N@c.ce','$2b$12$HGTeMrHQ3SavvUZIlshAcOj24vUYzVPdy1sCWKQwhOQ8Cpi7b8HfO','2018-09-26 17:40:45','2018-09-26 17:40:45');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2018-09-26 18:03:43
