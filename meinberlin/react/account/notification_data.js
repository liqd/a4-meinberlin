import django from 'django'

export const notificationData = [
  {
    header: django.gettext('Project-Related Notifications'),
    notifications: {
      email_newsletter: {
        title: django.gettext('E-Mail Newsletter'),
        description: django.gettext('Receive newsletters with updates and news about the projects you follow via e-mail.')
      },
      notify_followers_phase_started: {
        title: django.gettext('Participation Start'),
        description: django.gettext('Receive a notification when a participation begins in a project you follow.'),
        activityFeedName: 'track_followers_phase_started'
      },
      notify_followers_phase_over_soon: {
        title: django.gettext('Participation End'),
        description: django.gettext('Receive a notification when a participation is near its end in a project you follow.'),
        activityFeedName: 'track_followers_phase_over_soon'
      },
      notify_followers_event_upcoming: {
        title: django.gettext('Event'),
        description: django.gettext('Receive notifications for upcoming events in projects you follow.'),
        activityFeedName: 'track_followers_event_upcoming'
      }
    }
  },
  {
    header: django.gettext('Interactions with Other Users or Moderation'),
    notifications: {
      notify_creator: {
        title: django.gettext('Reactions of other users'),
        description: django.gettext('Receive a notification when someone reacts to your contribution with a comment.')
      },
      notify_creator_on_moderator_feedback: {
        title: django.gettext('Reactions of moderation'),
        description: django.gettext('Receive a notification for feedback and status changes of your idea from the moderation.')
      }
    }
  },
  {
    header: django.gettext('Notifications for Initiators and Moderators'),
    restricted: true,
    notifications: {
      notify_initiators_project_created: {
        title: django.gettext('New Project in Your Organization'),
        description: django.gettext('Receive a notification when a new project is created in your organization.')
      },
      notify_moderator: {
        title: django.gettext('New Contribution in a Moderated Project'),
        description: django.gettext('Receive a notification when a new contribution is added to a project you moderate.')
      }
    }
  }
]
