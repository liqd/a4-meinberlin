import React from 'react'
import django from 'django'

import { CardStats } from './CardStats'

const translated = {
  detailsStr: django.gettext('Item details'),
  toStr: django.gettext('to:')
}

export const Card = (props) => {
  const { item, permissions, children } = props

  return (
    <article className="modul-card" data-add-clickable-area="smart">
      <header className="card__header">
        <h3 className="title">{item.name}</h3>
        {children}
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
        <a href={item.url} className="more" data-mainlink="true">{translated.detailsStr}
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
