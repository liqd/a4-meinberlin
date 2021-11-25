import React from 'react'
import { render, screen } from '@testing-library/react'
import { BudgetingProposalListItem } from '../BudgetingProposalListItem'

test('render list item with vote button', () => {
  const proposal = {
    name: 'myProposal',
    url: 'www',
    creator: 'creator',
    created: '2021-11-11T15:37:19.490201+01:00'
  }
  render(<BudgetingProposalListItem proposal={proposal} isVotingPhase />)
  expect(screen.getByText('myProposal')).toBeTruthy()
  expect(screen.getByText('creator')).toBeTruthy()
  expect(screen.getByText('11. mock text 2021')).toBeTruthy()
})

test('render list item with stats', () => {
  const proposal = {
    name: 'myProposal',
    url: 'www',
    creator: 'creator',
    created: '2021-11-11T15:37:19.490201+01:00'
  }
  render(<BudgetingProposalListItem proposal={proposal} isVotingPhase={false} />)
  expect(screen.getByText('myProposal')).toBeTruthy()
  expect(screen.getByText('creator')).toBeTruthy()
  expect(screen.getByText('11. mock text 2021')).toBeTruthy()
})
