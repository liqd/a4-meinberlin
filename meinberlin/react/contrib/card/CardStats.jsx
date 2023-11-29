import React from 'react'
import django from 'django'

export const CardStats = (props) => {
  const { permissions } = props

  const positiveRatingsStr = django.gettext('Likes')
  const negativeRatingsStr = django.gettext('Dislikes')
  const supportStr = django.gettext('Support')
  const commentsStr = django.ngettext('Comment', 'Comments', props.commentCount)
  const votesStr = django.ngettext('Vote', 'Votes', props.voteCount)

  return (
    <div className="card__stats">
      {/* ratings visible to admins in 1 and 2 phase budgeting due to `has_perm`  */}
      {permissions.view_rate_count && (
        <>
          <p className="card__stat"><b>{props.positiveCount}</b>{positiveRatingsStr}</p>
          <p className="card__stat"><b>{props.negativeCount}</b>{negativeRatingsStr}</p>
        </>
      )}

      {permissions.view_support_count && (
        <p className="card__stat"><b>{props.positiveCount}</b>{supportStr}</p>
      )}
      {permissions.view_vote_count && (
        <p className="card__stat"><b>{props.voteCount}</b>{votesStr}</p>
      )}
      {permissions.view_comment_count && (
        <p className="card__stat"><b>{props.commentCount}</b>{commentsStr}</p>
      )}
    </div>
  )
}
