import React from 'react'
import django from 'django'
import { CardList } from '../contrib/card/CardList'

export const TopicPrioList = (props) => {
  const translations = {
    listStr: django.gettext('Map topics list')
  }

  return (
    <CardList
      apiUrl={props.topics_api_url}
      listStr={translations.listStr}
    />
  )
}
