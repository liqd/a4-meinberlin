import React from 'react'
import { render, screen } from '@testing-library/react'
import { CardStatus } from '../CardStatus'

// testing data:
const somePills = [
  ['category', 'category1'],
  ['label', 'label1'],
  ['label', 'label2']
]

const pointLabelPill = [
  ['point_label', 'labelwithicon']
]

const proposal = {
  moderator_status: 'ACCEPTED',
  get_moderator_status_display: 'Accepted'
}

test('displaying 3 labels', () => {
  render(
    <CardStatus
      pills={somePills}
      proposal={proposal}
    />
  )
  expect(screen.getByText('category1')).toBeTruthy()
  expect(screen.getByText('label1')).toBeTruthy()
  expect(screen.getByText('label2')).toBeTruthy()
  expect(screen.getByText('Accepted')).toBeTruthy()
})

test('displaying point label pill', () => {
  render(
    <CardStatus
      pills={pointLabelPill}
      proposal={proposal}
    />
  )
  expect(screen.getByText('labelwithicon')).toBeTruthy()
})

test('displaying first 3 pills and add more link', () => {
  render(
    <CardStatus
      pills={somePills}
      numOfMorePills={1}
      proposal={proposal}
    />
  )
  expect(screen.getByText('+1')).toBeTruthy()
  expect(screen.getByText('Accepted')).toBeTruthy()
})
