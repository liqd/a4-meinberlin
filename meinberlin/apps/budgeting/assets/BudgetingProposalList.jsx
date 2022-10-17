import React, { useEffect, useState } from 'react'
import django from 'django'
import { BudgetingProposalListItem } from './BudgetingProposalListItem'
import { Pagination } from './Pagination'
import { CountDown } from '../../contrib/assets/CountDown'
import { ControlBar } from './ControlBar'
import { useLocation, useSearchParams } from 'react-router-dom'

export const BudgetingProposalList = (props) => {
  const [data, setData] = useState([])
  const [meta, setMeta] = useState()
  const location = useLocation()
  const [queryParams] = useSearchParams()

  const fetchProposals = () => {
    const url = props.proposals_api_url + location.search
    fetch(url)
      .then(resp => resp.json())
      .then(json => {
        setData(json.results)
        setMeta({
          current_page: queryParams.get('page') || 1,
          page_count: json.page_count,
          is_paginated: json.page_count > 1,
          previous: json.previous,
          next: json.next,
          filters: json.filters,
          permissions: json.permissions,
          locale: json.locale,
          token_info: json.token_info,
          page_elided_range: json.page_elided_range
        })
      })
      .catch(error => console.log(error))
  }

  useEffect(() => {
    fetchProposals()
  }, [location.search])

  const renderList = (data) => {
    return (
      <>
        <ul className="u-list-reset">
          {data.map((proposal, idx) =>
            <BudgetingProposalListItem
              key={`budgeting-proposal-${idx}`}
              proposal={proposal}
              locale={meta?.locale}
              permissions={meta?.permissions}
              tokenvoteApiUrl={props.tokenvote_api_url}
              onVoteChange={selectedPage => fetchProposals(selectedPage)}
              currentPage={meta?.current_page}
              votesLeft={
                meta?.token_info
                  ? meta?.token_info.votes_left
                  : false
              }
            />)}
        </ul>
        {meta?.is_paginated &&
          <Pagination
            elidedRange={meta.page_elided_range}
            nextPage={meta.next}
            prevPage={meta.previous}
            pageCount={meta.page_count}
          />}
      </>
    )
  }

  const getVoteCountText = (votes) => {
    const countText = django.ngettext('you have 1 vote left', 'you have %s votes left', votes)
    return django.interpolate(countText, [votes])
  }

  return (
    <>
      {(props.is_voting_phase && meta?.token_info) &&
        <div className="module-content--light">
          <div className="container">
            <div className="offset-lg-3 col-lg-6">
              <CountDown
                countText={getVoteCountText(meta?.token_info.num_votes_left)}
                activeClass="btn btn--transparent btn--full u-spacer-bottom btn--huge u-primary"
                inactiveClass="btn btn--full btn--light u-spacer-bottom btn--huge"
                counter={meta?.token_info.num_votes_left}
              />
            </div>
          </div>
        </div>}
      <ControlBar
        filters={meta?.filters}
        numOfResults={data?.length}
      />
      <div className="module-content--light">
        <div className="container">
          <div className="offset-lg-2 col-lg-8">
            {renderList(data)}
          </div>
        </div>
      </div>
    </>
  )
}
