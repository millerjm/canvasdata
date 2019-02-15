CREATE 
    ALGORITHM = UNDEFINED 
    DEFINER = `millerjm`@`%` 
    SQL SECURITY DEFINER
VIEW `canvasdata`.`canvas_lda_vw` AS
    SELECT 
        `p`.`sis_user_id` AS `emplid`,
        `cs`.`sis_source_id` AS `sis_section_id`,
        MAX(`sd`.`submitted_at`) AS `last_activity_date`
    FROM
        ((((((`canvasdata`.`submission_fact` `sf`
        JOIN `canvasdata`.`submission_dim` `sd` ON ((`sf`.`submission_id` = `sd`.`id`)))
        LEFT JOIN `canvasdata`.`pseudonym_dim` `p` ON ((`sf`.`user_id` = `p`.`user_id`)))
        LEFT JOIN `canvasdata`.`enrollment_dim` `e` ON (((`sf`.`user_id` = `e`.`user_id`)
            AND (`sf`.`course_id` = `e`.`course_id`))))
        LEFT JOIN `canvasdata`.`course_section_dim` `cs` ON ((`e`.`course_section_id` = `cs`.`id`)))
        LEFT JOIN `canvasdata`.`course_dim` `c` ON ((`sf`.`course_id` = `c`.`id`)))
        LEFT JOIN `canvasdata`.`enrollment_term_dim` `t` ON ((`c`.`enrollment_term_id` = `t`.`id`)))
    WHERE
        ((`sd`.`submitted_at` IS NOT NULL)
            AND (`sd`.`workflow_state` IN ('graded' , 'pending_review', 'submitted'))
            AND (`e`.`type` = 'StudentEnrollment')
            AND (`e`.`workflow_state` <> 'deleted')
            AND (`e`.`workflow_state` <> 'rejected')
            AND (`cs`.`sis_source_id` IS NOT NULL)
            AND (NOT ((`cs`.`sis_source_id` LIKE '%-%-%')))
            AND (`p`.`workflow_state` <> 'deleted')
            AND (`p`.`sis_user_id` IS NOT NULL)
            AND (`p`.`sis_user_id` LIKE '1%')
            AND (`c`.`workflow_state` <> 'deleted')
            AND (`cs`.`workflow_state` <> 'deleted')
            AND ((`t`.`sis_source_id` LIKE '2%-A')
            OR (`t`.`sis_source_id` LIKE '2%-B')
            OR (`t`.`sis_source_id` LIKE '2%-FT')
            OR (`t`.`sis_source_id` LIKE '2%-OT')
            OR (`t`.`sis_source_id` LIKE '2%-12W'))
            AND (ISNULL(`sd`.`url`)
            OR ((`sd`.`submission_type` = 'online_url')
            AND (`sd`.`url` <> 'https://rollcall.instructure.com/launch'))))
    GROUP BY `cs`.`sis_source_id` , `p`.`sis_user_id`
