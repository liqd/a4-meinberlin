import React from 'react'
import { createRoot } from 'react-dom/client'
import ProjectsList from '../projects/ProjectsList'

function init () {
  const projectsList = document.querySelectorAll('[data-projects-list]')
  projectsList.forEach(el => {
    const root = createRoot(el)
    const projects = JSON.parse(el.getAttribute('data-projects') || '[]')
    const projectsUrl = el.getAttribute('data-projects-url')
    const topicChoices = JSON.parse(el.getAttribute('data-topic-choices'))
    root.render(
      <React.StrictMode>
        <ProjectsList
          projects={projects}
          projectsUrl={projectsUrl}
          topicChoices={topicChoices}
        />
      </React.StrictMode>)
  })
}

document.addEventListener('DOMContentLoaded', init, false)
document.addEventListener('a4.embed.ready', init, false)
