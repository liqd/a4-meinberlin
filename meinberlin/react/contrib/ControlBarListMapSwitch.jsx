import React from 'react'
import django from 'django'
import { useSearchParams } from 'react-router'
import { IconSwitch } from './IconSwitch'

const translated = {
  viewMode: django.gettext('View mode'),
  viewList: django.gettext('View as list'),
  list: django.gettext('List'),
  viewMap: django.gettext('View as map'),
  map: django.gettext('Map')
}

export const ControlBarListMapSwitch = () => {
  const [queryParams, setQueryParams] = useSearchParams()
  const viewMode = queryParams.get('mode') || 'list'

  const handleClick = () => {
    queryParams.set('mode', viewMode === 'list' ? 'map' : 'list')
    setQueryParams(queryParams)
  }

  return (
    <IconSwitch
      viewModeStr={translated.viewMode}
      buttons={[
        {
          ariaLabel: translated.viewList,
          label: translated.list,
          icon: 'fa fa-list',
          id: 'show_list',
          isActive: viewMode === 'list',
          handleClick
        },
        {
          ariaLabel: translated.viewMap,
          label: translated.map,
          icon: 'fa fa-map',
          id: 'show_map',
          isActive: viewMode === 'map',
          handleClick
        }
      ]}
    />
  )
}
