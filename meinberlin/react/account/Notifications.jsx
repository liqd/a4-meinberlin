import React from 'react'
import FeedItem from './FeedItem'
import FeedList from './FeedList'
import { notificationsData } from './notification_data'
import { toFilterList } from '../contrib/helpers'

export default function Notifications (urls) {
  return (
    <>
      <InteractionsFeed {...urls} />
      <SearchProfilesFeed {...urls} />
      <FollowedProjectsFeed {...urls} />
    </>
  )
}

function InteractionsFeed ({ interactionsApiUrl, notificationsApiUrl, planListUrl }) {
  return (
    <FeedList
      {...notificationsData.interactions}
      apiUrl={interactionsApiUrl}
      link={planListUrl}
      renderFeedItem={({ id, read, action, total_ratings: totalRatings }, index, handleMarkAsRead) => {
        const { type, timestamp, link, ...rest } = action
        const text = getInteractionText({ type, ...rest }, totalRatings)

        if (!text) {
          return null
        }

        const { title, body, linkText } = text

        return (
          <FeedItem
            key={timestamp + index}
            id={id}
            apiUrl={notificationsApiUrl}
            icon={type === 'comment' ? 'comment' : 'clock'}
            title={title}
            body={body}
            link={link}
            linkText={linkText}
            isRead={read}
            timestamp={timestamp}
            onClickReadLink={handleMarkAsRead}
          />
        )
      }}
    />
  )
}

function SearchProfilesFeed ({ searchProfilesApiUrl, notificationsApiUrl, planListUrl }) {
  return (
    <FeedList
      {...notificationsData.searchProfiles}
      apiUrl={searchProfilesApiUrl}
      link={planListUrl}
      renderFeedItem={({ id, search_profile: searchProfile, read, action }, index, handleMarkAsRead) => {
        const { timestamp, project, link, ...rest } = action
        const text = getSearchProfileText(searchProfile, { project, ...rest })
        const filterList = toFilterList(searchProfile).map((names) => names.join(', ')).slice(0, 3)

        const { title, body, linkText } = text

        const thumbnail = project.tile_image
          ? {
              url: project.tile_image,
              alt: project.tile_image_alt_text
            }
          : null

        return (
          <FeedItem
            key={timestamp + index}
            id={id}
            apiUrl={notificationsApiUrl}
            icon="heart"
            title={title}
            meta={filterList}
            thumbnail={thumbnail}
            body={body}
            link={link}
            linkText={linkText}
            isRead={read}
            timestamp={timestamp}
            onClickReadLink={handleMarkAsRead}
          />
        )
      }}
    />
  )
}

function FollowedProjectsFeed ({ followedProjectsApiUrl, notificationsApiUrl, planListUrl }) {
  return (
    <FeedList
      {...notificationsData.followedProjects}
      apiUrl={followedProjectsApiUrl}
      link={planListUrl}
      renderFeedItem={({ id, read, action }, index, handleMarkAsRead) => {
        const { type, timestamp, link, ...rest } = action
        const text = getFollowedProjectsText({ type, ...rest })

        if (!text) {
          return null
        }

        const { title, body, linkText } = text

        return (
          <FeedItem
            key={timestamp + index}
            id={id}
            apiUrl={notificationsApiUrl}
            icon="clock"
            title={title}
            body={body}
            link={link}
            linkText={linkText}
            isRead={read}
            timestamp={timestamp}
            onClickReadLink={handleMarkAsRead}
          />
        )
      }}
    />
  )
}

function getInteractionText (action, totalRatings) {
  const { type, source, body, actor, project } = action

  switch (type) {
    case 'comment':
      switch (source) {
        case 'idea':
        case 'mapidea':
          if (actor.is_moderator) {
            return {
              title: notificationsData.interactions.moderatorReplieIdeaText(project.title, project.url),
              body,
              linkText: notificationsData.viewCommentText
            }
          }

          return {
            title: notificationsData.interactions.userRepliedIdeaText(project.title, project.url),
            body,
            linkText: notificationsData.viewCommentText
          }

        case 'comment':
          if (actor.is_moderator) {
            return {
              title: notificationsData.interactions.moderatorRepliedCommentText(project.title, project.url),
              body,
              linkText: notificationsData.viewCommentText
            }
          }

          return {
            title: notificationsData.interactions.userRepliedCommentText(project.title, project.url),
            body,
            linkText: notificationsData.viewCommentText
          }
      }
      break

    case 'rating':
      switch (source) {
        case 'idea':
        case 'mapidea':
          if (totalRatings > 1) {
            return {
              title: notificationsData.interactions.usersRatedIdeaText(project.title, project.url),
              linkText: notificationsData.viewIdeaText
            }
          }

          return {
            title: notificationsData.interactions.userRatedIdeaText(project.title, project.url),
            linkText: notificationsData.viewIdeaText
          }

        case 'comment':
          if (totalRatings > 1) {
            return {
              title: notificationsData.interactions.usersRatedCommentText(project.title, project.url),
              linkText: notificationsData.viewIdeaText
            }
          }

          return {
            title: notificationsData.interactions.userRatedCommentText(project.title, project.url),
            body,
            linkText: notificationsData.viewCommentText
          }
      }
  }
}

function getSearchProfileText (searchProfile, action) {
  const { project } = action

  return {
    title: notificationsData.searchProfiles.projectMatchesSearchProfileText(project.title, project.url, searchProfile.name),
    body: project.title,
    linkText: notificationsData.viewProjectText
  }
}

function getFollowedProjectsText (action) {
  const { type, source, source_timestamp: sourceTimestamp, project } = action
  const date = new Date(project.active_phase[2])
  const sourceDate = new Date(sourceTimestamp).toLocaleString()

  switch (type) {
    case 'phase_started':
      return {
        title: notificationsData.followedProjects.phaseStartedText(project.title, project.url, date.toLocaleDateString()),
        linkText: notificationsData.viewProjectText
      }

    case 'phase_soon_over':
      return {
        title: notificationsData.followedProjects.phaseEndedText(project.title, project.url, date.toLocaleDateString()),
        linkText: notificationsData.viewProjectText
      }

    case 'offlineevent':
      return {
        title: notificationsData.followedProjects.offlineEvent(source, project.title, project.url, sourceDate.toLocaleString()),
        linkText: notificationsData.viewProjectText
      }
  }
}
