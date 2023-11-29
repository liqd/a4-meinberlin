import React from 'react'
import django from 'django'
import { CardList } from '../contrib/card/CardList'

export const MapIdeaList = (props) => {
  const translations = {
    listStr: django.gettext('Map Ideas list')
  }

  return (
    <CardList
      apiUrl={props.mapideas_api_url}
      listStr={translations.listStr}
      cardStatus
      cardMeta
    />
  )
}
