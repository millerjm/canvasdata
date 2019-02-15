
#populate discussion info  ====================

insert into canvasdata.ssc_discussion_counts (course_id, discussion_topic_count)
SELECT 
	dtf.course_id as course_id, 
    @discussion_topic_count := count(discussion_topic_id) 
FROM 
	canvasdata.discussion_topic_fact dtf 
		left outer join canvasdata.discussion_topic_dim dtd on dtf.discussion_topic_id = dtd.id
where 
	dtf.course_id is not null
	and dtd.type is null
    and dtd.workflow_state in ('active', 'locked', 'post_delayed')
group by 
	dtf.course_id
on duplicate key update 
	discussion_topic_count = @discussion_topic_count;


insert into canvasdata.ssc_discussion_counts (course_id, discussion_graded_count)
SELECT 
	dtf.course_id as course_id, 
	@discussion_graded_count := count(discussion_topic_id) 
FROM 
	canvasdata.discussion_topic_fact dtf 
		left outer join canvasdata.discussion_topic_dim dtd on dtf.discussion_topic_id = dtd.id
where 
	dtf.course_id is not null 
	and assignment_id is not null 
	and dtd.type is null
    and dtd.workflow_state in ('active', 'locked', 'post_delayed')
group by 
	dtf.course_id
on duplicate key 
update 
	discussion_graded_count = @discussion_graded_count;
    
insert into canvasdata.ssc_discussion_counts (course_id, discussion_entry_count)
SELECT 
	def.course_id as course_id, 
    @discussion_entry_count := count(def.discussion_entry_id) 
FROM 
	canvasdata.discussion_entry_fact def
    left outer join canvasdata.discussion_entry_dim ded on def.discussion_entry_id = ded.id
where 
	def.course_id is not null
    and ded.workflow_state = 'active'
group by 
	def.course_id
on duplicate key update discussion_entry_count = @discussion_entry_count;


insert into canvasdata.ssc_discussion_counts (course_id, discussion_announcement_count)
SELECT 
	dtf.course_id as course_id, 
    @discussion_announcement_count := count(discussion_topic_id) 
FROM 
	canvasdata.discussion_topic_fact dtf 
		left outer join canvasdata.discussion_topic_dim dtd on dtf.discussion_topic_id = dtd.id
where 
	dtf.course_id is not null
	and dtd.type = 'Announcement'
    and dtd.workflow_state in ('active', 'locked', 'post_delayed')
group by 
	dtf.course_id
on duplicate key update 
	discussion_announcement_count = @discussion_announcement_count
