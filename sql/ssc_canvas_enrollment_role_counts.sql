
#populate enrollment info  ====================
insert into ssc_canvas_enrollment_role_counts (course_id, section_id, student)
SELECT 
e.course_id, 
e.course_section_id as section_id, 
@enrollment_count := count(e.id)
 FROM canvasdata.enrollment_dim e
left outer join role_dim r on e.role_id = r.id
where e.workflow_state not in ('deleted', 'inactive', 'invited', 'rejected', 'creation_pending')
and r.name = 'StudentEnrollment'
group by section_id, role_id
ON DUPLICATE KEY UPDATE student = @enrollment_count;

insert into ssc_canvas_enrollment_role_counts (course_id, section_id, teacher)
SELECT 
e.course_id, 
e.course_section_id as section_id, 
@enrollment_count := count(e.id)
 FROM canvasdata.enrollment_dim e
left outer join role_dim r on e.role_id = r.id
where e.workflow_state not in ('deleted', 'inactive', 'invited', 'rejected', 'creation_pending')
and r.name = 'TeacherEnrollment'
group by section_id, role_id
ON DUPLICATE KEY UPDATE teacher = @enrollment_count;

insert into ssc_canvas_enrollment_role_counts (course_id, section_id, ta)
SELECT 
e.course_id, 
e.course_section_id as section_id, 
@enrollment_count := count(e.id)
 FROM canvasdata.enrollment_dim e
left outer join role_dim r on e.role_id = r.id
where e.workflow_state not in ('deleted', 'inactive', 'invited', 'rejected', 'creation_pending')
and r.name = 'TaEnrollment'
group by section_id, role_id
ON DUPLICATE KEY UPDATE ta = @enrollment_count;

insert into ssc_canvas_enrollment_role_counts (course_id, section_id, designer)
SELECT 
e.course_id, 
e.course_section_id as section_id, 
@enrollment_count := count(e.id)
 FROM canvasdata.enrollment_dim e
left outer join role_dim r on e.role_id = r.id
where e.workflow_state not in ('deleted', 'inactive', 'invited', 'rejected', 'creation_pending')
and r.name = 'DesignerEnrollment'
group by section_id, role_id
ON DUPLICATE KEY UPDATE designer = @enrollment_count;

insert into ssc_canvas_enrollment_role_counts (course_id, section_id, observer)
SELECT 
e.course_id, 
e.course_section_id as section_id, 
@enrollment_count := count(e.id)
 FROM canvasdata.enrollment_dim e
left outer join role_dim r on e.role_id = r.id
where e.workflow_state not in ('deleted', 'inactive', 'invited', 'rejected', 'creation_pending')
and r.name = 'ObserverEnrollment'
group by section_id, role_id
ON DUPLICATE KEY UPDATE observer = @enrollment_count;

insert into ssc_canvas_enrollment_role_counts (course_id, section_id, librarian)
SELECT 
e.course_id, 
e.course_section_id as section_id, 
@enrollment_count := count(e.id)
 FROM canvasdata.enrollment_dim e
left outer join role_dim r on e.role_id = r.id
where e.workflow_state not in ('deleted', 'inactive', 'invited', 'rejected', 'creation_pending')
and r.name = 'Librarian'
group by section_id, role_id
ON DUPLICATE KEY UPDATE librarian = @enrollment_count;

insert into ssc_canvas_enrollment_role_counts (course_id, section_id, coordinator)
SELECT 
e.course_id, 
e.course_section_id as section_id, 
@enrollment_count := count(e.id)
 FROM canvasdata.enrollment_dim e
left outer join role_dim r on e.role_id = r.id
where e.workflow_state not in ('deleted', 'inactive', 'invited', 'rejected', 'creation_pending')
and r.name = 'Coordinator'
group by section_id, role_id
ON DUPLICATE KEY UPDATE coordinator = @enrollment_count;

insert into ssc_canvas_enrollment_role_counts (course_id, section_id, ta2)
SELECT 
e.course_id, 
e.course_section_id as section_id, 
@enrollment_count := count(e.id)
 FROM canvasdata.enrollment_dim e
