import React from 'react'
import { createRoot } from 'react-dom/client'
import ProjectsListMapBox from '../projects/ProjectsListMapBox'
import { BrowserRouter } from 'react-router-dom'

function init () {
  const plansMapBox = document.querySelectorAll('[data-map="plans"]')
  plansMapBox.forEach(el => {
    const projectApiUrl = el.getAttribute('data-projects-url')
    const extprojectApiUrl = el.getAttribute('data-extprojects-url')
    const privateprojectApiUrl = el.getAttribute('data-privateprojects-url')
    const plansApiUrl = el.getAttribute('data-plans-url')
    const attribution = el.getAttribute('data-attribution')
    const baseUrl = el.getAttribute('data-baseurl')
    const bounds = JSON.parse(el.getAttribute('data-bounds'))
    const kiezradars = el.getAttribute('data-kiezradars') && JSON.parse(el.getAttribute('data-kiezradars'))
    const searchProfile = el.getAttribute('data-search-profile') && JSON.parse(el.getAttribute('data-search-profile'))
    const selectedDistrict = el.getAttribute('data-selected-district')
    const selectedTopic = el.getAttribute('data-selected-topic')
    const districts = JSON.parse(el.getAttribute('data-districts'))
    const organisations = JSON.parse(el.getAttribute('data-organisations'))
    const topicChoices = JSON.parse(el.getAttribute('data-topic-choices'))
    const mapboxToken = el.getAttribute('data-mapbox-token')
    const omtToken = el.getAttribute('data-omt-token')
    const useVectorMap = el.getAttribute('data-use_vector_map')
    const participationChoices = JSON.parse(el.getAttribute('data-participation-choices'))
    const searchProfilesApiUrl = el.getAttribute('data-search-profiles-api-url')
    const searchProfilesUrl = el.getAttribute('data-search-profiles-url')
    const searchProfilesCount = JSON.parse(el.getAttribute('data-search-profiles-count'))
    const isAuthenticated = JSON.parse(el.getAttribute('data-is-authenticated'))
    const projectStatus = JSON.parse(el.getAttribute('data-project-status'))
    const root = createRoot(el)
    root.render(
      <React.StrictMode>
        <BrowserRouter>
          <ProjectsListMapBox
            selectedDistrict={selectedDistrict}
            selectedTopic={selectedTopic}
            projectApiUrl={projectApiUrl}
            extprojectApiUrl={extprojectApiUrl}
            privateprojectApiUrl={privateprojectApiUrl}
            plansApiUrl={plansApiUrl}
            attribution={attribution}
            baseUrl={baseUrl}
            mapboxToken={mapboxToken}
            omtToken={omtToken}
            useVectorMap={useVectorMap}
            bounds={bounds}
            organisations={organisations}
            districts={districts}
            topicChoices={topicChoices}
            participationChoices={participationChoices}
            kiezradars={kiezradars}
            searchProfile={searchProfile}
            searchProfilesApiUrl={searchProfilesApiUrl}
            searchProfilesUrl={searchProfilesUrl}
            searchProfilesCount={searchProfilesCount}
            isAuthenticated={isAuthenticated}
            projectStatus={projectStatus}
          />
        </BrowserRouter>
      </React.StrictMode>)
  })
}

document.addEventListener('DOMContentLoaded', init, false)
document.addEventListener('a4.embed.ready', init, false)
