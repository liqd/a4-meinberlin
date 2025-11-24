import React from 'react'
import django from 'django'
import ProjectTile from './ProjectTile'
import { classNames } from 'adhocracy4'
import Spinner from '../contrib/Spinner'
const translated = {
  showCompletedProjectsHeading: django.gettext('Show completed projects too?'),
  showCompletedProjectsBody: django.gettext('Expand your search to view completed projects and discover more possibilities.'),
  showCompletedProjectsButton: django.gettext('Show completed')
}

const ProjectsList = ({
  projects: initialProjects,
  projectsUrl,
  topicChoices,
  isHorizontal,
  searchCompletedProjects,
  showSearchCompletedProjectsButton
}) => {
  const [projects, setProjects] = React.useState(initialProjects || [])
  const [loading, setLoading] = React.useState(!initialProjects)

  React.useEffect(() => {
    if (!projectsUrl) return

    const fetchData = async () => {
      try {
        const response = await fetch(projectsUrl)
        // eslint-disable-next-line no-restricted-syntax
        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`)

        const data = await response.json()
        setProjects(data)
      } catch (error) {
        console.error('Failed to fetch projects:', error)
        setProjects([])
      } finally {
        setLoading(false)
      }
    }

    fetchData()
  }, [projectsUrl])

  if (loading) return <Spinner />
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
