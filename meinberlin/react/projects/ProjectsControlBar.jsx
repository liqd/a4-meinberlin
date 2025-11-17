import React, { useEffect, useRef, useState } from 'react'
import django from 'django'
import { TypeaheadField } from '../contrib/TypeaheadField'
import { MultiSelect } from '../contrib/forms/MultiSelect'
import { classNames } from 'adhocracy4'
import { ControlBarFilterPills } from '../contrib/ControlBarFilterPills'
import SaveSearchProfile from '../plans/SaveSearchProfile'
import { GroupMultiSelect } from '../contrib/forms/GroupMultiSelect'

const translated = {
  search: django.gettext('Search'),
  reset: django.gettext('Reset'),
  showFilters: django.gettext('Show more'),
  hideFilters: django.gettext('Show less'),
  districtsKieze: django.gettext('Kiezes & Districts'),
  allDistrictsKieze: django.gettext('All districts'),
  savedKieze: django.gettext('Your saved Kieze'),
  createKiez: django.gettext('You can create your own Kieze in the user account settings.'),
  districts: django.gettext('Districts'),
  topics: django.gettext('Topics'),
  allTopics: django.gettext('All topics'),
  participations: django.gettext('Kind of participation'),
  allParticipation: django.gettext('All'),
  projectState: django.gettext('Project state'),
  projectStatePlaceholder: django.gettext('None'),
  organisation: django.gettext('Organization'),
  onlyShow: django.gettext('Only show:'),
  plans: django.gettext('Plans'),
  nav: django.gettext('Search, filter and sort the ideas list'),
  searchFor: django.gettext('Search for Proposals'),
  button: django.gettext('Show projects'),
  searchProfileCreatedTitle: django.gettext('Search profile created successfully'),
  searchProfileCreatedText: (url) =>
    django.interpolate(
      django.gettext('You will be informed about new projects that meet the selected filters. You can manage your search profiles in the User Settings under <a href="%(url)s">Search Profiles</a>.'),
      { url },
      true
    ),
  searchProfileLimitExceededTitle: django.gettext('Search profile cannot be saved'),
  searchProfileLimitExceededText: (url) =>
    django.interpolate(
      django.gettext('You have saved the maximum number of 10 search profiles. To save a new one, delete an existing profile in the User Settings under <a href="%(url)s">Search Profiles</a>.'),
      { url },
      true
    )
}

const statusNames = {
  active: django.gettext('ongoing'),
  future: django.gettext('upcoming'),
  past: django.gettext('done')
}

const initialState = {
  search: '',
  districts: [],
  organisation: [],
  participations: [],
  topics: [],
  projectState: ['active', 'future'],
  plansOnly: false,
  kiezradars: []
}

const getAlteredFilters = (
  {
    search,
    districts,
    topics,
    projectState,
    organisation,
    participations,
    kiezradars,
    plansOnly
  },
  topicChoices,
  participationChoices
) => {
  const filters = []
  if (search !== initialState.search) {
    filters.push({ label: search, type: 'search', value: search })
  }
  districts.forEach(d => filters.push({ label: d, type: 'districts', value: d }))
  topics.forEach(topicCode => {
    const choice = topicChoices.find(choice => choice.code === topicCode)
    if (choice) {
      filters.push({ label: choice.name, type: 'topics', value: topicCode })
    }
  })
  projectState.forEach(s => filters.push({ label: statusNames[s], type: 'projectState', value: s }))
  organisation.forEach(o => filters.push({ label: o, type: 'organisation', value: o }))
  participations.forEach(participationId => {
    const choice = participationChoices.find(choice => choice.value === participationId)
    if (typeof choice !== 'undefined') {
      filters.push({ label: choice.name, type: 'participations', value: participationId })
    }
  })
  kiezradars.forEach(k => filters.push({ label: k, type: 'kiezradars', value: k }))

  if (typeof plansOnly === 'boolean') {
    filters.push({ label: translated.plans, type: 'plansOnly', value: plansOnly })
  }

  return filters
}

