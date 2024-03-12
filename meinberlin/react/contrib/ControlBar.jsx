import React, { useEffect, useState } from 'react'
import { ControlBarDropdown } from './ControlBarDropdown'
import { ControlBarListMapSwitch } from './ControlBarListMapSwitch'
import { ControlBarSearch } from './ControlBarSearch'
import django from 'django'
import { useSearchParams } from 'react-router-dom'
import { ControlBarFilterPills } from './ControlBarFilterPills'
import { useFetchedItems } from './contexts/FetchItemsProvider'
import Spinner from './Spinner'

const translated = {
  reset: django.gettext('Reset'),
  showFilters: django.gettext('Show more'),
  hideFilters: django.gettext('Show less'),
  filters: django.gettext('Filters'),
  filter: django.gettext('Filter'),
  nav: django.gettext('Search, filter and sort the ideas list')
}

const getResultCountText = (count) => {
  const foundProposalsText = django.ngettext(
    '1 proposal found.',
    '%s proposals found.',
    count
  )
  return django.interpolate(foundProposalsText, [count])
}

export const ControlBar = () => {
  // grab the results for the list from the useFetchedItems hook
  const { results: { list }, isMapAndList, viewMode } = useFetchedItems()
  const [expandFilters, setExpandFilters] = useState(true)
  const [queryParams, setQueryParams] = useSearchParams()
  const term = queryParams.get('search') || ''

  const [filters, setFilters] = useState([])
  const appliedFilters = filters
    .concat([{ type: 'search', label: term, value: term }])
    .filter((f) =>
      f.type !== 'ordering' &&
    queryParams?.has(f.type)
    )
    .map((f) => ({ ...f, value: queryParams.get(f.type) || f.value }))
  const nonOrderingFilters = filters.filter((f) => f.type !== 'ordering')

  useEffect(() => {
    // initialize filters object
    if (list?.filters) {
      const updatedFilters = Object.keys(list.filters)
        .map((type) => ({ ...list.filters[type], type, value: queryParams.get(type) }))

      setFilters(updatedFilters)
    }
  }, [list?.filters])

  const applyQuery = (type, value) => {
    if (value || type === 'is_archived') {
      queryParams.set(type, value)
    } else {
      queryParams.delete(type)
    }
    queryParams.delete('page')
    setQueryParams(queryParams)
  }

  const handleSearch = (value) => {
    applyQuery('search', value)
  }

  const handleFilterChange = (type, choice) => {
    setFilters(filters.map(f => f.type === type ? { ...f, value: choice } : f))

    if (type === 'ordering') {
      applyQuery(type, choice)
    }
  }

  const applyAllFilters = () => {
    filters.forEach(f => {
      if (f.value || f.type === 'is_archived') {
        queryParams.set(f.type, f.value)
      } else {
        queryParams.delete(f.type)
      }
    })

    queryParams.delete('page')
    setQueryParams(queryParams)
  }

  const clearFilters = () => {
    setQueryParams('')
    setFilters(filters.map(f => ({ ...f, value: '' })))
  }

  if (!list) {
    return <Spinner />
  }

  return (
    <nav
      className="container u-spacer-bottom u-spacer-top-double"
      aria-label={translated.nav}
    >
      <div className="modul-facetingform js-facetingform">
        <div className="facetingform__container">
          <div className="container__body">
            <div className="facets">
              <fieldset className="facet">
                <div className="facet__body">
                  <div className="flexgrid grid--3">
                    <div className="span2">
                      <ControlBarSearch onSearch={(value) => handleSearch(value)} term={term} />
                    </div>
                    <div className="span1">
                      {viewMode === 'list' && list.filters?.ordering && (
                        <ControlBarDropdown
                          key="ordering_dropdown"
                          filter={list.filters.ordering}
                          current={queryParams.get('ordering')}
                          filterId="id_ordering"
                          onSelectFilter={(choice) => handleFilterChange('ordering', choice[0])}
                        />
                      )}
                    </div>
                  </div>
                </div>
              </fieldset>
              <fieldset className="facet">
                <legend className="facet__head">
                  <span className="facet-title">{translated.filters}</span>
                </legend>
                <div className="facet__body">
                  <div className="flexgrid grid--3" id="filters">
                    {nonOrderingFilters.length > 0 && (
                      nonOrderingFilters
                        .slice(0, expandFilters ? nonOrderingFilters.length : 3).map((filter) => (
                          <ControlBarDropdown
                            key={filter.type}
                            filter={filter}
                            current={filter.value}
                            filterId={'id_' + filter.type}
                            onSelectFilter={(choice) => handleFilterChange(filter.type, choice[0])}
                          />
                        ))
                    )}
                  </div>
                  {nonOrderingFilters.length > 3 && (
                    <button
                      onClick={() => setExpandFilters(!expandFilters)}
                      className="control-bar__filter-btn"
                      aria-controls="filters"
                      aria-expanded={expandFilters}
                    >
                      <span className={'fa fa-chevron-' + (expandFilters ? 'up' : 'down')} aria-hidden="true" />&nbsp;
                      {expandFilters ? translated.hideFilters : translated.showFilters}
                    </button>
                  )}
                </div>
              </fieldset>
              <div className="form-actions">
                <button className="link form-actions__left" onClick={clearFilters}>{translated.reset}</button>
                <button className="button button--light form-actions__right control-bar__action-btn" onClick={applyAllFilters}>{translated.filter}</button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div className="flexgrid grid grid--2 my-1 control-bar__bottom">
        <div>
          {list.count >= 0 && (
            <div className="text--strong">
              {getResultCountText(list.count)}
            </div>
          )}
          <ControlBarFilterPills
            filters={appliedFilters}
            onRemove={(type) => {
              handleFilterChange(type, '')
              applyQuery(type, '')
            }}
          />
        </div>
        {isMapAndList &&
          <div className="span6 align--right">
            <ControlBarListMapSwitch query={queryParams} />
          </div>}
      </div>
    </nav>
  )
}
