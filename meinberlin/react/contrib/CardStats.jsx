import React from 'react'
import django from 'django'

export const CardStats = (props) => {
  const { permissions } = props

  const positiveRatingsStr = django.gettext('Likes')
  const negativeRatingsStr = django.gettext('Dislikes')
  const supportStr = django.gettext('Support')
  const commentsStr = django.gettext('Comments')
  const votesStr = django.gettext('Votes')

  return (
    <div className="card__stats">
      {/* ratings visible to admins in 1 and 2 phase budgeting due to `has_perm`  */}
      {permissions.view_rate_count && (
        <>
          <p className="card__stat">{props.positiveCount} {positiveRatingsStr}</p>
          <p className="card__stat">{props.negativeCount} {negativeRatingsStr}</p>
        </>
      )}

      {permissions.view_support_count && (
        <p className="card__stat">{props.positiveCount} {supportStr}</p>
      )}
      {permissions.view_vote_count && (
        <p className="card__stat">{props.voteCount} {votesStr}</p>
      )}
      {permissions.view_comment_count && (
        <p className="card__stat">{props.commentCount} {commentsStr}</p>
      )}
    </div>
  )
}
