#populate assignment info  ====================
INSERT INTO canvasdata.ssc_assignment_counts(course_id,	total_assignment_count)
SELECT
    ad.course_id AS course_id,
    @total_assignment_count := count(id)
FROM
    canvasdata.assignment_dim ad
WHERE
    ad.workflow_state NOT IN('unpublished', 'deleted')
GROUP BY
    course_id 
ON DUPLICATE KEY UPDATE total_assignment_count = @total_assignment_count;

INSERT INTO canvasdata.ssc_assignment_counts(course_id,	graded_quiz_count)
SELECT
    ad.course_id AS course_id,
    @graded_quiz_count := count(id)
FROM
    canvasdata.assignment_dim ad
WHERE
    ad.workflow_state NOT IN('unpublished', 'deleted')
    AND submission_types = 'online_quiz'
GROUP BY
    course_id 
ON DUPLICATE KEY UPDATE graded_quiz_count = @graded_quiz_count;

INSERT INTO canvasdata.ssc_assignment_counts(course_id,	graded_discussion_count)
SELECT
    ad.course_id AS course_id,
    @graded_discussion_count := count(id)
FROM
    canvasdata.assignment_dim ad
WHERE
    ad.workflow_state NOT IN('unpublished', 'deleted')
    AND submission_types = 'discussion_topic'
GROUP BY
    course_id 
ON DUPLICATE KEY UPDATE graded_discussion_count = @graded_discussion_count;

INSERT INTO canvasdata.ssc_assignment_counts(course_id,	graded_canvas_assignment_count)
SELECT
	ad.course_id AS course_id,
	@graded_canvas_assignment_count := count(id)
FROM
	canvasdata.assignment_dim ad
WHERE
	ad.workflow_state NOT IN('unpublished', 'deleted')
	AND submission_types NOT IN ('online_quiz',	'discussion_topic',	'none',	'external_tool',	'not_graded',	'on_paper',	'')
GROUP BY
	course_id 
ON DUPLICATE KEY UPDATE graded_canvas_assignment_count = @graded_canvas_assignment_count;

INSERT INTO canvasdata.ssc_assignment_counts(course_id,	graded_external_tool_count)
SELECT
	ad.course_id AS course_id,
	@graded_external_tool_count := count(id)
FROM
	canvasdata.assignment_dim ad
WHERE
	ad.workflow_state NOT IN('unpublished', 'deleted')
	AND submission_types = 'external_tool'
GROUP BY
	course_id 
ON DUPLICATE KEY UPDATE graded_external_tool_count = @graded_external_tool_count;

INSERT INTO canvasdata.ssc_assignment_counts(course_id,	graded_manual_gradebook_count)
SELECT
	ad.course_id AS course_id,
	@graded_manual_gradebook_count := count(id)
FROM
	canvasdata.assignment_dim ad
WHERE
	ad.workflow_state NOT IN('unpublished', 'deleted')
	AND submission_types IN('not_graded', 'on_paper', '')
GROUP BY
	course_id 
ON DUPLICATE KEY UPDATE graded_manual_gradebook_count = @graded_manual_gradebook_count;

INSERT INTO canvasdata.ssc_assignment_counts(course_id,	peer_review_assignment_count)
SELECT
	ad.course_id AS course_id,
	@peer_review_assignment_count := count(id)
FROM
	canvasdata.assignment_dim ad
WHERE
	ad.workflow_state NOT IN('unpublished', 'deleted')
    and ad.peer_reviews = 'true'
GROUP BY
	course_id 
ON DUPLICATE KEY UPDATE peer_review_assignment_count = @peer_review_assignment_count
