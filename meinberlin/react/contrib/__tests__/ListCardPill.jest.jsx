import React from 'react'
import { render, screen } from '@testing-library/react'
import { ListCardPill } from '../ListCardPill'

// testing data:
const someBadges = [
  ['category', 'category1'],
  ['label', 'label1'],
  ['label', 'label2']
]

const pointLabelBadge = [
  ['point_label', 'labelwithicon']
]

test('displaying 3 labels', () => {
  render(
    <ListCardPill
      badges={someBadges}
    />
  )
  expect(screen.getByText('category1')).toBeTruthy()
  expect(screen.getByText('label1')).toBeTruthy()
  expect(screen.getByText('label2')).toBeTruthy()
})

test('displaying point label badge', () => {
  render(
    <ListCardPill
      badges={pointLabelBadge}
    />
  )
  expect(screen.getByText('labelwithicon')).toBeTruthy()
})

test('displaying first 3 badges and add more link', () => {
  render(
    <ListCardPill
      badges={someBadges}
      numOfMoreBadges={1}
    />
  )
  expect(screen.getByText('1 More')).toBeTruthy()
})
