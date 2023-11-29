import React from 'react'
import django from 'django'
import { CardList } from '../contrib/card/CardList'

export const IdeaList = (props) => {
  const translations = {
    listStr: django.gettext('Ideas list')
  }

  return (
    <CardList
      apiUrl={props.ideas_api_url}
      listStr={translations.listStr}
      cardStatus
      cardMeta
    />
  )
}
