import React from 'react'
import django from 'django'

const likesTag = django.gettext('Likes')

const QuestionPresent = ({ id, likes, questionText }) => {
  return (
    <li className="live-question__question-container" key={id}>
      <h3 className="title title--no-underline">{questionText}</h3>
      <span
        className="rating-button"
        title={likesTag}
        aria-label={likesTag}
      >
        <i className="far fa-thumbs-up mr-1" aria-hidden="true" />
        {likesTag} ({likes.count})
      </span>
    </li>
  )
}

export default QuestionPresent
