import React from 'react'
import { createRoot } from 'react-dom/client'
import ProjectsList from '../projects/ProjectsList'

function init () {
  const projectsList = document.querySelectorAll('[data-projects-list')
  projectsList.forEach(el => {
    const root = createRoot(el)
    const projects = JSON.parse(el.getAttribute('data-projects'))
    root.render(
      <React.StrictMode>
        <ProjectsList projects={projects} />
      </React.StrictMode>)
  })
}

document.addEventListener('DOMContentLoaded', init, false)
document.addEventListener('a4.embed.ready', init, false)
