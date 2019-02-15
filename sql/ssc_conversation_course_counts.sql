#populate conversation info  ====================
insert into canvasdata.ssc_conversation_course_counts (course_id, conversation_course_count)
select 
	course_id, 
    @conversation_course_count := count(id) 
from 
	canvasdata.conversation_dim 
where 
	course_id is not null
group by 
	course_id
ON DUPLICATE KEY UPDATE conversation_course_count = @conversation_course_count;

insert into canvasdata.ssc_conversation_course_counts (course_id, conversation_course_participant_count)
select 
	course_id, 
    @conversation_course_participant_count := count(conversation_message_id)
from 
	canvasdata.conversation_message_participant_fact 
where 
	course_id is not null
group by 
	course_id
ON DUPLICATE KEY UPDATE conversation_course_participant_count = @conversation_course_participant_count
