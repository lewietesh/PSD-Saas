-- phpMyAdmin SQL Dump
-- version 5.2.2
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Dec 04, 2025 at 10:55 AM
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
-- Database: `ibnusina_wordknox`
--

-- --------------------------------------------------------

--
-- Table structure for table `about_section`
--

CREATE TABLE `about_section` (
  `id` int(11) NOT NULL,
  `title` varchar(255) NOT NULL,
  `description` longtext NOT NULL,
  `media` varchar(100) DEFAULT NULL,
  `socials_urls` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL CHECK (json_valid(`socials_urls`)),
  `show_stats` tinyint(1) NOT NULL,
  `show_work_experience` tinyint(1) NOT NULL,
  `show_why_choose_us` tinyint(1) NOT NULL,
  `show_roadmap` tinyint(1) NOT NULL,
  `date_created` datetime(6) NOT NULL,
  `date_updated` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

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
(81, 'Can add FAQ', 21, 'add_faq'),
(82, 'Can change FAQ', 21, 'change_faq'),
(83, 'Can delete FAQ', 21, 'delete_faq'),
(84, 'Can view FAQ', 21, 'view_faq'),
(85, 'Can add Hero Section', 22, 'add_herosection'),
(86, 'Can change Hero Section', 22, 'change_herosection'),
(87, 'Can delete Hero Section', 22, 'delete_herosection'),
(88, 'Can view Hero Section', 22, 'view_herosection'),
(89, 'Can add Newsletter Subscription', 23, 'add_newslettersubscription'),
(90, 'Can change Newsletter Subscription', 23, 'change_newslettersubscription'),
(91, 'Can delete Newsletter Subscription', 23, 'delete_newslettersubscription'),
(92, 'Can view Newsletter Subscription', 23, 'view_newslettersubscription'),
(93, 'Can add Roadmap Milestone', 24, 'add_roadmap'),
(94, 'Can change Roadmap Milestone', 24, 'change_roadmap'),
(95, 'Can delete Roadmap Milestone', 24, 'delete_roadmap'),
(96, 'Can view Roadmap Milestone', 24, 'view_roadmap'),
(97, 'Can add Why Choose Us', 25, 'add_whychooseus'),
(98, 'Can change Why Choose Us', 25, 'change_whychooseus'),
(99, 'Can delete Why Choose Us', 25, 'delete_whychooseus'),
(100, 'Can view Why Choose Us', 25, 'view_whychooseus'),
(101, 'Can add Work Experience', 26, 'add_workexperience'),
(102, 'Can change Work Experience', 26, 'change_workexperience'),
(103, 'Can delete Work Experience', 26, 'delete_workexperience'),
(104, 'Can view Work Experience', 26, 'view_workexperience'),
(105, 'Can add Support Ticket', 27, 'add_supportticket'),
(106, 'Can change Support Ticket', 27, 'change_supportticket'),
(107, 'Can delete Support Ticket', 27, 'delete_supportticket'),
(108, 'Can view Support Ticket', 27, 'view_supportticket'),
(109, 'Can add Support Attachment', 28, 'add_supportattachment'),
(110, 'Can change Support Attachment', 28, 'change_supportattachment'),
(111, 'Can delete Support Attachment', 28, 'delete_supportattachment'),
(112, 'Can view Support Attachment', 28, 'view_supportattachment'),
(113, 'Can add Project', 29, 'add_project'),
(114, 'Can change Project', 29, 'change_project'),
(115, 'Can delete Project', 29, 'delete_project'),
(116, 'Can view Project', 29, 'view_project'),
(117, 'Can add Technology', 30, 'add_technology'),
(118, 'Can change Technology', 30, 'change_technology'),
(119, 'Can delete Technology', 30, 'delete_technology'),
(120, 'Can view Technology', 30, 'view_technology'),
(121, 'Can add Project Technology', 31, 'add_projecttechnology'),
(122, 'Can change Project Technology', 31, 'change_projecttechnology'),
(123, 'Can delete Project Technology', 31, 'delete_projecttechnology'),
(124, 'Can view Project Technology', 31, 'view_projecttechnology'),
(125, 'Can add Project Comment', 32, 'add_projectcomment'),
(126, 'Can change Project Comment', 32, 'change_projectcomment'),
(127, 'Can delete Project Comment', 32, 'delete_projectcomment'),
(128, 'Can view Project Comment', 32, 'view_projectcomment'),
(129, 'Can add Project Gallery Image', 33, 'add_projectgalleryimage'),
(130, 'Can change Project Gallery Image', 33, 'change_projectgalleryimage'),
(131, 'Can delete Project Gallery Image', 33, 'delete_projectgalleryimage'),
(132, 'Can view Project Gallery Image', 33, 'view_projectgalleryimage'),
(133, 'Can add Project Section', 34, 'add_projectsection'),
(134, 'Can change Project Section', 34, 'change_projectsection'),
(135, 'Can delete Project Section', 34, 'delete_projectsection'),
(136, 'Can view Project Section', 34, 'view_projectsection'),
(137, 'Can add Blog Post', 35, 'add_blogpost'),
(138, 'Can change Blog Post', 35, 'change_blogpost'),
(139, 'Can delete Blog Post', 35, 'delete_blogpost'),
(140, 'Can view Blog Post', 35, 'view_blogpost'),
(141, 'Can add Tag', 36, 'add_tag'),
(142, 'Can change Tag', 36, 'change_tag'),
(143, 'Can delete Tag', 36, 'delete_tag'),
(144, 'Can view Tag', 36, 'view_tag'),
(145, 'Can add Blog Post Tag', 37, 'add_blogposttag'),
(146, 'Can change Blog Post Tag', 37, 'change_blogposttag'),
(147, 'Can delete Blog Post Tag', 37, 'delete_blogposttag'),
(148, 'Can view Blog Post Tag', 37, 'view_blogposttag'),
(149, 'Can add Blog Comment', 38, 'add_blogcomment'),
(150, 'Can change Blog Comment', 38, 'change_blogcomment'),
(151, 'Can delete Blog Comment', 38, 'delete_blogcomment'),
(152, 'Can view Blog Comment', 38, 'view_blogcomment'),
(153, 'Can add Service Feature', 39, 'add_servicefeature'),
(154, 'Can change Service Feature', 39, 'change_servicefeature'),
(155, 'Can delete Service Feature', 39, 'delete_servicefeature'),
(156, 'Can view Service Feature', 39, 'view_servicefeature'),
(157, 'Can add Service Category', 40, 'add_servicecategory'),
(158, 'Can change Service Category', 40, 'change_servicecategory'),
(159, 'Can delete Service Category', 40, 'delete_servicecategory'),
(160, 'Can view Service Category', 40, 'view_servicecategory'),
(161, 'Can add Service', 41, 'add_service'),
(162, 'Can change Service', 41, 'change_service'),
(163, 'Can delete Service', 41, 'delete_service'),
(164, 'Can view Service', 41, 'view_service'),
(165, 'Can add Service Deliverable', 42, 'add_servicedeliverable'),
(166, 'Can change Service Deliverable', 42, 'change_servicedeliverable'),
(167, 'Can delete Service Deliverable', 42, 'delete_servicedeliverable'),
(168, 'Can view Service Deliverable', 42, 'view_servicedeliverable'),
(169, 'Can add Service FAQ', 43, 'add_servicefaq'),
(170, 'Can change Service FAQ', 43, 'change_servicefaq'),
(171, 'Can delete Service FAQ', 43, 'delete_servicefaq'),
(172, 'Can view Service FAQ', 43, 'view_servicefaq'),
(173, 'Can add Pricing Tier Feature', 44, 'add_pricingtierfeature'),
(174, 'Can change Pricing Tier Feature', 44, 'change_pricingtierfeature'),
(175, 'Can delete Pricing Tier Feature', 44, 'delete_pricingtierfeature'),
(176, 'Can view Pricing Tier Feature', 44, 'view_pricingtierfeature'),
(177, 'Can add Service Popular Use Case', 45, 'add_servicepopularusecase'),
(178, 'Can change Service Popular Use Case', 45, 'change_servicepopularusecase'),
(179, 'Can delete Service Popular Use Case', 45, 'delete_servicepopularusecase'),
(180, 'Can view Service Popular Use Case', 45, 'view_servicepopularusecase'),
(181, 'Can add Service Pricing Tier', 46, 'add_servicepricingtier'),
(182, 'Can change Service Pricing Tier', 46, 'change_servicepricingtier'),
(183, 'Can delete Service Pricing Tier', 46, 'delete_servicepricingtier'),
(184, 'Can view Service Pricing Tier', 46, 'view_servicepricingtier'),
(185, 'Can add Service Process Step', 47, 'add_serviceprocessstep'),
(186, 'Can change Service Process Step', 47, 'change_serviceprocessstep'),
(187, 'Can delete Service Process Step', 47, 'delete_serviceprocessstep'),
(188, 'Can view Service Process Step', 47, 'view_serviceprocessstep'),
(189, 'Can add Service Tool', 48, 'add_servicetool'),
(190, 'Can change Service Tool', 48, 'change_servicetool'),
(191, 'Can delete Service Tool', 48, 'delete_servicetool'),
(192, 'Can view Service Tool', 48, 'view_servicetool'),
(193, 'Can add Product', 49, 'add_product'),
(194, 'Can change Product', 49, 'change_product'),
(195, 'Can delete Product', 49, 'delete_product'),
(196, 'Can view Product', 49, 'view_product'),
(197, 'Can add Product Tag', 50, 'add_producttag'),
(198, 'Can change Product Tag', 50, 'change_producttag'),
(199, 'Can delete Product Tag', 50, 'delete_producttag'),
(200, 'Can view Product Tag', 50, 'view_producttag'),
(201, 'Can add Product Technology', 51, 'add_producttechnology'),
(202, 'Can change Product Technology', 51, 'change_producttechnology'),
(203, 'Can delete Product Technology', 51, 'delete_producttechnology'),
(204, 'Can view Product Technology', 51, 'view_producttechnology'),
(205, 'Can add Product Update', 52, 'add_productupdate'),
(206, 'Can change Product Update', 52, 'change_productupdate'),
(207, 'Can delete Product Update', 52, 'delete_productupdate'),
(208, 'Can view Product Update', 52, 'view_productupdate'),
(209, 'Can add Product Gallery Image', 53, 'add_productgalleryimage'),
(210, 'Can change Product Gallery Image', 53, 'change_productgalleryimage'),
(211, 'Can delete Product Gallery Image', 53, 'delete_productgalleryimage'),
(212, 'Can view Product Gallery Image', 53, 'view_productgalleryimage'),
(213, 'Can add Product Purchase', 54, 'add_productpurchase'),
(214, 'Can change Product Purchase', 54, 'change_productpurchase'),
(215, 'Can delete Product Purchase', 54, 'delete_productpurchase'),
(216, 'Can view Product Purchase', 54, 'view_productpurchase'),
(217, 'Can add Product Review', 55, 'add_productreview'),
(218, 'Can change Product Review', 55, 'change_productreview'),
(219, 'Can delete Product Review', 55, 'delete_productreview'),
(220, 'Can view Product Review', 55, 'view_productreview'),
(221, 'Can add Contact Message', 56, 'add_contactmessage'),
(222, 'Can change Contact Message', 56, 'change_contactmessage'),
(223, 'Can delete Contact Message', 56, 'delete_contactmessage'),
(224, 'Can view Contact Message', 56, 'view_contactmessage'),
(225, 'Can add Order', 57, 'add_order'),
(226, 'Can change Order', 57, 'change_order'),
(227, 'Can delete Order', 57, 'delete_order'),
(228, 'Can view Order', 57, 'view_order'),
(229, 'Can add payment', 58, 'add_payment'),
(230, 'Can change payment', 58, 'change_payment'),
(231, 'Can delete payment', 58, 'delete_payment'),
(232, 'Can view payment', 58, 'view_payment'),
(233, 'Can add PayPal Payment', 59, 'add_paypalpayment'),
(234, 'Can change PayPal Payment', 59, 'change_paypalpayment'),
(235, 'Can delete PayPal Payment', 59, 'delete_paypalpayment'),
(236, 'Can view PayPal Payment', 59, 'view_paypalpayment'),
(237, 'Can add Service Request', 60, 'add_servicerequest'),
(238, 'Can change Service Request', 60, 'change_servicerequest'),
(239, 'Can delete Service Request', 60, 'delete_servicerequest'),
(240, 'Can view Service Request', 60, 'view_servicerequest'),
(241, 'Can add Testimonial', 61, 'add_testimonial'),
(242, 'Can change Testimonial', 61, 'change_testimonial'),
(243, 'Can delete Testimonial', 61, 'delete_testimonial'),
(244, 'Can view Testimonial', 61, 'view_testimonial'),
(245, 'Can add Notification', 62, 'add_notification'),
(246, 'Can change Notification', 62, 'change_notification'),
(247, 'Can delete Notification', 62, 'delete_notification'),
(248, 'Can view Notification', 62, 'view_notification'),
(249, 'Can add Contact Message', 63, 'add_message'),
(250, 'Can change Contact Message', 63, 'change_message'),
(251, 'Can delete Contact Message', 63, 'delete_message'),
(252, 'Can view Contact Message', 63, 'view_message'),
(253, 'Can add Message Reply', 64, 'add_messagereply'),
(254, 'Can change Message Reply', 64, 'change_messagereply'),
(255, 'Can delete Message Reply', 64, 'delete_messagereply'),
(256, 'Can view Message Reply', 64, 'view_messagereply');

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
  `featured_image` varchar(100) DEFAULT NULL,
  `date_published` date DEFAULT NULL,
  `category` varchar(100) NOT NULL,
  `status` varchar(20) NOT NULL,
  `view_count` int(11) NOT NULL,
  `featured` tinyint(1) NOT NULL,
  `date_created` datetime(6) NOT NULL,
  `date_updated` datetime(6) NOT NULL,
  `author_id` varchar(36) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

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
(38, 'blog', 'blogcomment'),
(35, 'blog', 'blogpost'),
(37, 'blog', 'blogposttag'),
(36, 'blog', 'tag'),
(56, 'business', 'contactmessage'),
(62, 'business', 'notification'),
(57, 'business', 'order'),
(58, 'business', 'payment'),
(59, 'business', 'paypalpayment'),
(60, 'business', 'servicerequest'),
(61, 'business', 'testimonial'),
(9, 'contenttypes', 'contenttype'),
(18, 'core', 'aboutsection'),
(19, 'core', 'aboutstats'),
(20, 'core', 'contactinfo'),
(21, 'core', 'faq'),
(22, 'core', 'herosection'),
(23, 'core', 'newslettersubscription'),
(24, 'core', 'roadmap'),
(28, 'core', 'supportattachment'),
(27, 'core', 'supportticket'),
(25, 'core', 'whychooseus'),
(26, 'core', 'workexperience'),
(63, 'notifications', 'message'),
(64, 'notifications', 'messagereply'),
(49, 'products', 'product'),
(53, 'products', 'productgalleryimage'),
(54, 'products', 'productpurchase'),
(55, 'products', 'productreview'),
(50, 'products', 'producttag'),
(51, 'products', 'producttechnology'),
(52, 'products', 'productupdate'),
(29, 'projects', 'project'),
(32, 'projects', 'projectcomment'),
(33, 'projects', 'projectgalleryimage'),
(34, 'projects', 'projectsection'),
(31, 'projects', 'projecttechnology'),
(30, 'projects', 'technology'),
(44, 'services', 'pricingtierfeature'),
(41, 'services', 'service'),
(40, 'services', 'servicecategory'),
(42, 'services', 'servicedeliverable'),
(43, 'services', 'servicefaq'),
(39, 'services', 'servicefeature'),
(45, 'services', 'servicepopularusecase'),
(46, 'services', 'servicepricingtier'),
(47, 'services', 'serviceprocessstep'),
(48, 'services', 'servicetool'),
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
(1, 'contenttypes', '0001_initial', '2025-12-04 09:53:19.620709'),
(2, 'contenttypes', '0002_remove_content_type_name', '2025-12-04 09:53:19.684927'),
(3, 'auth', '0001_initial', '2025-12-04 09:53:19.928418'),
(4, 'auth', '0002_alter_permission_name_max_length', '2025-12-04 09:53:19.952329'),
(5, 'auth', '0003_alter_user_email_max_length', '2025-12-04 09:53:19.956399'),
(6, 'auth', '0004_alter_user_username_opts', '2025-12-04 09:53:19.961095'),
(7, 'auth', '0005_alter_user_last_login_null', '2025-12-04 09:53:19.964858'),
(8, 'auth', '0006_require_contenttypes_0002', '2025-12-04 09:53:19.966334'),
(9, 'auth', '0007_alter_validators_add_error_messages', '2025-12-04 09:53:19.970071'),
(10, 'auth', '0008_alter_user_username_max_length', '2025-12-04 09:53:19.973895'),
(11, 'auth', '0009_alter_user_last_name_max_length', '2025-12-04 09:53:19.977635'),
(12, 'auth', '0010_alter_group_name_max_length', '2025-12-04 09:53:19.998436'),
(13, 'auth', '0011_update_proxy_permissions', '2025-12-04 09:53:20.003039'),
(14, 'auth', '0012_alter_user_first_name_max_length', '2025-12-04 09:53:20.006951'),
(15, 'accounts', '0001_initial', '2025-12-04 09:53:20.482910'),
(16, 'admin', '0001_initial', '2025-12-04 09:53:20.602759'),
(17, 'admin', '0002_logentry_remove_auto_add', '2025-12-04 09:53:20.635145'),
(18, 'admin', '0003_logentry_add_action_flag_choices', '2025-12-04 09:53:20.647395'),
(19, 'authtoken', '0001_initial', '2025-12-04 09:53:20.707881'),
(20, 'authtoken', '0002_auto_20160226_1747', '2025-12-04 09:53:20.732619'),
(21, 'authtoken', '0003_tokenproxy', '2025-12-04 09:53:20.734574'),
(22, 'authtoken', '0004_alter_tokenproxy_options', '2025-12-04 09:53:20.737954'),
(23, 'blog', '0001_initial', '2025-12-04 09:53:21.428119'),
(24, 'services', '0001_initial', '2025-12-04 09:53:22.783889'),
(25, 'projects', '0001_initial', '2025-12-04 09:53:23.711091'),
(26, 'products', '0001_initial', '2025-12-04 09:53:25.138512'),
(27, 'business', '0001_initial', '2025-12-04 09:53:26.739587'),
(28, 'core', '0001_initial', '2025-12-04 09:53:27.134340'),
(29, 'notifications', '0001_initial', '2025-12-04 09:53:27.725323'),
(30, 'sessions', '0001_initial', '2025-12-04 09:53:27.770037'),
(31, 'default', '0001_initial', '2025-12-04 09:53:28.059205'),
(32, 'social_auth', '0001_initial', '2025-12-04 09:53:28.060692'),
(33, 'default', '0002_add_related_name', '2025-12-04 09:53:28.091391'),
(34, 'social_auth', '0002_add_related_name', '2025-12-04 09:53:28.092902'),
(35, 'default', '0003_alter_email_max_length', '2025-12-04 09:53:28.113059'),
(36, 'social_auth', '0003_alter_email_max_length', '2025-12-04 09:53:28.116359'),
(37, 'default', '0004_auto_20160423_0400', '2025-12-04 09:53:28.136393'),
(38, 'social_auth', '0004_auto_20160423_0400', '2025-12-04 09:53:28.139817'),
(39, 'social_auth', '0005_auto_20160727_2333', '2025-12-04 09:53:28.174542'),
(40, 'social_django', '0006_partial', '2025-12-04 09:53:28.218752'),
(41, 'social_django', '0007_code_timestamp', '2025-12-04 09:53:28.303488'),
(42, 'social_django', '0008_partial_timestamp', '2025-12-04 09:53:28.370019'),
(43, 'social_django', '0009_auto_20191118_0520', '2025-12-04 09:53:28.482283'),
(44, 'social_django', '0010_uid_db_index', '2025-12-04 09:53:28.534101'),
(45, 'social_django', '0011_alter_id_fields', '2025-12-04 09:53:28.823042'),
(46, 'social_django', '0012_usersocialauth_extra_data_new', '2025-12-04 09:53:28.924431'),
(47, 'social_django', '0013_migrate_extra_data', '2025-12-04 09:53:28.964053'),
(48, 'social_django', '0014_remove_usersocialauth_extra_data', '2025-12-04 09:53:29.038233'),
(49, 'social_django', '0015_rename_extra_data_new_usersocialauth_extra_data', '2025-12-04 09:53:29.107529'),
(50, 'social_django', '0016_alter_usersocialauth_extra_data', '2025-12-04 09:53:29.125148'),
(51, 'social_django', '0017_usersocialauth_user_social_auth_uid_required', '2025-12-04 09:53:29.191750'),
(52, 'token_blacklist', '0001_initial', '2025-12-04 09:53:29.380207'),
(53, 'token_blacklist', '0002_outstandingtoken_jti_hex', '2025-12-04 09:53:29.423802'),
(54, 'token_blacklist', '0003_auto_20171017_2007', '2025-12-04 09:53:29.464690'),
(55, 'token_blacklist', '0004_auto_20171017_2013', '2025-12-04 09:53:29.545188'),
(56, 'token_blacklist', '0005_remove_outstandingtoken_jti', '2025-12-04 09:53:29.594422'),
(57, 'token_blacklist', '0006_auto_20171017_2113', '2025-12-04 09:53:29.637099'),
(58, 'token_blacklist', '0007_auto_20171017_2214', '2025-12-04 09:53:29.973874'),
(59, 'token_blacklist', '0008_migrate_to_bigautofield', '2025-12-04 09:53:30.206205'),
(60, 'token_blacklist', '0010_fix_migrate_to_bigautofield', '2025-12-04 09:53:30.295441'),
(61, 'token_blacklist', '0011_linearizes_history', '2025-12-04 09:53:30.298802'),
(62, 'token_blacklist', '0012_alter_outstandingtoken_user', '2025-12-04 09:53:30.333180'),
(63, 'token_blacklist', '0013_alter_blacklistedtoken_options_and_more', '2025-12-04 09:53:30.357906'),
(64, 'social_django', '0001_initial', '2025-12-04 09:53:30.360289'),
(65, 'social_django', '0005_auto_20160727_2333', '2025-12-04 09:53:30.361762'),
(66, 'social_django', '0003_alter_email_max_length', '2025-12-04 09:53:30.363235'),
(67, 'social_django', '0004_auto_20160423_0400', '2025-12-04 09:53:30.364706'),
(68, 'social_django', '0002_add_related_name', '2025-12-04 09:53:30.366178');

-- --------------------------------------------------------

--
-- Table structure for table `django_session`
--

CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- --------------------------------------------------------

--
-- Table structure for table `faqs`
--

CREATE TABLE `faqs` (
  `id` bigint(20) NOT NULL,
  `question` longtext NOT NULL,
  `answer` longtext NOT NULL,
  `featured` tinyint(1) NOT NULL,
  `links` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL CHECK (json_valid(`links`)),
  `display_order` int(11) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_created` datetime(6) NOT NULL,
  `date_updated` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

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
  `media` varchar(100) DEFAULT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_created` datetime(6) NOT NULL,
  `date_updated` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- --------------------------------------------------------

--
-- Table structure for table `message`
--

CREATE TABLE `message` (
  `id` varchar(36) NOT NULL,
  `sender_name` varchar(255) NOT NULL,
  `email` varchar(254) NOT NULL,
  `message` longtext NOT NULL,
  `subject` varchar(100) NOT NULL,
  `status` varchar(20) NOT NULL,
  `phone` varchar(20) NOT NULL,
  `ip_address` char(39) DEFAULT NULL,
  `country` varchar(100) NOT NULL,
  `device` varchar(255) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `assigned_to_id` varchar(36) DEFAULT NULL,
  `user_id_id` varchar(36) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- --------------------------------------------------------

--
-- Table structure for table `message_reply`
--

CREATE TABLE `message_reply` (
  `id` varchar(36) NOT NULL,
  `sender_name` varchar(255) NOT NULL,
  `sender_type` varchar(20) NOT NULL,
  `reply_message` longtext NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `message_id` varchar(36) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

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
  `image` varchar(100) DEFAULT NULL,
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
  `client_id` varchar(36) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

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
  `image` varchar(100) DEFAULT NULL,
  `alt_text` varchar(255) NOT NULL,
  `sort_order` int(11) NOT NULL,
  `project_id` varchar(36) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

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
  `service_image` varchar(100) DEFAULT NULL,
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

-- --------------------------------------------------------

--
-- Table structure for table `why_choose_us`
--

CREATE TABLE `why_choose_us` (
  `id` bigint(20) NOT NULL,
  `reason_title` varchar(200) NOT NULL,
  `reason_description` longtext NOT NULL,
  `img` varchar(100) DEFAULT NULL,
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
-- Indexes for table `faqs`
--
ALTER TABLE `faqs`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `hero_section`
--
ALTER TABLE `hero_section`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `message`
--
ALTER TABLE `message`
  ADD PRIMARY KEY (`id`),
  ADD KEY `message_status_fbc084_idx` (`status`),
  ADD KEY `message_subject_9482ad_idx` (`subject`),
  ADD KEY `message_assigne_b1cb1b_idx` (`assigned_to_id`),
  ADD KEY `message_user_id_b56247_idx` (`user_id_id`),
  ADD KEY `message_created_19da1c_idx` (`created_at`);

--
-- Indexes for table `message_reply`
--
ALTER TABLE `message_reply`
  ADD PRIMARY KEY (`id`),
  ADD KEY `message_rep_message_88f030_idx` (`message_id`),
  ADD KEY `message_rep_created_8ce319_idx` (`created_at`);

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
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `about_stats`
--
ALTER TABLE `about_stats`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `accounts_partner`
--
ALTER TABLE `accounts_partner`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

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
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=257;

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
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

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
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `django_content_type`
--
ALTER TABLE `django_content_type`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=65;

--
-- AUTO_INCREMENT for table `django_migrations`
--
ALTER TABLE `django_migrations`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=69;

--
-- AUTO_INCREMENT for table `faqs`
--
ALTER TABLE `faqs`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `hero_section`
--
ALTER TABLE `hero_section`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

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
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

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
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

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
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `token_blacklist_outstandingtoken`
--
ALTER TABLE `token_blacklist_outstandingtoken`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

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
-- Constraints for table `message`
--
ALTER TABLE `message`
  ADD CONSTRAINT `message_assigned_to_id_c8e1e217_fk_auth_user_id` FOREIGN KEY (`assigned_to_id`) REFERENCES `auth_user` (`id`),
  ADD CONSTRAINT `message_user_id_id_11205d0e_fk_auth_user_id` FOREIGN KEY (`user_id_id`) REFERENCES `auth_user` (`id`);

--
-- Constraints for table `message_reply`
--
ALTER TABLE `message_reply`
  ADD CONSTRAINT `message_reply_message_id_03f028de_fk_message_id` FOREIGN KEY (`message_id`) REFERENCES `message` (`id`);

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
