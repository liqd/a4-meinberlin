import React from 'react'

const ImageWithPlaceholder = ({ src, alt, lazy = true, ...rest }) => {
  const hasImage = src && src.length
  return (
    <img
      src={hasImage ? src : '/static/images/placeholder.png'}
      alt={alt}
      loading={lazy ? 'lazy' : 'eager'}
      {...rest}
    />
  )
}

export default ImageWithPlaceholder
