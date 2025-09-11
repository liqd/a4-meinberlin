import React from 'react'

const ImageWithPlaceholder = ({ src, alt, lazy = true, className, ...rest }) => {
  const hasImage = src && src.length
  return hasImage
    ? (
      <img
        src={src}
        alt={alt}
        loading={lazy ? 'lazy' : 'eager'}
        className={className}
        {...rest}
      />
      )
    : (
      <picture className={className}>
        <source type="image/webp" srcSet="/static/images/placeholder_tile.webp" />
        <source type="image/avif" srcSet="/static/images/placeholder_tile.avif" />
        <img
          src="/static/images/placeholder_tile.svg"
          alt={alt}
          loading={lazy ? 'lazy' : 'eager'}
          {...rest}
          className="project-tile__placeholder"
        />
      </picture>
      )
}

export default ImageWithPlaceholder
