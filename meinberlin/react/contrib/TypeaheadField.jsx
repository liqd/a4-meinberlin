/* eslint-disable no-restricted-syntax */
import React, { useState, useRef, useEffect } from 'react'
import { Typeahead } from 'react-bootstrap-typeahead'
import django from 'django'

const suggestionsText = django.gettext('Suggestions will appear as you type.')
const resultsText = django.ngettext('%s suggestion available', '%s suggestions available', 0)

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

  const [suggestionCount, setSuggestionCount] = useState(0)
  const [inputValue, setInputValue] = useState('')
  const typeaheadRef = useRef(null)

  const handleInputChange = (text, e) => {
    setInputValue(text)

    if (text) {
      const filtered = typeaheadOptions.filter(option =>
        typeof option === 'string'
          ? option.toLowerCase().includes(text.toLowerCase())
          : option.name.toLowerCase().includes(text.toLowerCase())
      )
      setSuggestionCount(filtered.length)
    } else {
      setSuggestionCount(0)
    }
  }

  useEffect(() => {
    const liveRegion = document.getElementById(`${uniqueId}-description`)
    if (liveRegion) {
      if (inputValue && suggestionCount > 0) {
        liveRegion.textContent = django.interpolate(resultsText, [suggestionCount])
      } else {
        liveRegion.textContent = ''
      }
    }
  }, [suggestionCount, inputValue, uniqueId])

  return (
    <div className="form-group typeahead">
      <label htmlFor={uniqueId} className="label">
        {typeaheadHeading}
        <span className="sr-only"> {suggestionsText}</span>
      </label>
      <span className="typeahead__input-group">
        <Typeahead
          id={uniqueId}
          ref={typeaheadRef}
          className="typeahead__input-group-append"
          onChange={onTypeaheadChange}
          onInputChange={handleInputChange}
          labelKey="name"
          multiple={multipleBoolean}
          options={typeaheadOptions}
          selected={typeaheadSelected}
          placeholder={typeaheadPlaceholder}
          aria-describedby={`${uniqueId}-description`}
        />
      </span>
      <span
        id={`${uniqueId}-description`}
        className="sr-only"
        role="status"
        aria-live="polite"
        aria-atomic="true"
      >
        {inputValue && suggestionCount > 0
          ? django.interpolate(resultsText, [suggestionCount])
          : ''}
      </span>
    </div>
  )
}
