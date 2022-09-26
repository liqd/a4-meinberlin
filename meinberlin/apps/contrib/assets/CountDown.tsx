import React from 'react'

interface CountDownProps {
  activeClass: string
  inactiveClass: string
  countText: string
  counter: number
}

export const CountDown: React.FC<CountDownProps> = (props) => {
  const {
    activeClass,
    inactiveClass,
    countText,
    counter
  } = props

  return (
    <div
      className={counter > 0 ? activeClass : inactiveClass}
    >
      <span>{countText}</span>
    </div>
  )
}
