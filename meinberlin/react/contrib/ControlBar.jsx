import React, { useEffect, useState } from 'react'
import { ControlBarDropdown } from './ControlBarDropdown'
import { ControlBarListMapSwitch } from './ControlBarListMapSwitch'
import { ControlBarSearch } from './ControlBarSearch'
import django from 'django'
import { useSearchParams } from 'react-router-dom'
import { ControlBarFilterPills } from './ControlBarFilterPills'
import { useFetchedItems } from './contexts/FetchItemsProvider'

const translated = {
  reset: django.gettext('Reset'),
  showFilters: django.gettext('Show more'),
  hideFilters: django.gettext('Show less'),
  filters: django.gettext('Filters'),
  filter: django.gettext('filter'),
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
  const { results: { list }, isMapAndList } = useFetchedItems()
  const [expandFilters, setExpandFilters] = useState(true)
  const [queryParams, setQueryParams] = useSearchParams()
  const [filters, setFilters] = useState([])
  const term = queryParams.get('search') || ''
  const appliedFilters = filters
    .concat([{ type: 'search', label: term, value: term }])
    .filter((f) =>
      f.type !== 'ordering' &&
    queryParams?.has(f.type)
    )

  useEffect(() => {
    // initialize filters object
    if (list.filters) {
      const updatedFilters = Object.keys(list.filters)
        .map((type) => ({ ...list.filters[type], type, value: queryParams.get(type) }))

      setFilters(updatedFilters)
    }
  }, [list.filters])

  const applyQuery = (type, value) => {
    if (value && value !== '') {
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

    if (type === 'ordering' || choice === '') {
      applyQuery(type, choice)
    }
  }

  const applyAllFilters = () => {
    filters.forEach(f => {
      if (f.value && f.value !== '') {
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
                      {list.filters?.ordering && (
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
                    {filters.length > 0 && (
                      filters
                        .filter((f) => f.type !== 'ordering')
                        .slice(0, expandFilters ? filters.length : 3).map((filter) => (
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
                  {filters.length > 3 && (
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
                <button className="button button--light form-actions__right" onClick={applyAllFilters}>{translated.filter}</button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div className="row my-1">
        <div className="span6">
          <div>
            {/* only show result string if list filtered or searched not just ordered */}
            {appliedFilters.length > 0 && (
              <div className="text--strong">
                {list.total_count >= 0 && getResultCountText(list.total_count)}
              </div>
            )}
            <ControlBarFilterPills
              filters={appliedFilters}
              onRemove={(type) => handleFilterChange(type, '')}
            />
          </div>
        </div>
        {isMapAndList &&
          <div className="span6 align--right">
            <ControlBarListMapSwitch query={queryParams} />
          </div>}
      </div>
    </nav>
  )
}
