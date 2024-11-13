import React, { useEffect, useState, useCallback } from 'react'
import LikeCard from './LikeCard'
import django from 'django'

const shortlistText = django.gettext('on shortlist')

const QuestionUser = ({ is_on_shortlist: onShortList, likes, handleLike, id, children, category, hasLikingPermission }) => {
  const [isOnShortlist, setIsOnShortlist] = useState(onShortList)
  const [likeCount, setLikeCount] = useState(likes.count)
  const [sessionLike, setSessionLike] = useState(likes.session_like)

  useEffect(() => {
    setIsOnShortlist(onShortList)
  }, [onShortList])

  useEffect(() => {
    setLikeCount(likes.count)
    setSessionLike(likes.session_like)
  }, [likes])

  const handleErrors = (response) => {
    if (!response.ok) {
      throw new Error(response.statusText)
    }
    return response
  }

  const handleLikeClick = useCallback(() => {
    const newSessionLike = !sessionLike
    handleLike(id, newSessionLike)
      .then(handleErrors)
      .then(() => {
        setSessionLike(newSessionLike)
        setLikeCount((prevLikes) => prevLikes + (newSessionLike ? 1 : -1))
      })
      .catch((error) => {
        console.log(error.message)
      })
  }, [sessionLike, handleLike, id])

  return (
    <>
      {isOnShortlist &&
        <>
          <i className="far fa-list-alt u-primary u-icon-spacing" aria-hidden="true" />
          <span className="visually-hidden">{shortlistText}</span>
        </>}
      <LikeCard
        title={children}
        category={category}
        likes={{
          count: likeCount,
          session_like: sessionLike
        }}
        {...(hasLikingPermission && { onLikeClick: handleLikeClick })}
      />
    </>
  )
}

export default QuestionUser
