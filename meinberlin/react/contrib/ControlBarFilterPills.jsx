import React from 'react'
import django from 'django'
import { Pill } from './Pill'

const translated = { filterRemove: django.gettext('Remove filter %s') }

const getFilterRemoveText = (label) => {
  return django.interpolate(translated.filterRemove, [label])
}

export const ControlBarFilterPills = ({ filters: _filters, onRemove }) => {
  const filters = _filters.filter(f => f.value && f.value !== '')
  if (!filters.length) {
    return null
  }

  return (
    <ul className="pill__list">
      {
        filters.map((filter) => {
          const label = filter.label || filter.choices.find(c => c[0] === filter.value)[1]
          return (
            <Pill
              key={'pill_' + filter.type}
              pillClass="pill"
            >
              {label}
              <button
                onClick={() => onRemove(filter.type)}
                className="pill__close"
                title={getFilterRemoveText(label)}
              >
                <span className="fa fa-times" aria-label={getFilterRemoveText(label)} />
              </button>
            </Pill>
          )
        })
      }
    </ul>
  )
}
