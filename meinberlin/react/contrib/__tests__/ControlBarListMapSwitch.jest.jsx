import React from 'react'
import { render, screen } from '@testing-library/react'
import { ControlBarListMapSwitch } from '../ControlBarListMapSwitch'
import { BrowserRouter } from 'react-router-dom'

test('Buttonlink to map with href', () => {
  render(
    <BrowserRouter>
      <ControlBarListMapSwitch query="&ordering=-created" />
    </BrowserRouter>
  )
  const buttonToMap = screen.getAllByRole('button')
  expect(buttonToMap).toBeTruthy()
  expect(buttonToMap.length).toEqual(2)
})
