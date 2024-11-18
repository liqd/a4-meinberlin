import React from 'react'
import django from 'django'
import { Pill } from '../contrib/Pill'
import { classNames } from '../contrib/helpers'

const likedTag = django.gettext('Liked')
const likesTag = django.gettext('Likes')
const addLikeTag = django.gettext('add like')
const undoLikeTag = django.gettext('undo like')
const bookmarkedTag = django.gettext('bookmarked')

export default function LikeCard ({
  title,
  category,
  isOnShortlist,
  likes,
  onLikeClick,
  children
}) {
  const likeText = likes.session_like ? likedTag : likesTag

  return (
    <article className="modul-card card">
      <header className="card__header">
        <h3 className="title title--no-underline">{title}</h3>
        {(category || isOnShortlist) && (
          <div className="card__status status">
            {category && (
              <Pill pillClass="card__pill pill pill--label">{category}</Pill>
            )}
            {isOnShortlist && (
              <Pill pillClass="card__pill pill pill--shortlist">
                {bookmarkedTag}
              </Pill>
            )}
          </div>
        )}
      </header>
      {onLikeClick
        ? (
          <button
            type="button"
            className={classNames(
              'rating-button',
              likes.session_like && 'rating-button--active'
            )}
            onClick={onLikeClick}
            aria-label={likes.session_like ? addLikeTag : undoLikeTag}
          >
            <i className="far fa-thumbs-up" aria-hidden="true" />
            {likeText} ({likes.count})
          </button>
          )
        : (
          <span className="rating-button">
            <i className="far fa-thumbs-up" aria-hidden="true" />
            {likeText} ({likes.count})
          </span>
          )}
      <div className="card__header">
        {children}
      </div>
    </article>
  )
}
