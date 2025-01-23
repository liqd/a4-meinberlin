import React, { useState } from 'react'
import django from 'django'
import { TypeaheadField } from '../contrib/TypeaheadField'
import { MultiSelect } from '../contrib/forms/MultiSelect'
import { classNames } from 'adhocracy4'
import { ControlBarFilterPills } from '../contrib/ControlBarFilterPills'
import SaveSearchProfile from '../plans/SaveSearchProfile'

const translated = {
  search: django.gettext('Search'),
  reset: django.gettext('Reset'),
  showFilters: django.gettext('Show more'),
  hideFilters: django.gettext('Show less'),
  districts: django.gettext('Districts'),
  allDistricts: django.gettext('All districts'),
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
  button: django.gettext('Show projects')
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
  plansOnly: false
}

const getAlteredFilters = ({ search, districts, topics, projectState, organisation, participations }, topicChoices, participationChoices) => {
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
    const choice = participationChoices.find(choice => choice.id === participationId)
    if (choice) {
      filters.push({ label: choice.name, type: 'participations', value: participationId })
    }
  })

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
  hasContainer,
  searchProfile: initialSearchProfile,
  searchProfilesApiUrl,
  searchProfilesCount: initialSearchProfilesCount,
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

  const isFiltersInitialState = JSON.stringify(appliedFilters) === JSON.stringify(initialState)

  const removeSearchProfile = () => {
    setSearchProfile(null)
    window.history.replaceState({}, '', window.location.pathname)
  }

  const createSearchProfile = (searchProfile) => {
    setSearchProfile(searchProfile)
    setSearchProfilesCount(searchProfilesCount + 1)
    window.history.replaceState({}, '', window.location.pathname + '?search-profile=' + searchProfile.id
    )
  }

  return (
    <nav aria-label={translated.nav}>
      <form
        className={classNames('modul-facetingform js-facetingform', alteredFilters.length ? 'control-bar--no-spacing' : 'control-bar--spacing')}
        onSubmit={(e) => {
          e.preventDefault()
          const newFilters = { ...filters }
          if (newFilters.projectState.length === 0) {
            newFilters.projectState = initialState.projectState
          }
          onFiltered(newFilters)
          removeSearchProfile()
        }}
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
                            onChange={(e) => onFilterChange('search', e.target.value)}
                          />
                        </div>
                      </div>
                    </div>
                  </div>
                  <div className="flexgrid grid--2">
                    <div className="span--1">
                      <MultiSelect
                        label={translated.districts}
                        placeholder={translated.allDistricts}
                        choices={districts.map((choice) => ({ value: choice.name, name: choice.name }))}
                        values={filters.districts}
                        onChange={(choices) => onFilterChange('districts', choices)}
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
                    <>
                      <div className="flexgrid grid--2">
                        <div className="span--1">
                          <MultiSelect
                            label={translated.participations}
                            placeholder={translated.allParticipation}
                            choices={participationChoices.map((choice) => ({ value: choice.id, name: choice.name }))}
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
                    </>
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
                    onClick={() => {
                      setFilters(initialState)
                      onResetClick()
                      removeSearchProfile()
                    }}
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

                  setFilters(newFilters)
                  onFiltered(newFilters)
                }}
              />
              {!isFiltersInitialState && (
                <SaveSearchProfile
                  districts={districts}
                  organisations={organisations}
                  topicChoices={topicChoices}
                  participationChoices={participationChoices}
                  projectStatus={projectStatus}
                  searchProfile={searchProfile}
                  searchProfilesApiUrl={searchProfilesApiUrl}
                  searchProfilesCount={searchProfilesCount}
                  isAuthenticated={isAuthenticated}
                  appliedFilters={appliedFilters}
                  onSearchProfileCreate={createSearchProfile}
                />
              )}
            </div>
          </div>
          )
        : null}
    </nav>
  )
}
