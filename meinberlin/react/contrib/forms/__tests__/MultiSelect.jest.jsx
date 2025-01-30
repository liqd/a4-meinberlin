import React from 'react'
import { render, screen } from '@testing-library/react'
import { MultiSelect } from '../MultiSelect'
import useCombobox from 'adhocracy4/adhocracy4/static/forms/useCombobox'

jest.mock('adhocracy4/adhocracy4/static/forms/useCombobox')

describe('MultiSelect', () => {
  const choices = [
    { name: 'Swedish', value: 'sv' },
    { name: 'English', value: 'en' },
    { name: 'German', value: 'de' }
  ]

  const defaultMockHookReturn = {
    opened: false,
    labelId: 'test-label-id',
    activeItems: [],
    listboxAttrs: {
      role: 'listbox',
      'aria-multiselectable': 'true'
    },
    comboboxAttrs: {
      role: 'combobox',
      'aria-haspopup': 'true',
      'aria-expanded': false,
      'aria-labelledby': 'test-label-id'
    },
    getChoicesAttr: (choice) => ({
      role: 'option',
      'aria-selected': false,
      active: false,
      focused: false
    })
  }

  beforeEach(() => {
    useCombobox.mockImplementation(() => defaultMockHookReturn)
  })

  afterEach(() => {
    jest.clearAllMocks()
  })

  test('renders with label and options', () => {
    render(
      <MultiSelect label="My Label" choices={choices} />
    )

    expect(screen.getByText('My Label')).toBeInTheDocument()
    expect(screen.getByText('Swedish')).toBeInTheDocument()
    expect(screen.getByText('English')).toBeInTheDocument()
    expect(screen.getByText('German')).toBeInTheDocument()
  })

  test('displays active items when selected', () => {
    useCombobox.mockImplementation(() => ({
      ...defaultMockHookReturn,
      activeItems: [{ name: 'English', value: 'en' }]
    }))

    render(
      <MultiSelect
        label="My Label"
        choices={choices}
        placeholder="Select language"
      />
    )

    expect(screen.getAllByText('English')).toHaveLength(2)
  })

  test('displays placeholder when no items are selected', () => {
    render(
      <MultiSelect
        label="My Label"
        choices={choices}
        placeholder="Select language"
      />
    )

    expect(screen.getByText('Select language')).toBeInTheDocument()
  })

  test('applies correct classes', () => {
    useCombobox.mockImplementation(() => ({
      ...defaultMockHookReturn,
      opened: true
    }))

    const { container } = render(
      <MultiSelect
        label="My Label"
        choices={choices}
        comboboxClassName="combobox-custom"
        className="listbox-custom"
        liClassName="li-custom"
      />
    )

    const combobox = container.querySelector('.combobox-custom')
    expect(combobox).toBeInTheDocument()

    const listbox = container.querySelector('.listbox-custom')
    expect(listbox).toBeInTheDocument()

    const lis = container.querySelectorAll('.li-custom')
    expect(lis).toHaveLength(3)
  })

  test('renders check icon for active items', () => {
    useCombobox.mockImplementation(() => ({
      ...defaultMockHookReturn,
      getChoicesAttr: (choice) => ({
        ...defaultMockHookReturn.getChoicesAttr(choice),
        active: choice.value === 'en'
      })
    }))

    render(
      <MultiSelect label="My Label" choices={choices} />
    )

    const checkIcon = screen.getByText('English').closest('li').querySelector('.bicon-check')
    expect(checkIcon).toBeInTheDocument()
  })

  test('passes custom className to combobox', () => {
    render(
      <MultiSelect
        label="My Label"
        choices={choices}
        comboboxClassName="custom-combobox-class"
      />
    )

    const combobox = screen.getByRole('combobox')
    expect(combobox).toHaveClass('custom-combobox-class')
  })

  test('passes custom className to list items', () => {
    render(
      <MultiSelect
        label="My Label"
        choices={choices}
        liClassName="custom-li-class"
      />
    )

    const options = screen.getAllByRole('option')
    options.forEach(option => {
      expect(option).toHaveClass('custom-li-class')
    })
  })
})
