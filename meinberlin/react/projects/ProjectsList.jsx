import React from 'react'
import ProjectTile from './ProjectTile'
import { classNames } from 'adhocracy4'

const ProjectsList = ({ projects, topicChoices, isHorizontal, searchCompletedProjects }) => {
  return (
    <ul className={classNames('projects-list', isHorizontal ? 'projects-list--horizontal' : 'projects-list--vertical')}>
      {
        projects.length > 0 &&
        projects.map((project) => (
          <li key={project.id}>
            <ProjectTile
              project={project}
              isHorizontal={isHorizontal}
              topicChoices={topicChoices}
            />
          </li>
        ))
      }
      <li>
        <p>
          Show completed projects too?
        </p>
        <button
          onClick={searchCompletedProjects}
          className="button button--light"
          // aria-controls="filters"
          // aria-expanded={expandFilters}
          type="button"
        >
          Show completed
        </button>
      </li>
    </ul>
  )
}

export default ProjectsList
