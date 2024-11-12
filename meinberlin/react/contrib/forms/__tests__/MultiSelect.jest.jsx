import React from 'react'
import { render, screen, fireEvent } from '@testing-library/react'
import { getLoopedIndex, MultiSelect, toggleValue } from '../MultiSelect'

describe('MultiSelect', () => {
  const choices = [
    { name: 'Swedish', value: 'sv' },
    { name: 'English', value: 'en' },
    { name: 'German', value: 'de' }
  ]

  const openedClass = 'multi-select__container--opened'

  test('is displaying with label and options', () => {
    render(
      <MultiSelect label="My Label" choices={choices} />
    )

    const combobox = screen.getByLabelText(/My Label/)
    expect(combobox).toHaveRole('combobox')

    const options = screen.getAllByRole('option')
    expect(options).toHaveLength(3)

    expect(screen.getByText('Swedish')).toBeInTheDocument()
    expect(screen.getByText('English')).toBeInTheDocument()
    expect(screen.getByText('German')).toBeInTheDocument()
  })

  test('is changing values on click', () => {
    const onChange = jest.fn()
    render(
      <MultiSelect label="My Label" choices={choices} onChange={onChange} />
    )

    const combobox = screen.getByLabelText(/My Label/)
    const listbox = screen.getByRole('listbox')

    fireEvent.click(combobox)
    expect(listbox).toHaveClass(openedClass)

    fireEvent.click(screen.getByText('English'))
    expect(onChange).toHaveBeenCalledWith(['en'])
  })

  test('is closing on blur', () => {
    render(
      <MultiSelect label="My Label" choices={choices} />
    )

    const combobox = screen.getByLabelText(/My Label/)
    const listbox = screen.getByRole('listbox')

    fireEvent.click(combobox)
    expect(listbox).toHaveClass(openedClass)

    fireEvent.blur(combobox, { relatedTarget: null })
    expect(listbox).not.toHaveClass(openedClass)
  })

  test('is opening on space', async () => {
    render(
      <MultiSelect label="My Label" choices={choices} />
    )

    const combobox = screen.getByLabelText(/My Label/)
    const listbox = screen.getByRole('listbox')

    expect(listbox).not.toHaveClass(openedClass)
    fireEvent.focus(combobox)
    fireEvent.keyDown(combobox, { key: ' ' })
    expect(listbox).toHaveClass(openedClass)
  })

  test('is selecting with space and enter', () => {
    render(
      <MultiSelect label="My Label" choices={choices} />
    )

    const combobox = screen.getByLabelText(/My Label/)

    fireEvent.focus(combobox)
    fireEvent.keyDown(combobox, { key: 'Enter' })
    const firstOption = screen.getAllByRole('option')[0]
    expect(combobox).toHaveAttribute('aria-activedescendant', 'sv')
    expect(firstOption).toHaveAttribute('aria-selected', 'false')

    fireEvent.keyDown(combobox, { key: 'Enter' })
    expect(firstOption).toHaveAttribute('aria-selected', 'true')

    fireEvent.keyDown(combobox, { key: ' ' })
    fireEvent.keyDown(combobox, { key: ' ' })
    expect(firstOption).toHaveAttribute('aria-selected', 'false')
  })

  test('is closing with escape', () => {
    render(
      <MultiSelect label="My Label" choices={choices} />
    )

    const combobox = screen.getByLabelText(/My Label/)
    const listbox = screen.getByRole('listbox')

    fireEvent.focus(combobox)
    fireEvent.keyDown(combobox, { key: 'Enter' })
    expect(listbox).toHaveClass(openedClass)

    fireEvent.keyDown(combobox, { key: 'Escape' })
    expect(listbox).not.toHaveClass(openedClass)
  })

  test('is navigating with arrows', () => {
    render(
      <MultiSelect label="My Label" choices={choices} />
    )

    const combobox = screen.getByLabelText(/My Label/)

    fireEvent.focus(combobox)
    fireEvent.keyDown(combobox, { key: 'ArrowDown' })
    expect(combobox).toHaveAttribute('aria-activedescendant', 'sv')

    fireEvent.keyDown(combobox, { key: 'ArrowDown' })
    expect(combobox).toHaveAttribute('aria-activedescendant', 'en')

    fireEvent.keyDown(combobox, { key: 'ArrowUp' })
    fireEvent.keyDown(combobox, { key: 'ArrowUp' })
    expect(combobox).toHaveAttribute('aria-activedescendant', 'de')
  })

  test('is navigating with home and end', () => {
    render(
      <MultiSelect label="My Label" choices={choices} />
    )

    const combobox = screen.getByLabelText(/My Label/)

    fireEvent.focus(combobox)
    fireEvent.keyDown(combobox, { key: 'ArrowDown' })
    expect(combobox).toHaveAttribute('aria-activedescendant', 'sv')

    fireEvent.keyDown(combobox, { key: 'End' })
    expect(combobox).toHaveAttribute('aria-activedescendant', 'de')

    fireEvent.keyDown(combobox, { key: 'Home' })
    expect(combobox).toHaveAttribute('aria-activedescendant', 'sv')
  })

  test('is selecting when typing', () => {
    render(
      <MultiSelect label="My Label" choices={choices} />
    )

    const combobox = screen.getByLabelText(/My Label/)

    fireEvent.focus(combobox)
    fireEvent.keyDown(combobox, { key: 'ArrowDown' })
    expect(combobox).toHaveAttribute('aria-activedescendant', 'sv')

    fireEvent.keyDown(combobox, { key: 'G' })
    fireEvent.keyDown(combobox, { key: 'E' })
    expect(combobox).toHaveAttribute('aria-activedescendant', 'de')
  })

  test('keeps focus on combobox when blue', () => {
    render(
      <MultiSelect label="My Label" choices={choices} />
    )

    const combobox = screen.getByLabelText(/My Label/)

    combobox.focus()
    fireEvent.keyDown(combobox, { key: 'ArrowDown' })
    expect(combobox).toHaveAttribute('aria-activedescendant', 'sv')

    const germanOption = screen.getByRole('option', { name: 'German' })
    germanOption.focus()
    fireEvent.click(germanOption)
    fireEvent.blur(combobox, { relatedTarget: germanOption })
    expect(combobox).toHaveFocus()
  })
})

describe('getLoopedIndex', () => {
  const choices = [1, 2, 3]
  test('returns the correct index', () => {
    expect(getLoopedIndex(choices, 0)).toBe(1)
    expect(getLoopedIndex(choices, 2)).toBe(3)
    expect(getLoopedIndex(choices, 3)).toBe(1)
    expect(getLoopedIndex(choices, -1)).toBe(3)
    expect(getLoopedIndex(choices, -3)).toBe(1)
  })
})

describe('toggleValue', () => {
  const choices = [1, 2, 3]
  test('toggles the value correctly from a given list', () => {
    expect(toggleValue(1, choices)).toEqual([2, 3])
    expect(toggleValue(2, choices)).toEqual([1, 3])
    expect(toggleValue(3, choices)).toEqual([1, 2])
    expect(toggleValue(4, choices)).toEqual([1, 2, 3, 4])
  })
})
