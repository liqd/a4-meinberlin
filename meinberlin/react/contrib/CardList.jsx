import React, { useState, useEffect } from 'react'
import { useLocation, useSearchParams } from 'react-router-dom'
import django from 'django'
import { Card } from './Card'
import { CardMeta } from './CardMeta'
import { CardStatus } from './CardStatus'
import { Pagination } from './Pagination'

export const CardList = (props) => {
  const location = useLocation()
  const [queryParams] = useSearchParams()
  const [data, setData] = useState(null)
  const [currentPage, setCurrentPage] = useState(1)

  const translations = {
    noResults: django.gettext('Nothing to show'),
    pillList: django.gettext('Pill List')
  }

  useEffect(() => {
    const fetchData = async () => {
      try {
        const url = props.apiUrl + location.search
        const response = await fetch(url)
        const json = await response.json()
        setData(json)
        setCurrentPage(queryParams.get('page') || 1)
      } catch (error) {
        console.error(error)
      }
    }

    fetchData()
  }, [props.apiUrl, location.search])

  return (
    <>
      <h2 className="aural">{props.listStr}</h2>
      {data?.results && data.results.length > 0
        ? (
          <ul className="list--clean">
            {data.results.map((item, idx) => (
              <li key={idx}>
                <Card item={item} idx={idx} permissions={data?.permissions} currentPage={currentPage}>
                  {props.cardStatus &&
                    <CardStatus
                      pills={item.item_badges_for_list}
                      proposal={item}
                      numOfMorePills={item.additional_item_badges_for_list_count}
                      itemUrl={item.url}
                      pillHeader={translations.pillList}
                    />}
                  {props.cardMeta &&
                    <CardMeta
                      item={item}
                    />}
                </Card>
              </li>
            ))}
          </ul>
          )
        : (<p>{translations.noResults}</p>)}
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
