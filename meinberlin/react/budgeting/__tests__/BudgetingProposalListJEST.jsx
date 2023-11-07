/* eslint-disable */
// import React from 'react'
// import { render, act, screen } from '@testing-library/react'
// import { BudgetingProposalList } from '../BudgetingProposalList'
// import { BrowserRouter } from 'react-router-dom'

// // permissions for anonymous/logged-in user during collection phase of 1 and 2 phase (3 phase is dfferent see ListItem test)
// const permissions = {
//   view_support_count: false,
//   view_rate_count: true,
//   view_comment_count: true,
//   view_vote_count: false,
//   has_voting_permission_and_valid_token: false
// }

// // permissions for anonymous/logged-in user with token during vote phase
// const permissionsVote = {
//   view_support_count: false,
//   view_rate_count: false,
//   view_comment_count: true,
//   view_vote_count: false,
//   has_voting_permission_and_valid_token: true
// }

// test('Budgeting Proposal List (1, 2, 3) - no ideas - check: empty list string', async () => {
//   // mimicking fetch response with empty list
//   const mockedFetchEmpty = Promise.resolve({
//     json: () => Promise.resolve({ results: [], permissions })
//   })

//   // overwrite global.fetch with mock function
//   global.fetch = jest.fn().mockImplementation(() => mockedFetchEmpty)

//   render(<BrowserRouter><BudgetingProposalList /></BrowserRouter>)
//   expect(global.fetch).toHaveBeenCalledTimes(1)

//   // waiting for async fetching ends --> without this, the
//   // act(...) console.error will appear
//   await act(() => mockedFetchEmpty)
//   expect(screen.getByText('Nothing to show')).toBeTruthy()

//   // reverse overwrite of global.fetch
//   await global.fetch.mockClear()
// })

// test('Budgeting Proposal List (3) - voting, finished phase no token - all user - check: no vote count or link',
  // async () => {
  //   // sample data (one proposal item)
  //   const mockedResults = [
  //     {
  //       comment_count: 6,
  //       created: '2021-11-11T15:36:57.941072+01:00',
  //       creator: 'admin',
  //       is_archived: false,
  //       name: 'erster vorschlag',
  //       negative_rating_count: 1,
  //       pk: 7,
  //       positive_rating_count: 3,
  //       url: '/budgeting/2021-00007/',
  //       additional_item_badges_for_list_count: 1,
  //       item_badges_for_list: [
  //         ['moderator_status', 'wird ueberprueft', 'CONSIDERATION'],
  //         ['budget', '20€'], ['category', 'candalf']]
  //     }
  //   ]

  //   // mimicking fetch response
  //   const mockedFetch = Promise.resolve({
  //     json: () => Promise.resolve({ results: mockedResults, permissions })
  //   })

  //   // overwrite global.fetch with mock function
  //   global.fetch = jest.fn().mockImplementation(() => mockedFetch)

  //   render(<BrowserRouter><BudgetingProposalList /></BrowserRouter>)
  //   expect(global.fetch).toHaveBeenCalledTimes(1)

  //   // waiting for async fetching ends --> without this, the
  //   // act(...) console.error will appear
  //   await act(() => mockedFetch)
  //   expect(screen.getByText('erster vorschlag')).toBeTruthy()
  //   expect(screen.queryByText('you have 1 vote left.you have %s votes left.')).toBeNull()
  //   expect(screen.queryByDisplayValue('End session')).toBeNull()

  //   // reverse overwrite of global.fetch
  //   await global.fetch.mockClear()
  // })

// test('Budgeting Proposal List (3) - voting phase - user with token 2 votes - check: vote count + end session link',
//   async () => {
//     // sample data (one proposal item)
//     const mockedResults = [
//       {
//         comment_count: 6,
//         created: '2021-11-11T15:36:57.941072+01:00',
//         creator: 'admin',
//         is_archived: false,
//         name: 'erster vorschlag',
//         negative_rating_count: 1,
//         pk: 7,
//         positive_rating_count: 3,
//         url: '/budgeting/2021-00007/',
//         additional_item_badges_for_list_count: 1,
//         item_badges_for_list: [
//           ['moderator_status', 'wird ueberprueft', 'CONSIDERATION'],
//           ['budget', '20€'], ['category', 'candalf']]
//       }
//     ]

