import React from 'react'
import django from 'django'
import { toLocaleDate } from '../../contrib/assets/helpers'
import VoteButton from './VoteButton'
import { ListItemBadges } from './ListItemBadges'
import { ListItemStats } from './ListItemStats'

const updatedOnStr = django.gettext('updated on')
const createdOnStr = django.gettext('created on')

export const BudgetingProposalListItem = (props) => {
  const { idx, proposal, permissions, queryParams, tokenvoteApiUrl } = props
  const safeLocale = props.locale ? props.locale : undefined
  const date = proposal.modified
    ? updatedOnStr + ' ' + toLocaleDate(
      proposal.modified,
      safeLocale
    )
    : createdOnStr + ' ' + toLocaleDate(
      proposal.created,
      safeLocale
    )

  return (
    <li id={'proposal_' + proposal.pk} className="list-item">
      <ListItemStats
        permissions={permissions}
        positiveCount={proposal.positive_rating_count}
        negativeCount={proposal.negative_rating_count}
        commentCount={proposal.comment_count}
      />
      <h2 className="list-item__title">
        <a href={proposal.url.slice(0, -1) + '?id=' + idx + '&' + queryParams}>{proposal.name}</a>
      </h2>
      <ListItemBadges
        badges={proposal.item_badges_for_list}
        numOfMoreBadges={proposal.additional_item_badges_for_list_count}
        proposalUrl={proposal.url}
      />
      <div className="list-item__vote">
        <div>
          <span className="list-item__author test">{proposal.creator}</span>
          {date + ' - ' + proposal.reference_number}
        </div>
        {proposal.vote_allowed && (
          <VoteButton
            objectID={proposal.pk}
            tokenvoteApiUrl={tokenvoteApiUrl}
            isChecked={proposal.session_token_voted}
            onVoteChange={props.onVoteChange}
            currentPage={props.currentPage}
            disabled={!props.votesLeft && !proposal.session_token_voted}
          />
        )}
      </div>
    </li>
  )
}
