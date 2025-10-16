# Migration Guide: OfflineEventsComponent → OfflineEventModuleComponent

## Overview
Migration from the old project-based `OfflineEventsComponent` to the new module-based `OfflineEventModuleComponent` architecture.

## Areas to Delete/Clean Up

### 1. Dashboard Components (`meinberlin/apps/offlineevents/dashboard.py`)

#### Areas to Delete:
- **Lines 14-58**: Complete `OfflineEventsComponent` class

### 2. Views (`meinberlin/apps/offlineevents/views.py`)

#### Views to Delete:
- `OfflineEventDetailView` (lines 15-21)
- `OfflineEventListView` (lines 23-35)
- `OfflineEventCreateView` (lines 37-61)
- `OfflineEventUpdateView` (lines 63-83)
- `OfflineEventDeleteView` (lines 85-114)

### 3. URL References in Views

#### URL Names to Clean Up:
- `"a4dashboard:offlineevent-list"`
- `"a4dashboard:offlineevent-create"`
- `"a4dashboard:offlineevent-update"`
- `"a4dashboard:offlineevent-delete"`

#### Affected Files:
- `meinberlin/apps/projects/views.py` (line 379)
- `meinberlin/apps/offlineevents/views.py` (lines 59, 81, 112)

### 4. Templates

#### Templates to Delete:
- `meinberlin_offlineevents/offlineevent_list.html`
- `meinberlin_offlineevents/offlineevent_create_form.html`
- `meinberlin_offlineevents/offlineevent_update_form.html`
- `meinberlin_offlineevents/offlineevent_confirm_delete.html`
- `meinberlin_offlineevents/includes/offlineevent_list_item.html`

#### Keep:
- `meinberlin_offlineevents/offlineevent_detail.html`
- `meinberlin_offlineevents/offlineevent_module_dashboard_form.html`
- `meinberlin_offlineevents/offlineevent_settings_dashboard_form.html`

### 5. Models

#### Models to Delete:
- `OfflineEvent` Model: Complete removal
- `OfflineEventsQuerySet`: Complete removal

#### Keep:
- `OfflineEventItem` Model: Remains

### 6. Template Tags (`meinberlin/apps/offlineevents/templatetags/offlineevent_tags.py`)
#### Check entire file and likely delete:

### 7. Project Views (`meinberlin/apps/projects/views.py`)

#### Areas to Delete:
- `ProjectEventView` (lines 368-381): Complete removal
- Import `from meinberlin.apps.offlineevents.models import OfflineEvent` (line 32)

#### Keep:
- `ModuleDetailview.get_context_data()` (lines 416-428): Import of `OfflineEventItem`

### 8. Forms (`meinberlin/apps/offlineevents/forms.py`)

#### Forms to Delete:
- `OfflineEventForm` (lines 10-25): Uses `OfflineEvent` Model

#### Keep:
- `OfflineEventItemForm` (lines 27-58)
- `OfflineEventBasicForm` (lines 60-65)

### 9. Phases (`meinberlin/apps/offlineevents/phases.py`)

#### Areas to Clean Up:
- `OfflineEventPhase` (lines 11-24): 
  - `view = views.OfflineEventDetailView` → remove (view will be deleted)
  - `features = {"crud": (models.OfflineEvent,)}` → remove

### 10. Tests

#### Test Files to Delete:
- `tests/offlineevents/dashboard_components/test_views_project_offlineevents.py`
- `tests/offlineevents/test_commands.py`

#### Test Files to Clean Up:
- `tests/notifications/test_emails.py`: Remove import and usage of `OfflineEvent`
- `meinberlin/apps/notifications/management/commands/send_test_emails.py`: Remove import

### 11. Management Commands

#### Commands to Delete:
- `meinberlin/apps/offlineevents/management/commands/create_offlineevent_system_actions.py`

### 12. Templates

#### Templates to Clean Up:
- `meinberlin/apps/projects/templates/meinberlin_projects/project_detail.html`:
  - Lines 33-36: Remove `{# Bestehende OfflineEvent-Objekte #}` loop

### 13. Admin

#### Areas to Clean Up:
- `meinberlin/apps/offlineevents/admin.py`: Remove `OfflineEvent` admin class

## Cleanup Order

1. **Clean up dashboard components** (`dashboard.py`)
2. **Remove views** (`views.py`)
3. **Clean up forms** (`forms.py`)
4. **Adjust phases** (`phases.py`)
5. **Remove models** (`models.py`)
6. **Clean up template tags** (`templatetags/offlineevent_tags.py`)
7. **Clean up project views** (`projects/views.py`)
8. **Delete/clean up templates**
9. **Clean up admin** (`admin.py`)
10. **Remove/adjust tests**
11. **Remove management commands**
12. **Clean up URL references**
13. **Run migration** (`0013_migrate_offlineevent_to_item.py`)

## Important Notes

- **Run migration first**: The migration `0013_migrate_offlineevent_to_item.py` should be executed before deleting `OfflineEvent` model references
- **Template tag replacement**: `offlineevents_and_modules_sorted()` can be replaced by direct module queries
- **Admin interface**: After migration, offline events are accessible through module management
