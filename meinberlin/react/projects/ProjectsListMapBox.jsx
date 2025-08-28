/* global django */
import React, { useCallback, useEffect, useMemo, useRef, useState } from 'react'
import ProjectsList from '../projects/ProjectsList'
import { ToggleSwitch } from '../contrib/ToggleSwitch'
import { IconSwitch } from '../contrib/IconSwitch'
import { alert as Alert, classNames } from 'adhocracy4'
import sortProjects from './sort-projects'
import ProjectsMap from './ProjectsMap'
import Spinner from '../contrib/Spinner'
import { ProjectsControlBar } from './ProjectsControlBar'
import { filterProjects } from './filter-projects'
import { getDefaultProjectState, getDefaultState } from './getDefaultState'
import { useSearchParams } from 'react-router-dom'
import { toSearchParams } from '../contrib/helpers'

const pageHeader = django.gettext('Kiezradar')
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
  searchProfilesApiUrl,
  searchProfilesUrl,
  attribution,
  bounds,
  baseUrl,
  mapboxToken,
  omtToken,
  useVectorMap,
  // for filtering:
  districts,
  participationChoices,
  projectStatus,
  organisations,
  kiezradars,
  searchProfile,
  searchProfilesCount,
  isAuthenticated
}) => {
  const [searchParams, setSearchParams] = useSearchParams()
  const [showMap, setShowMap] = useState(true)
  const [loading, setLoading] = useState(true)
  const [projectState, setProjectState] = useState(getDefaultProjectState(searchParams))
  const [items, setItems] = useState([])
  const fetchCache = useRef({})
  const resultRef = useRef({})
  const [appliedFilters, setAppliedFilters] = useState(getDefaultState(searchParams, { districts, organisations, participationChoices, topicChoices, kiezradars }))
  const [alert, setAlert] = useState(null)
  const [error, setError] = useState(null)

  const setParams = (params) => {
    console.log(params)
    const searchParams = toSearchParams(params)
    setSearchParams(searchParams, { replace: true })
  }

  const [syncTrigger, setSyncTrigger] = useState(0)

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

  useEffect(() => {
    if (alert) {
      window.scrollTo({
        top: 0,
        left: 0,
        behavior: 'smooth'
      })
    }
  }, [alert])

  let status = nothingStr

  const filteredItems = useMemo(() => filterProjects(items, appliedFilters, kiezradars, topicChoices, projectState), [items, appliedFilters, kiezradars, projectState])
  if (loading) {
    status = (
      <Spinner />
    )
  } else if (filteredItems.length > 0) {
    status = getResultCountText(filteredItems.length)
  }

  return (
    <div>
      {(error || alert) && (
        <div className="container">
          {error && (
            <Alert
              type="danger"
              title={error.title}
              message={error.message}
              onClick={() => setError(null)}
            />
          )}
          {alert && (
            <Alert
              type="success"
              title={alert.title}
              message={alert.message}
              onClick={() => setAlert(null)}
            />
          )}
        </div>
      )}
      <ProjectsControlBar
        participationChoices={participationChoices}
        organisations={organisations}
        districts={districts}
        topicChoices={topicChoices}
        kiezradars={kiezradars}
        appliedFilters={{ ...appliedFilters, projectState }}
        hasContainer={!showMap}
        onFiltered={({ projectState, ...filters }) => {
          setProjectState(projectState)
          setAppliedFilters(filters)
          resultRef && resultRef.current.scrollIntoView({ behavior: 'smooth', block: 'center', inline: 'nearest' })
        }}
        onResetClick={() => {
          setAppliedFilters(getDefaultState(null, { districts, organisations, participationChoices, topicChoices, kiezradars }))
          setProjectState(['active', 'future'])
        }}
        onAlert={setAlert}
        onError={setError}
        searchProfile={searchProfile}
        searchProfilesApiUrl={searchProfilesApiUrl}
        searchProfilesUrl={searchProfilesUrl}
        searchProfilesCount={searchProfilesCount}
        setParams={setParams}
        syncTrigger={syncTrigger}
        isAuthenticated={isAuthenticated}
        projectStatus={projectStatus}
      />
      <div className={classNames('projects-list', !showMap && 'container')}>
        <h1 className="aural">{pageHeader}</h1>
        <div className={classNames('projects-list__list-meta', filteredItems.length === 0 && 'projects-list__list-meta--no-results')}>
          <div
            ref={resultRef}
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
              showSearchCompletedProjectsButton={
                !(projectState.length > 0 &&
                  projectState.includes('past'))
              }
              searchCompletedProjects={() => {
                const newFilters = {
                  ...appliedFilters,
                  projectState: ['past']
                }

                setAppliedFilters(newFilters)
                setProjectState(['past'])
                setParams(newFilters)

                // Tells child ProjectsControlBar to update
                setSyncTrigger(prev => prev + 1)

                setTimeout(() => {
                  resultRef?.current?.scrollIntoView({
                    behavior: 'smooth',
                    block: 'center'
                  })
                }, 100)
              }}
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
