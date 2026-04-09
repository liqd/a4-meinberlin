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
  showMap,
  searchCompletedProjects,
  showSearchCompletedProjectsButton,
  visibleProjects
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
      // When map is shown, use visibleProjects. When map is hidden, use all projects
      const projectsToShow = showMap ? (visibleProjects || []) : projects
      if (projectsToShow.length > 0) {
        setAnnouncement(django.interpolate(translated.showingProjects, [projectsToShow.length]))
      } else {
        setAnnouncement(translated.noProjectsFound)
      }
    }
  }, [projects, visibleProjects, loading, showMap])

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

  // When map is shown, show visible projects (could be empty)
  // When map is hidden, show all projects
  const displayProjects = showMap ? (visibleProjects || []) : projects

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
          displayProjects.length > 0 &&
          displayProjects.map((project, index) => (
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
