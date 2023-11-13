import React, { useEffect, useState } from 'react'
import django from 'django'
import { Card } from '../contrib/Card'

export const TopicPrioList = (props) => {
  const [data, setData] = useState([])
  const [meta, setMeta] = useState([])

  const translations = {
    list: django.gettext('Topics list'),
    pillList: django.gettext('Topic tags')
  }

  const fetchTopics = () => {
    const url = props.topics_api_url
    fetch(url)
      .then(resp => resp.json())
      .then(json => {
        setData(json.results)
        setMeta({
          permissions: json.permissions
        })
      })
      .catch(error => console.log(error))
  }

  useEffect(() => {
    fetchTopics()
  }, [])

  const renderList = (data) => {
    return (
      <>
        {data && data.map((topic, idx) =>
          <li id={'item_' + topic.pk} key={'budgeting-topic-' + idx}>
            <Card
              item={topic}
              permissions={meta?.permissions}
            />
          </li>)}
      </>
    )
  }

  return (
    <>
      <h2 className="visually-hidden">{translations.list}</h2>
      <ul className="u-list-reset">
        {renderList(data)}
      </ul>
    </>
  )
}
