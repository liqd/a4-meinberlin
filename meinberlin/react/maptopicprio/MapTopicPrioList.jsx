import React from 'react'
import django from 'django'
import { CardList } from '../contrib/CardList'

export const MapTopicPrioList = (props) => {
  const translations = {
    listStr: django.gettext('Map topics list')
  }

  return (
    <CardList
      apiUrl={props.map_topics_api_url}
      listStr={translations.listStr}
    />
  )
}
