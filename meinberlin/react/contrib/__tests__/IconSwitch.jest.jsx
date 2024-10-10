import React from 'react'
import { render, screen } from '@testing-library/react'
import { IconSwitch } from '../IconSwitch'

const props = {
  fullWidth: true,
  viewModeStr: 'View mode',
  buttons: [
    {
      ariaLabel: 'show list',
      label: 'list',
      icon: 'fa fa-list',
      id: 'show_list',
      isActive: true,
      handleClick: jest.fn()
    },
    {
      ariaLabel: 'show map',
      label: 'map',
      icon: 'fa fa-map',
      id: 'show_map',
      isActive: false,
      handleClick: jest.fn()
    }
  ]
}

test('IconSwitch is showing start state', () => {
  render(
    <IconSwitch {...props} />
  )
  const startTextButton = screen.getByLabelText('show list')
  const endTextButton = screen.getByLabelText('show map')
  expect(startTextButton.textContent).toBe('list')
  expect(endTextButton.textContent).toBe('map')
  expect(startTextButton.getAttribute('aria-pressed')).toEqual('true')
})

test('IconSwitch is showing end state', () => {
  render(
    <IconSwitch {...props} buttons={props.buttons.map(b => ({ ...b, isActive: !b.isActive }))} />
  )
  const startTextButton = screen.getByLabelText('show list')
  const endTextButton = screen.getByLabelText('show map')
  expect(startTextButton.textContent).toBe('list')
  expect(endTextButton.textContent).toBe('map')
  expect(endTextButton.getAttribute('aria-pressed')).toEqual('true')
})
