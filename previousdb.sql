-- phpMyAdmin SQL Dump
-- version 5.2.2
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Dec 04, 2025 at 10:46 AM
-- Server version: 10.6.23-MariaDB
-- PHP Version: 8.1.33

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `ibnusina_portfolio`
--

-- --------------------------------------------------------

--
-- Table structure for table `about_section`
--

CREATE TABLE `about_section` (
  `id` int(11) NOT NULL,
  `title` varchar(255) NOT NULL,
  `description` longtext NOT NULL,
  `socials_urls` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL CHECK (json_valid(`socials_urls`)),
  `show_stats` tinyint(1) NOT NULL,
  `show_work_experience` tinyint(1) NOT NULL,
  `show_why_choose_us` tinyint(1) NOT NULL,
  `show_roadmap` tinyint(1) NOT NULL,
  `date_created` datetime(6) NOT NULL,
  `date_updated` datetime(6) NOT NULL,
  `media` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `about_section`
--

INSERT INTO `about_section` (`id`, `title`, `description`, `socials_urls`, `show_stats`, `show_work_experience`, `show_why_choose_us`, `show_roadmap`, `date_created`, `date_updated`, `media`) VALUES
(1, 'About Us', 'He heard the loud impact before he ever saw the result. It had been so loud that it had actually made him jump back in his seat. As soon as he recovered from the surprise, he saw the crack in the windshield. It seemed to be an analogy of the current condition of his life.', NULL, 1, 1, 1, 0, '2025-10-10 15:19:32.995155', '2025-10-24 06:14:46.985509', 'about_section/1/pexels-fauxels-3183150.jpg');

-- --------------------------------------------------------

--
-- Table structure for table `about_stats`
--

CREATE TABLE `about_stats` (
  `id` bigint(20) NOT NULL,
  `stat_name` varchar(100) NOT NULL,
  `stat_value` varchar(50) NOT NULL,
  `stat_description` varchar(200) NOT NULL,
  `icon_name` varchar(50) NOT NULL,
  `display_order` int(11) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_created` datetime(6) NOT NULL,
  `date_updated` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `about_stats`
--

INSERT INTO `about_stats` (`id`, `stat_name`, `stat_value`, `stat_description`, `icon_name`, `display_order`, `is_active`, `date_created`, `date_updated`) VALUES
(1, 'Orders Complete', '1000+', '', '', 0, 1, '2025-11-13 08:31:55.182016', '2025-11-13 08:32:27.329408'),
(2, 'Digital Services', '20+', '', '', 0, 1, '2025-11-13 08:33:40.695385', '2025-11-13 08:33:40.695401'),
(3, 'Article Reads', '10000+', '', '', 0, 1, '2025-11-13 08:34:27.720827', '2025-11-13 08:34:47.400526');

-- --------------------------------------------------------

--
-- Table structure for table `accounts_partner`
--

CREATE TABLE `accounts_partner` (
  `id` bigint(20) NOT NULL,
  `professional_title` varchar(150) NOT NULL,
  `domain` varchar(120) NOT NULL,
  `professional_summary` longtext NOT NULL,
  `website` varchar(200) NOT NULL,
  `social_urls` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL CHECK (json_valid(`social_urls`)),
  `affiliate_clients` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL CHECK (json_valid(`affiliate_clients`)),
  `media_url` varchar(100) DEFAULT NULL,
  `services` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL CHECK (json_valid(`services`)),
  `orders` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL CHECK (json_valid(`orders`)),
  `blog_posts` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL CHECK (json_valid(`blog_posts`)),
  `projects` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL CHECK (json_valid(`projects`)),
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `user_id` varchar(36) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `accounts_partner`
--

INSERT INTO `accounts_partner` (`id`, `professional_title`, `domain`, `professional_summary`, `website`, `social_urls`, `affiliate_clients`, `media_url`, `services`, `orders`, `blog_posts`, `projects`, `created_at`, `updated_at`, `user_id`) VALUES
(1, '', '', '', '', '[]', '[]', '', '[]', '[]', '[]', '[]', '2025-10-24 08:00:27.076540', '2025-10-24 08:00:27.076559', 'ee26f538-08dc-4896-887c-b80e44e36ed8'),
(2, '', '', '', '', '[]', '[]', '', '[]', '[]', '[]', '[]', '2025-10-24 10:07:23.011040', '2025-10-24 10:07:23.011064', 'e6b5cd4a-2f9f-4197-95d0-f0a66d7764dd'),
(3, '', '', '', '', '[]', '[]', '', '[]', '[]', '[]', '[]', '2025-10-24 10:07:35.306086', '2025-10-24 10:07:35.306104', 'c344773a-d8bf-48ee-8ecf-50d419534e50'),
(4, '', '', '', '', '[]', '[]', '', '[]', '[]', '[]', '[]', '2025-10-24 10:07:50.206005', '2025-10-24 10:07:50.206024', '29652470-827f-4535-b0c7-ffff5fdef7a7'),
(5, 'Software Developer', 'Computer Science', 'I am a professional software developer dedicated to delivering autonomous, fast, and efficient \r\nbusiness solutions across web, mobile, and desktop applications.', 'http://lewis-codes.vercel.app', '[]', '[]', 'partners/media/pexels-shoper-pl-550490863-16675632.jpg', '[]', '[]', '[]', '[]', '2025-11-13 07:25:04.847639', '2025-11-13 07:41:53.939098', '81219bde-c597-416a-bfbf-bfd2b2fa36f1');

-- --------------------------------------------------------

--
-- Table structure for table `authtoken_token`
--

CREATE TABLE `authtoken_token` (
  `key` varchar(40) NOT NULL,
  `created` datetime(6) NOT NULL,
  `user_id` varchar(36) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- --------------------------------------------------------

--
-- Table structure for table `auth_group`
--

CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL,
  `name` varchar(150) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- --------------------------------------------------------

--
-- Table structure for table `auth_group_permissions`
--

CREATE TABLE `auth_group_permissions` (
  `id` bigint(20) NOT NULL,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- --------------------------------------------------------

--
-- Table structure for table `auth_permission`
--

CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `auth_permission`
--

INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES
(1, 'Can add association', 1, 'add_association'),
(2, 'Can change association', 1, 'change_association'),
(3, 'Can delete association', 1, 'delete_association'),
(4, 'Can view association', 1, 'view_association'),
(5, 'Can add code', 2, 'add_code'),
(6, 'Can change code', 2, 'change_code'),
(7, 'Can delete code', 2, 'delete_code'),
(8, 'Can view code', 2, 'view_code'),
(9, 'Can add nonce', 3, 'add_nonce'),
(10, 'Can change nonce', 3, 'change_nonce'),
(11, 'Can delete nonce', 3, 'delete_nonce'),
(12, 'Can view nonce', 3, 'view_nonce'),
(13, 'Can add user social auth', 4, 'add_usersocialauth'),
(14, 'Can change user social auth', 4, 'change_usersocialauth'),
(15, 'Can delete user social auth', 4, 'delete_usersocialauth'),
(16, 'Can view user social auth', 4, 'view_usersocialauth'),
(17, 'Can add partial', 5, 'add_partial'),
(18, 'Can change partial', 5, 'change_partial'),
(19, 'Can delete partial', 5, 'delete_partial'),
(20, 'Can view partial', 5, 'view_partial'),
(21, 'Can add log entry', 6, 'add_logentry'),
(22, 'Can change log entry', 6, 'change_logentry'),
(23, 'Can delete log entry', 6, 'delete_logentry'),
(24, 'Can view log entry', 6, 'view_logentry'),
(25, 'Can add permission', 7, 'add_permission'),
(26, 'Can change permission', 7, 'change_permission'),
(27, 'Can delete permission', 7, 'delete_permission'),
(28, 'Can view permission', 7, 'view_permission'),
(29, 'Can add group', 8, 'add_group'),
(30, 'Can change group', 8, 'change_group'),
(31, 'Can delete group', 8, 'delete_group'),
(32, 'Can view group', 8, 'view_group'),
(33, 'Can add content type', 9, 'add_contenttype'),
(34, 'Can change content type', 9, 'change_contenttype'),
(35, 'Can delete content type', 9, 'delete_contenttype'),
(36, 'Can view content type', 9, 'view_contenttype'),
(37, 'Can add session', 10, 'add_session'),
(38, 'Can change session', 10, 'change_session'),
(39, 'Can delete session', 10, 'delete_session'),
(40, 'Can view session', 10, 'view_session'),
(41, 'Can add Token', 11, 'add_token'),
(42, 'Can change Token', 11, 'change_token'),
(43, 'Can delete Token', 11, 'delete_token'),
(44, 'Can view Token', 11, 'view_token'),
(45, 'Can add Token', 12, 'add_tokenproxy'),
(46, 'Can change Token', 12, 'change_tokenproxy'),
(47, 'Can delete Token', 12, 'delete_tokenproxy'),
(48, 'Can view Token', 12, 'view_tokenproxy'),
(49, 'Can add Blacklisted Token', 13, 'add_blacklistedtoken'),
(50, 'Can change Blacklisted Token', 13, 'change_blacklistedtoken'),
(51, 'Can delete Blacklisted Token', 13, 'delete_blacklistedtoken'),
(52, 'Can view Blacklisted Token', 13, 'view_blacklistedtoken'),
(53, 'Can add Outstanding Token', 14, 'add_outstandingtoken'),
(54, 'Can change Outstanding Token', 14, 'change_outstandingtoken'),
(55, 'Can delete Outstanding Token', 14, 'delete_outstandingtoken'),
(56, 'Can view Outstanding Token', 14, 'view_outstandingtoken'),
(57, 'Can add User', 15, 'add_user'),
(58, 'Can change User', 15, 'change_user'),
(59, 'Can delete User', 15, 'delete_user'),
(60, 'Can view User', 15, 'view_user'),
(61, 'Can add Client Profile', 16, 'add_clientprofile'),
(62, 'Can change Client Profile', 16, 'change_clientprofile'),
(63, 'Can delete Client Profile', 16, 'delete_clientprofile'),
(64, 'Can view Client Profile', 16, 'view_clientprofile'),
(65, 'Can add Partner', 17, 'add_partner'),
(66, 'Can change Partner', 17, 'change_partner'),
(67, 'Can delete Partner', 17, 'delete_partner'),
(68, 'Can view Partner', 17, 'view_partner'),
(69, 'Can add About Section', 18, 'add_aboutsection'),
(70, 'Can change About Section', 18, 'change_aboutsection'),
(71, 'Can delete About Section', 18, 'delete_aboutsection'),
(72, 'Can view About Section', 18, 'view_aboutsection'),
(73, 'Can add About Statistic', 19, 'add_aboutstats'),
(74, 'Can change About Statistic', 19, 'change_aboutstats'),
(75, 'Can delete About Statistic', 19, 'delete_aboutstats'),
(76, 'Can view About Statistic', 19, 'view_aboutstats'),
(77, 'Can add Contact Info', 20, 'add_contactinfo'),
(78, 'Can change Contact Info', 20, 'change_contactinfo'),
(79, 'Can delete Contact Info', 20, 'delete_contactinfo'),
(80, 'Can view Contact Info', 20, 'view_contactinfo'),
(81, 'Can add Hero Section', 21, 'add_herosection'),
(82, 'Can change Hero Section', 21, 'change_herosection'),
(83, 'Can delete Hero Section', 21, 'delete_herosection'),
(84, 'Can view Hero Section', 21, 'view_herosection'),
(85, 'Can add Newsletter Subscription', 22, 'add_newslettersubscription'),
(86, 'Can change Newsletter Subscription', 22, 'change_newslettersubscription'),
(87, 'Can delete Newsletter Subscription', 22, 'delete_newslettersubscription'),
(88, 'Can view Newsletter Subscription', 22, 'view_newslettersubscription'),
(89, 'Can add Roadmap Milestone', 23, 'add_roadmap'),
(90, 'Can change Roadmap Milestone', 23, 'change_roadmap'),
(91, 'Can delete Roadmap Milestone', 23, 'delete_roadmap'),
(92, 'Can view Roadmap Milestone', 23, 'view_roadmap'),
(93, 'Can add Why Choose Us', 24, 'add_whychooseus'),
(94, 'Can change Why Choose Us', 24, 'change_whychooseus'),
(95, 'Can delete Why Choose Us', 24, 'delete_whychooseus'),
(96, 'Can view Why Choose Us', 24, 'view_whychooseus'),
(97, 'Can add Work Experience', 25, 'add_workexperience'),
(98, 'Can change Work Experience', 25, 'change_workexperience'),
(99, 'Can delete Work Experience', 25, 'delete_workexperience'),
(100, 'Can view Work Experience', 25, 'view_workexperience'),
(101, 'Can add Support Ticket', 26, 'add_supportticket'),
(102, 'Can change Support Ticket', 26, 'change_supportticket'),
(103, 'Can delete Support Ticket', 26, 'delete_supportticket'),
(104, 'Can view Support Ticket', 26, 'view_supportticket'),
(105, 'Can add Support Attachment', 27, 'add_supportattachment'),
(106, 'Can change Support Attachment', 27, 'change_supportattachment'),
(107, 'Can delete Support Attachment', 27, 'delete_supportattachment'),
(108, 'Can view Support Attachment', 27, 'view_supportattachment'),
(109, 'Can add Project', 28, 'add_project'),
(110, 'Can change Project', 28, 'change_project'),
(111, 'Can delete Project', 28, 'delete_project'),
(112, 'Can view Project', 28, 'view_project'),
(113, 'Can add Technology', 29, 'add_technology'),
(114, 'Can change Technology', 29, 'change_technology'),
(115, 'Can delete Technology', 29, 'delete_technology'),
(116, 'Can view Technology', 29, 'view_technology'),
(117, 'Can add Project Technology', 30, 'add_projecttechnology'),
(118, 'Can change Project Technology', 30, 'change_projecttechnology'),
(119, 'Can delete Project Technology', 30, 'delete_projecttechnology'),
(120, 'Can view Project Technology', 30, 'view_projecttechnology'),
(121, 'Can add Project Comment', 31, 'add_projectcomment'),
(122, 'Can change Project Comment', 31, 'change_projectcomment'),
(123, 'Can delete Project Comment', 31, 'delete_projectcomment'),
(124, 'Can view Project Comment', 31, 'view_projectcomment'),
(125, 'Can add Project Gallery Image', 32, 'add_projectgalleryimage'),
(126, 'Can change Project Gallery Image', 32, 'change_projectgalleryimage'),
(127, 'Can delete Project Gallery Image', 32, 'delete_projectgalleryimage'),
(128, 'Can view Project Gallery Image', 32, 'view_projectgalleryimage'),
(129, 'Can add Blog Post', 33, 'add_blogpost'),
(130, 'Can change Blog Post', 33, 'change_blogpost'),
(131, 'Can delete Blog Post', 33, 'delete_blogpost'),
(132, 'Can view Blog Post', 33, 'view_blogpost'),
(133, 'Can add Tag', 34, 'add_tag'),
(134, 'Can change Tag', 34, 'change_tag'),
(135, 'Can delete Tag', 34, 'delete_tag'),
(136, 'Can view Tag', 34, 'view_tag'),
(137, 'Can add Blog Post Tag', 35, 'add_blogposttag'),
(138, 'Can change Blog Post Tag', 35, 'change_blogposttag'),
(139, 'Can delete Blog Post Tag', 35, 'delete_blogposttag'),
(140, 'Can view Blog Post Tag', 35, 'view_blogposttag'),
(141, 'Can add Blog Comment', 36, 'add_blogcomment'),
(142, 'Can change Blog Comment', 36, 'change_blogcomment'),
(143, 'Can delete Blog Comment', 36, 'delete_blogcomment'),
(144, 'Can view Blog Comment', 36, 'view_blogcomment'),
(145, 'Can add Service Feature', 37, 'add_servicefeature'),
(146, 'Can change Service Feature', 37, 'change_servicefeature'),
(147, 'Can delete Service Feature', 37, 'delete_servicefeature'),
(148, 'Can view Service Feature', 37, 'view_servicefeature'),
(149, 'Can add Service Category', 38, 'add_servicecategory'),
(150, 'Can change Service Category', 38, 'change_servicecategory'),
(151, 'Can delete Service Category', 38, 'delete_servicecategory'),
(152, 'Can view Service Category', 38, 'view_servicecategory'),
(153, 'Can add Service', 39, 'add_service'),
(154, 'Can change Service', 39, 'change_service'),
(155, 'Can delete Service', 39, 'delete_service'),
(156, 'Can view Service', 39, 'view_service'),
(157, 'Can add Service Deliverable', 40, 'add_servicedeliverable'),
(158, 'Can change Service Deliverable', 40, 'change_servicedeliverable'),
(159, 'Can delete Service Deliverable', 40, 'delete_servicedeliverable'),
(160, 'Can view Service Deliverable', 40, 'view_servicedeliverable'),
(161, 'Can add Service FAQ', 41, 'add_servicefaq'),
(162, 'Can change Service FAQ', 41, 'change_servicefaq'),
(163, 'Can delete Service FAQ', 41, 'delete_servicefaq'),
(164, 'Can view Service FAQ', 41, 'view_servicefaq'),
(165, 'Can add Pricing Tier Feature', 42, 'add_pricingtierfeature'),
(166, 'Can change Pricing Tier Feature', 42, 'change_pricingtierfeature'),
(167, 'Can delete Pricing Tier Feature', 42, 'delete_pricingtierfeature'),
(168, 'Can view Pricing Tier Feature', 42, 'view_pricingtierfeature'),
(169, 'Can add Service Popular Use Case', 43, 'add_servicepopularusecase'),
(170, 'Can change Service Popular Use Case', 43, 'change_servicepopularusecase'),
(171, 'Can delete Service Popular Use Case', 43, 'delete_servicepopularusecase'),
(172, 'Can view Service Popular Use Case', 43, 'view_servicepopularusecase'),
(173, 'Can add Service Pricing Tier', 44, 'add_servicepricingtier'),
(174, 'Can change Service Pricing Tier', 44, 'change_servicepricingtier'),
(175, 'Can delete Service Pricing Tier', 44, 'delete_servicepricingtier'),
(176, 'Can view Service Pricing Tier', 44, 'view_servicepricingtier'),
(177, 'Can add Service Process Step', 45, 'add_serviceprocessstep'),
(178, 'Can change Service Process Step', 45, 'change_serviceprocessstep'),
(179, 'Can delete Service Process Step', 45, 'delete_serviceprocessstep'),
(180, 'Can view Service Process Step', 45, 'view_serviceprocessstep'),
(181, 'Can add Service Tool', 46, 'add_servicetool'),
(182, 'Can change Service Tool', 46, 'change_servicetool'),
(183, 'Can delete Service Tool', 46, 'delete_servicetool'),
(184, 'Can view Service Tool', 46, 'view_servicetool'),
(185, 'Can add Product', 47, 'add_product'),
(186, 'Can change Product', 47, 'change_product'),
(187, 'Can delete Product', 47, 'delete_product'),
(188, 'Can view Product', 47, 'view_product'),
(189, 'Can add Product Tag', 48, 'add_producttag'),
(190, 'Can change Product Tag', 48, 'change_producttag'),
(191, 'Can delete Product Tag', 48, 'delete_producttag'),
(192, 'Can view Product Tag', 48, 'view_producttag'),
(193, 'Can add Product Technology', 49, 'add_producttechnology'),
(194, 'Can change Product Technology', 49, 'change_producttechnology'),
(195, 'Can delete Product Technology', 49, 'delete_producttechnology'),
(196, 'Can view Product Technology', 49, 'view_producttechnology'),
(197, 'Can add Product Update', 50, 'add_productupdate'),
(198, 'Can change Product Update', 50, 'change_productupdate'),
(199, 'Can delete Product Update', 50, 'delete_productupdate'),
(200, 'Can view Product Update', 50, 'view_productupdate'),
(201, 'Can add Product Gallery Image', 51, 'add_productgalleryimage'),
(202, 'Can change Product Gallery Image', 51, 'change_productgalleryimage'),
(203, 'Can delete Product Gallery Image', 51, 'delete_productgalleryimage'),
(204, 'Can view Product Gallery Image', 51, 'view_productgalleryimage'),
(205, 'Can add Product Purchase', 52, 'add_productpurchase'),
(206, 'Can change Product Purchase', 52, 'change_productpurchase'),
(207, 'Can delete Product Purchase', 52, 'delete_productpurchase'),
(208, 'Can view Product Purchase', 52, 'view_productpurchase'),
(209, 'Can add Product Review', 53, 'add_productreview'),
(210, 'Can change Product Review', 53, 'change_productreview'),
(211, 'Can delete Product Review', 53, 'delete_productreview'),
(212, 'Can view Product Review', 53, 'view_productreview'),
(213, 'Can add Contact Message', 54, 'add_contactmessage'),
(214, 'Can change Contact Message', 54, 'change_contactmessage'),
(215, 'Can delete Contact Message', 54, 'delete_contactmessage'),
(216, 'Can view Contact Message', 54, 'view_contactmessage'),
(217, 'Can add Order', 55, 'add_order'),
(218, 'Can change Order', 55, 'change_order'),
(219, 'Can delete Order', 55, 'delete_order'),
(220, 'Can view Order', 55, 'view_order'),
(221, 'Can add payment', 56, 'add_payment'),
(222, 'Can change payment', 56, 'change_payment'),
(223, 'Can delete payment', 56, 'delete_payment'),
(224, 'Can view payment', 56, 'view_payment'),
(225, 'Can add PayPal Payment', 57, 'add_paypalpayment'),
(226, 'Can change PayPal Payment', 57, 'change_paypalpayment'),
(227, 'Can delete PayPal Payment', 57, 'delete_paypalpayment'),
(228, 'Can view PayPal Payment', 57, 'view_paypalpayment'),
(229, 'Can add Service Request', 58, 'add_servicerequest'),
(230, 'Can change Service Request', 58, 'change_servicerequest'),
(231, 'Can delete Service Request', 58, 'delete_servicerequest'),
(232, 'Can view Service Request', 58, 'view_servicerequest'),
(233, 'Can add Testimonial', 59, 'add_testimonial'),
(234, 'Can change Testimonial', 59, 'change_testimonial'),
(235, 'Can delete Testimonial', 59, 'delete_testimonial'),
(236, 'Can view Testimonial', 59, 'view_testimonial'),
(237, 'Can add Notification', 60, 'add_notification'),
(238, 'Can change Notification', 60, 'change_notification'),
(239, 'Can delete Notification', 60, 'delete_notification'),
(240, 'Can view Notification', 60, 'view_notification'),
(241, 'Can add Project Section', 61, 'add_projectsection'),
(242, 'Can change Project Section', 61, 'change_projectsection'),
(243, 'Can delete Project Section', 61, 'delete_projectsection'),
(244, 'Can view Project Section', 61, 'view_projectsection');

-- --------------------------------------------------------

--
-- Table structure for table `auth_user`
--

CREATE TABLE `auth_user` (
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `id` varchar(36) NOT NULL,
  `email` varchar(254) NOT NULL,
  `first_name` varchar(100) NOT NULL,
  `last_name` varchar(100) NOT NULL,
  `profile_img` varchar(100) DEFAULT NULL,
  `phone` varchar(20) NOT NULL,
  `role` varchar(20) NOT NULL,
  `is_verified` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `two_factor_enabled` tinyint(1) NOT NULL,
  `is_social_login` tinyint(1) NOT NULL,
  `affiliate_code` varchar(64) DEFAULT NULL,
  `account_balance` decimal(12,2) NOT NULL,
  `currency` varchar(10) NOT NULL,
  `language_preference` varchar(32) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  `date_updated` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `auth_user`
--

INSERT INTO `auth_user` (`password`, `last_login`, `is_superuser`, `id`, `email`, `first_name`, `last_name`, `profile_img`, `phone`, `role`, `is_verified`, `is_active`, `is_staff`, `two_factor_enabled`, `is_social_login`, `affiliate_code`, `account_balance`, `currency`, `language_preference`, `date_joined`, `date_updated`) VALUES
('!KsERrMHpm72kvJtKXbHDscnz7bSHo7eCUrgiYcvs', NULL, 0, '00c13dd7-8c5b-4c5a-9a3e-23100a32eba8', 'thuodiana3@gmail.com', 'Diana', 'Thuo', '', '', 'client', 1, 1, 0, 0, 1, NULL, 0.00, 'USD', 'English', '2025-11-20 09:16:00.661865', '2025-11-20 09:16:00.680980'),
('pbkdf2_sha256$1000000$bv639NKIR480Zz1TaE07FY$/3plpGYNSv80ieOg8slQ/qzz6dzqD0SIyXDXXLp6lG8=', NULL, 0, '29652470-827f-4535-b0c7-ffff5fdef7a7', 'bradleymumo01@gmail.com', '', '', '', '', 'partner', 0, 1, 1, 0, 0, 'Pass@123', 0.00, 'USD', 'English', '2025-10-24 10:00:29.753289', '2025-10-24 10:00:30.583287'),
('pbkdf2_sha256$1000000$mkjBmf72aCMHe7Bs6SgwYw$1XoIzK3mupvMe6qUZtywUK9fStIaf6hqjQbS1bXTJSk=', NULL, 0, '3464d20e-0f05-4d34-92b3-7aa263cff186', 'ausndia98@gmail.com', '', '', '', '', 'partner', 0, 1, 1, 0, 0, NULL, 0.00, 'USD', 'English', '2025-10-10 15:46:54.391735', '2025-10-24 08:01:01.873515'),
('!y2hOAetfinyR5AhU4s8kjeTkcqlxjE8TR5HiY7qv', NULL, 0, '81219bde-c597-416a-bfbf-bfd2b2fa36f1', 'lewismutembei001@gmail.com', 'Lewis', 'Mutembei', '', '', 'partner', 1, 1, 1, 0, 1, NULL, 0.00, 'USD', 'English', '2025-10-08 06:38:09.316792', '2025-10-08 06:38:09.336047'),
('pbkdf2_sha256$1000000$M8gFyRwDhmUcWPKcXxiNu2$1eOB0v/ck0Bsf/Ut2c1NrPUAtS6m/TuScU8KM67qYe4=', '2025-10-24 10:05:30.175447', 0, 'c344773a-d8bf-48ee-8ecf-50d419534e50', 'rhodahwamaitha86@gmail.com', '', '', '', '', 'partner', 0, 1, 1, 0, 0, NULL, 0.00, 'USD', 'English', '2025-10-24 10:02:15.366300', '2025-10-24 10:02:16.244382'),
('pbkdf2_sha256$1000000$R3zKnGBV8PFDxMARpt5JrR$BK6nLBX6+/xFoiQDfguH9Qj90vWyLNJhZGFxV84sS+I=', '2025-11-27 09:40:46.553817', 0, 'e6b5cd4a-2f9f-4197-95d0-f0a66d7764dd', 'dianathuo3@gmail.com', '', '', '', '', 'partner', 0, 1, 1, 0, 0, NULL, 0.00, 'USD', 'English', '2025-10-24 10:05:21.562262', '2025-11-20 10:43:57.940434'),
('pbkdf2_sha256$1000000$OtqVHkQPeT2uimA7KaYhgI$FrC2MLdWx0CVj4OcnScUzOy8m7jdX2yajUyeBUaOkiA=', NULL, 0, 'ee26f538-08dc-4896-887c-b80e44e36ed8', 'davidnyateng@gmail.com', '', '', '', '', 'partner', 0, 1, 1, 0, 0, NULL, 0.00, 'USD', 'English', '2025-10-10 15:44:37.356910', '2025-10-10 15:45:40.869558'),
('pbkdf2_sha256$1000000$uXNDqgrMJVUlUCknHlrBXb$TSn5ltdBUfxD5lNhgBw0XoiHqB8zMqYncWtTJdydGlE=', '2025-11-19 08:51:35.949843', 1, 'fe410b51-cbc2-4205-861a-c820f6dda5be', 'savvysolutions.ke@gmail.com', 'Happy', 'Savvy', '', '', 'admin', 0, 1, 1, 0, 0, NULL, 0.00, 'USD', 'English', '2025-10-08 06:31:19.648513', '2025-10-10 15:06:02.454494');

-- --------------------------------------------------------

--
-- Table structure for table `auth_user_groups`
--

CREATE TABLE `auth_user_groups` (
  `id` bigint(20) NOT NULL,
  `user_id` varchar(36) NOT NULL,
  `group_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- --------------------------------------------------------

--
-- Table structure for table `auth_user_user_permissions`
--

CREATE TABLE `auth_user_user_permissions` (
  `id` bigint(20) NOT NULL,
  `user_id` varchar(36) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- --------------------------------------------------------

--
-- Table structure for table `blogpost_tag`
--

CREATE TABLE `blogpost_tag` (
  `id` bigint(20) NOT NULL,
  `blogpost_id` varchar(36) NOT NULL,
  `tag_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- --------------------------------------------------------

--
-- Table structure for table `blog_comment`
--

CREATE TABLE `blog_comment` (
  `id` varchar(36) NOT NULL,
  `name` varchar(255) NOT NULL,
  `email` varchar(254) NOT NULL,
  `website` varchar(200) NOT NULL,
  `message` longtext NOT NULL,
  `approved` tinyint(1) NOT NULL,
  `date_created` datetime(6) NOT NULL,
  `parent_id` varchar(36) DEFAULT NULL,
  `blogpost_id` varchar(36) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- --------------------------------------------------------

--
-- Table structure for table `blog_post`
--

CREATE TABLE `blog_post` (
  `id` varchar(36) NOT NULL,
  `title` varchar(255) NOT NULL,
  `slug` varchar(255) NOT NULL,
  `excerpt` longtext NOT NULL,
  `content` longtext NOT NULL,
  `date_published` date DEFAULT NULL,
  `category` varchar(100) NOT NULL,
  `status` varchar(20) NOT NULL,
  `view_count` int(11) NOT NULL,
  `featured` tinyint(1) NOT NULL,
  `date_created` datetime(6) NOT NULL,
  `date_updated` datetime(6) NOT NULL,
  `author_id` varchar(36) NOT NULL,
  `featured_image` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `blog_post`
--

INSERT INTO `blog_post` (`id`, `title`, `slug`, `excerpt`, `content`, `date_published`, `category`, `status`, `view_count`, `featured`, `date_created`, `date_updated`, `author_id`, `featured_image`) VALUES
('8a569bca-87cc-42e0-ba32-0f5febf73e09', 'Machine Learning Prediction Model', 'machine-learning-prediction-model', 'In the mining industry, accurate estimation of ore grade plays a pivotal role in optimizing production processes, ensuring efficient resource allocation, and maximizing profitability. Traditionally, ore grade estimation has relied on statistical methods and geological expertise, which can be time-consuming, subjective, and prone to human error.', 'In the mining industry, accurate estimation of ore grade plays a pivotal role in optimizing production processes, ensuring efficient resource allocation, and maximizing profitability. Traditionally, ore grade estimation has relied on statistical methods and geological expertise, which can be time-consuming, subjective, and prone to human error. However, with the advent of machine learning techniques, a new era of predictive modelling has emerged. Utilizing statistical and machine learning methods the process aims to anticipate the levels of ore grades within a deposit. The precision of these forecasts plays a role, in mine planning, resource optimization and evaluations of economic feasibility. offering immense potential for more precise and automated ore grade estimation [1].\r\nThis proposal aims to explore the application of two prominent machine learning techniques, namely k-nearest neighbour (KNN) and neural networks (NN), to revolutionize the process of ore grade estimation. By harnessing the power of these algorithms, we can leverage vast amounts of historical data and extract valuable insights to predict ore grade accurately and efficiently.\r\nK-nearest neighbour (KNN) is a non-parametric classification algorithm that relies on the principle of similarity, this is a classification algorithm that doesn\'t rely on parameters. Its commonly used in machine learning for both classification and regression tasks. In the case of classification k-NN predicts the class label of a data point by considering the class labels of its neighbors, in the training data. It classifies data points by comparing them to their nearest neighbours in the feature space. In the context of ore grade estimation, k-NN can be trained on historical data consisting of geological attributes such as chemical composition, mineralogy, and physical characteristics [1], [2]. By identifying patterns and similarities between past ore samples and their corresponding grades, KNN can generate predictions for new, unexplored regions of the mine. The simplicity and interpretability of the KNN algorithm make it a better choice for initial exploration and benchmarking.', NULL, 'Tech', 'published', 8, 0, '2025-10-24 08:48:22.928424', '2025-10-24 08:48:25.994415', '81219bde-c597-416a-bfbf-bfd2b2fa36f1', 'blog/featured/pexels-fauxels-3183150.jpg');

-- --------------------------------------------------------

--
-- Table structure for table `client`
--

CREATE TABLE `client` (
  `user_id` varchar(36) NOT NULL,
  `company_name` varchar(255) NOT NULL,
  `industry` varchar(100) NOT NULL,
  `account_balance` decimal(12,2) NOT NULL,
  `date_created` datetime(6) NOT NULL,
  `date_updated` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `client`
--

INSERT INTO `client` (`user_id`, `company_name`, `industry`, `account_balance`, `date_created`, `date_updated`) VALUES
('00c13dd7-8c5b-4c5a-9a3e-23100a32eba8', '', '', 0.00, '2025-11-20 09:16:00.663355', '2025-11-20 09:16:00.663488'),
('3464d20e-0f05-4d34-92b3-7aa263cff186', '', '', 0.00, '2025-10-10 15:46:54.801252', '2025-10-10 15:46:54.801369'),
('81219bde-c597-416a-bfbf-bfd2b2fa36f1', '', '', 0.00, '2025-10-08 06:38:09.325837', '2025-10-08 06:38:09.326017'),
('ee26f538-08dc-4896-887c-b80e44e36ed8', '', '', 0.00, '2025-10-10 15:44:37.754960', '2025-10-10 15:44:37.755111');

-- --------------------------------------------------------

--
-- Table structure for table `contact_info`
--

CREATE TABLE `contact_info` (
  `id` bigint(20) NOT NULL,
  `brand_name` varchar(100) NOT NULL,
  `email` varchar(254) NOT NULL,
  `phone` varchar(30) NOT NULL,
  `location` varchar(255) NOT NULL,
  `social_links` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL CHECK (json_valid(`social_links`)),
  `date_created` datetime(6) NOT NULL,
  `date_updated` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `contact_info`
--

INSERT INTO `contact_info` (`id`, `brand_name`, `email`, `phone`, `location`, `social_links`, `date_created`, `date_updated`) VALUES
(1, 'Savvy Solutions', 'savvysolutions.ke@gmail.com', '0712345678', 'Nairobi, Kenya', '{\"ig\": \"\", \"git\": \"\", \"linkedin\": \"\", \"x\": \"\", \"reddit\": \"\"}', '2025-10-10 15:01:35.692380', '2025-10-10 15:01:35.692398');

-- --------------------------------------------------------

--
-- Table structure for table `contact_message`
--

CREATE TABLE `contact_message` (
  `id` varchar(36) NOT NULL,
  `name` varchar(255) NOT NULL,
  `email` varchar(254) NOT NULL,
  `phone` varchar(20) NOT NULL,
  `subject` varchar(255) NOT NULL,
  `message` longtext NOT NULL,
  `source` varchar(50) NOT NULL,
  `is_read` tinyint(1) NOT NULL,
  `replied` tinyint(1) NOT NULL,
  `priority` varchar(10) NOT NULL,
  `date_created` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- --------------------------------------------------------

--
-- Table structure for table `core_supportattachment`
--

CREATE TABLE `core_supportattachment` (
  `id` bigint(20) NOT NULL,
  `file` varchar(100) NOT NULL,
  `original_filename` varchar(255) NOT NULL,
  `file_size` int(10) UNSIGNED NOT NULL CHECK (`file_size` >= 0),
  `uploaded_at` datetime(6) NOT NULL,
  `ticket_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- --------------------------------------------------------

--
-- Table structure for table `core_supportticket`
--

CREATE TABLE `core_supportticket` (
  `id` bigint(20) NOT NULL,
  `subject` varchar(200) NOT NULL,
  `message` longtext NOT NULL,
  `priority` varchar(10) NOT NULL,
  `status` varchar(15) NOT NULL,
  `admin_reply` longtext DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `resolved_at` datetime(6) DEFAULT NULL,
  `admin_user_id` varchar(36) DEFAULT NULL,
  `user_id` varchar(36) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- --------------------------------------------------------

--
-- Table structure for table `django_admin_log`
--

CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext DEFAULT NULL,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) UNSIGNED NOT NULL CHECK (`action_flag` >= 0),
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` varchar(36) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `django_admin_log`
--

INSERT INTO `django_admin_log` (`id`, `action_time`, `object_id`, `object_repr`, `action_flag`, `change_message`, `content_type_id`, `user_id`) VALUES
(1, '2025-10-10 15:01:35.692820', '1', 'Savvy Solutions', 1, '[{\"added\": {}}]', 20, 'fe410b51-cbc2-4205-861a-c820f6dda5be'),
(2, '2025-10-10 15:03:29.480557', '1', 'Savvy Solutions', 1, '[{\"added\": {}}]', 21, 'fe410b51-cbc2-4205-861a-c820f6dda5be'),
(3, '2025-10-10 15:19:32.996106', '1', 'AboutSection object (1)', 1, '[{\"added\": {}}]', 18, 'fe410b51-cbc2-4205-861a-c820f6dda5be'),
(4, '2025-10-10 16:11:21.885955', 'fb631bb0-c771-4482-a89a-973fe8baa37a', 'Content Writing', 1, '[{\"added\": {}}]', 38, 'fe410b51-cbc2-4205-861a-c820f6dda5be'),
(5, '2025-10-10 16:11:37.033465', '18547e53-ab5b-46a4-a89b-5b36cc7943c5', 'Business', 1, '[{\"added\": {}}]', 38, 'fe410b51-cbc2-4205-861a-c820f6dda5be'),
(6, '2025-10-10 16:12:12.417315', '0ddd55f1-f736-4659-ac41-441ccc9b2d94', 'Coding & Tech', 1, '[{\"added\": {}}]', 38, 'fe410b51-cbc2-4205-861a-c820f6dda5be'),
(7, '2025-10-10 16:12:46.997227', '6550a32a-b3ac-4547-a47a-fa0ce4fb4a68', 'Video Editing', 1, '[{\"added\": {}}]', 38, 'fe410b51-cbc2-4205-861a-c820f6dda5be'),
(8, '2025-10-10 16:12:58.841050', '1b3a9818-5ad8-42b0-acc6-ece065abe250', 'Graphics & Design', 1, '[{\"added\": {}}]', 38, 'fe410b51-cbc2-4205-861a-c820f6dda5be'),
(9, '2025-10-10 16:13:38.531551', '5222ec79-ab29-4139-99e4-b9192f4f2f62', 'Digital Marketing', 1, '[{\"added\": {}}]', 38, 'fe410b51-cbc2-4205-861a-c820f6dda5be'),
(10, '2025-10-10 16:46:55.564151', '6bd424a8-38b6-4bc3-9264-221a305d10d6', 'Website Development', 1, '[{\"added\": {}}, {\"added\": {\"name\": \"Service Pricing Tier\", \"object\": \"Website Development - Starter\"}}]', 39, 'fe410b51-cbc2-4205-861a-c820f6dda5be'),
(11, '2025-10-16 19:56:16.615255', '1', 'AboutSection object (1)', 2, '[{\"changed\": {\"fields\": [\"Media\"]}}]', 18, 'fe410b51-cbc2-4205-861a-c820f6dda5be'),
(12, '2025-10-24 06:14:46.986602', '1', 'AboutSection object (1)', 2, '[{\"changed\": {\"fields\": [\"Media\"]}}]', 18, 'fe410b51-cbc2-4205-861a-c820f6dda5be'),
(13, '2025-10-24 08:00:27.077023', '1', 'davidnyateng@gmail.com Partner Profile', 1, '[{\"added\": {}}]', 17, 'fe410b51-cbc2-4205-861a-c820f6dda5be'),
(14, '2025-10-24 08:01:01.874747', '3464d20e-0f05-4d34-92b3-7aa263cff186', 'ausndia98@gmail.com', 2, '[{\"changed\": {\"fields\": [\"Role\", \"Is staff\"]}}]', 15, 'fe410b51-cbc2-4205-861a-c820f6dda5be'),
(15, '2025-10-24 08:48:26.003698', '8a569bca-87cc-42e0-ba32-0f5febf73e09', 'Machine Learning Prediction Model', 1, '[{\"added\": {}}]', 33, 'fe410b51-cbc2-4205-861a-c820f6dda5be'),
(16, '2025-10-24 08:55:26.016477', '36a8ea04-f582-4d90-a2ca-046ee1336abc', 'E-commerce Site', 1, '[{\"added\": {}}, {\"added\": {\"name\": \"Project Gallery Image\", \"object\": \"E-commerce Site - Image 0\"}}]', 28, 'fe410b51-cbc2-4205-861a-c820f6dda5be'),
(17, '2025-10-24 10:00:30.583909', '29652470-827f-4535-b0c7-ffff5fdef7a7', 'bradleymumo01@gmail.com', 1, '[{\"added\": {}}]', 15, 'fe410b51-cbc2-4205-861a-c820f6dda5be'),
(18, '2025-10-24 10:02:16.244980', 'c344773a-d8bf-48ee-8ecf-50d419534e50', 'rhodahwamaitha86@gmail.com', 1, '[{\"added\": {}}]', 15, 'fe410b51-cbc2-4205-861a-c820f6dda5be'),
(19, '2025-10-24 10:05:22.381224', 'e6b5cd4a-2f9f-4197-95d0-f0a66d7764dd', 'dianathuo3@gmail.com', 1, '[{\"added\": {}}]', 15, 'fe410b51-cbc2-4205-861a-c820f6dda5be'),
(20, '2025-10-24 10:07:23.011650', '2', 'dianathuo3@gmail.com Partner Profile', 1, '[{\"added\": {}}]', 17, 'fe410b51-cbc2-4205-861a-c820f6dda5be'),
(21, '2025-10-24 10:07:35.306534', '3', 'rhodahwamaitha86@gmail.com Partner Profile', 1, '[{\"added\": {}}]', 17, 'fe410b51-cbc2-4205-861a-c820f6dda5be'),
(22, '2025-10-24 10:07:50.206554', '4', 'bradleymumo01@gmail.com Partner Profile', 1, '[{\"added\": {}}]', 17, 'fe410b51-cbc2-4205-861a-c820f6dda5be'),
(23, '2025-11-13 06:40:50.838274', '6bd424a8-38b6-4bc3-9264-221a305d10d6', 'Website Development', 2, '[{\"changed\": {\"fields\": [\"Img url\", \"Pricing model\", \"Starting at\"]}}, {\"added\": {\"name\": \"Service Pricing Tier\", \"object\": \"Website Development - Standard Web App\"}}, {\"added\": {\"name\": \"Service Pricing Tier\", \"object\": \"Website Development - Pro Web Apps\"}}, {\"added\": {\"name\": \"Service Pricing Tier\", \"object\": \"Website Development - Premium Custom Web App\"}}, {\"changed\": {\"name\": \"Service Pricing Tier\", \"object\": \"Website Development - Basic Website\", \"fields\": [\"Name\", \"Price\", \"Estimated delivery\"]}}]', 39, 'fe410b51-cbc2-4205-861a-c820f6dda5be'),
(24, '2025-11-13 06:43:11.496029', '6bd424a8-38b6-4bc3-9264-221a305d10d6', 'Website Development', 2, '[{\"changed\": {\"fields\": [\"Pricing model\"]}}]', 39, 'fe410b51-cbc2-4205-861a-c820f6dda5be'),
(25, '2025-11-13 06:43:36.506441', '6bd424a8-38b6-4bc3-9264-221a305d10d6', 'Website Development', 2, '[{\"changed\": {\"fields\": [\"Pricing model\"]}}]', 39, 'fe410b51-cbc2-4205-861a-c820f6dda5be'),
(26, '2025-11-13 07:25:04.849057', '5', 'Lewis Mutembei Partner Profile', 1, '[{\"added\": {}}]', 17, 'fe410b51-cbc2-4205-861a-c820f6dda5be'),
(27, '2025-11-13 07:41:53.940120', '5', 'Lewis Mutembei Partner Profile', 2, '[{\"changed\": {\"fields\": [\"Media url\"]}}]', 17, 'fe410b51-cbc2-4205-861a-c820f6dda5be'),
(28, '2025-11-13 07:49:10.371488', '1', 'Send Order Proposal', 1, '[{\"added\": {}}]', 23, 'fe410b51-cbc2-4205-861a-c820f6dda5be'),
(29, '2025-11-13 07:54:36.261689', '2', 'Confirm Order', 1, '[{\"added\": {}}]', 23, 'fe410b51-cbc2-4205-861a-c820f6dda5be'),
(30, '2025-11-13 08:15:37.345674', '2', 'Confirm Order & Make Payment', 2, '[{\"changed\": {\"fields\": [\"Milestone title\", \"Milestone description\"]}}]', 23, 'fe410b51-cbc2-4205-861a-c820f6dda5be'),
(31, '2025-11-13 08:25:57.764071', '3', 'Service Delivery & Review', 1, '[{\"added\": {}}]', 23, 'fe410b51-cbc2-4205-861a-c820f6dda5be'),
(32, '2025-11-13 08:26:20.675898', '2', 'Confirm Order & Make Payment', 2, '[{\"changed\": {\"fields\": [\"Display order\"]}}]', 23, 'fe410b51-cbc2-4205-861a-c820f6dda5be'),
(33, '2025-11-13 08:26:41.630977', '3', 'Service Delivery & Review', 2, '[{\"changed\": {\"fields\": [\"Display order\"]}}]', 23, 'fe410b51-cbc2-4205-861a-c820f6dda5be'),
(34, '2025-11-13 08:31:55.182632', '1', 'Orders: 500+', 1, '[{\"added\": {}}]', 19, 'fe410b51-cbc2-4205-861a-c820f6dda5be'),
(35, '2025-11-13 08:32:07.729484', '1', 'Orders: 1000+', 2, '[{\"changed\": {\"fields\": [\"Stat value\"]}}]', 19, 'fe410b51-cbc2-4205-861a-c820f6dda5be'),
(36, '2025-11-13 08:32:27.330356', '1', 'Orders Complete: 1000+', 2, '[{\"changed\": {\"fields\": [\"Stat name\"]}}]', 19, 'fe410b51-cbc2-4205-861a-c820f6dda5be'),
(37, '2025-11-13 08:33:40.695825', '2', 'Digital Services: 20+', 1, '[{\"added\": {}}]', 19, 'fe410b51-cbc2-4205-861a-c820f6dda5be'),
(38, '2025-11-13 08:34:27.721411', '3', 'Articles: 30+', 1, '[{\"added\": {}}]', 19, 'fe410b51-cbc2-4205-861a-c820f6dda5be'),
(39, '2025-11-13 08:34:47.401413', '3', 'Article Reads: 10000+', 2, '[{\"changed\": {\"fields\": [\"Stat name\", \"Stat value\"]}}]', 19, 'fe410b51-cbc2-4205-861a-c820f6dda5be'),
(40, '2025-11-19 17:52:58.640997', 'a3562560-4b2b-4873-82e1-dbaa6ee700cc', 'Academic & Educational Writing', 1, '[{\"added\": {}}]', 38, 'fe410b51-cbc2-4205-861a-c820f6dda5be'),
(41, '2025-11-19 18:02:34.761017', '18547e53-ab5b-46a4-a89b-5b36cc7943c5', 'Business & Professional Writing', 2, '[{\"changed\": {\"fields\": [\"Name\", \"Slug\", \"Short desc\", \"Category url\", \"Sub categories\"]}}]', 38, 'fe410b51-cbc2-4205-861a-c820f6dda5be'),
(42, '2025-11-19 18:06:16.342063', '0ddd55f1-f736-4659-ac41-441ccc9b2d94', 'Programming & Data', 2, '[{\"changed\": {\"fields\": [\"Name\", \"Slug\", \"Category url\", \"Sub categories\"]}}]', 38, 'fe410b51-cbc2-4205-861a-c820f6dda5be'),
(43, '2025-11-19 18:12:04.578393', '5222ec79-ab29-4139-99e4-b9192f4f2f62', 'Web and Mobile Application', 2, '[{\"changed\": {\"fields\": [\"Name\", \"Slug\", \"Category url\", \"Sub categories\", \"Sort order\"]}}]', 38, 'fe410b51-cbc2-4205-861a-c820f6dda5be'),
(44, '2025-11-19 18:13:08.704095', 'a3562560-4b2b-4873-82e1-dbaa6ee700cc', 'Essay Writing & Translation', 2, '[{\"changed\": {\"fields\": [\"Name\"]}}]', 38, 'fe410b51-cbc2-4205-861a-c820f6dda5be'),
(45, '2025-11-19 18:16:01.504452', 'fb631bb0-c771-4482-a89a-973fe8baa37a', 'Creative & Personal Writing', 2, '[{\"changed\": {\"fields\": [\"Name\", \"Slug\", \"Sub categories\", \"Sort order\"]}}]', 38, 'fe410b51-cbc2-4205-861a-c820f6dda5be'),
(46, '2025-11-19 18:16:25.284938', 'fb631bb0-c771-4482-a89a-973fe8baa37a', 'Creative & Personal Writing', 2, '[{\"changed\": {\"fields\": [\"Category url\"]}}]', 38, 'fe410b51-cbc2-4205-861a-c820f6dda5be'),
(47, '2025-11-19 18:19:05.758789', '1b3a9818-5ad8-42b0-acc6-ece065abe250', 'Graphics & Design', 2, '[{\"changed\": {\"fields\": [\"Sub categories\", \"Sort order\"]}}]', 38, 'fe410b51-cbc2-4205-861a-c820f6dda5be'),
(48, '2025-11-19 18:20:25.545920', '1b3a9818-5ad8-42b0-acc6-ece065abe250', 'Graphics & Design', 2, '[{\"changed\": {\"fields\": [\"Category url\"]}}]', 38, 'fe410b51-cbc2-4205-861a-c820f6dda5be'),
(49, '2025-11-19 18:25:44.744781', '6550a32a-b3ac-4547-a47a-fa0ce4fb4a68', 'Tutoring & Instructional Support', 2, '[{\"changed\": {\"fields\": [\"Name\", \"Slug\", \"Sub categories\", \"Sort order\"]}}]', 38, 'fe410b51-cbc2-4205-861a-c820f6dda5be'),
(50, '2025-11-19 18:27:15.918143', '6550a32a-b3ac-4547-a47a-fa0ce4fb4a68', 'Tutoring & Instructional Support', 2, '[{\"changed\": {\"fields\": [\"Category url\"]}}]', 38, 'fe410b51-cbc2-4205-861a-c820f6dda5be'),
(51, '2025-11-19 18:29:35.215910', '648c73ad-997d-4d5c-a744-21be6d7efd43', 'Digital Marketing', 1, '[{\"added\": {}}]', 38, 'fe410b51-cbc2-4205-861a-c820f6dda5be'),
(52, '2025-11-19 18:35:00.097848', 'ff4135bc-38f4-4c35-9ff2-15ed42f1e22b', 'AI & Automation Services', 1, '[{\"added\": {}}]', 38, 'fe410b51-cbc2-4205-861a-c820f6dda5be'),
(53, '2025-11-19 18:36:41.603378', '648c73ad-997d-4d5c-a744-21be6d7efd43', 'Digital Marketing', 2, '[{\"changed\": {\"fields\": [\"Category url\"]}}]', 38, 'fe410b51-cbc2-4205-861a-c820f6dda5be'),
(54, '2025-11-19 20:43:36.810328', '1', 'WordKnox', 2, '[{\"changed\": {\"fields\": [\"Heading\"]}}]', 21, 'fe410b51-cbc2-4205-861a-c820f6dda5be'),
(55, '2025-11-20 11:04:58.213822', 'a623fdf7-848b-4748-a265-c261426fbab6', 'Essay Writing', 1, '[{\"added\": {}}, {\"added\": {\"name\": \"Service Pricing Tier\", \"object\": \"Essay Writing - Standard\"}}]', 39, 'fe410b51-cbc2-4205-861a-c820f6dda5be'),
(56, '2025-11-20 12:06:15.327866', 'a623fdf7-848b-4748-a265-c261426fbab6', 'Essay Writing', 2, '[]', 39, 'e6b5cd4a-2f9f-4197-95d0-f0a66d7764dd'),
(57, '2025-11-24 19:52:47.662084', '2', 'Explore Services', 1, '[{\"added\": {}}]', 21, 'fe410b51-cbc2-4205-861a-c820f6dda5be');

-- --------------------------------------------------------

--
-- Table structure for table `django_content_type`
--

CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `django_content_type`
--

INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES
(16, 'accounts', 'clientprofile'),
(17, 'accounts', 'partner'),
(15, 'accounts', 'user'),
(6, 'admin', 'logentry'),
(8, 'auth', 'group'),
(7, 'auth', 'permission'),
(11, 'authtoken', 'token'),
(12, 'authtoken', 'tokenproxy'),
(36, 'blog', 'blogcomment'),
(33, 'blog', 'blogpost'),
(35, 'blog', 'blogposttag'),
(34, 'blog', 'tag'),
(54, 'business', 'contactmessage'),
(60, 'business', 'notification'),
(55, 'business', 'order'),
(56, 'business', 'payment'),
(57, 'business', 'paypalpayment'),
(58, 'business', 'servicerequest'),
(59, 'business', 'testimonial'),
(9, 'contenttypes', 'contenttype'),
(18, 'core', 'aboutsection'),
(19, 'core', 'aboutstats'),
(20, 'core', 'contactinfo'),
(21, 'core', 'herosection'),
(22, 'core', 'newslettersubscription'),
(23, 'core', 'roadmap'),
(27, 'core', 'supportattachment'),
(26, 'core', 'supportticket'),
(24, 'core', 'whychooseus'),
(25, 'core', 'workexperience'),
(47, 'products', 'product'),
(51, 'products', 'productgalleryimage'),
(52, 'products', 'productpurchase'),
(53, 'products', 'productreview'),
(48, 'products', 'producttag'),
(49, 'products', 'producttechnology'),
(50, 'products', 'productupdate'),
(28, 'projects', 'project'),
(31, 'projects', 'projectcomment'),
(32, 'projects', 'projectgalleryimage'),
(61, 'projects', 'projectsection'),
(30, 'projects', 'projecttechnology'),
(29, 'projects', 'technology'),
(42, 'services', 'pricingtierfeature'),
(39, 'services', 'service'),
(38, 'services', 'servicecategory'),
(40, 'services', 'servicedeliverable'),
(41, 'services', 'servicefaq'),
(37, 'services', 'servicefeature'),
(43, 'services', 'servicepopularusecase'),
(44, 'services', 'servicepricingtier'),
(45, 'services', 'serviceprocessstep'),
(46, 'services', 'servicetool'),
(10, 'sessions', 'session'),
(1, 'social_django', 'association'),
(2, 'social_django', 'code'),
(3, 'social_django', 'nonce'),
(5, 'social_django', 'partial'),
(4, 'social_django', 'usersocialauth'),
(13, 'token_blacklist', 'blacklistedtoken'),
(14, 'token_blacklist', 'outstandingtoken');

-- --------------------------------------------------------

--
-- Table structure for table `django_migrations`
--

CREATE TABLE `django_migrations` (
  `id` bigint(20) NOT NULL,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `django_migrations`
--

INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES
(138, 'contenttypes', '0001_initial', '2025-12-04 09:41:40.576633');

-- --------------------------------------------------------

--
-- Table structure for table `django_session`
--

CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `django_session`
--

INSERT INTO `django_session` (`session_key`, `session_data`, `expire_date`) VALUES
('0by5yshg89of8ea4eb5qbl1roslhztwb', '.eJxVjksOwjAMRO-SNY3itE4CS_acobIdhxZQK_WzQtydVuoCZjvvjeZtWlqXrl1nndo-m4sp2oBjhEpYfNV4h1UKQJUk70rImZDVnH41JnnqsLv5QcN9tDIOy9Sz3RF7tLO9jVlf14P9G-ho7jabIrrCmB1CjFF4SyT2mBVTTL6IOAFfbw_AK8O5joEJAjYpiHpH5vMFMedBpg:1vERnL:ivIrjx8cmIWjywQGOlRNWLmBwtLMCkYf22WguIFawZE', '2025-11-13 12:30:23.420356'),
('7s6jhtxs9ubjbmwi2206bll8nnzhgobf', '.eJxVjEsOgzAMRO-SdRMFsGPSZfc9A3LspPQjkPisqt69ILFolzPz3rxNx-vSd-ucp-6u5mxySCgKbOsSi4Uqko2o3hbPIShRAFVz-tUSyzMPu6sPHm6jk3FYpntyO-KOdXbXUfPrcrB_Bz3P_Wa3LQlQoSRYN5SjIIPUvgmw9QqKAqEUX7YQamiq7BUJkyZsIbOS-XwBH4lBlQ:1vM28r:QoAlDiaDqUNOCU2crlSRQQa1dsF-0_blrf9g6KR2CYc', '2025-12-04 10:43:57.960352'),
('bp8hx8fuviq1a021uki0w04so33sqhh5', '.eJxVjksOwjAMRO-SNY3itE4CS_acobIdhxZQK_WzQtydVuoCZjvvjeZtWlqXrl1nndo-m4sp2oBjhEpYfNV4h1UKQJUk70rImZDVnH41JnnqsLv5QcN9tDIOy9Sz3RF7tLO9jVlf14P9G-ho7jabIrrCmB1CjFF4SyT2mBVTTL6IOAFfbw_AK8O5joEJAjYpiHpH5vMFMedBpg:1v7FS1:vfwG2I_j-NKvHtL04ArQ7wehfOs_76xIBksLqERP69A', '2025-10-24 15:54:37.798370'),
('ou32kzae54i73yi2q6c3kb3fw9wrvuwh', '.eJxVzDsOwjAQRdG9uMaWjT_xUNKzhmjGMyYBFEv5VIi9o0gpoH73vLfqcVuHfltk7kdWFyWJYuGA-lyh6uCg0xDZ6moxJe66FJjV6ZcRlqdMu-UHTvdmSpvWeSSzJ-ZYF3NrLK_r0f4dDLgMuyb22QFERJRCPqVQoHK0TjKhZ8TirCvB-RwJcqIg1op48IEdelSfL0XtQf0:1vCF1B:_1uVOxudd7rlFRmai3W2XtxTpzwUsEZsKuY6cxLlf6Q', '2025-11-07 10:27:33.812005'),
('p3kbb3q4fzsz0hkau8xwfbz1w463n0rn', '.eJxVjksOwjAMRO-SNY3itE4CS_acobIdhxZQK_WzQtydVuoCZjvvjeZtWlqXrl1nndo-m4sp2oBjhEpYfNV4h1UKQJUk70rImZDVnH41JnnqsLv5QcN9tDIOy9Sz3RF7tLO9jVlf14P9G-ho7jabIrrCmB1CjFF4SyT2mBVTTL6IOAFfbw_AK8O5joEJAjYpiHpH5vMFMedBpg:1vLduZ:ZRVjS5DIGYqUodQDzp3EeVDr6nILnoJqTyYYLqQnoYA', '2025-12-03 08:51:35.952397'),
('q48z05lmacctas7icsnrc5amc9636k08', '.eJxVzMsOwiAQheF3YS0EOkMBl-59hmZgBls1bdLLyvju2qQLXZ__Oy_V0bb23bbI3A2szqoAYghAmmOuGqOIjlKq9pbRJQ8o3qrTL8tUHjLulu803iZTpnGdh2z2xBzrYq4Ty_NytH8HPS39V8c2pWQdQ0XHQSiKjYgVU5EmAIPP5Kw4sZ6BApfQeFtzTC14wYSten8A7dRApQ:1vCEfq:_qvlualW24_rdKTwkR-twcvFbcPjJa9TvOkK4cNr4mM', '2025-11-07 10:05:30.179593'),
('sfmbtj11225xperddyyzele6dmptdrmb', '.eJxVjksOwjAMRO-SNY3itE4CS_acobIdhxZQK_WzQtydVuoCZjvvjeZtWlqXrl1nndo-m4sp2oBjhEpYfNV4h1UKQJUk70rImZDVnH41JnnqsLv5QcN9tDIOy9Sz3RF7tLO9jVlf14P9G-ho7jabIrrCmB1CjFF4SyT2mBVTTL6IOAFfbw_AK8O5joEJAjYpiHpH5vMFMedBpg:1v7FPi:R9K-nuu8zEMtjBoIAvB9dm9vTeVQyGSX3mDqXQ8UUt4', '2025-10-24 15:52:14.683346'),
('suz85517y1e2u08ltwq4rkgpw5xsoax2', '.eJxVjEsOgzAMRO-SdRMFsGPSZfc9A3LspPQjkPisqt69ILFolzPz3rxNx-vSd-ucp-6u5mxySCgKbOsSi4Uqko2o3hbPIShRAFVz-tUSyzMPu6sPHm6jk3FYpntyO-KOdXbXUfPrcrB_Bz3P_Wa3LQlQoSRYN5SjIIPUvgmw9QqKAqEUX7YQamiq7BUJkyZsIbOS-XwBH4lBlQ:1vM2CB:e2sMoI243gm4EZWnZINAuSnWgG4BbNxrBaIN0WrcFNw', '2025-12-04 10:47:23.237900'),
('y8com9925sjdtixb828az0jhno1d1ahz', '.eJxVjEsOgzAMRO-SdRMFsGPSZfc9A3LspPQjkPisqt69ILFolzPz3rxNx-vSd-ucp-6u5mxySCgKbOsSi4Uqko2o3hbPIShRAFVz-tUSyzMPu6sPHm6jk3FYpntyO-KOdXbXUfPrcrB_Bz3P_Wa3LQlQoSRYN5SjIIPUvgmw9QqKAqEUX7YQamiq7BUJkyZsIbOS-XwBH4lBlQ:1vOYUY:reRAkOjYvTUsTcASgZZba8LjyiWcM9nwKEO7y9APWzA', '2025-12-11 09:40:46.558020'),
('z98y3x7cpmp83rkx1ha5eatk62sc2943', '.eJxVjksOwjAMRO-SNY3itE4CS_acobIdhxZQK_WzQtydVuoCZjvvjeZtWlqXrl1nndo-m4sp2oBjhEpYfNV4h1UKQJUk70rImZDVnH41JnnqsLv5QcN9tDIOy9Sz3RF7tLO9jVlf14P9G-ho7jabIrrCmB1CjFF4SyT2mBVTTL6IOAFfbw_AK8O5joEJAjYpiHpH5vMFMedBpg:1v7GRD:4Z9OeoYv-x3-p0--XmAcwVgZjNVkQWmhTCTbWfv6neY', '2025-10-24 16:57:51.671338');

-- --------------------------------------------------------

--
-- Table structure for table `hero_section`
--

CREATE TABLE `hero_section` (
  `id` int(11) NOT NULL,
  `page` varchar(20) NOT NULL,
  `heading` varchar(255) NOT NULL,
  `subheading` varchar(500) NOT NULL,
  `cta_text` varchar(100) NOT NULL,
  `cta_link` longtext NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_created` datetime(6) NOT NULL,
  `date_updated` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `hero_section`
--

INSERT INTO `hero_section` (`id`, `page`, `heading`, `subheading`, `cta_text`, `cta_link`, `is_active`, `date_created`, `date_updated`) VALUES
(1, 'home', 'WordKnox', 'Get high quality work in no time', 'Request Order', '/request_service', 1, '2025-10-10 15:03:29.442835', '2025-11-19 20:43:36.809760'),
(2, 'services', 'Explore Services', '', '', '', 1, '2025-11-24 19:52:47.660320', '2025-11-24 19:52:47.661653');

-- --------------------------------------------------------

--
-- Table structure for table `newsletter_subscription`
--

CREATE TABLE `newsletter_subscription` (
  `id` bigint(20) NOT NULL,
  `email` varchar(254) NOT NULL,
  `date_subscribed` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- --------------------------------------------------------

--
-- Table structure for table `notification`
--

CREATE TABLE `notification` (
  `id` varchar(36) NOT NULL,
  `type` varchar(20) NOT NULL,
  `title` varchar(255) NOT NULL,
  `subject` varchar(255) NOT NULL,
  `message` longtext NOT NULL,
  `is_read` tinyint(1) NOT NULL,
  `priority` varchar(10) NOT NULL,
  `resource_id` varchar(36) NOT NULL,
  `resource_type` varchar(50) NOT NULL,
  `date_created` datetime(6) NOT NULL,
  `user_id` varchar(36) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- --------------------------------------------------------

--
-- Table structure for table `order`
--

CREATE TABLE `order` (
  `id` varchar(36) NOT NULL,
  `total_amount` decimal(12,2) NOT NULL,
  `currency` varchar(10) NOT NULL,
  `status` varchar(20) NOT NULL,
  `payment_status` varchar(20) NOT NULL,
  `payment_method` varchar(50) NOT NULL,
  `transaction_id` varchar(255) NOT NULL,
  `notes` longtext NOT NULL,
  `due_date` date DEFAULT NULL,
  `attachments` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL CHECK (json_valid(`attachments`)),
  `work_results` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL CHECK (json_valid(`work_results`)),
  `date_created` datetime(6) NOT NULL,
  `date_updated` datetime(6) NOT NULL,
  `client_id` varchar(36) NOT NULL,
  `pricing_tier_id` varchar(36) DEFAULT NULL,
  `product_id` varchar(36) DEFAULT NULL,
  `service_id` varchar(36) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `order`
--

INSERT INTO `order` (`id`, `total_amount`, `currency`, `status`, `payment_status`, `payment_method`, `transaction_id`, `notes`, `due_date`, `attachments`, `work_results`, `date_created`, `date_updated`, `client_id`, `pricing_tier_id`, `product_id`, `service_id`) VALUES
('21585dd0-46ee-4ef2-bdf5-b9ebaed43988', 200.00, 'KSH', 'pending', 'pending', '', '', 'Created from service request: Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry\'s standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.', NULL, '[\"b1e80d8b92d848faafdabd6a58ec054c_Full_stack_Blockchain_Developer.doc\"]', '[]', '2025-10-24 10:35:17.946795', '2025-10-24 10:35:17.947098', '81219bde-c597-416a-bfbf-bfd2b2fa36f1', NULL, NULL, '6bd424a8-38b6-4bc3-9264-221a305d10d6');

-- --------------------------------------------------------

--
-- Table structure for table `payment`
--

CREATE TABLE `payment` (
  `id` varchar(36) NOT NULL,
  `amount` decimal(12,2) NOT NULL,
  `currency` varchar(10) NOT NULL,
  `method` varchar(50) NOT NULL,
  `transaction_id` varchar(255) NOT NULL,
  `status` varchar(20) NOT NULL,
  `notes` longtext NOT NULL,
  `date_created` datetime(6) NOT NULL,
  `order_id` varchar(36) DEFAULT NULL,
  `user_id` varchar(36) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- --------------------------------------------------------

--
-- Table structure for table `paypal_payment`
--

CREATE TABLE `paypal_payment` (
  `id` bigint(20) NOT NULL,
  `paypal_order_id` varchar(255) NOT NULL,
  `paypal_payer_id` varchar(255) DEFAULT NULL,
  `paypal_payer_email` varchar(254) DEFAULT NULL,
  `paypal_payment_id` varchar(255) DEFAULT NULL,
  `paypal_status` varchar(50) NOT NULL,
  `paypal_intent` varchar(20) NOT NULL,
  `paypal_create_time` datetime(6) DEFAULT NULL,
  `paypal_update_time` datetime(6) DEFAULT NULL,
  `paypal_data` longtext DEFAULT NULL,
  `is_balance_deposit` tinyint(1) NOT NULL,
  `payment_id` varchar(36) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- --------------------------------------------------------

--
-- Table structure for table `pricingtier_feature`
--

CREATE TABLE `pricingtier_feature` (
  `id` bigint(20) NOT NULL,
  `feature_id` varchar(36) NOT NULL,
  `pricing_tier_id` varchar(36) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- --------------------------------------------------------

--
-- Table structure for table `product`
--

CREATE TABLE `product` (
  `id` varchar(36) NOT NULL,
  `name` varchar(255) NOT NULL,
  `slug` varchar(255) NOT NULL,
  `category` varchar(100) NOT NULL,
  `type` varchar(20) NOT NULL,
  `description` longtext NOT NULL,
  `short_description` longtext NOT NULL,
  `image_url` longtext NOT NULL,
  `price` decimal(12,2) NOT NULL,
  `currency` varchar(10) NOT NULL,
  `demo_url` longtext NOT NULL,
  `download_url` longtext NOT NULL,
  `repository_url` longtext NOT NULL,
  `documentation_url` longtext NOT NULL,
  `featured` tinyint(1) NOT NULL,
  `active` tinyint(1) NOT NULL,
  `download_count` int(11) NOT NULL,
  `version` varchar(20) NOT NULL,
  `license_type` varchar(20) NOT NULL,
  `requirements` longtext NOT NULL,
  `installation_notes` longtext NOT NULL,
  `date_created` datetime(6) NOT NULL,
  `date_updated` datetime(6) NOT NULL,
  `base_project_id` varchar(36) DEFAULT NULL,
  `creator_id` varchar(36) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- --------------------------------------------------------

--
-- Table structure for table `product_gallery_image`
--

CREATE TABLE `product_gallery_image` (
  `id` int(11) NOT NULL,
  `image_url` longtext NOT NULL,
  `alt_text` varchar(255) NOT NULL,
  `sort_order` int(11) NOT NULL,
  `product_id` varchar(36) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- --------------------------------------------------------

--
-- Table structure for table `product_purchase`
--

CREATE TABLE `product_purchase` (
  `id` varchar(36) NOT NULL,
  `purchase_amount` decimal(12,2) NOT NULL,
  `currency` varchar(10) NOT NULL,
  `status` varchar(20) NOT NULL,
  `download_count` int(11) NOT NULL,
  `download_limit` int(11) DEFAULT NULL,
  `license_key` varchar(255) NOT NULL,
  `expires_at` datetime(6) DEFAULT NULL,
  `payment_method` varchar(50) NOT NULL,
  `transaction_id` varchar(255) NOT NULL,
  `date_created` datetime(6) NOT NULL,
  `date_updated` datetime(6) NOT NULL,
  `client_id` varchar(36) NOT NULL,
  `product_id` varchar(36) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- --------------------------------------------------------

--
-- Table structure for table `product_review`
--

CREATE TABLE `product_review` (
  `id` varchar(36) NOT NULL,
  `rating` int(11) NOT NULL,
  `review_text` longtext NOT NULL,
  `approved` tinyint(1) NOT NULL,
  `date_created` datetime(6) NOT NULL,
  `client_id` varchar(36) NOT NULL,
  `product_id` varchar(36) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- --------------------------------------------------------

--
-- Table structure for table `product_tag`
--

CREATE TABLE `product_tag` (
  `id` bigint(20) NOT NULL,
  `product_id` varchar(36) NOT NULL,
  `tag_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- --------------------------------------------------------

--
-- Table structure for table `product_technology`
--

CREATE TABLE `product_technology` (
  `id` bigint(20) NOT NULL,
  `product_id` varchar(36) NOT NULL,
  `technology_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- --------------------------------------------------------

--
-- Table structure for table `product_update`
--

CREATE TABLE `product_update` (
  `id` varchar(36) NOT NULL,
  `version` varchar(20) NOT NULL,
  `title` varchar(255) NOT NULL,
  `description` longtext NOT NULL,
  `download_url` longtext NOT NULL,
  `is_major` tinyint(1) NOT NULL,
  `date_created` datetime(6) NOT NULL,
  `product_id` varchar(36) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- --------------------------------------------------------

--
-- Table structure for table `project`
--

CREATE TABLE `project` (
  `id` varchar(36) NOT NULL,
  `title` varchar(255) NOT NULL,
  `slug` varchar(255) NOT NULL,
  `category` varchar(100) NOT NULL,
  `domain` varchar(100) NOT NULL,
  `sections` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL CHECK (json_valid(`sections`)),
  `description` longtext NOT NULL,
  `content` longtext NOT NULL,
  `url` longtext NOT NULL,
  `repository_url` longtext NOT NULL,
  `likes` int(11) NOT NULL,
  `featured` tinyint(1) NOT NULL,
  `completion_date` date DEFAULT NULL,
  `status` varchar(20) NOT NULL,
  `date_created` datetime(6) NOT NULL,
  `date_updated` datetime(6) NOT NULL,
  `author_id` varchar(36) DEFAULT NULL,
  `client_id` varchar(36) DEFAULT NULL,
  `image` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `project`
--

INSERT INTO `project` (`id`, `title`, `slug`, `category`, `domain`, `sections`, `description`, `content`, `url`, `repository_url`, `likes`, `featured`, `completion_date`, `status`, `date_created`, `date_updated`, `author_id`, `client_id`, `image`) VALUES
('36a8ea04-f582-4d90-a2ca-046ee1336abc', 'E-commerce Site', 'e-commerce-site', 'Tech', '', '[]', 'Modern e-commerce platforms offer a robust suite of features designed to streamline online shopping and enhance user experience. Key functionalities include intuitive product search and filtering, personalized recommendations, and responsive design for seamless browsing on any device. Secure payment gateways support multiple payment options, such as credit cards, digital wallets, and buy-now-pay-later services. Real-time inventory management ensures product availability and accurate order processing. Integrated shopping carts, wishlists, and one-click checkout accelerate the purchasing process. Customer accounts and order tracking provide transparency and convenience. Platforms often include review systems to build trust and facilitate informed decisions. Advanced analytics support sales optimization, while marketing tools like email campaigns, abandoned cart recovery, and discount codes drive engagement. Support for international shipping, multi-language, and multi-currency capabilities enables global reach. Robust security measures and compliance with data protection regulations safeguard customer information, making modern e-commerce both user-friendly and trustworthy.', '', 'www.poshabodes.co.ke', '', 0, 0, '2025-08-20', 'completed', '2025-10-24 08:55:25.998269', '2025-10-24 08:55:26.013756', '81219bde-c597-416a-bfbf-bfd2b2fa36f1', NULL, 'projects/featured/9d792385-0b34-4cfe-baa2-5690034f1e49-cover.jpg');

-- --------------------------------------------------------

--
-- Table structure for table `project_comment`
--

CREATE TABLE `project_comment` (
  `id` varchar(36) NOT NULL,
  `name` varchar(255) NOT NULL,
  `email` varchar(254) NOT NULL,
  `message` longtext NOT NULL,
  `approved` tinyint(1) NOT NULL,
  `date_created` datetime(6) NOT NULL,
  `project_id` varchar(36) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- --------------------------------------------------------

--
-- Table structure for table `project_gallery_image`
--

CREATE TABLE `project_gallery_image` (
  `id` int(11) NOT NULL,
  `alt_text` varchar(255) NOT NULL,
  `sort_order` int(11) NOT NULL,
  `project_id` varchar(36) NOT NULL,
  `image` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `project_gallery_image`
--

INSERT INTO `project_gallery_image` (`id`, `alt_text`, `sort_order`, `project_id`, `image`) VALUES
(1, '', 0, '36a8ea04-f582-4d90-a2ca-046ee1336abc', 'projects/gallery/9d792385-0b34-4cfe-baa2-5690034f1e49-cover.jpg');

-- --------------------------------------------------------

--
-- Table structure for table `project_section`
--

CREATE TABLE `project_section` (
  `id` int(11) NOT NULL,
  `section_id` varchar(50) NOT NULL,
  `section_name` varchar(100) NOT NULL,
  `media` varchar(100) DEFAULT NULL,
  `description` longtext NOT NULL,
  `sort_order` int(11) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_created` datetime(6) NOT NULL,
  `project_id` varchar(36) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- --------------------------------------------------------

--
-- Table structure for table `project_technology`
--

CREATE TABLE `project_technology` (
  `id` bigint(20) NOT NULL,
  `project_id` varchar(36) NOT NULL,
  `technology_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- --------------------------------------------------------

--
-- Table structure for table `roadmap`
--

CREATE TABLE `roadmap` (
  `id` bigint(20) NOT NULL,
  `milestone_title` varchar(200) NOT NULL,
  `milestone_description` longtext NOT NULL,
  `target_date` date DEFAULT NULL,
  `is_completed` tinyint(1) NOT NULL,
  `completion_date` date DEFAULT NULL,
  `icon_name` varchar(50) NOT NULL,
  `display_order` int(11) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_created` datetime(6) NOT NULL,
  `date_updated` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `roadmap`
--

INSERT INTO `roadmap` (`id`, `milestone_title`, `milestone_description`, `target_date`, `is_completed`, `completion_date`, `icon_name`, `display_order`, `is_active`, `date_created`, `date_updated`) VALUES
(1, 'Send Order Proposal', 'Fill out the order request form, specifying the details of the task or project you wish to request.  Be sure to include specific details of your work, along with any relevant attachment documents, to help us deliver a solution that meets your precise needs.', NULL, 0, NULL, '', 0, 1, '2025-11-13 07:49:10.348598', '2025-11-13 07:49:10.348634'),
(2, 'Confirm Order & Make Payment', 'Upon receipt of your request, we respond within minutes.  One, you will receive a quotation for the order via email. Additionally, a team member will be assigned to support and ensure work delivery.  Once you click the \"Confirm Order\" button attached to the email or make a payment for the service down payment, your order is placed \"In progress\".', NULL, 0, NULL, '', 1, 1, '2025-11-13 07:54:36.244843', '2025-11-13 08:26:20.674965'),
(3, 'Service Delivery & Review', 'During the service delivery phase, we utilize our official communication channels to keep you updated on project status and can provide a draft of the work upon request. An email is sent upon order completion, along with a preview of the work. The work results are available for download upon full payment release. We appreciate feedback on service completion to help us enhance the quality of our service.', NULL, 0, NULL, '', 2, 1, '2025-11-13 08:25:57.763200', '2025-11-13 08:26:41.629930');

-- --------------------------------------------------------

--
-- Table structure for table `service`
--

CREATE TABLE `service` (
  `id` varchar(36) NOT NULL,
  `name` varchar(255) NOT NULL,
  `slug` varchar(255) NOT NULL,
  `description` longtext NOT NULL,
  `short_description` longtext NOT NULL,
  `img_url` longtext NOT NULL,
  `banner_url` longtext NOT NULL,
  `icon_url` longtext NOT NULL,
  `pricing_model` varchar(20) NOT NULL,
  `starting_at` decimal(12,2) DEFAULT NULL,
  `currency` varchar(10) NOT NULL,
  `timeline` varchar(100) NOT NULL,
  `featured` tinyint(1) NOT NULL,
  `active` tinyint(1) NOT NULL,
  `sort_order` int(11) NOT NULL,
  `date_created` datetime(6) NOT NULL,
  `date_updated` datetime(6) NOT NULL,
  `service_category_id` varchar(36) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `service`
--

INSERT INTO `service` (`id`, `name`, `slug`, `description`, `short_description`, `img_url`, `banner_url`, `icon_url`, `pricing_model`, `starting_at`, `currency`, `timeline`, `featured`, `active`, `sort_order`, `date_created`, `date_updated`, `service_category_id`) VALUES
('6bd424a8-38b6-4bc3-9264-221a305d10d6', 'Website Development', 'website-development', 'I\'ve rented a car in Las Vegas and have reserved a hotel in Twentynine Palms which is just north of Joshua Tree. We\'ll drive from Las Vegas through Mojave National Preserve and possibly do a short hike on our way down. Then spend all day on Monday at Joshua Tree. We can decide the next morning if we want to do more in Joshua Tree or Mojave before we head back.', '', 'https://images.pexels.com/photos/15717260/pexels-photo-15717260.jpeg', '', '', 'tiered', 100.00, '$', '', 0, 1, 0, '2025-10-10 16:46:55.546644', '2025-11-13 06:43:36.505145', '0ddd55f1-f736-4659-ac41-441ccc9b2d94'),
('a623fdf7-848b-4748-a265-c261426fbab6', 'Essay Writing', 'essay-writing', 'Professional academic writing support for high school, college, and university students. Our expert writers provide ethical assistance with essays, reviews, research papers, and academic consultations. We help students understand proper structure, develop strong arguments, and improve their writing skills while maintaining academic integrity. Services include essay drafting, editing, proofreading, literature reviews, and personalized academic coaching to help you succeed in your studies.', '', '', '', '', 'tiered', 4.00, '$', '', 0, 1, 0, '2025-11-20 11:04:58.186339', '2025-11-20 12:06:15.327051', 'a3562560-4b2b-4873-82e1-dbaa6ee700cc');

-- --------------------------------------------------------

--
-- Table structure for table `service_category`
--

CREATE TABLE `service_category` (
  `id` varchar(36) NOT NULL,
  `name` varchar(100) NOT NULL,
  `slug` varchar(100) NOT NULL,
  `short_desc` longtext NOT NULL,
  `category_url` varchar(100) DEFAULT NULL,
  `sub_categories` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL CHECK (json_valid(`sub_categories`)),
  `active` tinyint(1) NOT NULL,
  `sort_order` int(11) NOT NULL,
  `date_created` datetime(6) NOT NULL,
  `date_updated` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `service_category`
--

INSERT INTO `service_category` (`id`, `name`, `slug`, `short_desc`, `category_url`, `sub_categories`, `active`, `sort_order`, `date_created`, `date_updated`) VALUES
('0ddd55f1-f736-4659-ac41-441ccc9b2d94', 'Programming & Data', 'Programming-and-data', '', 'category_icons/backend.png', '[{\"id\": \"coding-assignment\", \"name\": \"Coding Assignment\"}, {\"id\": \"code-review\", \"name\": \"Code Review & Debugging\"}, {\"id\": \"algorithm-design\", \"name\": \"Algorithm Design\"}, {\"id\": \"project-development\", \"name\": \"Project Development\"}, {\"id\": \"script-writing\", \"name\": \"Script Writing (Python/R/JavaScript/etc.)\"}, {\"id\": \"data-analysis\", \"name\": \"Data Analysis\"}, {\"id\": \"data-visualization\", \"name\": \"Data Visualization\"}, {\"id\": \"data-cleaning\", \"name\": \"Data Cleaning & Preparation\"}, {\"id\": \"database-design\", \"name\": \"Database Design & Modeling\"}, {\"id\": \"api-development\", \"name\": \"API Development\"}, {\"id\": \"machine-learning\", \"name\": \"Machine Learning Projects\"}, {\"id\": \"web-scraping\", \"name\": \"Web Scraping\"}, {\"id\": \"automation-script\", \"name\": \"Automation Scripting\"}, {\"id\": \"documentation\", \"name\": \"Code Documentation & Tutorials\"}]', 1, 0, '2025-10-10 16:12:12.415855', '2025-11-19 18:06:16.341296'),
('18547e53-ab5b-46a4-a89b-5b36cc7943c5', 'Business & Professional Writing', 'business-professional-writing', 'Professional documents, career services, and presentation design', 'category_icons/business.png', '[{\"id\": \"business-plan\", \"name\": \"Business Plan\"}, {\"id\": \"resume\", \"name\": \"Resume\"}, {\"id\": \"cover-letter\", \"name\": \"Cover Letter\"}, {\"id\": \"cv\", \"name\": \"Curriculum Vitae (CV)\"}, {\"id\": \"application-letter\", \"name\": \"Application Letter\"}, {\"id\": \"presentation\", \"name\": \"Presentation\"}, {\"id\": \"ppt-presentation\", \"name\": \"PowerPoint Presentation\"}, {\"id\": \"poster-presentation\", \"name\": \"Poster Presentation\"}, {\"id\": \"speech\", \"name\": \"Speech\"}, {\"id\": \"typing\", \"name\": \"Typing & Editing\"}, {\"id\": \"profile-writing\", \"name\": \"Profile Writing\"}, {\"id\": \"statement-of-purpose\", \"name\": \"Statement of Purpose\"}, {\"id\": \"executive-summary\", \"name\": \"Executive Summary\"}]', 1, 0, '2025-10-10 16:11:37.031337', '2025-11-19 18:02:34.760198'),
('1b3a9818-5ad8-42b0-acc6-ece065abe250', 'Graphics & Design', 'graphics-design', '', 'category_icons/graphic-designer.png', '[{\"id\": \"logo-design\", \"name\": \"Logo Design\"}, {\"id\": \"poster-design\", \"name\": \"Poster Design\"}, {\"id\": \"flyer-design\", \"name\": \"Flyer Design\"}, {\"id\": \"banner-design\", \"name\": \"Banner Design\"}, {\"id\": \"social-media-graphics\", \"name\": \"Social Media Graphics\"}, {\"id\": \"brochure-design\", \"name\": \"Brochure Design\"}, {\"id\": \"business-card-design\", \"name\": \"Business Card Design\"}, {\"id\": \"infographic-design\", \"name\": \"Infographic Design\"}, {\"id\": \"photo-editing\", \"name\": \"Photo Editing\"}, {\"id\": \"video-editing\", \"name\": \"Video Editing\"}, {\"id\": \"thumbnail-design\", \"name\": \"Thumbnail Design\"}, {\"id\": \"presentation-design\", \"name\": \"Presentation Design (Slides)\"}, {\"id\": \"t-shirt-design\", \"name\": \"T-Shirt Design & Merchandise\"}, {\"id\": \"mockup-design\", \"name\": \"Mockup/Prototype Design\"}, {\"id\": \"animation\", \"name\": \"Basic Animation\"}, {\"id\": \"cover-design\", \"name\": \"Ebook/Cover Design\"}]', 1, 4, '2025-10-10 16:12:58.839655', '2025-11-19 18:20:25.544749'),
('5222ec79-ab29-4139-99e4-b9192f4f2f62', 'Web and Mobile Application', 'web-and-mobile-application', '', 'category_icons/mobile.png', '[{\"id\": \"website-development\", \"name\": \"Custom Website Development\"}, {\"id\": \"web-app-development\", \"name\": \"Web Application Development\"}, {\"id\": \"pwa-development\", \"name\": \"Progressive Web App (PWA) Development\"}, {\"id\": \"wordpress-services\", \"name\": \"WordPress Site Management\"}, {\"id\": \"wordpress-customization\", \"name\": \"WordPress Customization & Themes\"}, {\"id\": \"woocommerce-services\", \"name\": \"WooCommerce Store Setup & Management\"}, {\"id\": \"shopify-development\", \"name\": \"Shopify Store Development\"}, {\"id\": \"shopify-updates\", \"name\": \"Shopify Maintenance & Updates\"}, {\"id\": \"site-maintenance\", \"name\": \"Site Maintenance & Updates\"}, {\"id\": \"ecommerce-solutions\", \"name\": \"E-Commerce Platform Solutions\"}, {\"id\": \"mobile-app-development\", \"name\": \"Mobile App Development (Android/iOS)\"}, {\"id\": \"cross-platform-apps\", \"name\": \"Cross-Platform App Development (Flutter/React Native)\"}, {\"id\": \"landing-page-design\", \"name\": \"Landing Page Design\"}, {\"id\": \"ui-ux-design\", \"name\": \"UI/UX Design & Prototyping\"}, {\"id\": \"web-performance-optimization\", \"name\": \"Web Performance Optimization\"}, {\"id\": \"cms-integration\", \"name\": \"CMS Integration (Drupal, Joomla, etc.)\"}, {\"id\": \"site-migration\", \"name\": \"Website Migration & Hosting Setup\"}, {\"id\": \"api-integration\", \"name\": \"API Integration & Third-Party Services\"}, {\"id\": \"custom-plugin-development\", \"name\": \"Custom Plugin/Module Development\"}, {\"id\": \"security-audit\", \"name\": \"Website & App Security Audit\"}]', 1, 1, '2025-10-10 16:13:38.529572', '2025-11-19 18:12:04.577179'),
('648c73ad-997d-4d5c-a744-21be6d7efd43', 'Digital Marketing', 'digital-marketing', '', 'category_icons/icons8-digital-marketing-50.png', '[{\"id\": \"social-media-campaign\", \"name\": \"Social Media Campaign Design\"}, {\"id\": \"content-calendar\", \"name\": \"Content Calendar Creation\"}, {\"id\": \"profile-setup-optimization\", \"name\": \"Social Profile Setup & Optimization\"}, {\"id\": \"paid-ad-management\", \"name\": \"Paid Ad Management (Facebook/Instagram/Google)\"}, {\"id\": \"basic-seo\", \"name\": \"Basic SEO Optimization\"}, {\"id\": \"email-marketing\", \"name\": \"Email Newsletter Design & Setup\"}, {\"id\": \"engagement-analytics\", \"name\": \"Campaign Analytics & Performance Reporting\"}, {\"id\": \"brand-identity\", \"name\": \"Brand Identity Design for Campaigns\"}, {\"id\": \"competitive-analysis\", \"name\": \"Basic Competitive Benchmarking\"}, {\"id\": \"template-design\", \"name\": \"Social Media Template/Asset Design\"}]', 1, 6, '2025-11-19 18:29:35.205419', '2025-11-19 18:36:41.602719'),
('6550a32a-b3ac-4547-a47a-fa0ce4fb4a68', 'Tutoring & Instructional Support', 'tutoring-and-instructional-support', '', 'category_icons/tutor.png', '[{\"id\": \"python-programming\", \"name\": \"Python Programming\"}, {\"id\": \"scratch-programming\", \"name\": \"Scratch Programming\"}, {\"id\": \"javascript-programming\", \"name\": \"JavaScript Programming\"}, {\"id\": \"modern-web-development\", \"name\": \"Modern Web Development\"}, {\"id\": \"swahili-lessons\", \"name\": \"Swahili Language Lessons\"}, {\"id\": \"english-language\", \"name\": \"English Language Lessons\"}, {\"id\": \"mathematics-tutoring\", \"name\": \"Mathematics Tutoring\"}, {\"id\": \"science-tutoring\", \"name\": \"Science Tutoring\"}, {\"id\": \"exam-prep\", \"name\": \"Exam Preparation\"}, {\"id\": \"study-skills\", \"name\": \"Study Skills & Academic Coaching\"}, {\"id\": \"ict-literacy\", \"name\": \"ICT Literacy & Computer Basics\"}, {\"id\": \"curriculum-design\", \"name\": \"Curriculum & Lesson Plan Design\"}, {\"id\": \"custom-workshop\", \"name\": \"Custom Workshop Sessions\"}, {\"id\": \"group-tutoring\", \"name\": \"Group Tutoring & Peer Support\"}]', 1, 5, '2025-10-10 16:12:46.995740', '2025-11-19 18:27:15.917516'),
('a3562560-4b2b-4873-82e1-dbaa6ee700cc', 'Essay Writing & Translation', 'academic-educational-writing', 'Essays, reviews, assignments, tutoring for students.', 'category_icons/education.png', '[{\"id\": \"essay\", \"name\": \"Standard Essay\"}, {\"id\": \"review\", \"name\": \"Book/Movie Review\"}, {\"id\": \"literature\", \"name\": \"Literature Review\"}, {\"id\": \"structure\", \"name\": \"Structure & Editing\"}, {\"id\": \"consultation\", \"name\": \"Academic Consultation\"}]', 1, 0, '2025-11-19 17:52:51.750727', '2025-11-19 18:13:08.703443'),
('fb631bb0-c771-4482-a89a-973fe8baa37a', 'Creative & Personal Writing', 'creative-and-personal-writing', '', 'category_icons/creative-writing.png', '[{\"id\": \"creative-writing\", \"name\": \"Creative Writing\"}, {\"id\": \"personal-statement\", \"name\": \"Personal Statement\"}, {\"id\": \"biography\", \"name\": \"Biography\"}, {\"id\": \"blog-writing\", \"name\": \"Blog Writing\"}, {\"id\": \"memoir\", \"name\": \"Memoir\"}, {\"id\": \"short-story\", \"name\": \"Short Story\"}, {\"id\": \"article-writing\", \"name\": \"Article Writing\"}, {\"id\": \"poetry\", \"name\": \"Poetry\"}, {\"id\": \"script-writing\", \"name\": \"Script Writing\"}, {\"id\": \"copywriting\", \"name\": \"Copywriting\"}, {\"id\": \"profile-writing\", \"name\": \"Profile Writing\"}, {\"id\": \"content-rewriting\", \"name\": \"Content Rewriting & Editing\"}, {\"id\": \"letter-writing\", \"name\": \"Letter Writing\"}, {\"id\": \"ghostwriting\", \"name\": \"Ghostwriting\"}]', 1, 3, '2025-10-10 16:11:21.875607', '2025-11-19 18:16:25.283967'),
('ff4135bc-38f4-4c35-9ff2-15ed42f1e22b', 'AI & Automation Services', 'ai-automation-services', 'AI-powered tools for students/individuals: essay review, data processing', 'category_icons/icons8-ai-48.png', '[{\"id\": \"ai-removal\", \"name\": \"AI Content Removal\"}, {\"id\": \"paraphrasing\", \"name\": \"AI Paraphrasing/Rewriting\"}, {\"id\": \"plagiarism-check\", \"name\": \"Plagiarism Check & Report\"}, {\"id\": \"synthetic-data-gen\", \"name\": \"Synthetic Data Generation\"}, {\"id\": \"smart-chatbot\", \"name\": \"Smart AI Chatbot Setup\"}, {\"id\": \"text-summarization\", \"name\": \"AI Text Summarization\"}, {\"id\": \"sentiment-analysis\", \"name\": \"Sentiment Analysis\"}, {\"id\": \"document-classification\", \"name\": \"Document Classification\"}, {\"id\": \"keyword-extraction\", \"name\": \"Keyword Extraction\"}, {\"id\": \"ocr-document\", \"name\": \"OCR Document Conversion\"}, {\"id\": \"language-translation\", \"name\": \"AI Language Translation\"}, {\"id\": \"readability-improvement\", \"name\": \"Readability Improvement\"}]', 1, 7, '2025-11-19 18:35:00.095260', '2025-11-19 18:35:00.097077');

-- --------------------------------------------------------

--
-- Table structure for table `service_deliverable`
--

CREATE TABLE `service_deliverable` (
  `id` varchar(36) NOT NULL,
  `description` longtext NOT NULL,
  `icon_class` varchar(50) NOT NULL,
  `sort_order` int(11) NOT NULL,
  `service_id` varchar(36) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- --------------------------------------------------------

--
-- Table structure for table `service_faq`
--

CREATE TABLE `service_faq` (
  `id` varchar(36) NOT NULL,
  `question` longtext NOT NULL,
  `answer` longtext NOT NULL,
  `sort_order` int(11) NOT NULL,
  `service_id` varchar(36) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- --------------------------------------------------------

--
-- Table structure for table `service_feature`
--

CREATE TABLE `service_feature` (
  `id` varchar(36) NOT NULL,
  `title` varchar(255) NOT NULL,
  `description` longtext NOT NULL,
  `icon_class` varchar(50) NOT NULL,
  `category` varchar(50) NOT NULL,
  `included` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- --------------------------------------------------------

--
-- Table structure for table `service_popular_usecase`
--

CREATE TABLE `service_popular_usecase` (
  `id` varchar(36) NOT NULL,
  `use_case` varchar(255) NOT NULL,
  `description` longtext NOT NULL,
  `service_id` varchar(36) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- --------------------------------------------------------

--
-- Table structure for table `service_pricing_tier`
--

CREATE TABLE `service_pricing_tier` (
  `id` varchar(36) NOT NULL,
  `name` varchar(100) NOT NULL,
  `price` decimal(12,2) NOT NULL,
  `currency` varchar(10) NOT NULL,
  `unit` varchar(50) NOT NULL,
  `estimated_delivery` varchar(50) NOT NULL,
  `recommended` tinyint(1) NOT NULL,
  `sort_order` int(11) NOT NULL,
  `service_id` varchar(36) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `service_pricing_tier`
--

INSERT INTO `service_pricing_tier` (`id`, `name`, `price`, `currency`, `unit`, `estimated_delivery`, `recommended`, `sort_order`, `service_id`) VALUES
('0ea4f818-1da5-4c3b-b84d-c056854ab00d', 'Standard', 3.50, '$', 'Per page', '', 0, 0, 'a623fdf7-848b-4748-a265-c261426fbab6'),
('3ac879e1-8dfc-4f3c-98e1-a3b305baa6da', 'Basic Website', 80.00, '$', 'Flat fee', '3 -7 Days', 1, 0, '6bd424a8-38b6-4bc3-9264-221a305d10d6'),
('57f04a37-5e4d-4113-90d3-9f0a5e98fe16', 'Pro Web Apps', 350.00, '$', 'Flat fee', '4-6 Weeks', 0, 2, '6bd424a8-38b6-4bc3-9264-221a305d10d6'),
('a63fe629-b498-4400-ac67-60ee0492b2f2', 'Standard Web App', 200.00, '$', 'Flat fee', '2 - 4 Weeks', 0, 1, '6bd424a8-38b6-4bc3-9264-221a305d10d6'),
('b819b30f-ef39-4b4e-b342-5844bcbf8a28', 'Premium Custom Web App', 600.00, '$', 'Flat fee', '10-12 Weeks', 0, 3, '6bd424a8-38b6-4bc3-9264-221a305d10d6');

-- --------------------------------------------------------

--
-- Table structure for table `service_process_step`
--

CREATE TABLE `service_process_step` (
  `id` varchar(36) NOT NULL,
  `step_order` int(11) NOT NULL,
  `title` varchar(255) NOT NULL,
  `description` longtext NOT NULL,
  `icon_class` varchar(50) NOT NULL,
  `service_id` varchar(36) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- --------------------------------------------------------

--
-- Table structure for table `service_request`
--

CREATE TABLE `service_request` (
  `attachment` varchar(100) DEFAULT NULL,
  `id` varchar(36) NOT NULL,
  `name` varchar(100) NOT NULL,
  `email` varchar(254) NOT NULL,
  `project_description` longtext NOT NULL,
  `budget` varchar(50) NOT NULL,
  `timeline` varchar(100) NOT NULL,
  `service_type` varchar(20) NOT NULL,
  `subject` varchar(255) NOT NULL,
  `citations` varchar(255) NOT NULL,
  `formatting_style` varchar(100) NOT NULL,
  `pages` int(10) UNSIGNED DEFAULT NULL CHECK (`pages` >= 0),
  `status` varchar(20) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `order_id` varchar(36) DEFAULT NULL,
  `pricing_tier_id` varchar(36) DEFAULT NULL,
  `service_id` varchar(36) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `service_request`
--

INSERT INTO `service_request` (`attachment`, `id`, `name`, `email`, `project_description`, `budget`, `timeline`, `service_type`, `subject`, `citations`, `formatting_style`, `pages`, `status`, `created_at`, `updated_at`, `order_id`, `pricing_tier_id`, `service_id`) VALUES
('service_requests/Full_stack_Blockchain_Developer.doc', '2c934cb8-53af-4fec-8954-a10a8de7643c', '', 'lewismutembei001@gmail.com', 'Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry\'s standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.', '', '2025-10-30T15:30', 'technical', '', '', '', NULL, 'converted', '2025-10-24 10:30:24.386702', '2025-10-24 10:35:17.956272', '21585dd0-46ee-4ef2-bdf5-b9ebaed43988', NULL, '6bd424a8-38b6-4bc3-9264-221a305d10d6');

-- --------------------------------------------------------

--
-- Table structure for table `service_tool`
--

CREATE TABLE `service_tool` (
  `id` varchar(36) NOT NULL,
  `tool_name` varchar(100) NOT NULL,
  `tool_url` varchar(200) NOT NULL,
  `icon_url` longtext NOT NULL,
  `service_id` varchar(36) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- --------------------------------------------------------

--
-- Table structure for table `social_auth_association`
--

CREATE TABLE `social_auth_association` (
  `id` bigint(20) NOT NULL,
  `server_url` varchar(255) NOT NULL,
  `handle` varchar(255) NOT NULL,
  `secret` varchar(255) NOT NULL,
  `issued` int(11) NOT NULL,
  `lifetime` int(11) NOT NULL,
  `assoc_type` varchar(64) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- --------------------------------------------------------

--
-- Table structure for table `social_auth_code`
--

CREATE TABLE `social_auth_code` (
  `id` bigint(20) NOT NULL,
  `email` varchar(254) NOT NULL,
  `code` varchar(32) NOT NULL,
  `verified` tinyint(1) NOT NULL,
  `timestamp` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- --------------------------------------------------------

--
-- Table structure for table `social_auth_nonce`
--

CREATE TABLE `social_auth_nonce` (
  `id` bigint(20) NOT NULL,
  `server_url` varchar(255) NOT NULL,
  `timestamp` int(11) NOT NULL,
  `salt` varchar(65) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- --------------------------------------------------------

--
-- Table structure for table `social_auth_partial`
--

CREATE TABLE `social_auth_partial` (
  `id` bigint(20) NOT NULL,
  `token` varchar(32) NOT NULL,
  `next_step` smallint(5) UNSIGNED NOT NULL CHECK (`next_step` >= 0),
  `backend` varchar(32) NOT NULL,
  `timestamp` datetime(6) NOT NULL,
  `data` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL CHECK (json_valid(`data`))
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- --------------------------------------------------------

--
-- Table structure for table `social_auth_usersocialauth`
--

CREATE TABLE `social_auth_usersocialauth` (
  `id` bigint(20) NOT NULL,
  `provider` varchar(32) NOT NULL,
  `uid` varchar(255) NOT NULL,
  `user_id` varchar(36) NOT NULL,
  `created` datetime(6) NOT NULL,
  `modified` datetime(6) NOT NULL,
  `extra_data` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL CHECK (json_valid(`extra_data`))
) ;

-- --------------------------------------------------------

--
-- Table structure for table `tag`
--

CREATE TABLE `tag` (
  `id` int(11) NOT NULL,
  `name` varchar(50) NOT NULL,
  `slug` varchar(50) NOT NULL,
  `color` varchar(7) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- --------------------------------------------------------

--
-- Table structure for table `technology`
--

CREATE TABLE `technology` (
  `id` int(11) NOT NULL,
  `name` varchar(100) NOT NULL,
  `icon_url` longtext NOT NULL,
  `category` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- --------------------------------------------------------

--
-- Table structure for table `testimonial`
--

CREATE TABLE `testimonial` (
  `id` varchar(36) NOT NULL,
  `content` longtext NOT NULL,
  `rating` int(11) DEFAULT NULL,
  `featured` tinyint(1) NOT NULL,
  `approved` tinyint(1) NOT NULL,
  `date_created` datetime(6) NOT NULL,
  `client_id` varchar(36) NOT NULL,
  `project_id` varchar(36) DEFAULT NULL,
  `service_id` varchar(36) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- --------------------------------------------------------

--
-- Table structure for table `token_blacklist_blacklistedtoken`
--

CREATE TABLE `token_blacklist_blacklistedtoken` (
  `id` bigint(20) NOT NULL,
  `blacklisted_at` datetime(6) NOT NULL,
  `token_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `token_blacklist_blacklistedtoken`
--

INSERT INTO `token_blacklist_blacklistedtoken` (`id`, `blacklisted_at`, `token_id`) VALUES
(1, '2025-10-10 15:50:44.789617', 4);

-- --------------------------------------------------------

--
-- Table structure for table `token_blacklist_outstandingtoken`
--

CREATE TABLE `token_blacklist_outstandingtoken` (
  `id` bigint(20) NOT NULL,
  `token` longtext NOT NULL,
  `created_at` datetime(6) DEFAULT NULL,
  `expires_at` datetime(6) NOT NULL,
  `user_id` varchar(36) DEFAULT NULL,
  `jti` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `token_blacklist_outstandingtoken`
--

INSERT INTO `token_blacklist_outstandingtoken` (`id`, `token`, `created_at`, `expires_at`, `user_id`, `jti`) VALUES
(1, 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc2MDUxMDI4OSwiaWF0IjoxNzU5OTA1NDg5LCJqdGkiOiI5NzY0MDc4NjNkZTA0YTA1OTc4NjQyYjk3ZGY0Y2FjZCIsInVzZXJfaWQiOiI4MTIxOWJkZS1jNTk3LTQxNmEtYmZiZi1iZmQyYjJmYTM2ZjEifQ.3l14IhFKHpMr8nwOFpcZtb9RifzznIw9KP16zN1qRzY', '2025-10-08 06:38:09.338651', '2025-10-15 06:38:09.000000', '81219bde-c597-416a-bfbf-bfd2b2fa36f1', '976407863de04a05978642b97df4cacd'),
(2, 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc2MDUyNTYzMywiaWF0IjoxNzU5OTIwODMzLCJqdGkiOiJlOTkyNzVkOWY0M2Y0ZTZjODY5OTYzZGE0YmY4YjRlZCIsInVzZXJfaWQiOiI4MTIxOWJkZS1jNTk3LTQxNmEtYmZiZi1iZmQyYjJmYTM2ZjEifQ.S1QfqkpoEbwFEOArtbqQZLPJTdnsWafU1hbvVaeBnU8', '2025-10-08 10:53:53.573047', '2025-10-15 10:53:53.000000', '81219bde-c597-416a-bfbf-bfd2b2fa36f1', 'e99275d9f43f4e6c869963da4bf8b4ed'),
(3, 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc2MDY0NjUxMSwiaWF0IjoxNzYwMDQxNzExLCJqdGkiOiIyNjMyNzg0ZjQyMWQ0NTY0YmJlZmJmOGNlOTA2NDY5NyIsInVzZXJfaWQiOiI4MTIxOWJkZS1jNTk3LTQxNmEtYmZiZi1iZmQyYjJmYTM2ZjEifQ.BUog1fKyX5JV-DsWXjHdlgRB5ISipjLE2v_RlRgugOI', '2025-10-09 20:28:31.066550', '2025-10-16 20:28:31.000000', '81219bde-c597-416a-bfbf-bfd2b2fa36f1', '2632784f421d4564bbefbf8ce9064697'),
(4, 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc2MDcxNTg3OSwiaWF0IjoxNzYwMTExMDc5LCJqdGkiOiI3ZTJhMWU1MjBmYTk0MzI4ODE1YWVhYmE1NDI3OWRlMSIsInVzZXJfaWQiOiJlZTI2ZjUzOC0wOGRjLTQ4OTYtODg3Yy1iODBlNDRlMzZlZDgifQ.rrYDRABXXMNCfpsyixQ81cYYJtrwj47h7jg001OkCr0', '2025-10-10 15:44:39.433812', '2025-10-17 15:44:39.000000', 'ee26f538-08dc-4896-887c-b80e44e36ed8', '7e2a1e520fa94328815aeaba54279de1'),
(5, 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc2MDcxNTk0MCwiaWF0IjoxNzYwMTExMTQwLCJqdGkiOiI5YTUzYTUwYmI3ZGU0NmYxODQyODY0NjE4YzkxZjE0NiIsInVzZXJfaWQiOiJlZTI2ZjUzOC0wOGRjLTQ4OTYtODg3Yy1iODBlNDRlMzZlZDgifQ.Vbp3ZOQ9Y7T7UTCSHZ6U1omyjqh-sKHyRygwS8GdBL4', '2025-10-10 15:45:40.874028', '2025-10-17 15:45:40.000000', 'ee26f538-08dc-4896-887c-b80e44e36ed8', '9a53a50bb7de46f1842864618c91f146'),
(6, 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc2MDcxNjAxNiwiaWF0IjoxNzYwMTExMjE2LCJqdGkiOiJkNDM0MmM0MTBmNWM0MzY3ODY0MTNkNTRkNjY2NDRjZSIsInVzZXJfaWQiOiIzNDY0ZDIwZS0wZjA1LTRkMzQtOTJiMy03YWEyNjNjZmYxODYifQ.d-oouxRXcr-RWDyWlm4vEWiyIvpev8jOUsxLyi5VwWo', '2025-10-10 15:46:56.041019', '2025-10-17 15:46:56.000000', '3464d20e-0f05-4d34-92b3-7aa263cff186', 'd4342c410f5c436786413d54d66644ce'),
(7, 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc2MDcxNjAyOCwiaWF0IjoxNzYwMTExMjI4LCJqdGkiOiJiN2EyZjdiNzQ4NDc0MDRiOTIzMTZhOWNmNGRmOTVkNyIsInVzZXJfaWQiOiIzNDY0ZDIwZS0wZjA1LTRkMzQtOTJiMy03YWEyNjNjZmYxODYifQ.ebTmm9r7knAnyRqEJeNz6gU3qvpVjvTAP3dCkSICkYQ', '2025-10-10 15:47:08.047585', '2025-10-17 15:47:08.000000', '3464d20e-0f05-4d34-92b3-7aa263cff186', 'b7a2f7b74847404b92316a9cf4df95d7'),
(8, 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc2MDcxNjU2MCwiaWF0IjoxNzYwMTExNzYwLCJqdGkiOiJiM2YwOGU0YzgzNGY0MzNiYTk2ZWRjZGMzMTgyNmViNyIsInVzZXJfaWQiOiJmZTQxMGI1MS1jYmMyLTQyMDUtODYxYS1jODIwZjZkZGE1YmUifQ.LkPN2KXBRtvo7Gkkv735nvoJ7sFFp3t5CC6W4zgTvwY', '2025-10-10 15:56:00.794445', '2025-10-17 15:56:00.000000', 'fe410b51-cbc2-4205-861a-c820f6dda5be', 'b3f08e4c834f433ba96edcdc31826eb7'),
(9, 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc2MDcxNzM3NSwiaWF0IjoxNzYwMTEyNTc1LCJqdGkiOiI3NmIxYTg4YjMzN2M0ZGNmYmIwZjE2NzIzMWI5NDdjZCIsInVzZXJfaWQiOiJlZTI2ZjUzOC0wOGRjLTQ4OTYtODg3Yy1iODBlNDRlMzZlZDgifQ.4siaDf8bCdX-UwKMJNoYoVPcuo_PHgUciTqViEYdm7o', '2025-10-10 16:09:35.231408', '2025-10-17 16:09:35.000000', 'ee26f538-08dc-4896-887c-b80e44e36ed8', '76b1a88b337c4dcfbb0f167231b947cd'),
(10, 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc2MDcxODMwNCwiaWF0IjoxNzYwMTEzNTA0LCJqdGkiOiIyN2ViMmEwZWQwMDc0Zjg0OGM2YTc5YzY1ODdlNDJkNyIsInVzZXJfaWQiOiJmZTQxMGI1MS1jYmMyLTQyMDUtODYxYS1jODIwZjZkZGE1YmUifQ.d3SBMPBgTbsrVa3sTGNaZBlfQ6tnU2EQ_2TzH1PfQRE', '2025-10-10 16:25:04.002730', '2025-10-17 16:25:04.000000', 'fe410b51-cbc2-4205-861a-c820f6dda5be', '27eb2a0ed0074f848c6a79c6587e42d7'),
(11, 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc2MDcxODU4NiwiaWF0IjoxNzYwMTEzNzg2LCJqdGkiOiI4ZGM0NDkyMjUzZGE0YTI4YWJmYzkxMjM2MzAxNDBlMCIsInVzZXJfaWQiOiJlZTI2ZjUzOC0wOGRjLTQ4OTYtODg3Yy1iODBlNDRlMzZlZDgifQ.zFtmbkEIho3u2GjaSze4dwQiR_fRJR-FMd7FRiOeVN4', '2025-10-10 16:29:46.673460', '2025-10-17 16:29:46.000000', 'ee26f538-08dc-4896-887c-b80e44e36ed8', '8dc4492253da4a28abfc9123630140e0'),
(12, 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc2MDc3Mzk4NSwiaWF0IjoxNzYwMTY5MTg1LCJqdGkiOiJjYjI0YzIxZTZjZGI0ZmE4YWVhNDliY2QyZjFiZjAwNiIsInVzZXJfaWQiOiI4MTIxOWJkZS1jNTk3LTQxNmEtYmZiZi1iZmQyYjJmYTM2ZjEifQ.Q1AiDS4z-LhpwNrQK4kkOJjIBgUDzF1OMNzFwWiZJd8', '2025-10-11 07:53:05.629338', '2025-10-18 07:53:05.000000', '81219bde-c597-416a-bfbf-bfd2b2fa36f1', 'cb24c21e6cdb4fa8aea49bcd2f1bf006'),
(13, 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc2MTkwNzA5OSwiaWF0IjoxNzYxMzAyMjk5LCJqdGkiOiJiN2UwNDJjZmMxYzg0YjdlYmVlMTA3NTA0YjFhM2Q4MSIsInVzZXJfaWQiOiI4MTIxOWJkZS1jNTk3LTQxNmEtYmZiZi1iZmQyYjJmYTM2ZjEifQ.qF9odxfPwabu_SZGtzqzkVZrAUMIusTO8rJySif_nZ8', '2025-10-24 10:38:19.522232', '2025-10-31 10:38:19.000000', '81219bde-c597-416a-bfbf-bfd2b2fa36f1', 'b7e042cfc1c84b7ebee107504b1a3d81'),
(14, 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc2NDIzNDk2MCwiaWF0IjoxNzYzNjMwMTYwLCJqdGkiOiI0N2JjYjY2YzgzMDc0MzY1YTQ3MDU1OGU2OWI0YWRjZSIsInVzZXJfaWQiOiIwMGMxM2RkNy04YzViLTRjNWEtOWEzZS0yMzEwMGEzMmViYTgifQ.snPyd6Qyn5-wYd9Oa06hisBog6GpPD0muQ0vbF_RvKs', '2025-11-20 09:16:00.683152', '2025-11-27 09:16:00.000000', '00c13dd7-8c5b-4c5a-9a3e-23100a32eba8', '47bcb66c83074365a470558e69b4adce'),
(15, 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc2NDIzOTY2OCwiaWF0IjoxNzYzNjM0ODY4LCJqdGkiOiIzOWU3Y2I0ODJjZTg0OWFjYTFkOWNkNjNiODNiNDI4MSIsInVzZXJfaWQiOiIwMGMxM2RkNy04YzViLTRjNWEtOWEzZS0yMzEwMGEzMmViYTgifQ.qyjSFZaKNlYgFDPNdqGz5VKxHVySoj-d-J7FEPrilew', '2025-11-20 10:34:28.507454', '2025-11-27 10:34:28.000000', '00c13dd7-8c5b-4c5a-9a3e-23100a32eba8', '39e7cb482ce849aca1d9cd63b83b4281'),
(16, 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc2NDc4NDM5MCwiaWF0IjoxNzY0MTc5NTkwLCJqdGkiOiIyNzViMmI3YTBkNTI0MTE4OTE2NzAzYzFlZjkwYjk3OCIsInVzZXJfaWQiOiI4MTIxOWJkZS1jNTk3LTQxNmEtYmZiZi1iZmQyYjJmYTM2ZjEifQ.nHxfb0UBPYde63Z9Zfk-NkiOuIn-OmLlCX2CFRhqfgE', '2025-11-26 17:53:10.150663', '2025-12-03 17:53:10.000000', '81219bde-c597-416a-bfbf-bfd2b2fa36f1', '275b2b7a0d524118916703c1ef90b978');

-- --------------------------------------------------------

--
-- Table structure for table `why_choose_us`
--

CREATE TABLE `why_choose_us` (
  `id` bigint(20) NOT NULL,
  `reason_title` varchar(200) NOT NULL,
  `reason_description` longtext NOT NULL,
  `icon_name` varchar(50) NOT NULL,
  `display_order` int(11) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_created` datetime(6) NOT NULL,
  `date_updated` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- --------------------------------------------------------

--
-- Table structure for table `work_experience`
--

CREATE TABLE `work_experience` (
  `id` bigint(20) NOT NULL,
  `company_name` varchar(200) NOT NULL,
  `job_title` varchar(200) NOT NULL,
  `industry` varchar(100) NOT NULL,
  `company_logo` varchar(200) NOT NULL,
  `company_website` varchar(200) NOT NULL,
  `start_month` int(11) NOT NULL,
  `start_year` int(11) NOT NULL,
  `end_month` int(11) DEFAULT NULL,
  `end_year` int(11) DEFAULT NULL,
  `is_current` tinyint(1) NOT NULL,
  `description` longtext NOT NULL,
  `key_responsibilities` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL CHECK (json_valid(`key_responsibilities`)),
  `achievements` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL CHECK (json_valid(`achievements`)),
  `technology_stack` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL CHECK (json_valid(`technology_stack`)),
  `is_featured` tinyint(1) NOT NULL,
  `display_order` int(11) NOT NULL,
  `date_created` datetime(6) NOT NULL,
  `date_updated` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `about_section`
--
ALTER TABLE `about_section`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `about_stats`
--
ALTER TABLE `about_stats`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `accounts_partner`
--
ALTER TABLE `accounts_partner`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `user_id` (`user_id`);

--
-- Indexes for table `authtoken_token`
--
ALTER TABLE `authtoken_token`
  ADD PRIMARY KEY (`key`),
  ADD UNIQUE KEY `user_id` (`user_id`);

--
-- Indexes for table `auth_group`
--
ALTER TABLE `auth_group`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Indexes for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  ADD KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`);

--
-- Indexes for table `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`);

--
-- Indexes for table `auth_user`
--
ALTER TABLE `auth_user`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`),
  ADD UNIQUE KEY `affiliate_code` (`affiliate_code`);

--
-- Indexes for table `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  ADD KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`);

--
-- Indexes for table `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  ADD KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`);

--
-- Indexes for table `blogpost_tag`
--
ALTER TABLE `blogpost_tag`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `blogpost_tag_blogpost_id_tag_id_6dfb6737_uniq` (`blogpost_id`,`tag_id`),
  ADD KEY `blogpost_tag_tag_id_1867eac5_fk_tag_id` (`tag_id`);

--
-- Indexes for table `blog_comment`
--
ALTER TABLE `blog_comment`
  ADD PRIMARY KEY (`id`),
  ADD KEY `blog_commen_blogpos_8c0b71_idx` (`blogpost_id`),
  ADD KEY `blog_commen_approve_b97e33_idx` (`approved`),
  ADD KEY `blog_commen_parent__43ce68_idx` (`parent_id`);

--
-- Indexes for table `blog_post`
--
ALTER TABLE `blog_post`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `slug` (`slug`),
  ADD KEY `blog_post_slug_cdb902_idx` (`slug`),
  ADD KEY `blog_post_status_02ce19_idx` (`status`),
  ADD KEY `blog_post_feature_716fbe_idx` (`featured`),
  ADD KEY `blog_post_author__038a48_idx` (`author_id`),
  ADD KEY `blog_post_date_pu_31985e_idx` (`date_published`);

--
-- Indexes for table `client`
--
ALTER TABLE `client`
  ADD PRIMARY KEY (`user_id`);

--
-- Indexes for table `contact_info`
--
ALTER TABLE `contact_info`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `contact_message`
--
ALTER TABLE `contact_message`
  ADD PRIMARY KEY (`id`),
  ADD KEY `contact_mes_is_read_b66dbc_idx` (`is_read`),
  ADD KEY `contact_mes_replied_ebfacc_idx` (`replied`),
  ADD KEY `contact_mes_priorit_341767_idx` (`priority`),
  ADD KEY `contact_mes_source_5bfb88_idx` (`source`);

--
-- Indexes for table `core_supportattachment`
--
ALTER TABLE `core_supportattachment`
  ADD PRIMARY KEY (`id`),
  ADD KEY `core_supportattachme_ticket_id_1a848412_fk_core_supp` (`ticket_id`);

--
-- Indexes for table `core_supportticket`
--
ALTER TABLE `core_supportticket`
  ADD PRIMARY KEY (`id`),
  ADD KEY `core_supportticket_admin_user_id_16c04187_fk_auth_user_id` (`admin_user_id`),
  ADD KEY `core_supportticket_user_id_5a23444c_fk_auth_user_id` (`user_id`);

--
-- Indexes for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD PRIMARY KEY (`id`),
  ADD KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  ADD KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`);

--
-- Indexes for table `django_content_type`
--
ALTER TABLE `django_content_type`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`);

--
-- Indexes for table `django_migrations`
--
ALTER TABLE `django_migrations`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `django_session`
--
ALTER TABLE `django_session`
  ADD PRIMARY KEY (`session_key`),
  ADD KEY `django_session_expire_date_a5c62663` (`expire_date`);

--
-- Indexes for table `hero_section`
--
ALTER TABLE `hero_section`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `newsletter_subscription`
--
ALTER TABLE `newsletter_subscription`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`);

--
-- Indexes for table `notification`
--
ALTER TABLE `notification`
  ADD PRIMARY KEY (`id`),
  ADD KEY `notificatio_user_id_3cbd6f_idx` (`user_id`),
  ADD KEY `notificatio_is_read_8a483f_idx` (`is_read`),
  ADD KEY `notificatio_type_f65c28_idx` (`type`),
  ADD KEY `notificatio_priorit_86bdfc_idx` (`priority`);

--
-- Indexes for table `order`
--
ALTER TABLE `order`
  ADD PRIMARY KEY (`id`),
  ADD KEY `order_client__392ace_idx` (`client_id`),
  ADD KEY `order_status_35c31c_idx` (`status`),
  ADD KEY `order_payment_57a3c1_idx` (`payment_status`),
  ADD KEY `order_pricing_tier_id_a0091ceb_fk_service_pricing_tier_id` (`pricing_tier_id`),
  ADD KEY `order_product_id_5feb8b6f_fk_product_id` (`product_id`),
  ADD KEY `order_service_id_b31d8a3e_fk_service_id` (`service_id`);

--
-- Indexes for table `payment`
--
ALTER TABLE `payment`
  ADD PRIMARY KEY (`id`),
  ADD KEY `payment_order_id_98f7562d_fk_order_id` (`order_id`),
  ADD KEY `payment_user_id_cfc22004_fk_auth_user_id` (`user_id`);

--
-- Indexes for table `paypal_payment`
--
ALTER TABLE `paypal_payment`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `payment_id` (`payment_id`);

--
-- Indexes for table `pricingtier_feature`
--
ALTER TABLE `pricingtier_feature`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `pricingtier_feature_pricing_tier_id_feature_id_395272bd_uniq` (`pricing_tier_id`,`feature_id`),
  ADD KEY `pricingtier_feature_feature_id_2cf9ec5c_fk_service_feature_id` (`feature_id`);

--
-- Indexes for table `product`
--
ALTER TABLE `product`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `slug` (`slug`),
  ADD KEY `product_slug_b8980b_idx` (`slug`),
  ADD KEY `product_categor_a3ecae_idx` (`category`,`active`),
  ADD KEY `product_feature_30d6e3_idx` (`featured`,`active`),
  ADD KEY `product_creator_594f34_idx` (`creator_id`),
  ADD KEY `product_base_pr_2596f2_idx` (`base_project_id`);

--
-- Indexes for table `product_gallery_image`
--
ALTER TABLE `product_gallery_image`
  ADD PRIMARY KEY (`id`),
  ADD KEY `product_gal_product_e0d7cf_idx` (`product_id`);

--
-- Indexes for table `product_purchase`
--
ALTER TABLE `product_purchase`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `license_key` (`license_key`),
  ADD KEY `product_pur_client__63f324_idx` (`client_id`),
  ADD KEY `product_pur_status_351a8c_idx` (`status`),
  ADD KEY `product_pur_product_b22019_idx` (`product_id`);

--
-- Indexes for table `product_review`
--
ALTER TABLE `product_review`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `product_review_product_id_client_id_d69178ef_uniq` (`product_id`,`client_id`),
  ADD KEY `product_review_client_id_cf1306d2_fk_auth_user_id` (`client_id`),
  ADD KEY `product_rev_product_b4e72e_idx` (`product_id`),
  ADD KEY `product_rev_approve_5b0d10_idx` (`approved`);

--
-- Indexes for table `product_tag`
--
ALTER TABLE `product_tag`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `product_tag_product_id_tag_id_4be184c7_uniq` (`product_id`,`tag_id`),
  ADD KEY `product_tag_tag_id_be0ab736_fk_tag_id` (`tag_id`);

--
-- Indexes for table `product_technology`
--
ALTER TABLE `product_technology`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `product_technology_product_id_technology_id_693e8345_uniq` (`product_id`,`technology_id`),
  ADD KEY `product_technology_technology_id_7c7ab9d8_fk_technology_id` (`technology_id`);

--
-- Indexes for table `product_update`
--
ALTER TABLE `product_update`
  ADD PRIMARY KEY (`id`),
  ADD KEY `product_upd_product_c5a55f_idx` (`product_id`),
  ADD KEY `product_upd_version_9a24cc_idx` (`version`);

--
-- Indexes for table `project`
--
ALTER TABLE `project`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `slug` (`slug`),
  ADD KEY `project_slug_99d028_idx` (`slug`),
  ADD KEY `project_status_37437c_idx` (`status`),
  ADD KEY `project_feature_2c6d4f_idx` (`featured`),
  ADD KEY `project_client__3ae9f5_idx` (`client_id`),
  ADD KEY `project_author__80fdfd_idx` (`author_id`);

--
-- Indexes for table `project_comment`
--
ALTER TABLE `project_comment`
  ADD PRIMARY KEY (`id`),
  ADD KEY `project_com_project_c29a95_idx` (`project_id`),
  ADD KEY `project_com_approve_069ed4_idx` (`approved`);

--
-- Indexes for table `project_gallery_image`
--
ALTER TABLE `project_gallery_image`
  ADD PRIMARY KEY (`id`),
  ADD KEY `project_gal_project_828c43_idx` (`project_id`);

--
-- Indexes for table `project_section`
--
ALTER TABLE `project_section`
  ADD PRIMARY KEY (`id`),
  ADD KEY `project_sec_project_0c3118_idx` (`project_id`),
  ADD KEY `project_sec_sort_or_27b40f_idx` (`sort_order`);

--
-- Indexes for table `project_technology`
--
ALTER TABLE `project_technology`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `project_technology_project_id_technology_id_c522c0d7_uniq` (`project_id`,`technology_id`),
  ADD KEY `project_technology_technology_id_fb6fb636_fk_technology_id` (`technology_id`);

--
-- Indexes for table `roadmap`
--
ALTER TABLE `roadmap`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `service`
--
ALTER TABLE `service`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `slug` (`slug`),
  ADD KEY `service_slug_41154d_idx` (`slug`),
  ADD KEY `service_service_5f0c60_idx` (`service_category_id`),
  ADD KEY `service_feature_b420ea_idx` (`featured`),
  ADD KEY `service_active_c7ea36_idx` (`active`);

--
-- Indexes for table `service_category`
--
ALTER TABLE `service_category`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`),
  ADD UNIQUE KEY `slug` (`slug`),
  ADD KEY `service_cat_slug_bad00b_idx` (`slug`),
  ADD KEY `service_cat_active_c6dc1b_idx` (`active`),
  ADD KEY `service_cat_sort_or_19fac6_idx` (`sort_order`);

--
-- Indexes for table `service_deliverable`
--
ALTER TABLE `service_deliverable`
  ADD PRIMARY KEY (`id`),
  ADD KEY `service_del_service_9d132d_idx` (`service_id`);

--
-- Indexes for table `service_faq`
--
ALTER TABLE `service_faq`
  ADD PRIMARY KEY (`id`),
  ADD KEY `service_faq_service_a565a1_idx` (`service_id`);

--
-- Indexes for table `service_feature`
--
ALTER TABLE `service_feature`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `service_popular_usecase`
--
ALTER TABLE `service_popular_usecase`
  ADD PRIMARY KEY (`id`),
  ADD KEY `service_pop_service_337fb9_idx` (`service_id`);

--
-- Indexes for table `service_pricing_tier`
--
ALTER TABLE `service_pricing_tier`
  ADD PRIMARY KEY (`id`),
  ADD KEY `service_pri_service_91ea46_idx` (`service_id`),
  ADD KEY `service_pri_recomme_a78b62_idx` (`recommended`);

--
-- Indexes for table `service_process_step`
--
ALTER TABLE `service_process_step`
  ADD PRIMARY KEY (`id`),
  ADD KEY `service_pro_service_5867b3_idx` (`service_id`),
  ADD KEY `service_pro_step_or_af84b9_idx` (`step_order`);

--
-- Indexes for table `service_request`
--
ALTER TABLE `service_request`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `order_id` (`order_id`),
  ADD KEY `service_request_pricing_tier_id_c1a92b29_fk_service_p` (`pricing_tier_id`),
  ADD KEY `service_request_service_id_d2e31331_fk_service_id` (`service_id`);

--
-- Indexes for table `service_tool`
--
ALTER TABLE `service_tool`
  ADD PRIMARY KEY (`id`),
  ADD KEY `service_too_service_7fb607_idx` (`service_id`);

--
-- Indexes for table `social_auth_association`
--
ALTER TABLE `social_auth_association`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `social_auth_association_server_url_handle_078befa2_uniq` (`server_url`,`handle`);

--
-- Indexes for table `social_auth_code`
--
ALTER TABLE `social_auth_code`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `social_auth_code_email_code_801b2d02_uniq` (`email`,`code`),
  ADD KEY `social_auth_code_code_a2393167` (`code`),
  ADD KEY `social_auth_code_timestamp_176b341f` (`timestamp`);

--
-- Indexes for table `social_auth_nonce`
--
ALTER TABLE `social_auth_nonce`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `social_auth_nonce_server_url_timestamp_salt_f6284463_uniq` (`server_url`,`timestamp`,`salt`);

--
-- Indexes for table `social_auth_partial`
--
ALTER TABLE `social_auth_partial`
  ADD PRIMARY KEY (`id`),
  ADD KEY `social_auth_partial_token_3017fea3` (`token`),
  ADD KEY `social_auth_partial_timestamp_50f2119f` (`timestamp`);

--
-- Indexes for table `social_auth_usersocialauth`
--
ALTER TABLE `social_auth_usersocialauth`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `social_auth_usersocialauth_provider_uid_e6b5e668_uniq` (`provider`,`uid`),
  ADD KEY `social_auth_usersocialauth_user_id_17d28448_fk_auth_user_id` (`user_id`),
  ADD KEY `social_auth_usersocialauth_uid_796e51dc` (`uid`);

--
-- Indexes for table `tag`
--
ALTER TABLE `tag`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`),
  ADD UNIQUE KEY `slug` (`slug`),
  ADD KEY `tag_slug_0f9213_idx` (`slug`);

--
-- Indexes for table `technology`
--
ALTER TABLE `technology`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`),
  ADD KEY `technology_name_ef7438_idx` (`name`),
  ADD KEY `technology_categor_e82aba_idx` (`category`);

--
-- Indexes for table `testimonial`
--
ALTER TABLE `testimonial`
  ADD PRIMARY KEY (`id`),
  ADD KEY `testimonial_client__3151f7_idx` (`client_id`),
  ADD KEY `testimonial_feature_d07373_idx` (`featured`),
  ADD KEY `testimonial_approve_f52d08_idx` (`approved`),
  ADD KEY `testimonial_project_id_d8eff2ee_fk_project_id` (`project_id`),
  ADD KEY `testimonial_service_id_60fc4e0a_fk_service_id` (`service_id`);

--
-- Indexes for table `token_blacklist_blacklistedtoken`
--
ALTER TABLE `token_blacklist_blacklistedtoken`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `token_id` (`token_id`);

--
-- Indexes for table `token_blacklist_outstandingtoken`
--
ALTER TABLE `token_blacklist_outstandingtoken`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `token_blacklist_outstandingtoken_jti_hex_d9bdf6f7_uniq` (`jti`),
  ADD KEY `token_blacklist_outs_user_id_83bc629a_fk_auth_user` (`user_id`);

--
-- Indexes for table `why_choose_us`
--
ALTER TABLE `why_choose_us`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `work_experience`
--
ALTER TABLE `work_experience`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `about_section`
--
ALTER TABLE `about_section`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `about_stats`
--
ALTER TABLE `about_stats`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `accounts_partner`
--
ALTER TABLE `accounts_partner`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `auth_group`
--
ALTER TABLE `auth_group`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `auth_permission`
--
ALTER TABLE `auth_permission`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=245;

--
-- AUTO_INCREMENT for table `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `blogpost_tag`
--
ALTER TABLE `blogpost_tag`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `contact_info`
--
ALTER TABLE `contact_info`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `core_supportattachment`
--
ALTER TABLE `core_supportattachment`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `core_supportticket`
--
ALTER TABLE `core_supportticket`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=58;

--
-- AUTO_INCREMENT for table `django_content_type`
--
ALTER TABLE `django_content_type`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=62;

--
-- AUTO_INCREMENT for table `django_migrations`
--
ALTER TABLE `django_migrations`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=139;

--
-- AUTO_INCREMENT for table `hero_section`
--
ALTER TABLE `hero_section`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `newsletter_subscription`
--
ALTER TABLE `newsletter_subscription`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `paypal_payment`
--
ALTER TABLE `paypal_payment`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `pricingtier_feature`
--
ALTER TABLE `pricingtier_feature`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `product_gallery_image`
--
ALTER TABLE `product_gallery_image`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `product_tag`
--
ALTER TABLE `product_tag`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `product_technology`
--
ALTER TABLE `product_technology`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `project_gallery_image`
--
ALTER TABLE `project_gallery_image`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `project_section`
--
ALTER TABLE `project_section`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `project_technology`
--
ALTER TABLE `project_technology`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `roadmap`
--
ALTER TABLE `roadmap`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `social_auth_association`
--
ALTER TABLE `social_auth_association`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `social_auth_code`
--
ALTER TABLE `social_auth_code`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `social_auth_nonce`
--
ALTER TABLE `social_auth_nonce`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `social_auth_partial`
--
ALTER TABLE `social_auth_partial`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `social_auth_usersocialauth`
--
ALTER TABLE `social_auth_usersocialauth`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `tag`
--
ALTER TABLE `tag`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `technology`
--
ALTER TABLE `technology`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `token_blacklist_blacklistedtoken`
--
ALTER TABLE `token_blacklist_blacklistedtoken`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `token_blacklist_outstandingtoken`
--
ALTER TABLE `token_blacklist_outstandingtoken`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=17;

--
-- AUTO_INCREMENT for table `why_choose_us`
--
ALTER TABLE `why_choose_us`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `work_experience`
--
ALTER TABLE `work_experience`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `accounts_partner`
--
ALTER TABLE `accounts_partner`
  ADD CONSTRAINT `accounts_partner_user_id_f40bb6f1_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Constraints for table `authtoken_token`
--
ALTER TABLE `authtoken_token`
  ADD CONSTRAINT `authtoken_token_user_id_35299eff_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Constraints for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`);

--
-- Constraints for table `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`);

--
-- Constraints for table `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  ADD CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  ADD CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Constraints for table `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  ADD CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Constraints for table `blogpost_tag`
--
ALTER TABLE `blogpost_tag`
  ADD CONSTRAINT `blogpost_tag_blogpost_id_5c08098e_fk_blog_post_id` FOREIGN KEY (`blogpost_id`) REFERENCES `blog_post` (`id`),
  ADD CONSTRAINT `blogpost_tag_tag_id_1867eac5_fk_tag_id` FOREIGN KEY (`tag_id`) REFERENCES `tag` (`id`);

--
-- Constraints for table `blog_comment`
--
ALTER TABLE `blog_comment`
  ADD CONSTRAINT `blog_comment_blogpost_id_a2749b6a_fk_blog_post_id` FOREIGN KEY (`blogpost_id`) REFERENCES `blog_post` (`id`),
  ADD CONSTRAINT `blog_comment_parent_id_f2a027bb_fk_blog_comment_id` FOREIGN KEY (`parent_id`) REFERENCES `blog_comment` (`id`);

--
-- Constraints for table `blog_post`
--
ALTER TABLE `blog_post`
  ADD CONSTRAINT `blog_post_author_id_dd7a8485_fk_auth_user_id` FOREIGN KEY (`author_id`) REFERENCES `auth_user` (`id`);

--
-- Constraints for table `client`
--
ALTER TABLE `client`
  ADD CONSTRAINT `client_user_id_af1c5063_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Constraints for table `core_supportattachment`
--
ALTER TABLE `core_supportattachment`
  ADD CONSTRAINT `core_supportattachme_ticket_id_1a848412_fk_core_supp` FOREIGN KEY (`ticket_id`) REFERENCES `core_supportticket` (`id`);

--
-- Constraints for table `core_supportticket`
--
ALTER TABLE `core_supportticket`
  ADD CONSTRAINT `core_supportticket_admin_user_id_16c04187_fk_auth_user_id` FOREIGN KEY (`admin_user_id`) REFERENCES `auth_user` (`id`),
  ADD CONSTRAINT `core_supportticket_user_id_5a23444c_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Constraints for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  ADD CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Constraints for table `notification`
--
ALTER TABLE `notification`
  ADD CONSTRAINT `notification_user_id_1002fc38_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Constraints for table `order`
--
ALTER TABLE `order`
  ADD CONSTRAINT `order_client_id_53f540f5_fk_auth_user_id` FOREIGN KEY (`client_id`) REFERENCES `auth_user` (`id`),
  ADD CONSTRAINT `order_pricing_tier_id_a0091ceb_fk_service_pricing_tier_id` FOREIGN KEY (`pricing_tier_id`) REFERENCES `service_pricing_tier` (`id`),
  ADD CONSTRAINT `order_product_id_5feb8b6f_fk_product_id` FOREIGN KEY (`product_id`) REFERENCES `product` (`id`),
  ADD CONSTRAINT `order_service_id_b31d8a3e_fk_service_id` FOREIGN KEY (`service_id`) REFERENCES `service` (`id`);

--
-- Constraints for table `payment`
--
ALTER TABLE `payment`
  ADD CONSTRAINT `payment_order_id_98f7562d_fk_order_id` FOREIGN KEY (`order_id`) REFERENCES `order` (`id`),
  ADD CONSTRAINT `payment_user_id_cfc22004_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Constraints for table `paypal_payment`
--
ALTER TABLE `paypal_payment`
  ADD CONSTRAINT `paypal_payment_payment_id_24c38c48_fk_payment_id` FOREIGN KEY (`payment_id`) REFERENCES `payment` (`id`);

--
-- Constraints for table `pricingtier_feature`
--
ALTER TABLE `pricingtier_feature`
  ADD CONSTRAINT `pricingtier_feature_feature_id_2cf9ec5c_fk_service_feature_id` FOREIGN KEY (`feature_id`) REFERENCES `service_feature` (`id`),
  ADD CONSTRAINT `pricingtier_feature_pricing_tier_id_a2567e6b_fk_service_p` FOREIGN KEY (`pricing_tier_id`) REFERENCES `service_pricing_tier` (`id`);

--
-- Constraints for table `product`
--
ALTER TABLE `product`
  ADD CONSTRAINT `product_base_project_id_ff5e0971_fk_project_id` FOREIGN KEY (`base_project_id`) REFERENCES `project` (`id`),
  ADD CONSTRAINT `product_creator_id_36eca0c7_fk_auth_user_id` FOREIGN KEY (`creator_id`) REFERENCES `auth_user` (`id`);

--
-- Constraints for table `product_gallery_image`
--
ALTER TABLE `product_gallery_image`
  ADD CONSTRAINT `product_gallery_image_product_id_3c1ec19e_fk_product_id` FOREIGN KEY (`product_id`) REFERENCES `product` (`id`);

--
-- Constraints for table `product_purchase`
--
ALTER TABLE `product_purchase`
  ADD CONSTRAINT `product_purchase_client_id_695eff60_fk_auth_user_id` FOREIGN KEY (`client_id`) REFERENCES `auth_user` (`id`),
  ADD CONSTRAINT `product_purchase_product_id_bf5b9436_fk_product_id` FOREIGN KEY (`product_id`) REFERENCES `product` (`id`);

--
-- Constraints for table `product_review`
--
ALTER TABLE `product_review`
  ADD CONSTRAINT `product_review_client_id_cf1306d2_fk_auth_user_id` FOREIGN KEY (`client_id`) REFERENCES `auth_user` (`id`),
  ADD CONSTRAINT `product_review_product_id_428b0c5c_fk_product_id` FOREIGN KEY (`product_id`) REFERENCES `product` (`id`);

--
-- Constraints for table `product_tag`
--
ALTER TABLE `product_tag`
  ADD CONSTRAINT `product_tag_product_id_d59e832c_fk_product_id` FOREIGN KEY (`product_id`) REFERENCES `product` (`id`),
  ADD CONSTRAINT `product_tag_tag_id_be0ab736_fk_tag_id` FOREIGN KEY (`tag_id`) REFERENCES `tag` (`id`);

--
-- Constraints for table `product_technology`
--
ALTER TABLE `product_technology`
  ADD CONSTRAINT `product_technology_product_id_958399aa_fk_product_id` FOREIGN KEY (`product_id`) REFERENCES `product` (`id`),
  ADD CONSTRAINT `product_technology_technology_id_7c7ab9d8_fk_technology_id` FOREIGN KEY (`technology_id`) REFERENCES `technology` (`id`);

--
-- Constraints for table `product_update`
--
ALTER TABLE `product_update`
  ADD CONSTRAINT `product_update_product_id_647bf428_fk_product_id` FOREIGN KEY (`product_id`) REFERENCES `product` (`id`);

--
-- Constraints for table `project`
--
ALTER TABLE `project`
  ADD CONSTRAINT `project_author_id_c601d117_fk_auth_user_id` FOREIGN KEY (`author_id`) REFERENCES `auth_user` (`id`),
  ADD CONSTRAINT `project_client_id_0696401f_fk_auth_user_id` FOREIGN KEY (`client_id`) REFERENCES `auth_user` (`id`);

--
-- Constraints for table `project_comment`
--
ALTER TABLE `project_comment`
  ADD CONSTRAINT `project_comment_project_id_988d95c3_fk_project_id` FOREIGN KEY (`project_id`) REFERENCES `project` (`id`);

--
-- Constraints for table `project_gallery_image`
--
ALTER TABLE `project_gallery_image`
  ADD CONSTRAINT `project_gallery_image_project_id_a19e4a03_fk_project_id` FOREIGN KEY (`project_id`) REFERENCES `project` (`id`);

--
-- Constraints for table `project_section`
--
ALTER TABLE `project_section`
  ADD CONSTRAINT `project_section_project_id_e2abed0b_fk_project_id` FOREIGN KEY (`project_id`) REFERENCES `project` (`id`);

--
-- Constraints for table `project_technology`
--
ALTER TABLE `project_technology`
  ADD CONSTRAINT `project_technology_project_id_fc0d5440_fk_project_id` FOREIGN KEY (`project_id`) REFERENCES `project` (`id`),
  ADD CONSTRAINT `project_technology_technology_id_fb6fb636_fk_technology_id` FOREIGN KEY (`technology_id`) REFERENCES `technology` (`id`);

--
-- Constraints for table `service`
--
ALTER TABLE `service`
  ADD CONSTRAINT `service_service_category_id_620c19d4_fk_service_category_id` FOREIGN KEY (`service_category_id`) REFERENCES `service_category` (`id`);

--
-- Constraints for table `service_deliverable`
--
ALTER TABLE `service_deliverable`
  ADD CONSTRAINT `service_deliverable_service_id_4a0cb400_fk_service_id` FOREIGN KEY (`service_id`) REFERENCES `service` (`id`);

--
-- Constraints for table `service_faq`
--
ALTER TABLE `service_faq`
  ADD CONSTRAINT `service_faq_service_id_1bbf4546_fk_service_id` FOREIGN KEY (`service_id`) REFERENCES `service` (`id`);

--
-- Constraints for table `service_popular_usecase`
--
ALTER TABLE `service_popular_usecase`
  ADD CONSTRAINT `service_popular_usecase_service_id_9fa8f6e0_fk_service_id` FOREIGN KEY (`service_id`) REFERENCES `service` (`id`);

--
-- Constraints for table `service_pricing_tier`
--
ALTER TABLE `service_pricing_tier`
  ADD CONSTRAINT `service_pricing_tier_service_id_0c1e802d_fk_service_id` FOREIGN KEY (`service_id`) REFERENCES `service` (`id`);

--
-- Constraints for table `service_process_step`
--
ALTER TABLE `service_process_step`
  ADD CONSTRAINT `service_process_step_service_id_59b64e8e_fk_service_id` FOREIGN KEY (`service_id`) REFERENCES `service` (`id`);

--
-- Constraints for table `service_request`
--
ALTER TABLE `service_request`
  ADD CONSTRAINT `service_request_order_id_04036253_fk_order_id` FOREIGN KEY (`order_id`) REFERENCES `order` (`id`),
  ADD CONSTRAINT `service_request_pricing_tier_id_c1a92b29_fk_service_p` FOREIGN KEY (`pricing_tier_id`) REFERENCES `service_pricing_tier` (`id`),
  ADD CONSTRAINT `service_request_service_id_d2e31331_fk_service_id` FOREIGN KEY (`service_id`) REFERENCES `service` (`id`);

--
-- Constraints for table `service_tool`
--
ALTER TABLE `service_tool`
  ADD CONSTRAINT `service_tool_service_id_92b2c7ba_fk_service_id` FOREIGN KEY (`service_id`) REFERENCES `service` (`id`);

--
-- Constraints for table `social_auth_usersocialauth`
--
ALTER TABLE `social_auth_usersocialauth`
  ADD CONSTRAINT `social_auth_usersocialauth_user_id_17d28448_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Constraints for table `testimonial`
--
ALTER TABLE `testimonial`
  ADD CONSTRAINT `testimonial_client_id_8ecb170c_fk_auth_user_id` FOREIGN KEY (`client_id`) REFERENCES `auth_user` (`id`),
  ADD CONSTRAINT `testimonial_project_id_d8eff2ee_fk_project_id` FOREIGN KEY (`project_id`) REFERENCES `project` (`id`),
  ADD CONSTRAINT `testimonial_service_id_60fc4e0a_fk_service_id` FOREIGN KEY (`service_id`) REFERENCES `service` (`id`);

--
-- Constraints for table `token_blacklist_blacklistedtoken`
--
ALTER TABLE `token_blacklist_blacklistedtoken`
  ADD CONSTRAINT `token_blacklist_blacklistedtoken_token_id_3cc7fe56_fk` FOREIGN KEY (`token_id`) REFERENCES `token_blacklist_outstandingtoken` (`id`);

--
-- Constraints for table `token_blacklist_outstandingtoken`
--
ALTER TABLE `token_blacklist_outstandingtoken`
  ADD CONSTRAINT `token_blacklist_outs_user_id_83bc629a_fk_auth_user` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
