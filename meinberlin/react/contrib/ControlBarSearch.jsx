import React, { useEffect, useState } from 'react'
import django from 'django'
import { Input } from './forms/Input'

export const ControlBarSearch = (props) => {
  const translated = {
    search: django.gettext('Search'),
    startSearch: django.gettext('Start search'),
    searchFor: django.gettext('Search for Proposals')
  }

  const [value, setValue] = useState(props.term)

  const handleSubmit = (e) => {
    e.preventDefault()
    props.onSearch(value)
  }

  const handleChange = (e) => {
    setValue(e.target.value)
  }

  useEffect(() => {
    setValue(props.term)
  }, [props.term])

  return (
    <form
      onSubmit={handleSubmit}
      className="input-group"
    >
      <Input
        label={translated.search} id="id-filter-search"
        onChange={handleChange}
        before={<i className="fa fa-search" aria-hidden="true" />}
      >
        <button type="submit" title={translated.startSearch}>
          <i className="fa fa-arrow-right" aria-hidden="true" />
          <span className="visually-hidden">
            {translated.startSearch}
          </span>
        </button>
      </Input>
    </form>
  )
}
