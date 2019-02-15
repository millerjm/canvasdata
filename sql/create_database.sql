CREATE TABLE `account_dim` (
  `id` bigint(20) NOT NULL,
  `canvas_id` bigint(20) DEFAULT NULL,
  `name` varchar(256) DEFAULT NULL,
  `depth` int(10) unsigned DEFAULT NULL,
  `workflow_state` varchar(256) DEFAULT NULL,
  `parent_account` varchar(256) DEFAULT NULL,
  `parent_account_id` bigint(20) DEFAULT NULL,
  `grandparent_account` varchar(256) DEFAULT NULL,
  `grandparent_account_id` bigint(20) DEFAULT NULL,
  `root_account` varchar(256) DEFAULT NULL,
  `root_account_id` bigint(20) DEFAULT NULL,
  `subaccount1` varchar(256) DEFAULT NULL,
  `subaccount1_id` bigint(20) DEFAULT NULL,
  `subaccount2` varchar(256) DEFAULT NULL,
  `subaccount2_id` bigint(20) DEFAULT NULL,
  `subaccount3` varchar(256) DEFAULT NULL,
  `subaccount3_id` bigint(20) DEFAULT NULL,
  `subaccount4` varchar(256) DEFAULT NULL,
  `subaccount4_id` bigint(20) DEFAULT NULL,
  `subaccount5` varchar(256) DEFAULT NULL,
  `subaccount5_id` bigint(20) DEFAULT NULL,
  `subaccount6` varchar(256) DEFAULT NULL,
  `subaccount6_id` bigint(20) DEFAULT NULL,
  `subaccount7` varchar(256) DEFAULT NULL,
  `subaccount7_id` bigint(20) DEFAULT NULL,
  `subaccount8` varchar(256) DEFAULT NULL,
  `subaccount8_id` bigint(20) DEFAULT NULL,
  `subaccount9` varchar(256) DEFAULT NULL,
  `subaccount9_id` bigint(20) DEFAULT NULL,
  `subaccount10` varchar(256) DEFAULT NULL,
  `subaccount10_id` bigint(20) DEFAULT NULL,
  `subaccount11` varchar(256) DEFAULT NULL,
  `subaccount11_id` bigint(20) DEFAULT NULL,
  `subaccount12` varchar(256) DEFAULT NULL,
  `subaccount12_id` bigint(20) DEFAULT NULL,
  `subaccount13` varchar(256) DEFAULT NULL,
  `subaccount13_id` bigint(20) DEFAULT NULL,
  `subaccount14` varchar(256) DEFAULT NULL,
  `subaccount14_id` bigint(20) DEFAULT NULL,
  `subaccount15` varchar(256) DEFAULT NULL,
  `subaccount15_id` bigint(20) DEFAULT NULL,
  `sis_source_id` varchar(256) DEFAULT NULL,
  `data_timestamp` datetime DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE KEY `id` (`id`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci ROW_FORMAT=COMPACT;

CREATE TABLE `assignment_dim` (
  `id` bigint(20) NOT NULL,
  `canvas_id` bigint(20) DEFAULT NULL,
  `course_id` bigint(20) DEFAULT NULL,
  `title` varchar(256) DEFAULT NULL,
  `description` longtext DEFAULT NULL,
  `due_at` datetime DEFAULT NULL,
  `unlock_at` datetime DEFAULT NULL,
  `lock_at` datetime DEFAULT NULL,
  `points_possible` double DEFAULT NULL,
  `grading_type` varchar(256) DEFAULT NULL,
  `submission_types` varchar(256) DEFAULT NULL,
  `workflow_state` varchar(256) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `peer_review_count` int(10) unsigned DEFAULT NULL,
  `peer_reviews_due_at` datetime DEFAULT NULL,
  `peer_reviews_assigned` varchar(5) DEFAULT NULL,
  `peer_reviews` varchar(5) DEFAULT NULL,
  `automatic_peer_reviews` varchar(5) DEFAULT NULL,
  `all_day` varchar(5) DEFAULT NULL,
  `all_day_date` date DEFAULT NULL,
  `could_be_locked` varchar(5) DEFAULT NULL,
  `grade_group_students_individually` varchar(5) DEFAULT NULL,
  `anonymous_peer_reviews` varchar(5) DEFAULT NULL,
  `muted` varchar(5) DEFAULT NULL,
  `assignment_group_id` bigint(20) DEFAULT NULL,
  `position` bigint(20) DEFAULT NULL,
  `visibility` varchar(256) DEFAULT NULL,
  `data_timestamp` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE `assignment_dim_body` (
  `id` bigint(20) NOT NULL,
  `description` longtext DEFAULT NULL,
  `data_timestamp` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE `assignment_fact` (
  `assignment_id` bigint(20) NOT NULL,
  `course_id` bigint(20) DEFAULT NULL,
  `course_account_id` bigint(20) DEFAULT NULL,
  `enrollment_term_id` bigint(20) DEFAULT NULL,
  `points_possible` double DEFAULT NULL,
  `peer_review_count` int(10) unsigned DEFAULT NULL,
  `assignment_group_id` bigint(20) DEFAULT NULL,
  `external_tool_id` bigint(20) DEFAULT NULL,
  `data_timestamp` datetime DEFAULT NULL,
  PRIMARY KEY (`assignment_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci ROW_FORMAT=COMPACT;

CREATE TABLE `assignment_group_dim` (
  `id` bigint(20) NOT NULL,
  `canvas_id` bigint(20) DEFAULT NULL,
  `course_id` bigint(20) DEFAULT NULL,
  `name` varchar(256) DEFAULT NULL,
  `default_assignment_name` varchar(256) DEFAULT NULL,
  `workflow_state` varchar(256) DEFAULT NULL,
  `position` int(10) unsigned DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `data_timestamp` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE `assignment_group_fact` (
  `assignment_group_id` bigint(20) NOT NULL,
  `course_id` bigint(20) DEFAULT NULL,
  `group_weight` double DEFAULT NULL,
  `data_timestamp` datetime DEFAULT NULL,
  PRIMARY KEY (`assignment_group_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE `assignment_group_rule_dim` (
  `assignment_group_id` bigint(20) NOT NULL,
  `drop_lowest` int(10) unsigned DEFAULT NULL,
  `drop_highest` int(10) unsigned DEFAULT NULL,
  `data_timestamp` datetime DEFAULT NULL,
  PRIMARY KEY (`assignment_group_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE `assignment_group_score_dim` (
  `score_id` bigint(20) NOT NULL,
  `canvas_id` bigint(20) DEFAULT NULL,
  `assignment_group_id` double DEFAULT NULL,
  `enrollment_id` bigint(20) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `workflow_state` varchar(255) DEFAULT NULL,
  `data_timestamp` datetime DEFAULT NULL,
  PRIMARY KEY (`score_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE `assignment_group_score_fact` (
  `score_id` bigint(20) NOT NULL,
  `canvas_id` bigint(20) DEFAULT NULL,
  `account_id` bigint(20) DEFAULT NULL,
  `course_id` bigint(20) DEFAULT NULL,
  `assignment_group_id` double DEFAULT NULL,
  `enrollment_id` bigint(20) DEFAULT NULL,
  `current_score` double DEFAULT NULL,
  `final_score` double DEFAULT NULL,
  `muted_current_score` double DEFAULT NULL,
  `muted_final_score` double DEFAULT NULL,
  `data_timestamp` datetime DEFAULT NULL,
  PRIMARY KEY (`score_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE `assignment_override_dim` (
  `id` bigint(20) NOT NULL,
  `canvas_id` bigint(20) DEFAULT NULL,
  `assignment_id` bigint(20) DEFAULT NULL,
  `course_section_id` bigint(20) DEFAULT NULL,
  `group_id` bigint(20) DEFAULT NULL,
  `quiz_id` bigint(20) DEFAULT NULL,
  `all_day` varchar(255) DEFAULT NULL,
  `all_day_date` date DEFAULT NULL,
  `assignment_version` int(11) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `due_at` datetime DEFAULT NULL,
  `due_at_overridden` varchar(255) DEFAULT NULL,
  `lock_at` datetime DEFAULT NULL,
  `lock_at_overridden` varchar(255) DEFAULT NULL,
  `set_type` varchar(255) DEFAULT NULL,
  `title` text DEFAULT NULL,
  `unlock_at` datetime DEFAULT NULL,
  `unlock_at_overridden` varchar(255) DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `quiz_version` int(11) DEFAULT NULL,
  `workflow_state` varchar(255) DEFAULT NULL,
  `data_timestamp` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE `assignment_override_fact` (
  `assignment_override_id` bigint(20) NOT NULL,
  `account_id` bigint(20) DEFAULT NULL,
  `assignment_id` bigint(20) DEFAULT NULL,
  `assignment_group_id` bigint(20) DEFAULT NULL,
  `course_id` bigint(20) DEFAULT NULL,
  `course_section_id` bigint(20) DEFAULT NULL,
  `enrollment_term_id` bigint(20) DEFAULT NULL,
  `group_id` bigint(20) DEFAULT NULL,
  `group_category_id` bigint(20) DEFAULT NULL,
  `group_parent_account_id` bigint(20) DEFAULT NULL,
  `nonxlist_course_id` bigint(20) DEFAULT NULL,
  `quiz_id` bigint(20) DEFAULT NULL,
  `group_wiki_id` bigint(20) DEFAULT NULL,
  `data_timestamp` datetime DEFAULT NULL,
  PRIMARY KEY (`assignment_override_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE `assignment_override_user_dim` (
  `id` bigint(20) NOT NULL,
  `canvas_id` bigint(20) DEFAULT NULL,
  `assignment_id` bigint(20) DEFAULT NULL,
  `assignment_override_id` bigint(20) DEFAULT NULL,
  `quiz_id` bigint(20) DEFAULT NULL,
  `user_id` bigint(20) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `data_timestamp` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE `assignment_override_user_fact` (
  `assignment_override_user_id` bigint(20) NOT NULL,
  `account_id` bigint(20) DEFAULT NULL,
  `assignment_group_id` bigint(20) DEFAULT NULL,
  `assignment_id` bigint(20) DEFAULT NULL,
  `assignment_override_id` bigint(20) DEFAULT NULL,
  `course_id` bigint(20) DEFAULT NULL,
  `enrollment_term_id` bigint(20) DEFAULT NULL,
  `quiz_id` bigint(20) DEFAULT NULL,
  `user_id` bigint(20) DEFAULT NULL,
  `data_timestamp` datetime DEFAULT NULL,
  PRIMARY KEY (`assignment_override_user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE `assignment_override_user_rollup_fact` (
  `assignment_id` bigint(20) DEFAULT NULL,
  `assignment_override_id` bigint(20) NOT NULL,
  `assignment_override_user_adhoc_id` bigint(20) DEFAULT NULL,
  `assignment_group_id` bigint(20) DEFAULT NULL,
  `course_id` bigint(20) DEFAULT NULL,
  `course_account_id` bigint(20) DEFAULT NULL,
  `course_section_id` bigint(20) DEFAULT NULL,
  `enrollment_id` bigint(20) DEFAULT NULL,
  `enrollment_term_id` bigint(20) DEFAULT NULL,
  `group_category_id` bigint(20) DEFAULT NULL,
  `group_id` bigint(20) DEFAULT NULL,
  `group_parent_account_id` bigint(20) DEFAULT NULL,
  `group_wiki_id` bigint(20) DEFAULT NULL,
  `nonxlist_course_id` bigint(20) DEFAULT NULL,
  `quiz_id` bigint(20) DEFAULT NULL,
  `user_id` bigint(20) NOT NULL,
  `data_timestamp` datetime DEFAULT NULL,
  PRIMARY KEY (`assignment_override_id`,`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE `assignment_rule_dim` (
  `assignment_id` bigint(20) NOT NULL,
  `drop_rule` varchar(256) DEFAULT NULL,
  `data_timestamp` datetime DEFAULT NULL,
  PRIMARY KEY (`assignment_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE `communication_channel_dim` (
  `id` bigint(20) NOT NULL,
  `canvas_id` bigint(20) DEFAULT NULL,
  `user_id` bigint(20) DEFAULT NULL,
  `address` varchar(256) DEFAULT NULL,
  `type` varchar(256) DEFAULT NULL,
  `position` int(10) unsigned DEFAULT NULL,
  `workflow_state` varchar(256) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY `id` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci ROW_FORMAT=COMPACT;

CREATE TABLE `communication_channel_fact` (
  `communication_channel_id` bigint(20) DEFAULT NULL,
  `user_id` bigint(20) DEFAULT NULL,
  `bounce_count` int(10) unsigned DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci ROW_FORMAT=COMPACT;

CREATE TABLE `conversation_dim` (
  `id` bigint(20) NOT NULL,
  `canvas_id` bigint(20) DEFAULT NULL,
  `has_attachments` varchar(5) DEFAULT NULL,
  `has_media_objects` varchar(5) DEFAULT NULL,
  `subject` varchar(256) DEFAULT NULL,
  `course_id` bigint(20) DEFAULT NULL,
  `group_id` bigint(20) DEFAULT NULL,
  `account_id` bigint(20) DEFAULT NULL,
  `data_timestamp` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci ROW_FORMAT=COMPACT;

CREATE TABLE `conversation_message_dim` (
  `id` bigint(20) NOT NULL,
  `canvas_id` bigint(20) DEFAULT NULL,
  `conversation_id` bigint(20) DEFAULT NULL,
  `author_id` bigint(20) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `generated` varchar(5) DEFAULT NULL,
  `has_attachments` varchar(5) DEFAULT NULL,
  `has_media_objects` varchar(5) DEFAULT NULL,
  `body` longtext COLLATE utf8mb4_unicode_ci,
  `data_timestamp` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci ROW_FORMAT=COMPACT;

CREATE TABLE `conversation_message_dim_body` (
  `id` bigint(20) NOT NULL,
  `body` longtext COLLATE utf8mb4_unicode_ci,
  `data_timestamp` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci ROW_FORMAT=COMPACT;

CREATE TABLE `conversation_message_participant_fact` (
  `conversation_message_id` bigint(20) NOT NULL,
  `conversation_id` bigint(20) DEFAULT NULL,
  `user_id` bigint(20) NOT NULL,
  `course_id` bigint(20) DEFAULT NULL,
  `enrollment_term_id` bigint(20) DEFAULT NULL,
  `course_account_id` bigint(20) DEFAULT NULL,
  `group_id` bigint(20) DEFAULT NULL,
  `account_id` bigint(20) DEFAULT NULL,
  `enrollment_rollup_id` bigint(20) DEFAULT NULL,
  `message_size_bytes` int(10) unsigned DEFAULT NULL,
  `message_character_count` int(10) unsigned DEFAULT NULL,
  `message_word_count` int(10) unsigned DEFAULT NULL,
  `message_line_count` int(10) unsigned DEFAULT NULL,
  `data_timestamp` datetime DEFAULT NULL,
  PRIMARY KEY (`conversation_message_id`,`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci ROW_FORMAT=COMPACT;

CREATE TABLE `course_dim` (
  `id` bigint(20) NOT NULL,
  `canvas_id` bigint(20) DEFAULT NULL,
  `root_account_id` bigint(20) DEFAULT NULL,
  `account_id` bigint(20) DEFAULT NULL,
  `enrollment_term_id` bigint(20) DEFAULT NULL,
  `name` varchar(256) DEFAULT NULL,
  `code` varchar(256) DEFAULT NULL,
  `type` varchar(256) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `start_at` datetime DEFAULT NULL,
  `conclude_at` datetime DEFAULT NULL,
  `publicly_visible` varchar(5) DEFAULT NULL,
  `sis_source_id` varchar(256) DEFAULT NULL,
  `workflow_state` varchar(256) DEFAULT NULL,
  `wiki_id` bigint(20) DEFAULT NULL,
  `syllabus_body` tinyint(4) DEFAULT NULL,
  `data_timestamp` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci ROW_FORMAT=COMPACT;

CREATE TABLE `course_dim_body` (
  `id` bigint(20) NOT NULL,
  `syllabus_body` longtext COLLATE utf8mb4_unicode_ci,
  `data_timestamp` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE `course_score_dim` (
  `score_id` bigint(20) NOT NULL,
  `canvas_id` bigint(20) DEFAULT NULL,
  `enrollment_id` bigint(20) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `workflow_state` varchar(255) DEFAULT NULL,
  `data_timestamp` datetime DEFAULT NULL,
  PRIMARY KEY (`score_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE `course_score_fact` (
  `score_id` bigint(20) NOT NULL,
  `canvas_id` bigint(20) DEFAULT NULL,
  `account_id` bigint(20) DEFAULT NULL,
  `course_id` bigint(20) DEFAULT NULL,
  `enrollment_id` bigint(20) DEFAULT NULL,
  `current_score` double DEFAULT NULL,
  `final_score` double DEFAULT NULL,
  `muted_current_score` double DEFAULT NULL,
  `muted_final_score` double DEFAULT NULL,
  `data_timestamp` datetime DEFAULT NULL,
  PRIMARY KEY (`score_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE `course_section_dim` (
  `id` bigint(20) NOT NULL,
  `canvas_id` bigint(20) DEFAULT NULL,
  `name` varchar(256) DEFAULT NULL,
  `course_id` bigint(20) DEFAULT NULL,
  `enrollment_term_id` bigint(20) DEFAULT NULL,
  `default_section` varchar(5) DEFAULT NULL,
  `accepting_enrollments` varchar(5) DEFAULT NULL,
  `can_manually_enroll` varchar(5) DEFAULT NULL,
  `start_at` datetime DEFAULT NULL,
  `end_at` datetime DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `workflow_state` varchar(256) DEFAULT NULL,
  `restrict_enrollments_to_section_dates` varchar(5) DEFAULT NULL,
  `nonxlist_course_id` bigint(20) DEFAULT NULL,
  `sis_source_id` varchar(256) DEFAULT NULL,
  `data_timestamp` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 ROW_FORMAT=COMPACT;
                      
CREATE TABLE `course_ui_canvas_navigation_dim` (
  `id` bigint(20) NOT NULL,
  `canvas_id` bigint(20) DEFAULT NULL,
  `name` varchar(256) DEFAULT NULL,
  `default` varchar(256) DEFAULT NULL,
  `original_position` varchar(256) DEFAULT NULL,
  UNIQUE KEY `id` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci ROW_FORMAT=COMPACT;

CREATE TABLE `course_ui_navigation_item_dim` (
  `id` bigint(20) NOT NULL,
  `root_account_id` bigint(20) DEFAULT NULL,
  `visible` varchar(256) DEFAULT NULL,
  `position` int(10) unsigned DEFAULT NULL,
  UNIQUE KEY `id` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci ROW_FORMAT=COMPACT;

CREATE TABLE `course_ui_navigation_item_fact` (
  `root_account_id` bigint(20) DEFAULT NULL,
  `course_ui_navigation_item_id` bigint(20) DEFAULT NULL,
  `course_ui_canvas_navigation_id` bigint(20) DEFAULT NULL,
  `external_tool_activation_id` bigint(20) DEFAULT NULL,
  `course_id` bigint(20) DEFAULT NULL,
  `course_account_id` bigint(20) DEFAULT NULL,
  `enrollment_term_id` bigint(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci ROW_FORMAT=COMPACT;

CREATE TABLE `discussion_entry_dim` (
  `id` bigint(20) NOT NULL,
  `canvas_id` bigint(20) DEFAULT NULL,
  `message` longtext,
  `workflow_state` varchar(256) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `deleted_at` datetime DEFAULT NULL,
  `depth` int(10) unsigned DEFAULT NULL,
  `data_timestamp` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `discussion_entry_dim_body` (
  `id` bigint(20) NOT NULL,
  `message` longtext COLLATE utf8mb4_unicode_ci,
  `data_timestamp` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE `discussion_entry_fact` (
  `discussion_entry_id` bigint(20) NOT NULL,
  `parent_discussion_entry_id` bigint(20) DEFAULT NULL,
  `user_id` bigint(20) DEFAULT NULL,
  `topic_id` bigint(20) DEFAULT NULL,
  `course_id` bigint(20) DEFAULT NULL,
  `enrollment_term_id` bigint(20) DEFAULT NULL,
  `course_account_id` bigint(20) DEFAULT NULL,
  `topic_user_id` bigint(20) DEFAULT NULL,
  `topic_assignment_id` bigint(20) DEFAULT NULL,
  `topic_editor_id` bigint(20) DEFAULT NULL,
  `enrollment_rollup_id` bigint(20) DEFAULT NULL,
  `message_length` int(10) unsigned DEFAULT NULL,
  `data_timestamp` datetime DEFAULT NULL,
  PRIMARY KEY (`discussion_entry_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `discussion_topic_dim` (
  `id` bigint(20) NOT NULL,
  `canvas_id` bigint(20) DEFAULT NULL,
  `title` varchar(256) CHARACTER SET utf8 DEFAULT NULL,
  `message` longtext CHARACTER SET utf8,
  `type` varchar(256) CHARACTER SET utf8 DEFAULT NULL,
  `workflow_state` varchar(256) CHARACTER SET utf8 DEFAULT NULL,
  `last_reply_at` datetime DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `delayed_post_at` datetime DEFAULT NULL,
  `posted_at` datetime DEFAULT NULL,
  `deleted_at` datetime DEFAULT NULL,
  `discussion_type` varchar(256) CHARACTER SET utf8 DEFAULT NULL,
  `pinned` varchar(5) CHARACTER SET utf8 DEFAULT NULL,
  `locked` varchar(5) CHARACTER SET utf8 DEFAULT NULL,
  `course_id` bigint(20) DEFAULT NULL,
  `group_id` bigint(20) DEFAULT NULL,
  `data_timestamp` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=cp1251;

CREATE TABLE `discussion_topic_dim_body` (
  `id` bigint(20) NOT NULL,
  `message` longtext COLLATE utf8mb4_unicode_ci,
  `data_timestamp` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE `discussion_topic_fact` (
  `discussion_topic_id` bigint(20) NOT NULL,
  `course_id` bigint(20) DEFAULT NULL,
  `enrollment_term_id` bigint(20) DEFAULT NULL,
  `course_account_id` bigint(20) DEFAULT NULL,
  `user_id` bigint(20) DEFAULT NULL,
  `assignment_id` bigint(20) DEFAULT NULL,
  `editor_id` bigint(20) DEFAULT NULL,
  `enrollment_rollup_id` bigint(20) DEFAULT NULL,
  `message_length` bigint(20) unsigned DEFAULT NULL,
  `group_id` bigint(20) DEFAULT NULL,
  `group_parent_course_id` bigint(20) DEFAULT NULL,
  `data_timestamp` datetime DEFAULT NULL,
  PRIMARY KEY (`discussion_topic_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `enrollment_dim` (
  `id` bigint(20) NOT NULL,
  `canvas_id` bigint(20) DEFAULT NULL,
  `root_account_id` bigint(20) DEFAULT NULL,
  `course_section_id` bigint(20) DEFAULT NULL,
  `role_id` bigint(20) DEFAULT NULL,
  `type` varchar(256) DEFAULT NULL,
  `workflow_state` varchar(256) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `start_at` datetime DEFAULT NULL,
  `end_at` datetime DEFAULT NULL,
  `completed_at` datetime DEFAULT NULL,
  `self_enrolled` varchar(5) DEFAULT NULL,
  `sis_source_id` varchar(256) DEFAULT NULL,
  `course_id` bigint(20) DEFAULT NULL,
  `user_id` bigint(20) DEFAULT NULL,
  `last_activity_at` datetime DEFAULT NULL,
  `data_timestamp` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  KEY `course_id` (`course_id`),
  KEY `section_id` (`course_section_id`),
  KEY `workflow_state` (`workflow_state`(191)),
  KEY `type` (`type`(191)),
  KEY `canvas_id` (`canvas_id`),
  KEY `role_id` (`role_id`),
  KEY `last_activity_at` (`last_activity_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci ROW_FORMAT=COMPACT;

CREATE TABLE `enrollment_fact` (
  `enrollment_id` bigint(20) NOT NULL,
  `user_id` bigint(20) DEFAULT NULL,
  `course_id` bigint(20) DEFAULT NULL,
  `enrollment_term_id` bigint(20) DEFAULT NULL,
  `course_account_id` bigint(20) DEFAULT NULL,
  `course_section_id` bigint(20) DEFAULT NULL,
  `computed_final_score` double DEFAULT NULL,
  `computed_current_score` double DEFAULT NULL,
  `data_timestamp` datetime DEFAULT NULL,
  PRIMARY KEY (`enrollment_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci ROW_FORMAT=COMPACT;

CREATE TABLE `enrollment_rollup_dim` (
  `id` bigint(20) NOT NULL,
  `user_id` bigint(20) DEFAULT NULL,
  `course_id` bigint(20) DEFAULT NULL,
  `enrollment_count` int(10) unsigned DEFAULT NULL,
  `role_count` int(10) unsigned DEFAULT NULL,
  `base_role_count` int(10) unsigned DEFAULT NULL,
  `account_admin_role_count` int(10) unsigned DEFAULT NULL,
  `teacher_enrollment_role_count` int(10) unsigned DEFAULT NULL,
  `designer_enrollment_role_count` int(10) unsigned DEFAULT NULL,
  `ta_enrollment_role_count` int(10) unsigned DEFAULT NULL,
  `student_enrollment_role_count` int(10) unsigned DEFAULT NULL,
  `observer_enrollment_role_count` int(10) unsigned DEFAULT NULL,
  `account_membership_role_count` int(10) unsigned DEFAULT NULL,
  `no_permissions_role_count` int(10) unsigned DEFAULT NULL,
  `account_admin_enrollment_id` bigint(20) DEFAULT NULL,
  `teacher_enrollment_enrollment_id` bigint(20) DEFAULT NULL,
  `designer_enrollment_enrollment_id` bigint(20) DEFAULT NULL,
  `ta_enrollment_enrollment_id` bigint(20) DEFAULT NULL,
  `student_enrollment_enrollment_id` bigint(20) DEFAULT NULL,
  `observer_enrollment_enrollment_id` bigint(20) DEFAULT NULL,
  `account_membership_enrollment_id` bigint(20) DEFAULT NULL,
  `no_permissions_enrollment_id` bigint(20) DEFAULT NULL,
  `most_privileged_role` varchar(256) DEFAULT NULL,
  `least_privileged_role` varchar(256) DEFAULT NULL,
  `data_timestamp` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci ROW_FORMAT=COMPACT;

CREATE TABLE `enrollment_term_dim` (
  `id` bigint(20) NOT NULL,
  `canvas_id` bigint(20) DEFAULT NULL,
  `root_account_id` bigint(20) DEFAULT NULL,
  `name` varchar(256) DEFAULT NULL,
  `date_start` datetime DEFAULT NULL,
  `date_end` datetime DEFAULT NULL,
  `sis_source_id` varchar(256) DEFAULT NULL,
  `data_timestamp` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `sis_term_id` (`sis_source_id`(191)),
  KEY `name` (`name`(191))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci ROW_FORMAT=COMPACT;

CREATE TABLE `external_tool_activation_dim` (
  `id` bigint(20) NOT NULL,
  `canvas_id` bigint(20) DEFAULT NULL,
  `course_id` bigint(20) DEFAULT NULL,
  `account_id` bigint(20) DEFAULT NULL,
  `activation_target_type` varchar(256) DEFAULT NULL,
  `url` varchar(4096) DEFAULT NULL,
  `name` varchar(256) DEFAULT NULL,
  `description` varchar(256) DEFAULT NULL,
  `workflow_state` varchar(256) DEFAULT NULL,
  `privacy_level` varchar(256) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `tool_id` varchar(256) DEFAULT NULL,
  `selectable_all` varchar(5) DEFAULT NULL,
  `data_timestamp` datetime DEFAULT NULL,
  UNIQUE KEY `id` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci ROW_FORMAT=COMPACT;

CREATE TABLE `external_tool_activation_fact` (
  `external_tool_activation_id` bigint(20) DEFAULT NULL,
  `course_id` bigint(20) DEFAULT NULL,
  `account_id` bigint(20) DEFAULT NULL,
  `root_account_id` bigint(20) DEFAULT NULL,
  `enrollment_term_id` bigint(20) DEFAULT NULL,
  `course_account_id` bigint(20) DEFAULT NULL,
  `data_timestamp` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci ROW_FORMAT=COMPACT;

CREATE TABLE `file_dim` (
  `id` bigint(20) NOT NULL,
  `canvas_id` bigint(20) DEFAULT NULL,
  `display_name` longtext COLLATE utf8mb4_unicode_ci,
  `account_id` bigint(20) DEFAULT NULL,
  `assignment_id` bigint(20) DEFAULT NULL,
  `conversation_message_id` bigint(20) DEFAULT NULL,
  `course_id` bigint(20) DEFAULT NULL,
  `folder_id` bigint(20) DEFAULT NULL,
  `group_id` bigint(20) DEFAULT NULL,
  `quiz_id` bigint(20) DEFAULT NULL,
  `quiz_submission_id` bigint(20) DEFAULT NULL,
  `replacement_file_id` bigint(20) DEFAULT NULL,
  `root_file_id` bigint(20) DEFAULT NULL,
  `submission_id` bigint(20) DEFAULT NULL,
  `uploader_id` bigint(20) DEFAULT NULL,
  `user_id` bigint(20) DEFAULT NULL,
  `owner_entity_type` enum('account','assignment','conversation_message','course','group','quiz','quiz_submission','submission','user') DEFAULT NULL,
  `content_type` varchar(256) DEFAULT NULL,
  `md5` varchar(256) DEFAULT NULL,
  `file_state` enum('available','broken','deleted','errored','hidden') DEFAULT NULL,
  `could_be_locked` enum('allow_locking','disallow_locking') DEFAULT NULL,
  `locked` enum('is_locked','is_not_locked') DEFAULT NULL,
  `lock_at` datetime DEFAULT NULL,
  `unlock_at` datetime DEFAULT NULL,
  `viewed_at` datetime DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `deleted_at` datetime DEFAULT NULL,
  UNIQUE KEY `id` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci ROW_FORMAT=COMPACT;

CREATE TABLE `file_fact` (
  `file_id` bigint(20) DEFAULT NULL,
  `account_id` bigint(20) DEFAULT NULL,
  `assignment_id` bigint(20) DEFAULT NULL,
  `assignment_group_id` bigint(20) DEFAULT NULL,
  `conversation_id` bigint(20) DEFAULT NULL,
  `conversation_message_author_id` bigint(20) DEFAULT NULL,
  `conversation_message_id` bigint(20) DEFAULT NULL,
  `course_id` bigint(20) DEFAULT NULL,
  `enrollment_rollup_id` bigint(20) DEFAULT NULL,
  `enrollment_term_id` bigint(20) DEFAULT NULL,
  `folder_id` bigint(20) DEFAULT NULL,
  `grader_id` bigint(20) DEFAULT NULL,
  `group_id` bigint(20) DEFAULT NULL,
  `group_category_id` bigint(20) DEFAULT NULL,
  `quiz_id` bigint(20) DEFAULT NULL,
  `quiz_submission_id` bigint(20) DEFAULT NULL,
  `replacement_file_id` bigint(20) DEFAULT NULL,
  `root_file_id` bigint(20) DEFAULT NULL,
  `sis_source_id` varchar(256) DEFAULT NULL,
  `submission_id` bigint(20) DEFAULT NULL,
  `uploader_id` bigint(20) DEFAULT NULL,
  `user_id` bigint(20) DEFAULT NULL,
  `wiki_id` bigint(20) DEFAULT NULL,
  `size` bigint(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci ROW_FORMAT=COMPACT;

CREATE TABLE `grading_period_dim` (
  `id` bigint(20) NOT NULL,
  `canvas_id` bigint(20) DEFAULT NULL,
  `grading_period_group_id` bigint(20) DEFAULT NULL,
  `close_date` datetime DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `end_date` datetime DEFAULT NULL,
  `start_date` datetime DEFAULT NULL,
  `title` varchar(255) DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `workflow_state` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE `grading_period_fact` (
  `grading_period_id` bigint(20) DEFAULT NULL,
  `canvas_id` bigint(20) DEFAULT NULL,
  `grading_period_group_id` bigint(20) DEFAULT NULL,
  `grading_period_group_account_id` bigint(20) DEFAULT NULL,
  `grading_period_group_course_id` bigint(20) DEFAULT NULL,
  `weight` double DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE `grading_period_group_dim` (
  `id` bigint(20) NOT NULL,
  `canvas_id` bigint(20) DEFAULT NULL,
  `course_id` bigint(20) DEFAULT NULL,
  `account_id` bigint(20) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `title` varchar(255) DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `workflow_state` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE `grading_period_score_dim` (
  `score_id` bigint(20) DEFAULT NULL,
  `canvas_id` bigint(20) DEFAULT NULL,
  `enrollment_id` bigint(20) DEFAULT NULL,
  `grading_period_id` bigint(20) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `workflow_state` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE `grading_period_score_fact` (
  `score_id` bigint(20) DEFAULT NULL,
  `canvas_id` bigint(20) DEFAULT NULL,
  `account_id` bigint(20) DEFAULT NULL,
  `course_id` bigint(20) DEFAULT NULL,
  `enrollment_id` bigint(20) DEFAULT NULL,
  `grading_period_id` bigint(20) DEFAULT NULL,
  `grading_period_group_id` bigint(20) DEFAULT NULL,
  `grading_period_group_account_id` bigint(20) DEFAULT NULL,
  `current_score` double DEFAULT NULL,
  `final_score` double DEFAULT NULL,
  `muted_current_score` double DEFAULT NULL,
  `muted_final_score` double DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE `group_dim` (
  `id` bigint(20) NOT NULL,
  `canvas_id` bigint(20) DEFAULT NULL,
  `name` varchar(256) DEFAULT NULL,
  `description` longtext COLLATE utf8mb4_unicode_ci,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `deleted_at` datetime DEFAULT NULL,
  `is_public` varchar(5) DEFAULT NULL,
  `workflow_state` varchar(256) DEFAULT NULL,
  `context_type` varchar(256) DEFAULT NULL,
  `category` longtext COLLATE utf8mb4_unicode_ci,
  `join_level` varchar(256) DEFAULT NULL,
  `default_view` varchar(256) DEFAULT NULL,
  `sis_source_id` bigint(20) DEFAULT NULL,
  `group_category_id` bigint(20) DEFAULT NULL,
  `account_id` bigint(20) DEFAULT NULL,
  `wiki_id` bigint(20) DEFAULT NULL,
  `data_timestamp` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci ROW_FORMAT=COMPACT;

CREATE TABLE `group_fact` (
  `group_id` bigint(20) NOT NULL,
  `parent_course_id` bigint(20) DEFAULT NULL,
  `parent_account_id` bigint(20) DEFAULT NULL,
  `parent_course_account_id` bigint(20) DEFAULT NULL,
  `enrollment_term_id` bigint(20) DEFAULT NULL,
  `max_membership` int(10) unsigned DEFAULT NULL,
  `storage_quota` bigint(20) DEFAULT NULL,
  `group_category_id` bigint(20) DEFAULT NULL,
  `account_id` bigint(20) DEFAULT NULL,
  `wiki_id` bigint(20) DEFAULT NULL,
  `data_timestamp` datetime DEFAULT NULL,
  PRIMARY KEY (`group_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci ROW_FORMAT=COMPACT;

CREATE TABLE `group_membership_dim` (
  `id` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
  `canvas_id` varchar(255) DEFAULT NULL,
  `group_id` bigint(20) DEFAULT NULL,
  `moderator` varchar(255) DEFAULT NULL,
  `workflow_state` varchar(255) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `data_timestamp` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE `group_membership_fact` (
  `group_id` bigint(20) DEFAULT NULL,
  `parent_course_id` bigint(20) DEFAULT NULL,
  `parent_account_id` bigint(20) DEFAULT NULL,
  `parent_course_account_id` bigint(20) DEFAULT NULL,
  `enrollment_term_id` bigint(20) DEFAULT NULL,
  `user_id` bigint(20) DEFAULT NULL,
  `group_membership_id` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
  `data_timestamp` datetime DEFAULT NULL,
  PRIMARY KEY (`group_membership_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci ROW_FORMAT=COMPACT;

CREATE TABLE `module_completion_requirement_dim` (
  `id` bigint(20) NOT NULL,
  `module_id` bigint(20) DEFAULT NULL,
  `module_item_id` bigint(20) DEFAULT NULL,
  `requirement_type` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE `module_completion_requirement_fact` (
  `module_completion_requirement_id` bigint(20) DEFAULT NULL,
  `account_id` bigint(20) DEFAULT NULL,
  `assignment_id` bigint(20) DEFAULT NULL,
  `assignment_group_id` bigint(20) DEFAULT NULL,
  `course_id` bigint(20) DEFAULT NULL,
  `discussion_topic_id` bigint(20) DEFAULT NULL,
  `discussion_topic_editor_id` bigint(20) DEFAULT NULL,
  `enrollment_rollup_id` bigint(20) DEFAULT NULL,
  `enrollment_term_id` bigint(20) DEFAULT NULL,
  `file_id` bigint(20) DEFAULT NULL,
  `module_id` bigint(20) DEFAULT NULL,
  `module_item_id` bigint(20) DEFAULT NULL,
  `quiz_id` bigint(20) DEFAULT NULL,
  `user_id` bigint(20) DEFAULT NULL,
  `wiki_id` bigint(20) DEFAULT NULL,
  `wiki_page_id` bigint(20) DEFAULT NULL,
  `min_score` double DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE `module_dim` (
  `id` bigint(20) NOT NULL,
  `canvas_id` bigint(20) DEFAULT NULL,
  `course_id` bigint(20) DEFAULT NULL,
  `require_sequential_progress` varchar(255) DEFAULT NULL,
  `workflow_state` varchar(255) DEFAULT NULL,
  `position` bigint(20) DEFAULT NULL,
  `name` varchar(255) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `deleted_at` datetime DEFAULT NULL,
  `unlock_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE `module_fact` (
  `module_id` bigint(20) DEFAULT NULL,
  `account_id` bigint(20) DEFAULT NULL,
  `course_id` bigint(20) DEFAULT NULL,
  `enrollment_term_id` bigint(20) DEFAULT NULL,
  `wiki_id` bigint(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE `module_item_dim` (
  `id` bigint(20) NOT NULL,
  `canvas_id` bigint(20) DEFAULT NULL,
  `assignment_id` bigint(20) DEFAULT NULL,
  `course_id` bigint(20) DEFAULT NULL,
  `discussion_topic_id` bigint(20) DEFAULT NULL,
  `file_id` bigint(20) DEFAULT NULL,
  `module_id` bigint(20) DEFAULT NULL,
  `quiz_id` bigint(20) DEFAULT NULL,
  `wiki_page_id` bigint(20) DEFAULT NULL,
  `content_type` varchar(255) DEFAULT NULL,
  `workflow_state` varchar(255) DEFAULT NULL,
  `position` bigint(20) DEFAULT NULL,
  `title` varchar(255) DEFAULT NULL,
  `url` varchar(255) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE `module_item_fact` (
  `module_item_id` bigint(20) DEFAULT NULL,
  `account_id` bigint(20) DEFAULT NULL,
  `assignment_id` bigint(20) DEFAULT NULL,
  `assignment_group_id` bigint(20) DEFAULT NULL,
  `course_id` bigint(20) DEFAULT NULL,
  `discussion_topic_id` bigint(20) DEFAULT NULL,
  `discussion_topic_editor_id` bigint(20) DEFAULT NULL,
  `enrollment_rollup_id` bigint(20) DEFAULT NULL,
  `enrollment_term_id` bigint(20) DEFAULT NULL,
  `file_id` bigint(20) DEFAULT NULL,
  `module_id` bigint(20) DEFAULT NULL,
  `quiz_id` bigint(20) DEFAULT NULL,
  `user_id` bigint(20) DEFAULT NULL,
  `wiki_id` bigint(20) DEFAULT NULL,
  `wiki_page_id` bigint(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE `module_prerequisite_dim` (
  `id` bigint(20) NOT NULL,
  `module_id` bigint(20) DEFAULT NULL,
  `prerequisite_module_id` bigint(20) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE `module_prerequisite_fact` (
  `module_prerequisite_id` bigint(20) DEFAULT NULL,
  `account_id` bigint(20) DEFAULT NULL,
  `course_id` bigint(20) DEFAULT NULL,
  `enrollment_term_id` bigint(20) DEFAULT NULL,
  `module_id` bigint(20) DEFAULT NULL,
  `prerequisite_module_id` bigint(20) DEFAULT NULL,
  `prerequisite_wiki_id` bigint(20) DEFAULT NULL,
  `wiki_id` bigint(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE `module_progression_completion_requirement_dim` (
  `id` bigint(20) NOT NULL,
  `module_progression_id` bigint(20) DEFAULT NULL,
  `module_item_id` bigint(20) DEFAULT NULL,
  `requirement_type` bigint(20) DEFAULT NULL,
  `completion_status` bigint(20) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE `module_progression_completion_requirement_fact` (
  `module_progression_completion_requirement_id` bigint(20) DEFAULT NULL,
  `account_id` bigint(20) DEFAULT NULL,
  `assignment_id` bigint(20) DEFAULT NULL,
  `assignment_group_id` bigint(20) DEFAULT NULL,
  `course_id` bigint(20) DEFAULT NULL,
  `discussion_topic_id` bigint(20) DEFAULT NULL,
  `discussion_topic_editor_id` bigint(20) DEFAULT NULL,
  `enrollment_rollup_id` bigint(20) DEFAULT NULL,
  `enrollment_term_id` bigint(20) DEFAULT NULL,
  `file_id` bigint(20) DEFAULT NULL,
  `module_id` bigint(20) DEFAULT NULL,
  `module_item_id` bigint(20) DEFAULT NULL,
  `module_progression_id` bigint(20) DEFAULT NULL,
  `quiz_id` bigint(20) DEFAULT NULL,
  `user_id` bigint(20) DEFAULT NULL,
  `wiki_id` bigint(20) DEFAULT NULL,
  `wiki_page_id` bigint(20) DEFAULT NULL,
  `min_score` double DEFAULT NULL,
  `score` double DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE `module_progression_dim` (
  `id` bigint(20) NOT NULL,
  `canvas_id` bigint(20) DEFAULT NULL,
  `module_id` bigint(20) DEFAULT NULL,
  `user_id` bigint(20) DEFAULT NULL,
  `collapsed` varchar(255) DEFAULT NULL,
  `is_current` varchar(255) DEFAULT NULL,
  `workflow_state` varchar(255) DEFAULT NULL,
  `current_position` bigint(20) DEFAULT NULL,
  `lock_version` bigint(20) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `completed_at` datetime DEFAULT NULL,
  `evaluated_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE `module_progression_fact` (
  `module_progression_id` bigint(20) DEFAULT NULL,
  `account_id` bigint(20) DEFAULT NULL,
  `course_id` bigint(20) DEFAULT NULL,
  `enrollment_term_id` bigint(20) DEFAULT NULL,
  `module_id` bigint(20) DEFAULT NULL,
  `user_id` bigint(20) DEFAULT NULL,
  `wiki_id` bigint(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
              
CREATE TABLE `pseudonym_dim` (
  `id` bigint(20) NOT NULL,
  `canvas_id` bigint(20) DEFAULT NULL,
  `user_id` bigint(20) DEFAULT NULL,
  `account_id` bigint(20) DEFAULT NULL,
  `workflow_state` varchar(256) DEFAULT NULL,
  `last_request_at` datetime DEFAULT NULL,
  `last_login_at` datetime DEFAULT NULL,
  `current_login_at` datetime DEFAULT NULL,
  `last_login_ip` varchar(256) DEFAULT NULL,
  `current_login_ip` varchar(256) DEFAULT NULL,
  `position` int(10) unsigned DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `password_auto_generated` varchar(5) DEFAULT NULL,
  `deleted_at` datetime DEFAULT NULL,
  `sis_user_id` varchar(256) DEFAULT NULL,
  `unique_name` varchar(256) DEFAULT NULL,
  `integration_id` varchar(255) DEFAULT NULL,
  `authentication_provider_id` bigint(20) DEFAULT NULL,
  `data_timestamp` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `workflow_state` (`workflow_state`(255)),
  KEY `sis_user_id` (`sis_user_id`(255)),
  KEY `unique_name` (`unique_name`(255)),
  KEY `user_id` (`user_id`),
  KEY `user_info` (`user_id`,`sis_user_id`(255),`unique_name`(255)),
  KEY `canvas_id` (`canvas_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `pseudonym_fact` (
  `pseudonym_id` bigint(20) NOT NULL,
  `user_id` bigint(20) DEFAULT NULL,
  `account_id` bigint(20) DEFAULT NULL,
  `login_count` int(10) unsigned DEFAULT NULL,
  `failed_login_count` int(10) unsigned DEFAULT NULL,
  `data_timestamp` datetime DEFAULT NULL,
  PRIMARY KEY (`pseudonym_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `quiz_dim` (
  `id` bigint(20) NOT NULL,
  `canvas_id` bigint(20) DEFAULT NULL,
  `root_account_id` bigint(20) DEFAULT NULL,
  `name` varchar(256) DEFAULT NULL,
  `points_possible` double DEFAULT NULL,
  `description` longtext CHARACTER SET utf8,
  `quiz_type` varchar(256) DEFAULT NULL,
  `course_id` bigint(20) DEFAULT NULL,
  `assignment_id` bigint(20) DEFAULT NULL,
  `workflow_state` varchar(256) DEFAULT NULL,
  `scoring_policy` varchar(256) DEFAULT NULL,
  `anonymous_submissions` varchar(256) DEFAULT NULL,
  `display_questions` varchar(256) DEFAULT NULL,
  `answer_display_order` varchar(256) DEFAULT NULL,
  `go_back_to_previous_question` varchar(256) DEFAULT NULL,
  `could_be_locked` varchar(256) DEFAULT NULL,
  `browser_lockdown` varchar(256) DEFAULT NULL,
  `browser_lockdown_for_displaying_results` varchar(256) DEFAULT NULL,
  `browser_lockdown_monitor` varchar(256) DEFAULT NULL,
  `ip_filter` varchar(256) DEFAULT NULL,
  `show_results` varchar(256) DEFAULT NULL,
  `show_correct_answers` varchar(256) DEFAULT NULL,
  `show_correct_answers_at` datetime DEFAULT NULL,
  `hide_correct_answers_at` datetime DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `published_at` datetime DEFAULT NULL,
  `unlock_at` datetime DEFAULT NULL,
  `lock_at` datetime DEFAULT NULL,
  `due_at` datetime DEFAULT NULL,
  `deleted_at` datetime DEFAULT NULL,
  `data_timestamp` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE `quiz_dim_body` (
  `id` bigint(20) NOT NULL,
  `description` longtext COLLATE utf8mb4_unicode_ci,
  `data_timestamp` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE `quiz_fact` (
  `quiz_id` bigint(20) NOT NULL,
  `points_possible` double DEFAULT NULL,
  `time_limit` int(10) unsigned DEFAULT NULL,
  `allowed_attempts` int(10) unsigned DEFAULT NULL,
  `unpublished_question_count` int(10) unsigned DEFAULT NULL,
  `question_count` int(10) unsigned DEFAULT NULL,
  `course_id` bigint(20) DEFAULT NULL,
  `assignment_id` bigint(20) DEFAULT NULL,
  `course_account_id` bigint(20) DEFAULT NULL,
  `enrollment_term_id` bigint(20) DEFAULT NULL,
  `data_timestamp` datetime DEFAULT NULL,
  PRIMARY KEY (`quiz_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `quiz_question_answer_dim` (
  `id` bigint(20) NOT NULL,
  `canvas_id` bigint(20) DEFAULT NULL,
  `quiz_question_id` bigint(20) DEFAULT NULL,
  `text` longtext,
  `html` longtext,
  `comments` longtext,
  `text_after_answers` longtext,
  `answer_match_left` varchar(256) DEFAULT NULL,
  `answer_match_right` varchar(256) DEFAULT NULL,
  `matching_answer_incorrect_matches` varchar(256) DEFAULT NULL,
  `numerical_answer_type` varchar(256) DEFAULT NULL,
  `blank_id` varchar(256) DEFAULT NULL,
  `exact` double DEFAULT NULL,
  `margin` double DEFAULT NULL,
  `starting_range` double DEFAULT NULL,
  `ending_range` double DEFAULT NULL,
  UNIQUE KEY `id` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `quiz_question_answer_fact` (
  `quiz_question_answer_id` bigint(20) DEFAULT NULL,
  `quiz_question_id` bigint(20) DEFAULT NULL,
  `quiz_question_group_id` bigint(20) DEFAULT NULL,
  `quiz_id` bigint(20) DEFAULT NULL,
  `assessment_question_id` bigint(20) DEFAULT NULL,
  `course_id` bigint(20) DEFAULT NULL,
  `assignment_id` bigint(20) DEFAULT NULL,
  `course_account_id` bigint(20) DEFAULT NULL,
  `enrollment_term_id` bigint(20) DEFAULT NULL,
  `weight` double DEFAULT NULL,
  `exact` double DEFAULT NULL,
  `margin` double DEFAULT NULL,
  `starting_range` double DEFAULT NULL,
  `ending_range` double DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `quiz_question_dim` (
  `id` bigint(20) NOT NULL,
  `canvas_id` bigint(20) DEFAULT NULL,
  `quiz_id` bigint(20) DEFAULT NULL,
  `quiz_question_group_id` bigint(20) DEFAULT NULL,
  `position` int(10) unsigned DEFAULT NULL,
  `workflow_state` varchar(256) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `assessment_question_id` bigint(20) DEFAULT NULL,
  `assessment_question_version` int(10) unsigned DEFAULT NULL,
  `name` varchar(256) DEFAULT NULL,
  `question_type` varchar(256) DEFAULT NULL,
  `question_text` longtext,
  `regrade_option` varchar(256) DEFAULT NULL,
  `correct_comments` longtext,
  `incorrect_comments` longtext,
  `neutral_comments` longtext,
  UNIQUE KEY `id` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `quiz_question_fact` (
  `quiz_question_id` bigint(20) DEFAULT NULL,
  `quiz_id` bigint(20) DEFAULT NULL,
  `quiz_question_group_id` bigint(20) DEFAULT NULL,
  `assessment_question_id` bigint(20) DEFAULT NULL,
  `course_id` bigint(20) DEFAULT NULL,
  `assignment_id` bigint(20) DEFAULT NULL,
  `course_account_id` bigint(20) DEFAULT NULL,
  `enrollment_term_id` bigint(20) DEFAULT NULL,
  `points_possible` double DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `quiz_question_group_dim` (
  `id` bigint(20) NOT NULL,
  `canvas_id` bigint(20) DEFAULT NULL,
  `quiz_id` bigint(20) DEFAULT NULL,
  `name` varchar(256) DEFAULT NULL,
  `position` int(10) unsigned DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  UNIQUE KEY `id` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `quiz_question_group_fact` (
  `quiz_question_group_id` bigint(20) DEFAULT NULL,
  `pick_count` int(10) unsigned DEFAULT NULL,
  `question_points` double DEFAULT NULL,
  `quiz_id` bigint(20) DEFAULT NULL,
  `course_id` bigint(20) DEFAULT NULL,
  `assignment_id` bigint(20) DEFAULT NULL,
  `course_account_id` bigint(20) DEFAULT NULL,
  `enrollment_term_id` bigint(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `quiz_submission_dim` (
  `id` bigint(20) NOT NULL,
  `canvas_id` bigint(20) DEFAULT NULL,
  `quiz_id` bigint(20) DEFAULT NULL,
  `submission_id` bigint(20) DEFAULT NULL,
  `user_id` bigint(20) DEFAULT NULL,
  `workflow_state` varchar(256) DEFAULT NULL,
  `quiz_state_during_submission` varchar(256) DEFAULT NULL,
  `submission_scoring_policy` varchar(256) DEFAULT NULL,
  `submission_source` varchar(256) DEFAULT NULL,
  `has_seen_results` varchar(256) DEFAULT NULL,
  `temporary_user_code` varchar(256) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `started_at` datetime DEFAULT NULL,
  `finished_at` datetime DEFAULT NULL,
  `due_at` datetime DEFAULT NULL,
  UNIQUE KEY `id` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `quiz_submission_fact` (
  `score` double DEFAULT NULL,
  `kept_score` double DEFAULT NULL,
  `date` datetime DEFAULT NULL,
  `course_id` bigint(20) DEFAULT NULL,
  `enrollment_term_id` bigint(20) DEFAULT NULL,
  `course_account_id` bigint(20) DEFAULT NULL,
  `quiz_id` bigint(20) DEFAULT NULL,
  `assignment_id` bigint(20) DEFAULT NULL,
  `user_id` bigint(20) DEFAULT NULL,
  `submission_id` bigint(20) DEFAULT NULL,
  `enrollment_rollup_id` bigint(20) DEFAULT NULL,
  `quiz_submission_id` bigint(20) DEFAULT NULL,
  `quiz_points_possible` double DEFAULT NULL,
  `score_before_regrade` double DEFAULT NULL,
  `fudge_points` double DEFAULT NULL,
  `total_attempts` int(10) unsigned DEFAULT NULL,
  `extra_attempts` int(10) unsigned DEFAULT NULL,
  `extra_time` int(10) unsigned DEFAULT NULL,
  `time_taken` int(10) unsigned DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `quiz_submission_historical_dim` (
  `id` bigint(20) NOT NULL,
  `canvas_id` bigint(20) DEFAULT NULL,
  `quiz_id` bigint(20) DEFAULT NULL,
  `submission_id` bigint(20) DEFAULT NULL,
  `user_id` bigint(20) DEFAULT NULL,
  `version_number` int(10) unsigned DEFAULT NULL,
  `submission_state` varchar(256) DEFAULT NULL,
  `workflow_state` varchar(256) DEFAULT NULL,
  `quiz_state_during_submission` varchar(256) DEFAULT NULL,
  `submission_scoring_policy` varchar(256) DEFAULT NULL,
  `submission_source` varchar(256) DEFAULT NULL,
  `has_seen_results` varchar(256) DEFAULT NULL,
  `temporary_user_code` varchar(256) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `started_at` datetime DEFAULT NULL,
  `finished_at` datetime DEFAULT NULL,
  `due_at` datetime DEFAULT NULL,
  UNIQUE KEY `id` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `quiz_submission_historical_fact` (
  `score` double DEFAULT NULL,
  `kept_score` double DEFAULT NULL,
  `date` datetime DEFAULT NULL,
  `course_id` bigint(20) DEFAULT NULL,
  `enrollment_term_id` bigint(20) DEFAULT NULL,
  `course_account_id` bigint(20) DEFAULT NULL,
  `quiz_id` bigint(20) DEFAULT NULL,
  `assignment_id` bigint(20) DEFAULT NULL,
  `user_id` bigint(20) DEFAULT NULL,
  `submission_id` bigint(20) DEFAULT NULL,
  `enrollment_rollup_id` bigint(20) DEFAULT NULL,
  `quiz_submission_historical_id` bigint(20) DEFAULT NULL,
  `quiz_points_possible` double DEFAULT NULL,
  `score_before_regrade` double DEFAULT NULL,
  `fudge_points` double DEFAULT NULL,
  `total_attempts` int(10) unsigned DEFAULT NULL,
  `extra_attempts` int(10) unsigned DEFAULT NULL,
  `extra_time` int(10) unsigned DEFAULT NULL,
  `time_taken` int(10) unsigned DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `role_dim` (
  `id` bigint(20) NOT NULL,
  `canvas_id` bigint(20) DEFAULT NULL,
  `root_account_id` bigint(20) DEFAULT NULL,
  `account_id` bigint(20) DEFAULT NULL,
  `name` varchar(256) DEFAULT NULL,
  `base_role_type` varchar(256) DEFAULT NULL,
  `workflow_state` varchar(256) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `deleted_at` datetime DEFAULT NULL,
  `data_timestamp` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`),
  KEY `name` (`name`(191)),
  KEY `base_role` (`base_role_type`(191))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci ROW_FORMAT=COMPACT;

CREATE TABLE `submission_dim` (
  `id` bigint(20) NOT NULL,
  `canvas_id` bigint(20) DEFAULT NULL,
  `body` longtext DEFAULT NULL,
  `url` varchar(256) DEFAULT NULL,
  `grade` varchar(256) DEFAULT NULL,
  `submitted_at` datetime DEFAULT NULL,
  `submission_type` enum('discussion_topic','external_tool','media_recording','online_file_upload','online_quiz','online_text_entry','online_upload','online_url','basic_lti_launch') DEFAULT NULL,
  `workflow_state` enum('graded','pending_review','submitted','unsubmitted','deleted') DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `processed` varchar(5) DEFAULT NULL,
  `grade_matches_current_submission` varchar(5) DEFAULT NULL,
  `published_grade` varchar(256) DEFAULT NULL,
  `graded_at` datetime DEFAULT NULL,
  `has_rubric_assessment` varchar(5) DEFAULT NULL,
  `attempt` int(10) unsigned DEFAULT NULL,
  `has_admin_comment` varchar(5) DEFAULT NULL,
  `assignment_id` bigint(20) DEFAULT NULL,
  `excused` enum('excused_submission','regular_submission') DEFAULT NULL,
  `graded_anonymously` enum('graded_anonymously','not_graded_anonymously') DEFAULT NULL,
  `grader_id` bigint(20) DEFAULT NULL,
  `group_id` bigint(20) DEFAULT NULL,
  `quiz_submission_id` bigint(20) DEFAULT NULL,
  `user_id` bigint(20) DEFAULT NULL,
  `grade_state` enum('auto_graded','human_graded','not_graded') DEFAULT NULL,
  `data_timestamp` datetime DEFAULT NULL,
  `data_source` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  KEY `workflow_state` (`workflow_state`),
  KEY `url` (`url`(191)),
  KEY `type` (`submission_type`),
  KEY `submitted_at` (`submitted_at`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci ROW_FORMAT=COMPACT;

CREATE TABLE `submission_dim_body` (
  `id` bigint(20) NOT NULL,
  `body` longtext DEFAULT NULL,
  `data_timestamp` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci ROW_FORMAT=COMPACT;

CREATE TABLE `submission_fact` (
  `submission_id` bigint(20) NOT NULL,
  `assignment_id` bigint(20) DEFAULT NULL,
  `course_id` bigint(20) DEFAULT NULL,
  `enrollment_term_id` bigint(20) DEFAULT NULL,
  `user_id` bigint(20) DEFAULT NULL,
  `grader_id` bigint(20) DEFAULT NULL,
  `course_account_id` bigint(20) DEFAULT NULL,
  `enrollment_rollup_id` bigint(20) DEFAULT NULL,
  `score` double DEFAULT NULL,
  `published_score` double DEFAULT NULL,
  `what_if_score` double DEFAULT NULL,
  `submission_comments_count` int(10) unsigned DEFAULT NULL,
  `account_id` bigint(20) DEFAULT NULL,
  `assignment_group_id` bigint(20) DEFAULT NULL,
  `group_id` bigint(20) DEFAULT NULL,
  `quiz_id` bigint(20) DEFAULT NULL,
  `quiz_submission_id` bigint(20) DEFAULT NULL,
  `wiki_id` bigint(20) DEFAULT NULL,
  `data_timestamp` datetime DEFAULT NULL,
  PRIMARY KEY (`submission_id`),
  KEY `assignment_id` (`assignment_id`),
  KEY `enrollment_term_id` (`enrollment_term_id`),
  KEY `enrollment_rollup_id` (`enrollment_rollup_id`),
  KEY `user_id` (`user_id`),
  KEY `course_id` (`course_id`),
  KEY `lda_group_by` (`course_id`,`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci ROW_FORMAT=COMPACT;

CREATE TABLE `user_dim` (
  `id` bigint(20) NOT NULL,
  `canvas_id` bigint(20) DEFAULT NULL,
  `root_account_id` bigint(20) DEFAULT NULL,
  `name` varchar(256) DEFAULT NULL,
  `time_zone` varchar(256) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `visibility` varchar(256) DEFAULT NULL,
  `school_name` varchar(256) DEFAULT NULL,
  `school_position` varchar(256) DEFAULT NULL,
  `gender` varchar(256) DEFAULT NULL,
  `locale` varchar(256) DEFAULT NULL,
  `public` varchar(256) DEFAULT NULL,
  `birthdate` datetime DEFAULT NULL,
  `country_code` varchar(256) DEFAULT NULL,
  `workflow_state` varchar(256) DEFAULT NULL,
  `sortable_name` varchar(256) DEFAULT NULL,
  `global_canvas_id` bigint(20) DEFAULT NULL,
  `data_timestamp` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`),
  KEY `workflow_state` (`workflow_state`(191)),
  KEY `name` (`name`(191)),
  KEY `sortable_name` (`sortable_name`(191)),
  KEY `global_canvas_id` (`global_canvas_id`),
  KEY `canvas_id` (`canvas_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci ROW_FORMAT=COMPACT;

CREATE TABLE `wiki_dim` (
  `id` bigint(20) NOT NULL,
  `canvas_id` bigint(20) DEFAULT NULL,
  `parent_type` varchar(256) DEFAULT NULL,
  `title` longtext DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `front_page_url` longtext DEFAULT NULL,
  `has_no_front_page` varchar(5) DEFAULT NULL,
  `data_timestamp` datetime DEFAULT NULL,
  UNIQUE KEY `id` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci ROW_FORMAT=COMPACT;

CREATE TABLE `wiki_fact` (
  `wiki_id` bigint(20) DEFAULT NULL,
  `parent_course_id` bigint(20) DEFAULT NULL,
  `parent_group_id` bigint(20) DEFAULT NULL,
  `parent_course_account_id` bigint(20) DEFAULT NULL,
  `parent_group_account_id` bigint(20) DEFAULT NULL,
  `account_id` bigint(20) DEFAULT NULL,
  `root_account_id` bigint(20) DEFAULT NULL,
  `enrollment_term_id` bigint(20) DEFAULT NULL,
  `group_category_id` bigint(20) DEFAULT NULL,
  `data_timestamp` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci ROW_FORMAT=COMPACT;

CREATE TABLE `wiki_page_dim` (
  `id` bigint(20) NOT NULL,
  `canvas_id` bigint(20) DEFAULT NULL,
  `title` varchar(256) DEFAULT NULL,
  `body` longtext DEFAULT NULL,
  `workflow_state` varchar(256) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `url` longtext DEFAULT NULL,
  `protected_editing` varchar(5) DEFAULT NULL,
  `editing_roles` varchar(256) DEFAULT NULL,
  `revised_at` datetime DEFAULT NULL,
  `could_be_locked` varchar(5) DEFAULT NULL,
  `data_timestamp` datetime DEFAULT NULL,
  UNIQUE KEY `id` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci ROW_FORMAT=COMPACT;

CREATE TABLE `wiki_page_fact` (
  `wiki_page_id` bigint(20) DEFAULT NULL,
  `wiki_id` bigint(20) DEFAULT NULL,
  `parent_course_id` bigint(20) DEFAULT NULL,
  `parent_group_id` bigint(20) DEFAULT NULL,
  `parent_course_account_id` bigint(20) DEFAULT NULL,
  `parent_group_account_id` bigint(20) DEFAULT NULL,
  `user_id` bigint(20) DEFAULT NULL,
  `account_id` bigint(20) DEFAULT NULL,
  `root_account_id` bigint(20) DEFAULT NULL,
  `enrollment_term_id` bigint(20) DEFAULT NULL,
  `group_category_id` bigint(20) DEFAULT NULL,
  `wiki_page_comments_count` int(10) unsigned DEFAULT NULL,
  `view_count` int(10) unsigned DEFAULT NULL,
  `data_timestamp` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci ROW_FORMAT=COMPACT;

CREATE TABLE `wiki_page_dim_body` (
  `id` bigint(20) NOT NULL,
  `body` longtext DEFAULT NULL,
  `data_timestamp` datetime DEFAULT NULL,
  UNIQUE KEY `id` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci ROW_FORMAT=COMPACT;
