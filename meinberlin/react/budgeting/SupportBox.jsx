import React from 'react'
import django from 'django'
import RatingBox from 'adhocracy4/adhocracy4/ratings/static/ratings/RatingBox'
import SupportButton from './SupportButton'

function getSupportText (ratings, userRatingData) {
  const supportCount = ratings.positive
  const supportWithoutUser = django.ngettext(
    '1 person has supported this idea.',
    '%s people have supported this idea.',
    supportCount
  )

  const supportWithUser = django.ngettext(
    'You have supported this idea.',
    '<strong>You</strong> and %s people have supported this idea.',
    supportCount === 1 ? 1 : supportCount - 1
  )

  let text = userRatingData.userHasRating
    ? django.interpolate(supportWithUser, [supportCount === 1 ? 1 : supportCount - 1])
    : django.interpolate(supportWithoutUser, [supportCount])

  if (supportCount === 0) {
    text = django.gettext('This idea has not yet been supported.')
  } else if (supportCount === 2 && userRatingData.userHasRating) {
    // overrides the supportWithUser case when there are two supporters
    // but we would have to subtract one because it says "you and ..."
    // and then we would end up with supportCount = 1 again even though there
    // are two supporters
    text = django.gettext('<strong>You</strong> and 1 other person have supported this idea.')
  }
  return text
}

export const SupportBox = ({
  authenticated,
  support,
  isReadOnly,
  userSupported,
  userSupportId,
  objectId,
  contentType,
  isArchived
}) => (
  <RatingBox
    authenticatedAs={authenticated}
    positiveRatings={support}
    userHasRating={userSupported}
    userRatingId={userSupportId}
    isReadOnly={isReadOnly}
    objectId={objectId}
    contentType={contentType}
    render={(props) => {
      const text = getSupportText(props.ratings, props.userRatingData)

      return (
        <div className="modul-servicepanel servicepanel--centered panel--heavy">
          <div className="servicepanel__main" dangerouslySetInnerHTML={{ __html: text }} />
          <div className="servicepanel__right">
            <SupportButton {...props} isArchived={isArchived} />
          </div>
        </div>
      )
    }}
  />
)
