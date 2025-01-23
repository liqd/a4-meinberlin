import React from 'react'
import ProjectTile from './ProjectTile'
import { classNames } from 'adhocracy4'

const ProjectsList = ({ projects, topicChoices, isHorizontal }) => {
  if (projects.length > 0) {
    return (
      <ul className={classNames('projects-list', isHorizontal ? 'projects-list--horizontal' : 'projects-list--vertical')}>
        {projects.map((project) => (
          <li key={project.id}>
            <ProjectTile
              project={project}
              isHorizontal={isHorizontal}
              topicChoices={topicChoices}
            />
          </li>
        ))}
      </ul>
    )
  } else {
    return null
  }
}
export default ProjectsList
