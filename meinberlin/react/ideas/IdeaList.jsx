import React, { useEffect, useState } from 'react'
import { useLocation, useSearchParams } from 'react-router-dom'
import django from 'django'

import { Card } from '../contrib/Card'
import { CardStatus } from '../contrib/CardStatus'
import { CardMeta } from '../contrib/CardMeta'
import { Pagination } from '../contrib/Pagination'

export const IdeaList = (props) => {
  const location = useLocation()
  const [queryParams] = useSearchParams()

  const translations = {
    list: django.gettext('Ideas list'),
    noResults: django.gettext('Nothing to show'),
    pillList: django.gettext('Proposal tags')
  }

  const [data, setData] = useState(null)
  const [currentPage, setCurrentPage] = useState(1)

  useEffect(() => {
    const fetchIdeas = async () => {
      try {
        const url = props.ideas_api_url + location.search
        const response = await fetch(url)
        const json = await response.json()
        setData(json)
        setCurrentPage(queryParams.get('page') || 1)
      } catch (error) {
        console.error(error)
      }
    }

    fetchIdeas()
  }, [props.ideas_api_url, location.search])

  return (
    <>
      <h2 className="visually-hidden">{translations.list}</h2>
      {data?.results && data.results.length > 0
        ? (
          <ul className="u-list-reset">
            {data.results.map((idea, idx) => (
              <li id={'item_' + idea.pk} key={'idea-' + idx}>
                <Card
                  item={idea}
                  permissions={data?.permissions}
                  currentPage={currentPage}
                >
                  <CardStatus
                    pills={idea.item_badges_for_list}
                    proposal={idea}
                    numOfMorePills={idea.additional_item_badges_for_list_count}
                    itemUrl={idea.url}
                    pillHeader={translations.pillList}
                  />
                  <CardMeta
                    item={idea}
                  />
                </Card>
              </li>
            ))}
          </ul>
          )
        : (
          <p>{translations.noResults}</p>
          )}
      {data?.page_count > 1 && (
        <Pagination
          elidedRange={data.page_elided_range}
          nextPage={data.next}
          prevPage={data.previous}
          pageCount={data.page_count}
        />
      )}
    </>
  )
}
