import React, { useEffect, useState, useCallback } from 'react'
import LikeCard from './LikeCard'

const QuestionUser = ({
  is_on_shortlist: isOnShortlist,
  likes,
  handleLike,
  id,
  children,
  category,
  hasLikingPermission
}) => {
  const [likeCount, setLikeCount] = useState(likes.count)
  const [sessionLike, setSessionLike] = useState(likes.session_like)

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
    <LikeCard
      title={children}
      category={category}
      isOnShortlist={isOnShortlist}
      likes={{
        count: likeCount,
        session_like: sessionLike
      }}
      {...(hasLikingPermission && { onLikeClick: handleLikeClick })}
    />
  )
}

export default QuestionUser
