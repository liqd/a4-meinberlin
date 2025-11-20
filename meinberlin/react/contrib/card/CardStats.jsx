import React from 'react'
import django from 'django'

export const CardStats = (props) => {
  const { permissions } = props

  const positiveRatingsStr = django.ngettext('Like', 'Likes', props.positiveCount)
  const negativeRatingsStr = django.ngettext('Dislike', 'Dislikes', props.negativeCount)
  const supportStr = django.ngettext('Supporter', 'Supporters', props.positiveCount)
  const commentsStr = django.npgettext('card', 'Comment', 'Comments', props.commentCount)
  const votesStr = django.ngettext('Vote', 'Votes', props.voteCount)

  return (
    <dl className="card__stats stats-dl">
      {/* ratings visible to admins in 1 and 2 phase budgeting due to `has_perm`  */}
      {permissions.view_rate_count && (
        <>
          <div className="stat-items card__stat ">
            <dt>{positiveRatingsStr}</dt>
            <dd>{props.positiveCount}</dd>
          </div>
          <div className="card__stat stat-items">
            <dt>{negativeRatingsStr}</dt>
            <dd>{props.negativeCount}</dd>
          </div>
        </>
      )}

      {permissions.view_support_count && (
        <div className="stat-items card__stat ">
          <dt>{supportStr}</dt>
          <dd>{props.positiveCount}</dd>
        </div>
      )}
      {permissions.view_vote_count && (
        <div className="stat-items card__stat ">
          <dt>{votesStr}</dt>
          <dd>{props.voteCount}</dd>
        </div>
      )}
      {permissions.view_comment_count && (
        <div className="stat-items card__stat ">
          <dt>{commentsStr}</dt>
          <dd>{props.commentCount}</dd>
        </div>
      )}
    </dl>
  )
}
