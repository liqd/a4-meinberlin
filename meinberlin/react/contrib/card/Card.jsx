import React, { useState } from 'react'
import django from 'django'

import { CardStats } from './CardStats'

const translated = {
  detailsStr: django.gettext('Show'),
  toStr: django.gettext('to:')
}

export const Card = (props) => {
  const { item, idx, permissions, children } = props

  // needed as BO JS library does not work with async libraries
  const [hover, setHover] = useState()

  const handleClick = () => {
    document.getElementById('card-link-' + idx).click()
  }

  const handleMouseEnter = () => {
    setHover(!hover)
  }

  const handleMouseLeave = () => {
    setHover(!hover)
  }

  return (
    <article className={'modul-card ' + (item.is_archived ? 'card--archived' : '')}>
      <header className="card__header">
        {/* eslint-disable-next-line */}
        <h2
          className="title title-3" onClick={handleClick} onMouseEnter={handleMouseEnter}
          onMouseLeave={handleMouseLeave}
        >{item.name}
        </h2>
        {children ? <>{children}</> : null}
      </header>
      <section className="card__footer--light">
        <CardStats
          item={item}
          permissions={permissions}
          positiveCount={item.positive_rating_count}
          negativeCount={item.negative_rating_count}
          commentCount={item.comment_count}
          voteCount={item.vote_count}
        />
        <a href={item.url} id={'card-link-' + idx} className={'card__link more' + (hover ? ' card__link--hover' : '')} data-mainlink="true">{translated.detailsStr}
          <span className="aural">{translated.toStr} {item.name}</span>
        </a>
      </section>
      {/* <div className="list-item__vote">
        {permissions.has_voting_permission_and_valid_token && item.vote_allowed && (
          <VoteButton
            objectID={item.pk}
            tokenvoteApiUrl={tokenvoteApiUrl}
            isChecked={item.session_token_voted}
            onVoteChange={props.onVoteChange}
            currentPage={props.currentPage}
            disabled={!props.votesLeft && !item.session_token_voted}
          />
        )}
      </div> */}
    </article>
  )
}
