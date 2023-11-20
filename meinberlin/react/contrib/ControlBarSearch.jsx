import React, { useEffect, useState } from 'react'
import django from 'django'

const translated = {
  search: django.gettext('Search'),
  startSearch: django.gettext('Start search'),
  searchFor: django.gettext('Search for Proposals')
}

export const ControlBarSearch = ({ onSearch, term }) => {
  const [value, setValue] = useState(term)
  const handleSubmit = (e) => {
    e.preventDefault()
    onSearch(value)
  }

  const handleChange = (e) => {
    setValue(e.target.value)
  }

  useEffect(() => {
    setValue(term)
  }, [term])

  return (
    <form onSubmit={handleSubmit} className="searchform-slot my-0">
      <div className="form-group">
        <label htmlFor="searchterm" className="form-label">
          {translated.search}
        </label>
        <div className="searchterm">
          <div className="input-wrapper">
            <i className="bicon bicon-search lens" aria-hidden="true" />
            <input
              type="search"
              className="form-control search"
              placeholder={translated.searchFor}
              value={value}
              id="searchterm"
              onChange={handleChange}
            />
          </div>
          <button className="button button--clean submit" type="submit" title={translated.startSearch}>
            <span className="aural">{translated.startSearch}</span>
            <i className="bicon bicon-arrow-right icon" aria-hidden="true" />
          </button>
        </div>
      </div>
    </form>
  )
}
