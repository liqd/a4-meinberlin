import React, { useState } from 'react'
import django from 'django'
import { MultiSelect } from '../contrib/forms/MultiSelect'
import { classNames } from 'adhocracy4'

const allTag = django.gettext('All')
const categoriesLabelText = django.gettext('Affiliation')
const markedLabelText = django.gettext('Marked Questions')
const markedOptionsText = [
  { name: django.gettext('Bookmarked'), value: 'bookmarked' },
  { name: django.gettext('Not Bookmarked'), value: 'not_bookmarked' },
  { name: django.gettext('Answered'), value: 'answered' },
  { name: django.gettext('Open'), value: 'not_answered' },
  { name: django.gettext('On Screen'), value: 'screen' },
  { name: django.gettext('Not on Screen'), value: 'not_screen' }
]
const displayLabelText = django.gettext('Display')
const displayOptionsText = [
  { name: django.gettext('Visible'), value: 'visible' },
  { name: django.gettext('Hidden'), value: 'hidden' }
]
const questionsText = django.gettext('Questions')
const filterText = django.gettext('Filter')

const Filter = ({
  filters: initialFilters,
  categories,
  isModerator,
  onFiltered
}) => {
  const [filters, setFilters] = useState({
    categories: [],
    marked: [],
    display: [],
    ...initialFilters
  })

  const onFilterChange = (type, choice) => {
    setFilters({ ...filters, [type]: choice })
  }

  if (!isModerator && categories.length === 0) {
    return null
  }

  const filterColumns = isModerator
    ? categories.length > 0
      ? 'grid--3'
      : 'grid--2'
    : 'grid--1'

  return (
    <>
      <h2 id="filter-form-heading">{questionsText}</h2>
      <form
        className="form panel--heavy"
        onSubmit={(e) => {
          e.preventDefault()
          onFiltered(filters)
        }}
        aria-labelledby="filter-form-heading"
      >
        <div className={classNames('flexgrid', filterColumns)}>
          {categories.length > 0 && (
            <MultiSelect
              label={categoriesLabelText}
              placeholder={allTag}
              choices={categories.map((choice) => ({
                value: choice,
                name: choice
              }))}
              values={filters.categories}
              onChange={(choices) => onFilterChange('categories', choices)}
            />
          )}
          {isModerator && (
            <>
              <MultiSelect
                label={markedLabelText}
                placeholder={allTag}
                choices={markedOptionsText}
                values={filters.marked}
                onChange={(choices) => onFilterChange('marked', choices)}
              />
              <MultiSelect
                label={displayLabelText}
                placeholder={allTag}
                choices={displayOptionsText}
                values={filters.display}
                onChange={(choices) => onFilterChange('display', choices)}
              />
            </>
          )}
        </div>
        <div className="form-actions">
          <div className="form-actions__right">
            <button type="submit" className="button">{filterText}</button>
          </div>
        </div>
      </form>
    </>
  )
}

export default Filter
