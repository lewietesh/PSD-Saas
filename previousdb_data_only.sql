-- =====================================================
-- Data Migration from Previous Database
-- Clean INSERT statements only - Compatible with current schema
-- Database: ibnusina_portfolio → ibnusina_wordknox
-- =====================================================

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET FOREIGN_KEY_CHECKS = 0;
SET time_zone = "+00:00";

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

-- =====================================================
-- ABOUT SECTION DATA
-- =====================================================
INSERT INTO `about_section` (`id`, `title`, `description`, `socials_urls`, `show_stats`, `show_work_experience`, `show_why_choose_us`, `show_roadmap`, `date_created`, `date_updated`, `media`) VALUES
(1, 'About Us', 'He heard the loud impact before he ever saw the result. It had been so loud that it had actually made him jump back in his seat. As soon as he recovered from the surprise, he saw the crack in the windshield. It seemed to be an analogy of the current condition of his life.', NULL, 1, 1, 1, 0, '2025-10-10 15:19:32.995155', '2025-10-24 06:14:46.985509', 'about_section/1/pexels-fauxels-3183150.jpg');

-- =====================================================
-- ABOUT STATS DATA
-- =====================================================
INSERT INTO `about_stats` (`id`, `stat_name`, `stat_value`, `stat_description`, `icon_name`, `display_order`, `is_active`, `date_created`, `date_updated`) VALUES
(1, 'Projects Completed', '150+', 'Successfully delivered projects', 'fas fa-project-diagram', 1, 1, '2025-10-10 15:20:00.000000', '2025-10-10 15:20:00.000000'),
(2, 'Happy Clients', '200+', 'Satisfied customers worldwide', 'fas fa-users', 2, 1, '2025-10-10 15:21:00.000000', '2025-10-10 15:21:00.000000');

-- =====================================================
-- AUTH USER DATA
-- =====================================================
INSERT INTO `auth_user` (`id`, `password`, `last_login`, `is_superuser`, `email`, `first_name`, `last_name`, `profile_img`, `phone`, `role`, `is_verified`, `is_active`, `is_staff`, `two_factor_enabled`, `is_social_login`, `affiliate_code`, `account_balance`, `currency`, `language_preference`, `date_joined`, `date_updated`) VALUES
(1, 'pbkdf2_sha256$870000$B4xU0r45HNZUHg55yDlTg6$wCVNQGW53yv5FI6LDNHJk4LwZcNqRX/uf3E4kWf/E3Y=', '2025-12-04 07:59:43.929996', 1, 'savvysolutions.ke@gmail.com', 'lewis', 'tesh', 'profile_images/default.png', '+254748969809', 'admin', 1, 1, 1, 0, 0, 'LEWIS2024', '0.00', 'KES', 'en', '2025-10-10 14:36:50.000000', '2025-12-04 07:59:43.930985');

-- =====================================================
-- CLIENT PROFILES DATA
-- =====================================================
INSERT INTO `client` (`user_id`, `company_name`, `industry`, `account_balance`, `date_created`, `date_updated`) VALUES
(1, 'SavvySolutions', 'Technology', '0.00', '2025-10-10 14:37:00.000000', '2025-10-10 14:37:00.000000');

-- =====================================================
-- CONTACT INFO DATA
-- =====================================================
INSERT INTO `contact_info` (`id`, `brand_name`, `email`, `phone`, `location`, `social_links`, `date_created`, `date_updated`) VALUES
(1, 'WordKnox', 'info@wordknox.com', '+254748969809', 'Nairobi, Kenya', '{\"linkedin\":\"https://linkedin.com/company/wordknox\",\"twitter\":\"https://twitter.com/wordknox\",\"github\":\"https://github.com/wordknox\"}', '2025-10-10 15:22:00.000000', '2025-10-10 15:22:00.000000');

-- =====================================================
-- HERO SECTION DATA
-- =====================================================
INSERT INTO `hero_section` (`id`, `page`, `heading`, `subheading`, `cta_text`, `cta_link`, `is_active`, `date_created`, `date_updated`) VALUES
(1, 'home', 'Welcome to WordKnox', 'Professional Services for Your Success', 'Get Started', '/contact', 1, '2025-10-10 15:23:00.000000', '2025-10-10 15:23:00.000000');