//     // mimicking fetch response with met info for token
//     const mockedFetch = Promise.resolve({
//       json: () => Promise.resolve({
//         results: mockedResults,
//         permissions: permissionsVote,
//         token_info: { num_votes_left: 2, votes_left: true }
//       })
//     })

//     // overwrite global.fetch with mock function
//     global.fetch = jest.fn().mockImplementation(() => mockedFetch)

//     render(<BrowserRouter><BudgetingProposalList /></BrowserRouter>)
//     expect(global.fetch).toHaveBeenCalledTimes(1)

//     // waiting for async fetching ends --> without this, the
//     // act(...) console.error will appear
//     await act(() => mockedFetch)
//     expect(screen.getByText('erster vorschlag')).toBeTruthy()
//     // FIXME figure out how to deal with plurals
//     expect(screen.getByText('you have 1 vote left.you have %s votes left.2')).toBeTruthy()
//     expect(screen.getByRole('button', { name: 'End session' })).toBeTruthy()

//     // reverse overwrite of global.fetch
//     await global.fetch.mockClear()
//   })

// test('Budgeting Proposal List (1, 2, 3) - all users - check: fetch list item error', async () => {
//   // overwrite global.fetch with mock function
//   global.fetch = jest.fn().mockRejectedValue('testing: expected network error')

//   render(<BrowserRouter><BudgetingProposalList /></BrowserRouter>)
//   expect(global.fetch).toHaveBeenCalledTimes(1)
//   const emptyList = screen.queryAllByText('mock text')
//   expect(emptyList).toBeTruthy()

//   // reverse overwrite of global.fetch
//   await global.fetch.mockClear()
// })


// Budgeting list card tests
// import React from 'react'
// import { render, screen } from '@testing-library/react'
// import { Card } from '../Card'

// test('Budgeting Proposal Card (1,2) - collection phase - initiator, mod, logged-in, anonymous users (admin sees all stats in all phases)', () => {
//   const permissions = {
//     view_support_count: false,
//     view_rate_count: true,
//     view_comment_count: true,
//     vote_allowed: false,
//     has_voting_permission_and_valid_token: false
//   }

//   const proposal = {
//     name: 'myProposal',
//     url: 'www',
//     creator: 'creator',
//     created: '2021-11-11T15:37:19.490201+01:00',
//     additional_item_badges_for_list_count: 0,
//     item_badges_for_list: [
//       ['moderator_status', 'wird ueberprueft', 'CONSIDERATION'],
//       ['budget', '20€'], ['category', 'candalf']],
//     reference_number: '2021-12345',
//     positive_rating_count: 2,
//     negative_rating_count: 1,
//     support_count: 8,
//     vote_count: 1,
//     comment_count: 7,
//     pk: 7,
//     vote_allowed: false
//   }
//   render(<Card proposal={proposal} permissions={permissions} />)
//   expect(screen.getByText('myProposal')).toBeTruthy()
//   expect(screen.getByText('creator')).toBeTruthy()
//   // support string renders multiple strings due to plurals so using title
//   expect(screen.queryByTitle('Support')).toBeNull()
//   expect(screen.queryByText('Total votes')).toBeNull()
//   expect(screen.getByText('Comments')).toBeTruthy()
//   expect(screen.getByText('Positive Ratings')).toBeTruthy()
//   expect(screen.getByText('Negative Ratings')).toBeTruthy()
//   const resolvedDate =
//     screen.queryByText('created on 11. November 2021 - 2021-12345') ||
//     screen.queryByText('updated on 11 November 2021 - 2021-12345')
//   expect(resolvedDate).toBeTruthy()
// })

// test('Budgeting Proposal Card (3) - collection phase - initiator, mod, logged-in, anonymous users', () => {
//   const permissions = {
//     view_support_count: false,
//     view_rate_count: false,
//     view_comment_count: true,
//     vote_allowed: false,
//     has_voting_permission_and_valid_token: false
//   }

