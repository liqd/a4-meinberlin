import React, { useState } from 'react'
import django from 'django'
import { TypeaheadField } from '../contrib/TypeaheadField'
import { MultiSelect } from '../contrib/forms/MultiSelect'
import { arraysEqual, classNames } from '../contrib/helpers'
import { ControlBarFilterPills } from '../contrib/ControlBarFilterPills'

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
  organisation: django.gettext('Organization'),
  nav: django.gettext('Search, filter and sort the ideas list'),
  searchFor: django.gettext('Search for Proposals'),
  button: django.gettext('Show projects')
}

const statusNames = {
  active: django.gettext('ongoing'),
  future: django.gettext('upcoming'),
  past: django.gettext('done')
}

export const initialState = {
  search: '',
  districts: [],
  organisation: [],
  participations: [],
  topics: [],
  projectState: ['active', 'future']
}

const getAlteredFilters = ({ search, ...arrayFilters }) => {
  const filters = []
  if (search !== initialState.search) {
    filters.push({ label: translated.search, type: 'search', value: search })
  }

  Object.keys(arrayFilters).forEach(key => {
    if (!arraysEqual(arrayFilters[key], initialState[key])) {
      filters.push({ label: translated[key], type: key, value: arrayFilters[key] })
    }
  })

  return filters
}

export const ProjectsControlBar = ({
  districtNames,
  organisations,
  participationChoices,
  topicChoices,
  appliedFilters,
  onFiltered,
  hasContainer
}) => {
  const [expandFilters, setExpandFilters] = useState(false)
  const [filters, setFilters] = useState(initialState)
  const onFilterChange = (type, choice) => {
    setFilters({ ...filters, [type]: choice })
  }
  const alteredFilters = getAlteredFilters(appliedFilters)

  return (
    <nav aria-label={translated.nav}>
      <form
        className={classNames('modul-facetingform js-facetingform', alteredFilters.length ? 'control-bar--no-spacing' : 'control-bar--spacing')}
        onSubmit={(e) => {
          e.preventDefault()
          onFiltered({ ...filters })
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
                        choices={districtNames.map((choice) => ({ value: choice, name: choice }))}
                        values={filters.districts}
                        onChange={(choices) => onFilterChange('districts', choices)}
                      />
                    </div>
                    <div className="span--1">
                      <MultiSelect
                        label={translated.topics}
                        placeholder={translated.allTopics}
                        choices={Object.entries(topicChoices).map(([key, choice]) => ({ value: key, name: choice }))}
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
                            choices={participationChoices.map((choice, index) => ({ value: index, name: choice }))}
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
                          />
                        </div>
                      </div>
                      <TypeaheadField
                        typeaheadHeading={translated.organisation}
                        uniqueId="organisation-typeahead-id"
                        onTypeaheadChange={(choice) => onFilterChange('organisation', choice)}
                        typeaheadOptions={organisations}
                        typeaheadSelected={filters.organisation}
                        multipleBoolean
                      />
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
            <div className="flexgrid grid grid--2 control-bar__bottom--projects">
              <ControlBarFilterPills
                filters={alteredFilters}
                onRemove={(type) => {
                  const newFilters = { ...filters, [type]: initialState[type] }
                  setFilters(newFilters)
                  onFiltered(newFilters)
                }}
              />
            </div>
          </div>
          )
        : null}
    </nav>
  )
}