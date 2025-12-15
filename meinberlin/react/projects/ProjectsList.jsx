import React from 'react'
import django from 'django'
import ProjectTile from './ProjectTile'
import { classNames } from 'adhocracy4'
import Spinner from '../contrib/Spinner'

const translated = {
  showCompletedProjectsHeading: django.gettext('Show completed projects too?'),
  showCompletedProjectsBody: django.gettext('Expand your search to view completed projects and discover more possibilities.'),
  showCompletedProjectsButton: django.gettext('Show completed'),
  showingProjects: django.ngettext(
    'Showing %s project',
    'Showing %s projects',
    0
  ),
  noProjectsFound: django.gettext('No projects found')
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
  const [announcement, setAnnouncement] = React.useState('')

  React.useEffect(() => {
    setProjects(initialProjects)
  }, [initialProjects])

  React.useEffect(() => {
    if (!projectsUrl) return

    const fetchData = async () => {
      try {
        setLoading(true)
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

  React.useEffect(() => {
    if (!loading) {
      if (projects.length > 0) {
        setAnnouncement(django.interpolate(translated.showingProjects, [projects.length]))
      } else {
        setAnnouncement(translated.noProjectsFound)
      }
    }
  }, [projects, loading])

  React.useEffect(() => {
    if (initialProjects !== undefined) {
      const count = initialProjects.length
      const message = count > 0
        ? django.interpolate(django.ngettext(
          'Showing %s project',
          'Showing %s projects',
          count
        ), [count])
        : django.gettext('No projects found')
      setAnnouncement(message)
    }
  }, [initialProjects])

  if (loading) return <Spinner />

  return (
    <>
      <div
        aria-live="polite"
        aria-atomic="true"
        className="sr-only"
        role="status"
      >
        {announcement}
      </div>

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
    </>
  )
}

export default ProjectsList
