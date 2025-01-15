/* global django */
import React, { useCallback, useEffect, useMemo, useRef, useState } from 'react'
import ProjectsList from '../projects/ProjectsList'
import { ToggleSwitch } from '../contrib/ToggleSwitch'
import { IconSwitch } from '../contrib/IconSwitch'
import { classNames } from '../contrib/helpers'
import sortProjects from './sort-projects'
import ProjectsMap from './ProjectsMap'
import Spinner from '../contrib/Spinner'
import { ProjectsControlBar } from './ProjectsControlBar'
import { filterProjects } from './filter-projects'
import {
  getDefaultProjectState,
  getDefaultState
} from './getDefaultState'

const pageHeader = django.gettext('Project overview')
const showMapStr = django.gettext('Show map')
const nothingStr = django.gettext('Unfortunately, there are no projects matching your search. Please adjust the search criteria.')
const showMapAriaStr = django.gettext('show map')
const listStr = django.gettext('List')
const mapStr = django.gettext('Map')
const showListStr = django.gettext('show list')
const viewModeStr = django.gettext('View mode')

const getResultCountText = (count) => {
  const foundProposalsText = django.ngettext(
    '1 Proposal found.',
    '%s Proposals found.',
    count
  )
  return django.interpolate(foundProposalsText, [count])
}

const ProjectsListMapBox = ({
  topicChoices,
  projectApiUrl,
  plansApiUrl,
  extprojectApiUrl,
  privateprojectApiUrl,
  attribution,
  bounds,
  baseUrl,
  mapboxToken,
  omtToken,
  useVectorMap,
  // for filtering:
  districtNames,
  districts,
  participationChoices,
  organisations,
  searchProfile
}) => {
  const [showMap, setShowMap] = useState(true)
  const [loading, setLoading] = useState(true)
  const [projectState, setProjectState] = useState(getDefaultProjectState(searchProfile))
  const [items, setItems] = useState([])
  const fetchCache = useRef({})
  const [appliedFilters, setAppliedFilters] = useState(getDefaultState(searchProfile))

  const fetchItems = useCallback(async () => {
    setLoading(true)
    const urls = [
      plansApiUrl,
      extprojectApiUrl,
      privateprojectApiUrl,
      ...projectState.map(state => projectApiUrl + '?status=' + state + 'Participation')
    ]
    const tempItems = []

    Promise.all(
      urls.map(async (url) => {
        try {
          let data
          if (fetchCache.current[url]) {
            data = fetchCache.current[url]
          } else {
            const response = await fetch(url)
            data = await response.json()
            fetchCache.current[url] = data
          }
          tempItems.push(...data)
          setItems(
            // filter out duplicates by title (id is not unique as there are
            // different models in items that can have the same id)
            [...new Map(tempItems.map(v => [v.title, v])).values()]
              .sort(sortProjects)
          )
        } catch (e) {
          console.error(e)
        }
      })
    ).finally(() => setLoading(false))
  }, [plansApiUrl, extprojectApiUrl, privateprojectApiUrl, projectState, projectApiUrl])

  useEffect(() => {
    fetchItems()
  }, [fetchItems])

  let status = nothingStr

  const filteredItems = useMemo(() => filterProjects(items, appliedFilters), [items, appliedFilters])
  if (loading) {
    status = (
      <Spinner />
    )
  } else if (filteredItems.length > 0) {
    status = getResultCountText(filteredItems.length)
  }

  return (
    <div>
      <ProjectsControlBar
        districtNames={districtNames}
        participationChoices={participationChoices}
        organisations={organisations}
        districts={districts}
        topicChoices={topicChoices}
        appliedFilters={{ ...appliedFilters, projectState }}
        hasContainer={!showMap}
        onFiltered={({ projectState, ...filters }) => {
          setProjectState(projectState)
          setAppliedFilters(filters)
        }}
        onResetClick={() => {
          setAppliedFilters(getDefaultState(searchProfile))
          setProjectState(['active', 'future'])
        }}
      />
      <div className={classNames('projects-list', !showMap && 'container')}>
        <h1 className="aural">{pageHeader}</h1>
        <div className={classNames('projects-list__list-meta', filteredItems.length === 0 && 'projects-list__list-meta--no-results')}>
          <div
            role="status"
            className="projects-list__status"
          >
            {status}
          </div>
          <ToggleSwitch
            uniqueId="map-switch"
            className="projects-list__toggle-switch"
            toggleSwitch={() => {
              setShowMap(!showMap)
            }}
            onSwitchStr={showMapStr}
            checked={showMap}
          />
        </div>

        <IconSwitch
          fullWidth
          className="projects-list__icon-switch"
          viewModeStr={viewModeStr}
          buttons={[
            {
              ariaLabel: showListStr,
              label: listStr,
              icon: 'fa fa-list',
              id: 'show_list',
              isActive: !showMap,
              handleClick: () => {
                setShowMap(false)
              }
            },
            {
              ariaLabel: showMapAriaStr,
              label: mapStr,
              icon: 'fa fa-map',
              id: 'show_map',
              isActive: showMap,
              handleClick: () => {
                setShowMap(true)
              }
            }
          ]}
        />
        <div
          className={classNames('projects-list__wrapper', showMap && ' projects-list__wrapper--combined')}
        >
          <div id="list" className="projects-list__list">
            <ProjectsList
              projects={filteredItems}
              isHorizontal={showMap}
              topicChoices={topicChoices}
              loading={loading}
            />
          </div>
          {showMap &&
            <div id="map" className="projects-list__map">
              <ProjectsMap
                attribution={attribution}
                items={filteredItems}
                bounds={bounds}
                baseUrl={baseUrl}
                mapboxToken={mapboxToken}
                omtToken={omtToken}
                useVectorMap={useVectorMap}
                topicChoices={topicChoices}
              />
            </div>}
        </div>
      </div>
    </div>
  )
}

export default ProjectsListMapBox
