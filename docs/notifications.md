# Notifications System Documentation

## Overview
The notifications system tracks user interactions and system events, providing separate views for different notification types. Key features include:
-   Batch read operations
-   Celery based notifications cleanup
-   logic to aggregate all rating notifications into one per i.e. proposal, comment, idea
---

## Models

### `Notification`
Core model storing user notifications.

#### Fields
| Field             | Type               | Description                        |
|-------------------|--------------------|------------------------------------|
| `recipient`       | ForeignKey(User)   | User receiving the notification    |
| `action`          | ForeignKey(Action) | Linked action item from adhocracy4 |
| `read`            | BooleanField       | Read status (default: `False`)     |
| `read_at`         | DateTimeField      | Timestamp of when marked as read   |


#### Key Features
-   **Automatic Timestamp Handling**: `read_at` set automatically on mark-as-read
-   **Notification Rules**: `should_notify` classmethod determines notification eligibility
---

## API Endpoints

### Base URL: `/api/notifications/`

All API endpoints return a paginated list of notifications specific to the current user.

**They all support these query parameters:**:
-   `?page=` - Pagination control
-   `?page_size=` - Items per page (default: 10)

### 1. List Notifications (GET)
**`GET /`**  
List all notifications in regards to the current user.


### 2. Interactions Feed (GET/POST)
**`GET|POST /interactions/`**  
Notifications where user is the target (comments, ratings, moderator feedback, etc).

**Features**:
-   **POST** marks all interaction notifications as read
-   Aggregates ratings by target object

**Response**:
```json
{
  "count": 15,
  "next": "http://localhost:8003/api/notifications/?page=2",
  "previous": null,
  "results": [
    {
      "action": { ... },
      "read": false,
      "read_at": null,
      "total_ratings": 5  // Only for aggregated ratings
    }
  ]
}
```
#### POST `/interactions`
If you post to this endpoint, it will mark all interaction notifications as read and then return the updated, paginated list.

**Request**:
```json
{
  "read": true
}
```

### 3. Followed Projects (GET/POST)
**`GET|POST /followed_projects/`**  
Project-specific notifications (phases, events).

**Shows**:
-   Phase transitions (start and end of phases)
-   Offline event starts

#### POST `/followed_projects`
If you post to this endpoint, it will mark all `followed_projects` notifications as read and then return the updated, paginated list.

**Request**:
```json
{
  "read": true
}
```
---
## Serializers
### ActionSerializer

**Fields**:
- `type` - Notification type
  * `support` - if a proposal is supported 
  * `rating` - if an item or a comment has been rated
  * `comment` - if an idea or a comment has been commented
  * `moderatorremark` - if an idea or a comment has received a ModeratorRemark
  * `phase_soon_over` - if a phase in a followed project is soon over
  * `phase_started` - if a phase in a followed project starts soon
  * `offlineevent` - if an event in a followed project starts soon
- `body` - Notification preview
- `link` - Link to notification trigger
- `item` - Name of the item (e.g. Idea, Proposal) where the action happened
- `project` - Name of the project where the action happened
- `actor` - User who performed the action
- `target_creator` - User who was the target of the action
  - i.e. if an idea was commented on, the creator of the idea
- `timestamp` - Timestamp of the action


## Aggregation Logic

### Rating Notifications
```python
most_recent_ratings = rating_qs.annotate(
    row_number=Window(
        RowNumber(),
        partition_by=F('action__target_object_id'),
        order_by=F('action__timestamp').desc()
    ),
    total_ratings=Window(
        Count('id'),
        partition_by=F('action__target_object_id')
    )
).filter(row_number=1)
```

**Behaviour**:
1. Groups by target object ID
2. Orders by timestamp descending
3. Filters for the first record in each group
4. Annotates with total ratings count
5. Combines with non-ratings via `UNION`

---

## Maintenance

### Celery scheduled tasks (tasks.py)
```python
@shared_task(name="periodic_notifications_cleanup")
def periodic_notifications_cleanup():
    """
    This task makes sure that any notification data older >6 months is deleted.
    """
    Notification.objects.filter(
        action__timestamp__gt=timezone.now() - timedelta(days=180)
    ).delete()
```

**Configuration**:
-   Runs daily via Celery beat
-   6-month retention
---

## Example Usage

### Mark All Interactions as Read
```python
POST /api/notifications/interactions/ {"read": true}

Response: 200 {
  "count": 15,
  "next": "http://localhost:8003/api/notifications/?page=2",
  "previous": null,
  "results": [
    {
      "action": { ... },
      "read": true,
      "read_at": "2025-02-11T14:53:07.161808+01:00",

      "total_ratings": 5  # Only for aggregated ratings
    }
  ]
}
```

### Get Followed Project Notifications
```python
GET /api/notifications/followed-projects/

Response: {
  "count": 15,
  "next": "http://localhost:8003/api/notifications/?page=2",
  "previous": null,
  "results": [
    {
      "action": { ... },
      "read": false,
      "read_at": null,
      "total_ratings": 5  // Only for aggregated ratings
    }
  ]
}
```
