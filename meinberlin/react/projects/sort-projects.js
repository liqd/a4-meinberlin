export default function sortProjects (item1, item2) {
  const item1Type = (item1.subtype === 'default' || item1.subtype === 'external') ? 'project' : item1.subtype
  const item2Type = (item2.subtype === 'default' || item2.subtype === 'external') ? 'project' : item2.subtype

  const sortByPhase = (phase1, phase2, earliestFirst) => {
    if (phase1 && phase2) {
      const date1 = Date.parse(phase1)
      const date2 = Date.parse(phase2)
      if (earliestFirst) {
        return date1 <= date2 ? -1 : 1
      } else {
        return date1 >= date2 ? -1 : 1
      }
    }
    if (phase1 || phase2) {
      return phase1 ? -1 : 1
    }
    return false
  }

  if (item1Type === item2Type) {
    /* show
       1. projects with active phase
       2. projects with future phase
       3. projects with past phase
       4. projects without phase (can happen for external ones) */
    if (item1Type === 'project') {
      const active = sortByPhase(item1.active_phase[2], item2.active_phase[2], true)
      if (active) {
        return active
      }
      const future = sortByPhase(item1.future_phase, item2.future_phase, true)
      if (future) {
        return future
      }
      const past = sortByPhase(item1.past_phase, item2.past_phase, false)
      if (past) {
        return past
      }
    } else {
      /* sort plans by modified */
      return (new Date(item1.created_or_modified) >= new Date(item2.created_or_modified)) ? -1 : 1
    }
  } else {
    /* show projects first, plans second */
    switch (item1Type) {
      case 'project':
        return -1
      case 'plan':
        return 1
    }
  }
}
