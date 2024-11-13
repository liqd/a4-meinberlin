import React from 'react'
import django from 'django'
import { Pill } from '../contrib/Pill'
import { classNames } from '../contrib/helpers'

const likedTag = django.gettext('Liked')
const likesTag = django.gettext('Likes')
const addLikeTag = django.gettext('add like')
const undoLikeTag = django.gettext('undo like')

export default function LikeCard ({
  title,
  category,
  likes,
  onLikeClick
}) {
  const likeText = likes.session_like ? likedTag : likesTag

  return (
    <article className="modul-card card">
      <header className="card__header">
        <h3 className="title">{title}</h3>
        {category && (
          <div className="card__status status">
            <Pill pillClass="card__pill pill pill--label">{category}</Pill>
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
    </article>
  )
}