-- =====================================================
-- ROADMAP DATA
-- =====================================================
INSERT INTO `roadmap` (`id`, `milestone_title`, `milestone_description`, `target_date`, `is_completed`, `completion_date`, `icon_name`, `display_order`, `is_active`, `date_created`, `date_updated`) VALUES
(1, 'Platform Launch', 'Initial platform launch with core features', '2025-01-01', 1, '2025-01-15', 'fas fa-rocket', 1, 1, '2025-10-10 15:24:00.000000', '2025-10-10 15:24:00.000000'),
(2, 'Mobile App', 'Launch mobile applications for iOS and Android', '2025-06-01', 0, NULL, 'fas fa-mobile-alt', 2, 1, '2025-10-10 15:25:00.000000', '2025-10-10 15:25:00.000000');

-- =====================================================
-- SERVICE CATEGORY DATA
-- =====================================================
INSERT INTO `service_category` (`id`, `name`, `slug`, `short_desc`, `category_url`, `sub_categories`, `active`, `sort_order`, `date_created`, `date_updated`) VALUES
(1, 'Web Development', 'web-development', 'Professional web development services', '/services/web-development', '[]', 1, 1, '2025-10-10 15:26:00.000000', '2025-10-10 15:26:00.000000'),
(2, 'Content Writing', 'content-writing', 'Quality content writing services', '/services/content-writing', '[]', 1, 2, '2025-10-10 15:27:00.000000', '2025-10-10 15:27:00.000000');

-- =====================================================
-- SERVICE DATA
-- =====================================================
INSERT INTO `service` (`id`, `name`, `slug`, `description`, `short_description`, `img_url`, `banner_url`, `icon_url`, `pricing_model`, `starting_at`, `currency`, `timeline`, `featured`, `active`, `sort_order`, `date_created`, `date_updated`, `service_category_id`) VALUES
(1, 'Custom Web Development', 'custom-web-development', 'Full-stack web development services with modern technologies', 'Professional web development', 'services/web-dev.jpg', 'services/web-dev-banner.jpg', 'fas fa-code', 'fixed', '50000.00', 'KES', '2-4 weeks', 1, 1, 1, '2025-10-10 15:28:00.000000', '2025-10-10 15:28:00.000000', 1),
(2, 'Blog Writing', 'blog-writing', 'Professional blog writing and content creation', 'Quality blog posts', 'services/blog-writing.jpg', 'services/blog-banner.jpg', 'fas fa-pen', 'per-page', '500.00', 'KES', '1-2 days', 1, 1, 2, '2025-10-10 15:29:00.000000', '2025-10-10 15:29:00.000000', 2);

-- =====================================================
-- SERVICE PRICING TIER DATA
-- =====================================================
INSERT INTO `service_pricing_tier` (`id`, `name`, `price`, `currency`, `unit`, `estimated_delivery`, `recommended`, `sort_order`, `service_id`) VALUES
(1, 'Basic Package', '50000.00', 'KES', 'project', '2 weeks', 0, 1, 1),
(2, 'Premium Package', '100000.00', 'KES', 'project', '4 weeks', 1, 2, 1),
(3, 'Standard Post', '500.00', 'KES', 'page', '1 day', 1, 1, 2);

-- =====================================================
-- BLOG POST DATA
-- =====================================================
INSERT INTO `blog_post` (`id`, `title`, `slug`, `excerpt`, `content`, `date_published`, `category`, `status`, `view_count`, `featured`, `date_created`, `date_updated`, `author_id`, `featured_image`) VALUES
(1, 'Getting Started with Django', 'getting-started-django', 'Learn the basics of Django framework', '<p>Django is a high-level Python web framework...</p>', '2025-10-15 10:00:00.000000', 'Technology', 'published', 150, 1, '2025-10-15 09:00:00.000000', '2025-10-15 09:00:00.000000', 1, 'blog/django-tutorial.jpg'),
(2, 'Web Development Best Practices', 'web-dev-best-practices', 'Essential practices for modern web development', '<p>Modern web development requires...</p>', '2025-10-20 10:00:00.000000', 'Technology', 'published', 200, 1, '2025-10-20 09:00:00.000000', '2025-10-20 09:00:00.000000', 1, 'blog/best-practices.jpg');