export const ProjectsControlBar = ({
  districts,
  organisations,
  participationChoices,
  topicChoices,
  appliedFilters,
  onFiltered,
  onResetClick,
  onAlert,
  onError,
  hasContainer,
  kiezradars,
  searchProfile: initialSearchProfile,
  searchProfilesApiUrl,
  searchProfilesUrl,
  searchProfilesCount: initialSearchProfilesCount,
  setParams,
  syncTrigger,
  isAuthenticated,
  projectStatus
}) => {
  const [expandFilters, setExpandFilters] = useState(false)
  const [filters, setFilters] = useState(appliedFilters)
  const onFilterChange = (type, choice) => {
    setFilters({ ...filters, [type]: choice })
  }
  const alteredFilters = getAlteredFilters(appliedFilters, topicChoices, participationChoices)
  const [searchProfile, setSearchProfile] = useState(initialSearchProfile)
  const [searchProfilesCount, setSearchProfilesCount] = useState(initialSearchProfilesCount)
  const filtersContainerRef = useRef(null)

  const isFiltersInitialState = JSON.stringify(appliedFilters) === JSON.stringify(initialState)

  useEffect(() => {
    if (JSON.stringify(appliedFilters) !== JSON.stringify(filters)) {
      setFilters(appliedFilters)
    }
  }, [syncTrigger])

  useEffect(() => {
    if (expandFilters && filtersContainerRef.current) {
      filtersContainerRef.current.focus()
    }
  }, [expandFilters])

  const handleCreateSearchProfile = (searchProfile, limitExceeded) => {
    if (limitExceeded) {
      onError({
        title: translated.searchProfileLimitExceededTitle,
        message: (
          <div
            dangerouslySetInnerHTML={{
              __html: translated.searchProfileLimitExceededText(searchProfilesUrl)
            }}
          />
        )
      })
      return
    }

    setSearchProfile(searchProfile)
    setSearchProfilesCount(searchProfilesCount + 1)
    setParams({ 'search-profile': searchProfile.id, ...filters })

    onAlert({
      title: translated.searchProfileCreatedTitle,
      message: (
        <div
          dangerouslySetInnerHTML={{
            __html: translated.searchProfileCreatedText(searchProfilesUrl)
          }}
        />
      )
    })
  }

  const handleSubmit = (e) => {
    e.preventDefault()

    const newFilters = { ...filters }
    if (newFilters.projectState.length === 0) {
      newFilters.projectState = initialState.projectState
    }

    onFiltered(newFilters)
    setSearchProfile(null)
    setParams(newFilters)
  }

  const handleReset = () => {
    setFilters(initialState)
    onResetClick()
    setSearchProfile(null)
    setParams({})
  }

  return (
    <div aria-label={translated.nav}>
      <form
        className={classNames('modul-facetingform js-facetingform', alteredFilters.length ? 'control-bar--no-spacing' : 'control-bar--spacing')}
        onSubmit={handleSubmit}
      >
        <div className="facetingform__container">
          <div className="facets">
            <div className="container">
              <fieldset className="facet">
                <div className="facet__body">
                  <div className="searchform-slot mb-3">
                    <div className="form-group">
                      <label htmlFor="searchterm" className="form-label">
                        {translated.search}
                      </label>
                      <div className="a4-control-bar__search__term my-0">
                        <div className="input-wrapper">
                          <i className="a4-control-bar__search__logo-start" aria-hidden="true" />
                          <input
                            type="search"
                            className="form-control a4-control-bar__search__input"
                            placeholder={translated.searchPlaceholder}
                            value={filters.search}
                            id="searchterm"
                            autoComplete="on"
                            onChange={(e) => onFilterChange('search', e.target.value)}
                          />
                        </div>
                      </div>
                    </div>
                  </div>
                  <div className="flexgrid grid--2">
                    <div className="span--1">
                      <GroupMultiSelect
                        label={translated.districtsKieze}
                        placeholder={translated.allDistrictsKieze}
                        groups={[
                          {
                            title: translated.savedKieze,
                            info: kiezradars.length === 0 ? translated.createKiez : null,
                            choices: kiezradars.map((choice) => ({
                              value: choice.name,
                              name: choice.name
                            }))
                          },
                          {
                            title: translated.districts,
                            choices: districts.map((choice) => ({
                              value: choice.name,
                              name: choice.name
                            }))
                          }
                        ]}
                        values={[...filters.kiezradars, ...filters.districts]}
                        onChange={(choices) => {
                          const selectedKiezradars = choices.filter((choice) =>
                            kiezradars.some((kiezradar) => kiezradar.name === choice)
                          )

                          const selectedDistricts = choices.filter((choice) =>
                            districts.some((district) => district.name === choice)
                          )

                          const hasKiezradarsChanged =
                            selectedKiezradars.length !== filters.kiezradars.length ||
                            selectedKiezradars.some((k) => !filters.kiezradars.includes(k))

                          const hasDistrictsChanged =
                            selectedDistricts.length !== filters.districts.length ||
                            selectedDistricts.some((d) => !filters.districts.includes(d))

                          if (hasKiezradarsChanged) {
                            onFilterChange('kiezradars', selectedKiezradars)
                          }

                          if (hasDistrictsChanged) {
                            onFilterChange('districts', selectedDistricts)
                          }
                        }}
                      />
                    </div>
                    <div className="span--1">
                      <MultiSelect
                        label={translated.topics}
                        placeholder={translated.allTopics}
                        choices={topicChoices.map((topic) => ({ value: topic.code, name: topic.name }))}
                        values={filters.topics}
                        onChange={(choices) => onFilterChange('topics', choices)}
                      />
                    </div>
                  </div>
                  {expandFilters && (
                    <div ref={filtersContainerRef} tabIndex="-1">
                      <div className="flexgrid grid--2">
                        <div className="span--1">
                          <MultiSelect
                            label={translated.participations}
                            placeholder={translated.allParticipation}
                            choices={participationChoices.map((choice) => ({ value: choice.value, name: choice.name }))}
                            onChange={(choices) => onFilterChange('participations', choices)}
                            values={filters.participations}
                          />
                        </div>
                        <div className="span--1">
                          <MultiSelect
                            label={translated.projectState}
                            choices={Object.entries(statusNames).map(([key, choice]) => ({ value: key, name: choice }))}
                            values={filters.projectState}
                            onChange={(choices) => onFilterChange('projectState', choices)}
                            placeholder={translated.projectStatePlaceholder}
                          />
                        </div>
                      </div>
                      <TypeaheadField
                        typeaheadHeading={translated.organisation}
                        uniqueId="organisation-typeahead-id"
                        onTypeaheadChange={(choice) => onFilterChange('organisation', choice)}
                        typeaheadOptions={organisations.map((organisation) => organisation.name)}
                        typeaheadSelected={filters.organisation}
                        multipleBoolean
                      />
                      <fieldset className="control-bar__checkboxes">
                        <legend className="control-bar__checkboxes-legend">{translated.onlyShow}</legend>
                        <div className="form-check form-check-inline control-bar__form-check-inline">
                          <input
                            id="plans"
                            className="form-check-input control-bar__check-input"
                            type="checkbox"
                            checked={filters.plansOnly}
                            onChange={() => onFilterChange('plansOnly', !filters.plansOnly)}
                          />
                          <label className="form-check-label" htmlFor="plans">
                            {translated.plans}
                          </label>
                        </div>
                      </fieldset>
                    </div>
                  )}
                  <button
                    onClick={() => setExpandFilters(!expandFilters)}
                    className="control-bar__filter-btn"
                    aria-controls="filters"
                    aria-expanded={expandFilters}
                    type="button"
                  >
                    <span className={'fa fa-chevron-' + (expandFilters ? 'up' : 'down')} aria-hidden="true" />&nbsp;
                    {expandFilters ? translated.hideFilters : translated.showFilters}
                  </button>
                </div>
              </fieldset>
              <div className="form-actions">
                <div className="form-actions__left">
                  <button
                    type="button"
                    className="link"
                    onClick={handleReset}
                  >
                    {translated.reset}
                  </button>
                </div>
                <div className="form-actions__right">
                  <button
                    className="button control-bar__action-btn"
                    type="submit"
                  >
                    {translated.button}
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </form>

      {alteredFilters.length
        ? (
          <div className={hasContainer && 'container'}>
            <div className="control-bar__bottom--projects">
              <ControlBarFilterPills
                filters={alteredFilters}
                onRemove={(type, value) => {
                  const newFilters = { ...filters }

                  if (Array.isArray(newFilters[type])) {
                    newFilters[type] = newFilters[type].filter(f => f !== value)
                  } else {
                    newFilters[type] = initialState[type]
                  }

                  // If no more value for projectState filter, this avoids showing 0 results
                  if (newFilters.projectState.length === 0) {
                    newFilters.projectState = ['active', 'future']
                  }

                  setFilters(newFilters)
                  onFiltered(newFilters)
                  setParams(newFilters)
                }}
              />
              {!isFiltersInitialState && (
                <SaveSearchProfile
                  districts={districts}
                  organisations={organisations}
                  topicChoices={topicChoices}
                  participationChoices={participationChoices}
                  projectStatus={projectStatus}
                  kiezradars={kiezradars}
                  searchProfile={searchProfile}
                  searchProfilesApiUrl={searchProfilesApiUrl}
                  searchProfilesCount={searchProfilesCount}
                  isAuthenticated={isAuthenticated}
                  appliedFilters={appliedFilters}
                  onSearchProfileCreate={handleCreateSearchProfile}
                />
              )}
            </div>
          </div>
          )
        : null}
    </div>
  )
}