//   const proposal = {
//     name: 'myProposal',
//     url: 'www',
//     creator: 'creator',
//     created: '2021-11-11T15:37:19.490201+01:00',
//     additional_item_badges_for_list_count: 0,
//     item_badges_for_list: [
//       ['moderator_status', 'wird ueberprueft', 'CONSIDERATION'],
//       ['budget', '20€'], ['category', 'candalf']],
//     reference_number: '2021-12345',
//     positive_rating_count: 2,
//     negative_rating_count: 1,
//     support_count: 8,
//     vote_count: 1,
//     comment_count: 7,
//     pk: 7,
//     vote_allowed: false
//   }
//   render(<Card proposal={proposal} permissions={permissions} />)
//   expect(screen.getByText('myProposal')).toBeTruthy()
//   expect(screen.getByText('creator')).toBeTruthy()
//   expect(screen.queryByTitle('Support')).toBeNull()
//   expect(screen.queryByText('Total votes')).toBeNull()
//   expect(screen.getByText('Comments')).toBeTruthy()
//   expect(screen.queryByText('Positive Ratings')).toBeNull()
//   expect(screen.queryByText('Negative Ratings')).toBeNull()
//   const resolvedDate =
//     screen.queryByText('created on 11. November 2021 - 2021-12345') ||
//     screen.queryByText('updated on 11 November 2021 - 2021-12345')
//   expect(resolvedDate).toBeTruthy()
// })

// test('Budgeting Proposal Card (3) - support phase and between support and vote phase - initiator, mod, logged-in, anonymous users', () => {
//   const permissions = {
//     view_support_count: true,
//     view_rate_count: false,
//     view_comment_count: true,
//     vote_allowed: false,
//     has_voting_permission_and_valid_token: false
//   }

//   const proposal = {
//     name: 'myProposal',
//     url: 'www',
//     creator: 'creator',
//     created: '2021-11-11T15:37:19.490201+01:00',
//     additional_item_badges_for_list_count: 0,
//     item_badges_for_list: [
//       ['moderator_status', 'wird ueberprueft', 'CONSIDERATION'],
//       ['budget', '20€'], ['category', 'candalf']],
//     reference_number: '2021-12345',
//     positive_rating_count: 2,
//     negative_rating_count: 1,
//     support_count: 8,
//     vote_count: 1,
//     comment_count: 7,
//     pk: 7,
//     vote_allowed: false
//   }
//   render(<Card proposal={proposal} permissions={permissions} />)
//   expect(screen.getByText('myProposal')).toBeTruthy()
//   expect(screen.getByText('creator')).toBeTruthy()
//   expect(screen.getByTitle('Support')).toBeTruthy()
//   expect(screen.queryByText('Total votes')).toBeNull()
//   expect(screen.getByText('Comments')).toBeTruthy()
//   expect(screen.queryByText('Positive Ratings')).toBeNull()
//   expect(screen.queryByText('Negative Ratings')).toBeNull()
//   const resolvedDate =
//     screen.queryByText('created on 11. November 2021 - 2021-12345') ||
//     screen.queryByText('updated on 11 November 2021 - 2021-12345')
//   expect(resolvedDate).toBeTruthy()
// })

// test('Budgeting Proposal Card (3) - vote phase with token - logged-in, anonymous', () => {
//   const permissions = {
//     view_support_count: false,
//     view_rate_count: false,
//     view_comment_count: true,
//     view_vote_count: false,
//     vote_allowed: true,
//     has_voting_permission_and_valid_token: true
//   }

//   const proposal = {
//     name: 'myProposal',
//     url: 'www',
//     creator: 'creator',
//     created: '2021-11-11T15:37:19.490201+01:00',
//     additional_item_badges_for_list_count: 0,
//     item_badges_for_list: [
//       ['moderator_status', 'wird ueberprueft', 'CONSIDERATION'],
//       ['budget', '20€'], ['category', 'candalf']],
//     reference_number: '2021-12345',
//     positive_rating_count: 2,
//     negative_rating_count: 1,
//     support_count: 8,
//     vote_count: 1,
//     comment_count: 7,
//     pk: 7,
//     vote_allowed: true
//   }
//   render(<Card proposal={proposal} permissions={permissions} />)
//   expect(screen.getByText('myProposal')).toBeTruthy()
//   expect(screen.getByText('creator')).toBeTruthy()
//   expect(screen.queryByTitle('Support')).toBeNull()
//   expect(screen.queryByText('Total votes')).toBeNull()
//   expect(screen.getByText('Comments')).toBeTruthy()
//   expect(screen.queryByText('Positive Ratings')).toBeNull()
//   expect(screen.queryByText('Negative Ratings')).toBeNull()
//   expect(screen.getByText('Give my vote')).toBeTruthy()
//   const resolvedDate =
//     screen.queryByText('created on 11. November 2021 - 2021-12345') ||
//     screen.queryByText('updated on 11 November 2021 - 2021-12345')
//   expect(resolvedDate).toBeTruthy()
// })

