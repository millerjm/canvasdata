
insert into canvasdata.ssc_discussion_inst_counts (course_id, user_id, discussion_entry_inst_count)
SELECT 
	def.course_id as course_id, 
    def.user_id as user_id, 
    @discussion_entry_inst_count := count(def.discussion_entry_id) 
FROM 
	canvasdata.discussion_entry_fact def
    left outer join canvasdata.discussion_entry_dim ded on def.discussion_entry_id = ded.id
where 
	def.course_id is not null
    and ded.workflow_state = 'active'
group by 
	def.course_id, def.user_id
on duplicate key update discussion_entry_inst_count = @discussion_entry_inst_count
