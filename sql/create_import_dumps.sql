CREATE TABLE `import_dumps` (
  `dump_id` varchar(191) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '',
  `sequence` int(11) DEFAULT '0',
  `file_count` int(11) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `expires_at` datetime DEFAULT NULL,
  `historical` tinyint(4) DEFAULT NULL,
  `finished` tinyint(4) DEFAULT NULL,
  `partial` tinyint(4) DEFAULT NULL,
  `data_timestamp` datetime DEFAULT NULL,
  PRIMARY KEY (`dump_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