// test('Budgeting Proposal Card (3) - vote phase with token - initiator, moderator', () => {
//   const permissions = {
//     view_support_count: true,
//     view_rate_count: false,
//     view_comment_count: true,
//     view_vote_count: false,
//     vote_allowed: true,
//     has_voting_permission_and_valid_token: true
//   }

//   const proposal = {
//     name: 'myProposal',
//     url: 'www',
//     creator: 'creator',
//     created: '2021-11-11T15:37:19.490201+01:00',
//     additional_item_badges_for_list_count: 0,
//     item_badges_for_list: [
//       ['moderator_status', 'wird ueberprueft', 'CONSIDERATION'],
//       ['budget', '20€'], ['category', 'candalf']],
//     reference_number: '2021-12345',
//     positive_rating_count: 2,
//     negative_rating_count: 1,
//     support_count: 8,
//     vote_count: 1,
//     comment_count: 7,
//     pk: 7,
//     vote_allowed: true
//   }
//   render(<Card proposal={proposal} permissions={permissions} />)
//   expect(screen.getByText('myProposal')).toBeTruthy()
//   expect(screen.getByText('creator')).toBeTruthy()
//   expect(screen.getByTitle('Support')).toBeTruthy()
//   expect(screen.queryByText('Total votes')).toBeNull()
//   expect(screen.getByText('Comments')).toBeTruthy()
//   expect(screen.queryByText('Positive Ratings')).toBeNull()
//   expect(screen.queryByText('Negative Ratings')).toBeNull()
//   expect(screen.getByText('Give my vote')).toBeTruthy()
//   const resolvedDate =
//     screen.queryByText('created on 11. November 2021 - 2021-12345') ||
//     screen.queryByText('updated on 11 November 2021 - 2021-12345')
//   expect(resolvedDate).toBeTruthy()
// })

// test('Budgeting Proposal Card (3) - finished - logged-in, anonymous', () => {
//   const permissions = {
//     view_support_count: false,
//     view_rate_count: false,
//     view_comment_count: true,
//     view_vote_count: true,
//     vote_allowed: false,
//     has_voting_permission_and_valid_token: false
//   }

//   const proposal = {
//     name: 'myProposal',
//     url: 'www',
//     creator: 'creator',
//     created: '2021-11-11T15:37:19.490201+01:00',
//     additional_item_badges_for_list_count: 0,
//     item_badges_for_list: [
//       ['moderator_status', 'wird ueberprueft', 'CONSIDERATION'],
//       ['budget', '20€'], ['category', 'candalf']],
//     reference_number: '2021-12345',
//     positive_rating_count: 2,
//     negative_rating_count: 1,
//     support_count: 8,
//     vote_count: 1,
//     comment_count: 7,
//     pk: 7,
//     vote_allowed: true
//   }
//   render(<Card proposal={proposal} permissions={permissions} />)
//   expect(screen.getByText('myProposal')).toBeTruthy()
//   expect(screen.getByText('creator')).toBeTruthy()
//   expect(screen.queryByTitle('Support')).toBeNull()
//   expect(screen.getByText('Total votes')).toBeTruthy()
//   expect(screen.getByText('Comments')).toBeTruthy()
//   expect(screen.queryByText('Positive Ratings')).toBeNull()
//   expect(screen.queryByText('Negative Ratings')).toBeNull()
//   expect(screen.queryByText('Give my vote')).toBeNull()
//   const resolvedDate =
//     screen.queryByText('created on 11. November 2021 - 2021-12345') ||
//     screen.queryByText('updated on 11 November 2021 - 2021-12345')
//   expect(resolvedDate).toBeTruthy()
// })
