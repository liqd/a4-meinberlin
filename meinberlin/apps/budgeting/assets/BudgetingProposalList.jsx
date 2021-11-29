import React, { useEffect, useState } from 'react'
import django from 'django'
import { BudgetingProposalListItem } from './BudgetingProposalListItem'
import { Pagination } from './Pagination'

export const BudgetingProposalList = (props) => {
  const [data, setData] = useState([])
  const [meta, setMeta] = useState()

  const fetchProposals = (newIndex) => {
    const pageNumber = newIndex || 1
    const url = `${props.proposals_api_url}?page=${pageNumber}`
    fetch(url)
      .then(resp => resp.json())
      .then(json => {
        setData(json.results)
        setMeta({
          current_page: pageNumber,
          page_count: json.page_count,
          is_paginated: json.page_count > 1,
          previous: json.previous,
          next: json.next
        })
      })
      .catch(error => console.log(error))
  }

  const onPaginate = (selectedPage) => {
    fetchProposals(selectedPage)
  }

  useEffect(fetchProposals, [])

  const renderList = (data) => {
    let list
    if (data.length > 0) {
      list = (
        <>
          <ul className="u-list-reset">
            {data.map((proposal, idx) =>
              <BudgetingProposalListItem
                key={`budgeting-proposal-${idx}`}
                proposal={proposal}
                isVotingPhase={props.is_voting_phase}
              />)}
          </ul>
          {meta?.is_paginated &&
            <Pagination
              currPageIndex={meta.current_page}
              pageCount={meta.page_count}
              onPaginate={newUrl => onPaginate(newUrl)}
            />}
        </>
      )
    } else {
      list = (
        <span>{django.gettext('Nothing to show')}</span>
      )
    }
    return list
  }

  return (
    <div className="module-content--light">
      <div className="l-wrapper">
        <div className="l-center-8">
          {renderList(data)}
        </div>
      </div>
    </div>
  )
}
