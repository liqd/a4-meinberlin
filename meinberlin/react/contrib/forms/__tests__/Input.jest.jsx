import React from 'react'
import { render, screen, fireEvent } from '@testing-library/react'
import { Input } from '../Input'

describe('Input', () => {
  test('is displaying with label, before and children', () => {
    render(
      <Input label="My Label" id="TestId" before="Before">
        <span>Children</span>
      </Input>
    )
    const input = screen.getByLabelText(/My Label/)
    const before = screen.getByText(/Before/)
    const children = screen.getByText(/Children/)
    expect(input).toBeTruthy()
    expect(before).toBeTruthy()
    expect(children).toBeTruthy()
  })
  test('rest props are passed', () => {
    render(
      <Input label="My Label" id="TestId" defaultValue="DefaultValue">
        <span>Children</span>
      </Input>
    )
    const input = screen.getByLabelText(/My Label/)
    expect(input.value).toEqual('DefaultValue')
  })
  test('onChange is called', () => {
    const onChangeFn = jest.fn()
    render(
      <Input
        label="My Label"
        id="TestId"
        onChange={onChangeFn}
      />
    )
    const input = screen.getByLabelText(/My Label/)
    fireEvent.change(input, { target: { value: 'test' } })
    expect(onChangeFn).toHaveBeenCalled()
  })
})
