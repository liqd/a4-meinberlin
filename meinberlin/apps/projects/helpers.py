from django.http import HttpResponse
from django.shortcuts import render
from django.db import connection

def public_projects_exec_raw_query():
	query = """CREATE OR REPLACE VIEW public_project_view AS
        SELECT 
            project.*, 
            district.*, 
            organisation.*, 
            moderator.*, 
            plan.*, 
            initiators.*, 
            phases.*
        FROM 
            a4projects_project project
        LEFT JOIN 
            a4administrative_districts_administrativedistrict district ON project.administrative_district_id = district.id
        LEFT JOIN 
            meinberlin_organisations_organisation organisation ON project.organisation_id = organisation.id
        LEFT JOIN 
            a4projects_project_moderators moderator ON project.id = moderator.project_id
        LEFT JOIN 
            meinberlin_plans_plan plan ON project.id = moderator.project_id
        LEFT JOIN 
            meinberlin_organisations_organisation_initiators initiators ON organisation.id = initiators.organisation_id
        LEFT JOIN 
            a4modules_module module ON project.id = module.project_id
        LEFT JOIN 
            a4phases_phase phases ON module.id = phases.module_id
        WHERE 
            (project.project_type = 'a4projects.Project' OR project.project_type = 'meinberlin_bplan.Bplan')
            AND (project.access = 1 OR project.access = 2)
            AND project.is_draft = FALSE
            AND project.is_archived = FALSE
        ORDER BY 
            project.created;"""

	with connection.cursor() as cursor:
		cursor.execute(query)
