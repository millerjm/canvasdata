CREATE 
    ALGORITHM = UNDEFINED 
    DEFINER = `millerjm`@`%` 
    SQL SECURITY DEFINER
VIEW `canvasdata`.`canvas_login_student_vw` AS
    SELECT 
        `pd`.`sis_user_id` AS `emplid`,
        `csd`.`sis_source_id` AS `sis_section_id`,
        `ed`.`last_activity_at` AS `course_last_login`,
        `ed`.`data_timestamp` AS `data_timestamp`
    FROM
        (((((`canvasdata`.`enrollment_dim` `ed`
        LEFT JOIN `canvasdata`.`enrollment_fact` `ef` ON ((`ed`.`id` = `ef`.`enrollment_id`)))
        LEFT JOIN `canvasdata`.`pseudonym_dim` `pd` ON ((`pd`.`user_id` = `ef`.`user_id`)))
        LEFT JOIN `canvasdata`.`course_dim` `cd` ON ((`cd`.`id` = `ed`.`course_id`)))
        LEFT JOIN `canvasdata`.`course_section_dim` `csd` ON ((`csd`.`id` = `ed`.`course_section_id`)))
        LEFT JOIN `canvasdata`.`enrollment_term_dim` `etd` ON ((`etd`.`id` = `cd`.`enrollment_term_id`)))
    WHERE
        ((`ed`.`workflow_state` IN ('active' , 'inactive', 'completed'))
            AND (`ed`.`type` = 'StudentEnrollment')
            AND (`csd`.`sis_source_id` IS NOT NULL)
            AND (NOT ((`csd`.`sis_source_id` LIKE '%-%-%')))
            AND (`pd`.`workflow_state` <> 'deleted')
            AND (`pd`.`sis_user_id` IS NOT NULL)
            AND (`pd`.`sis_user_id` LIKE '1%')
            AND (`cd`.`workflow_state` <> 'deleted')
            AND (`csd`.`workflow_state` <> 'deleted')
            AND ((`etd`.`sis_source_id` LIKE '2%-A')
            OR (`etd`.`sis_source_id` LIKE '2%-B')
            OR (`etd`.`sis_source_id` LIKE '2%-FT')
            OR (`etd`.`sis_source_id` LIKE '2%-OT')
            OR (`etd`.`sis_source_id` LIKE '2%-12W'))
            AND (`ed`.`last_activity_at` IS NOT NULL))
    ORDER BY `csd`.`sis_source_id` , `pd`.`sis_user_id`
