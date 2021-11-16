import React, { useEffect, useState } from 'react'
import { BudgetingProposalListItem } from './BudgetingProposalListItem'
import { VotingCodeForm } from './VotingCodeForm'

export const BudgetingProposalList = (props) => {
  const [proposals, setProposals] = useState([])
  useEffect(() => {
    fetch(props.proposals_api_url)
      .then(resp => resp.json())
      .then(json => setProposals(json))
  }, [])
  return (
    <ul className="u-list-reset">
      <VotingCodeForm />
      {proposals.map((proposal, idx) =>
        <BudgetingProposalListItem
          key={`budgeting-proposal-${idx}`}
          proposal={proposal}
        />)}
    </ul>
  )
}