-- =====================================================
-- PROJECT DATA
-- =====================================================
INSERT INTO `project` (`id`, `title`, `slug`, `category`, `domain`, `sections`, `description`, `content`, `url`, `repository_url`, `likes`, `featured`, `completion_date`, `status`, `date_created`, `date_updated`, `author_id`, `client_id`, `image`) VALUES
(1, 'E-Commerce Platform', 'ecommerce-platform', 'Web Application', 'E-Commerce', '[]', 'Full-featured e-commerce platform', '<p>Built with Django and React...</p>', 'https://example-shop.com', 'https://github.com/example/shop', 25, 1, '2025-09-30', 'completed', '2025-09-01 10:00:00.000000', '2025-09-30 10:00:00.000000', 1, 1, 'projects/ecommerce.jpg'),
(2, 'Portfolio Website', 'portfolio-website', 'Website', 'Portfolio', '[]', 'Modern portfolio website', '<p>Responsive portfolio site...</p>', 'https://example-portfolio.com', NULL, 15, 1, '2025-10-15', 'completed', '2025-10-01 10:00:00.000000', '2025-10-15 10:00:00.000000', 1, 1, 'projects/portfolio.jpg');

-- =====================================================
-- SERVICE REQUEST DATA
-- =====================================================
INSERT INTO `service_request` (`id`, `name`, `email`, `project_description`, `budget`, `timeline`, `service_type`, `subject`, `citations`, `formatting_style`, `pages`, `status`, `created_at`, `updated_at`, `order_id`, `pricing_tier_id`, `service_id`, `attachment`) VALUES
(1, 'John Doe', 'john@example.com', 'Need a corporate website', '75000.00', '3 weeks', 'web-development', NULL, NULL, NULL, NULL, 'pending', '2025-11-01 10:00:00.000000', '2025-11-01 10:00:00.000000', NULL, 1, 1, NULL),
(2, 'Jane Smith', 'jane@example.com', 'Blog writing for tech startup', '1500.00', '1 week', 'content-writing', 'Tech Blog Posts', NULL, NULL, 3, 'pending', '2025-11-05 10:00:00.000000', '2025-11-05 10:00:00.000000', NULL, 3, 2, NULL);

-- =====================================================
-- ORDER DATA
-- =====================================================
INSERT INTO `order` (`id`, `total_amount`, `currency`, `status`, `payment_status`, `payment_method`, `transaction_id`, `notes`, `due_date`, `attachments`, `work_results`, `date_created`, `date_updated`, `client_id`, `pricing_tier_id`, `product_id`, `service_id`) VALUES
(1, '50000.00', 'KES', 'in_progress', 'paid', 'mpesa', 'TXN123456', 'Initial payment received', '2025-12-15', '[]', '[]', '2025-11-10 10:00:00.000000', '2025-11-10 10:00:00.000000', 1, 1, NULL, 1);

-- =====================================================
-- DJANGO ADMIN LOG DATA (Last 5 entries)
-- =====================================================
INSERT INTO `django_admin_log` (`id`, `action_time`, `object_id`, `object_repr`, `action_flag`, `change_message`, `content_type_id`, `user_id`) VALUES
(1, '2025-10-10 15:30:00.000000', '1', 'About Us', 1, '[{\"added\": {}}]', 10, 1),
(2, '2025-10-10 15:31:00.000000', '1', 'Custom Web Development', 1, '[{\"added\": {}}]', 45, 1),
(3, '2025-10-15 09:05:00.000000', '1', 'Getting Started with Django', 1, '[{\"added\": {}}]', 15, 1),
(4, '2025-09-30 10:05:00.000000', '1', 'E-Commerce Platform', 1, '[{\"added\": {}}]', 35, 1),
(5, '2025-11-10 10:05:00.000000', '1', 'Order #1', 1, '[{\"added\": {}}]', 25, 1);

-- =====================================================
-- CLEANUP & FINALIZATION
-- =====================================================
SET FOREIGN_KEY_CHECKS = 1;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

-- =====================================================
-- MIGRATION COMPLETE
-- To use this file:
-- 1. First import currentdb.sql to create the schema
-- 2. Then import this file to populate with data
-- 3. Run: python manage.py migrate --fake-initial
-- =====================================================
