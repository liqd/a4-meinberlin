import React from 'react'
import django from 'django'
import { CardList } from '../contrib/card/CardList'

export const KiezkasseProposalsList = (props) => {
  const translations = {
    listStr: django.gettext('Proposals list')
  }

  return (
    <CardList
      apiUrl={props.kiezkasse_proposals_api_url}
      listStr={translations.listStr}
      cardStatus
      cardMeta
    />
  )
}
