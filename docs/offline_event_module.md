# Event Module – Short Documentation

To enable the Offline Event module in meinBerlin, several changes were necessary:

## Key Changes

### Dashboard

#### Hide Standard Module Components
- Standard module components can now be hidden using:
  `ModulePhasesComponent.hide_for("OE")`, 
  `ModuleBasicComponent.hide_for("OE")`
  (These changes also affect A4)

#### Initial Module Components
- The first module component (the first form for editing a module) is now determined by weight (and is no longer default ModuleBasicComponent)

### Project View

Modules can be registered via `register_event_module("OE")` → `meinberlin/apps/dashboard/__init__.py`

#### Events Module List

They are then no longer displayed in the module list but instead in the event list directly below

#### Events Module Detail

- For the module detail view, a special template is used: `meinberlin_projects/module_offline_event_detail.html`
  (Additional context: `offline_event_item` and `project_events`)

### Templates
- New module detail template: `meinberlin/apps/projects/templates/meinberlin_projects/module_offline_event_detail.html`
- Detail page for individual events: `meinberlin/apps/offlineevents/templates/meinberlin_offlineevents/offlineevent_detail.html`
