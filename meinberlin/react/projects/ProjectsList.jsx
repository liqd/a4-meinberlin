import React from 'react'
import django from 'django'
import ProjectTile from './ProjectTile'
import { classNames } from 'adhocracy4'

const translated = {
  showCompletedProjectsHeading: django.gettext('Show completed projects too?'),
  showCompletedProjectsBody: django.gettext('Expand your search to view completed projects and discover more possibilities.'),
  showCompletedProjectsButton: django.gettext('Show completed')
}

const ProjectsList = ({
  projects,
  topicChoices,
  isHorizontal,
  searchCompletedProjects,
  showSearchCompletedProjectsButton
}) => {
  return (
    <ul className={classNames('projects-list', isHorizontal ? 'projects-list--horizontal' : 'projects-list--vertical')}>
      {
        projects.length > 0 &&
        projects.map((project, index) => (
          <li key={'project-' + project.id + '-' + index}>
            <ProjectTile
              project={project}
              isHorizontal={isHorizontal}
              topicChoices={topicChoices}
            />
          </li>
        ))
      }
      {
        showSearchCompletedProjectsButton && (
          <li key="show-completed-projects">
            <h3 className="projects-list__showCompletedHeading">{translated.showCompletedProjectsHeading}</h3>
            <p>
              {translated.showCompletedProjectsBody}
            </p>
            <button
              onClick={searchCompletedProjects}
              className="button button--light"
              type="button"
            >
              {translated.showCompletedProjectsButton}
            </button>
          </li>
        )
      }
    </ul>
  )
}

export default ProjectsList
