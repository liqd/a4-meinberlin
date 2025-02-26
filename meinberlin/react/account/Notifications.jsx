import React from 'react'
import FeedItem from './FeedItem'
import FeedList from './FeedList'
import { notificationsData } from './notification_data'

export default function Notifications ({ interactionsApiUrl, followedProjectsApiUrl, planListUrl }) {
  return (
    <>
      <InteractionsFeed apiUrl={interactionsApiUrl} planListUrl={planListUrl} />
      <FollowedProjectsFeed apiUrl={followedProjectsApiUrl} planListUrl={planListUrl} />
    </>
  )
}

function InteractionsFeed ({ apiUrl, planListUrl }) {
  return (
    <FeedList
      {...notificationsData.interactions}
      apiUrl={apiUrl}
      link={planListUrl}
      renderFeedItem={({ read, action }, index) => {
        const { type, timestamp, link, ...rest } = action
        const text = getInteractionText({ type, ...rest })

        if (!text) {
          return null
        }

        const { title, body, linkText } = text

        return (
          <FeedItem
            key={timestamp + index}
            icon={type === 'comment' ? 'comment' : 'clock'}
            title={title}
            body={body}
            link={link}
            linkText={linkText}
            isRead={read}
            timestamp={timestamp}
          />
        )
      }}
    />
  )
}

function FollowedProjectsFeed ({ apiUrl, planListUrl }) {
  return (
    <FeedList
      {...notificationsData.followedProjects}
      apiUrl={apiUrl}
      link={planListUrl}
      renderFeedItem={({ read, action }, index) => {
        const { type, timestamp, link, ...rest } = action
        const text = getFollowedProjectsText({ type, ...rest })

        if (!text) {
          return null
        }

        const { title, body, linkText } = text

        return (
          <FeedItem
            key={timestamp + index}
            icon="clock"
            title={title}
            body={body}
            link={link}
            linkText={linkText}
            isRead={read}
            timestamp={timestamp}
          />
        )
      }}
    />
  )
}

function getInteractionText (action) {
  const { type, source, body, actor, project } = action

  switch (type) {
    case 'comment':
      switch (source) {
        case 'idea':
        case 'mapidea':
          if (actor.is_moderator) {
            return {
              title: notificationsData.interactions.moderatorReplieIdeaText(project.title),
              body,
              linkText: notificationsData.viewCommentText
            }
          }

          return {
            title: notificationsData.interactions.userRepliedIdeaText(project.title),
            body,
            linkText: notificationsData.viewCommentText
          }

        case 'comment':
          if (actor.is_moderator) {
            return {
              title: notificationsData.interactions.moderatorRepliedCommentText(project.title),
              body,
              linkText: notificationsData.viewCommentText
            }
          }

          return {
            title: notificationsData.interactions.userRepliedCommentText(project.title),
            body,
            linkText: notificationsData.viewCommentText
          }
      }
      break

    case 'rating':
      switch (source) {
        case 'idea':
        case 'mapidea':
          return {
            title: notificationsData.interactions.userRatedIdeaText(project.title),
            linkText: notificationsData.viewIdeaText
          }

        case 'comment':
          return {
            title: notificationsData.interactions.userRatedCommentText(project.title),
            body,
            linkText: notificationsData.viewCommentText
          }
      }
  }
}

function getFollowedProjectsText (action) {
  const { type, project } = action
  const date = new Date(project.active_phase[2])

  switch (type) {
    case 'phase_started':
      return {
        title: notificationsData.followedProjects.phaseStartedText(project.title, date.toLocaleDateString()),
        linkText: notificationsData.viewProjectText
      }

    case 'phase_soon_over':
      return {
        title: notificationsData.followedProjects.phaseEndedText(project.title, date.toLocaleDateString()),
        linkText: notificationsData.viewProjectText
      }
  }
}
