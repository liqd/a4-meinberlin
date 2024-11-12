import React from 'react'
import { Typeahead } from 'react-bootstrap-typeahead'

export const TypeaheadField = (props) => {
  const {
    typeaheadHeading,
    uniqueId,
    onTypeaheadChange,
    typeaheadOptions,
    typeaheadSelected,
    typeaheadPlaceholder,
    multipleBoolean
  } = props

  return (
    <div className="form-group typeahead">
      <label htmlFor={uniqueId} className="label">{typeaheadHeading}</label>
      <span className="typeahead__input-group">
        <Typeahead
          id={uniqueId}
          className="typeahead__input-group-append"
          onChange={onTypeaheadChange}
          labelKey="name"
          multiple={multipleBoolean}
          options={typeaheadOptions}
          selected={typeaheadSelected}
          placeholder={typeaheadPlaceholder}
        />
      </span>
    </div>
  )
}
