import React, { useState } from 'react'
import django from 'django'

const getItemByFilter = (items, filter) => {
  return items.find(item => item.filter === filter)
}

export const FilterBar = (props) => {
  const filterItems = [
    { name: 'Pending', filter: '?is_pending=true' },
    { name: 'Archived', filter: '?is_pending=false' },
    { name: 'All', filter: '' }
  ]
  const [currFilterItem, setCurrFilterItem] =
    useState(getItemByFilter(filterItems, props.selectedFilter))

  const onSelectFilter = (filterItem) => {
    setCurrFilterItem(filterItem)
    props.onFilterChange(filterItem)
  }

  return (
    <div
      className="filter-bar justify-content-end"
      aria-label={django.gettext('Filter')}
    >
      <div className="mt-2 mt-sm-0">
        <div className="dropdown dropdown-menu-end">
          <button
            type="button"
            className="dropdown-toggle btn btn--light btn--select"
            data-bs-toggle="dropdown"
            aria-expanded="false"
          >
            {django.gettext('Filter')}: {currFilterItem.name}
            <i className="fa fa-caret-down" aria-hidden="true" />
          </button>
          <ul className="dropdown-menu">
            {filterItems.map((filterItem, i) => (
              <li key={`${i}_${filterItem.name}`}>
                <button onClick={() => onSelectFilter(filterItem)}>
                  {django.gettext(filterItem.name)}
                </button>
              </li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  )
}
