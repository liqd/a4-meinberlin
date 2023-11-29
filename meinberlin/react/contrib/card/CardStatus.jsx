import React from 'react'
import django from 'django'

import { ModeratorStatus } from '../ModeratorStatus'
import { Pill } from '../Pill'

const translated = {
  more: django.gettext('More')
}

export const CardStatus = props => {
  const getClass = (pill) => {
    const pillClass = 'pill'
    const colourClass = 'pill--' + pill[0].toLowerCase()
    return pillClass + ' ' + colourClass
  }

  // only return icon for pointLabels
  const hasPointLabelIcon = (type) => {
    if (type !== 'point_label') {
      return
    }
    return <span className="fas fa-map-marker-alt" aria-hidden="true" />
  }

  return (
    <div className="card__status status">
      <ul className="pill__list" aria-label={props.pillHeader}>
        {props.pills.map((pill, idx) => {
          // Hide the label if it's 'moderator_status'
          if (pill[0] === 'moderator_status') {
            return null
          }
          return (
            <Pill
              key={'pill_' + idx}
              pillClass={getClass(pill)}
            >
              {hasPointLabelIcon(pill[0])}
              {pill[1]}
            </Pill>
          )
        })}
        {props.numOfMorePills > 0 &&
          <li className="pill pill--info">
            {props.numOfMorePills + ' ' + translated.more}
          </li>}
      </ul>
      <ModeratorStatus
        modStatus={props.proposal.moderator_status}
        modStatusDisplay={props.proposal.get_moderator_status_display}
      />
    </div>
  )
}
