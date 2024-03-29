from adhocracy4.dashboard import ProjectDashboard
from adhocracy4.dashboard import components


class TypedProjectDashboard(ProjectDashboard):
    def __init__(self, project):
        if project.project_type == "meinberlin_bplan.Bplan":
            project = project.externalproject.bplan
        elif project.project_type == "meinberlin_extprojects.ExternalProject":
            project = project.externalproject
        super().__init__(project)

    def get_project_components(self):
        if self.project.project_type == "meinberlin_bplan.Bplan":
            return [
                components.projects.get("bplan"),
                components.projects.get("plans"),
                components.projects.get("adminlog"),
            ]
        elif self.project.project_type == "meinberlin_extprojects.ExternalProject":
            return [
                components.projects.get("external"),
                components.projects.get("topics"),
                components.projects.get("point"),
                components.projects.get("plans"),
                components.projects.get("adminlog"),
            ]
        return [
            component
            for component in components.get_project_components()
            if component.is_effective(self.project)
        ]

    def get_module_components(self):
        if self.project.project_type == "meinberlin_bplan.Bplan":
            return []
        elif self.project.project_type == "meinberlin_extprojects.ExternalProject":
            return []

        return components.get_module_components()