left outer join role_dim r on e.role_id = r.id
where e.workflow_state not in ('deleted', 'inactive', 'invited', 'rejected', 'creation_pending')
and r.name = 'TA 2'
group by section_id, role_id
ON DUPLICATE KEY UPDATE ta2 = @enrollment_count;

insert into ssc_canvas_enrollment_role_counts (course_id, section_id, bulkta)
SELECT 
e.course_id, 
e.course_section_id as section_id, 
@enrollment_count := count(e.id)
 FROM canvasdata.enrollment_dim e
left outer join role_dim r on e.role_id = r.id
where e.workflow_state not in ('deleted', 'inactive', 'invited', 'rejected', 'creation_pending')
and r.name = 'BulkTA'
group by section_id, role_id
ON DUPLICATE KEY UPDATE bulkta = @enrollment_count;

insert into ssc_canvas_enrollment_role_counts (course_id, section_id, bulkta_d)
SELECT 
e.course_id, 
e.course_section_id as section_id, 
@enrollment_count := count(e.id)
 FROM canvasdata.enrollment_dim e
left outer join role_dim r on e.role_id = r.id
where e.workflow_state not in ('deleted', 'inactive', 'invited', 'rejected', 'creation_pending')
and r.name = 'BulkTA-D'
group by section_id, role_id
ON DUPLICATE KEY UPDATE bulkta_d = @enrollment_count;

insert into ssc_canvas_enrollment_role_counts (course_id, section_id, tutor)
SELECT 
e.course_id, 
e.course_section_id as section_id, 
@enrollment_count := count(e.id)
 FROM canvasdata.enrollment_dim e
left outer join role_dim r on e.role_id = r.id
where e.workflow_state not in ('deleted', 'inactive', 'invited', 'rejected', 'creation_pending')
and r.name = 'Tutor'
group by section_id, role_id
ON DUPLICATE KEY UPDATE tutor = @enrollment_count;

insert into ssc_canvas_enrollment_role_counts (course_id, section_id, participant)
SELECT 
e.course_id, 
e.course_section_id as section_id, 
@enrollment_count := count(e.id)
 FROM canvasdata.enrollment_dim e
left outer join role_dim r on e.role_id = r.id
where e.workflow_state not in ('deleted', 'inactive', 'invited', 'rejected', 'creation_pending')
and r.name = 'Participant'
group by section_id, role_id
ON DUPLICATE KEY UPDATE participant = @enrollment_count;

insert into ssc_canvas_enrollment_role_counts (course_id, section_id, club_officer)
SELECT 
e.course_id, 
e.course_section_id as section_id, 
@enrollment_count := count(e.id)
 FROM canvasdata.enrollment_dim e
left outer join role_dim r on e.role_id = r.id
where e.workflow_state not in ('deleted', 'inactive', 'invited', 'rejected', 'creation_pending')
and r.name = 'Club Officer'
group by section_id, role_id
ON DUPLICATE KEY UPDATE club_officer = @enrollment_count;

insert into ssc_canvas_enrollment_role_counts (course_id, section_id, grading_ta)
SELECT 
e.course_id, 
e.course_section_id as section_id, 
@enrollment_count := count(e.id)
 FROM canvasdata.enrollment_dim e
left outer join role_dim r on e.role_id = r.id
where e.workflow_state not in ('deleted', 'inactive', 'invited', 'rejected', 'creation_pending')
and r.name = 'GradingTA'
group by section_id, role_id
ON DUPLICATE KEY UPDATE grading_ta = @enrollment_count;

insert into ssc_canvas_enrollment_role_counts (course_id, section_id, etc_observer)
SELECT 
e.course_id, 
e.course_section_id as section_id, 
@enrollment_count := count(e.id)
 FROM canvasdata.enrollment_dim e
left outer join role_dim r on e.role_id = r.id
where e.workflow_state not in ('deleted', 'inactive', 'invited', 'rejected', 'creation_pending')
and r.name = 'ETC Observer'
group by section_id, role_id
ON DUPLICATE KEY UPDATE etc_observer = @enrollment_count;

insert into ssc_canvas_enrollment_role_counts (course_id, section_id, career_coach)
SELECT 
e.course_id, 
e.course_section_id as section_id, 
@enrollment_count := count(e.id)
 FROM canvasdata.enrollment_dim e
