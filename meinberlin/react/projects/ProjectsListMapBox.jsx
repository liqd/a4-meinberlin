/* global django */
import React, { useCallback, useEffect, useState } from 'react'
import ProjectsList from '../projects/ProjectsList'
import { ToggleSwitch } from '../contrib/ToggleSwitch'
import { IconSwitch } from '../contrib/IconSwitch'
import { classNames } from '../contrib/helpers'
import sortProjects from './sort-projects'
import ProjectsMap from './ProjectsMap'
import Spinner from '../contrib/Spinner'

// const statusNames = [
//   django.gettext('ongoing'),
//   django.gettext('done')
// ]

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
  useVectorMap
}) => {
  const [showMap, setShowMap] = useState(true)
  const [loading, setLoading] = useState(true)
  const [projectState] = useState(['active', 'future'])
  const [items, setItems] = useState([])

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
          const response = await fetch(url)
          const data = await response.json()
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
    )
      .finally(() => setLoading(false))
    // TODO: Check if needed when implementing filter story:
    //  this.updateList()
  }, [plansApiUrl, extprojectApiUrl, privateprojectApiUrl, projectState, projectApiUrl])

  useEffect(() => {
    fetchItems()
  }, [fetchItems])

  useEffect(() => {
    // toggle between full width (when map + list) and narrow (when list only)
    document.querySelector('.mb-project-overview').classList.toggle('fullwidth', !!showMap)
  }, [showMap])

  let status = nothingStr

  if (loading) {
    status = (
      <Spinner />
    )
  } else if (items.length > 0) {
    status = getResultCountText(items.length)
  }

  return (
    <div>
      <div className="projects-list">
        <h1 className="aural">{pageHeader}</h1>
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
              handleClick: () => setShowMap(false)
            },
            {
              ariaLabel: showMapAriaStr,
              label: mapStr,
              icon: 'fa fa-map',
              id: 'show_map',
              isActive: showMap,
              handleClick: () => setShowMap(true)
            }
          ]}
        />
        <div
          className={classNames('projects-list__wrapper', showMap && ' projects-list__wrapper--combined')}
        >
          <div id="list" className="projects-list__list">
            <div className={classNames('projects-list__list-meta', items.length === 0 && 'projects-list__list-meta--no-results')}>
              <div
                role="status"
                className="projects-list__status"
              >
                {status}
              </div>
              <ToggleSwitch
                uniqueId="map-switch"
                className="projects-list__toggle-switch"
                toggleSwitch={() => setShowMap(!showMap)}
                onSwitchStr={showMapStr}
                checked={showMap}
              />
            </div>
            <ProjectsList
              projects={items}
              isHorizontal={showMap}
              topicChoices={topicChoices}
              loading={loading}
            />
          </div>
          {showMap &&
            <div id="map" className="projects-list__map">
              {/* <StickyBox offsetTop={0} offsetBottom={0}> */}
              <ProjectsMap
                attribution={attribution}
                items={items}
                bounds={bounds}
                 // currentDistrict={this.state.district}
                 // nonValue={districtnames[districtnames.length - 1]}
                 // districts={districts}
                baseUrl={baseUrl}
                mapboxToken={mapboxToken}
                omtToken={omtToken}
                useVectorMap={useVectorMap}
              />
              {/* </StickyBox> */}
            </div>}
        </div>
      </div>
    </div>
  )
}

export default ProjectsListMapBox
