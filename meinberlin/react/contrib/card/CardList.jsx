import React, { useRef } from 'react'
import django from 'django'
import { Card } from './Card'
import { CardMeta } from './CardMeta'
import { CardStatus } from './CardStatus'
import { Pagination } from '../Pagination'
import { useFetchedItems } from '../contexts/FetchItemsProvider'
import { ControlBar } from '../ControlBar'

export const CardList = (props) => {
  const { results, currentPage, isMapAndList } = useFetchedItems()
  const container = useRef(null)
  const data = results.list
  const translations = {
    noResults: django.gettext('Nothing to show'),
    pillList: django.gettext('Pill List')
  }

  return (
    <>
      {!isMapAndList && <ControlBar />}
      <h2 className="aural">{props.listStr}</h2>
      {data?.results && data.results.length > 0
        ? (
          <ul className="list--clean" ref={container}>
            {data.results.map((item, idx) => (
              <li key={idx}>
                <Card item={item} idx={idx} permissions={data?.permissions} currentPage={currentPage}>
                  {item.item_badges_for_list?.length > 0 && (
                    <CardStatus
                      pills={item.item_badges_for_list}
                      proposal={item}
                      numOfMorePills={item.additional_item_badges_for_list_count}
                      itemUrl={item.url}
                      pillHeader={translations.pillList}
                    />
                  )}
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
          containerTop={container.current?.offsetTop}
        />
      )}
    </>
  )
}