left outer join role_dim r on e.role_id = r.id
where e.workflow_state not in ('deleted', 'inactive', 'invited', 'rejected', 'creation_pending')
and r.name = 'Career Coach'
group by section_id, role_id
ON DUPLICATE KEY UPDATE career_coach = @enrollment_count;

insert into ssc_canvas_enrollment_role_counts (course_id, section_id, career_prog_advsr)
SELECT 
e.course_id, 
e.course_section_id as section_id, 
@enrollment_count := count(e.id)
 FROM canvasdata.enrollment_dim e
left outer join role_dim r on e.role_id = r.id
where e.workflow_state not in ('deleted', 'inactive', 'invited', 'rejected', 'creation_pending')
and r.name = 'Career Prog Advsr'
group by section_id, role_id
ON DUPLICATE KEY UPDATE career_prog_advsr = @enrollment_count;

insert into ssc_canvas_enrollment_role_counts (course_id, section_id, librarian_health_sciences)
SELECT 
e.course_id, 
e.course_section_id as section_id, 
@enrollment_count := count(e.id)
 FROM canvasdata.enrollment_dim e
left outer join role_dim r on e.role_id = r.id
where e.workflow_state not in ('deleted', 'inactive', 'invited', 'rejected', 'creation_pending')
and r.name = 'Librarian - Health Sciences'
group by section_id, role_id
ON DUPLICATE KEY UPDATE librarian_health_sciences = @enrollment_count;

insert into ssc_canvas_enrollment_role_counts (course_id, section_id, career_prog_advsr_ii)
SELECT 
e.course_id, 
e.course_section_id as section_id, 
@enrollment_count := count(e.id)
 FROM canvasdata.enrollment_dim e
left outer join role_dim r on e.role_id = r.id
where e.workflow_state not in ('deleted', 'inactive', 'invited', 'rejected', 'creation_pending')
and r.name = 'Career Prog Advsr II'
group by section_id, role_id
ON DUPLICATE KEY UPDATE career_prog_advsr_ii = @enrollment_count;

insert into ssc_canvas_enrollment_role_counts (course_id, section_id, advisor)
SELECT 
e.course_id, 
e.course_section_id as section_id, 
@enrollment_count := count(e.id)
 FROM canvasdata.enrollment_dim e
left outer join role_dim r on e.role_id = r.id
where e.workflow_state not in ('deleted', 'inactive', 'invited', 'rejected', 'creation_pending')
and r.name = 'Advisor'
group by section_id, role_id
ON DUPLICATE KEY UPDATE advisor = @enrollment_count;

insert into ssc_canvas_enrollment_role_counts (course_id, section_id, tutor_acg)
SELECT 
e.course_id, 
e.course_section_id as section_id, 
@enrollment_count := count(e.id)
 FROM canvasdata.enrollment_dim e
left outer join role_dim r on e.role_id = r.id
where e.workflow_state not in ('deleted', 'inactive', 'invited', 'rejected', 'creation_pending')
and r.name = 'Tutor (ACG)'
group by section_id, role_id
ON DUPLICATE KEY UPDATE tutor_acg = @enrollment_count;

insert into ssc_canvas_enrollment_role_counts (course_id, section_id, academic_success_coach)
SELECT 
e.course_id, 
e.course_section_id as section_id, 
@enrollment_count := count(e.id)
 FROM canvasdata.enrollment_dim e
left outer join role_dim r on e.role_id = r.id
where e.workflow_state not in ('deleted', 'inactive', 'invited', 'rejected', 'creation_pending')
and r.name = 'Academic Success Coach'
group by section_id, role_id
ON DUPLICATE KEY UPDATE academic_success_coach = @enrollment_count;

insert into ssc_canvas_enrollment_role_counts (course_id, section_id, career_coach)
SELECT 
e.course_id, 
e.course_section_id as section_id, 
@enrollment_count := count(e.id)
 FROM canvasdata.enrollment_dim e
left outer join role_dim r on e.role_id = r.id
where e.workflow_state not in ('deleted', 'inactive', 'invited', 'rejected', 'creation_pending')
and r.name in ('Career Center Teacher', 'Teacher - Career Center', 'Career Coach')
group by section_id, role_id
ON DUPLICATE KEY UPDATE career_coach = @enrollment_count
