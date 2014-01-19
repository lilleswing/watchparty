site:
    / --> Create Group Page && intro
    /{groupname} does everything using backbone


ws goes on /api


group
    GET group/{group.name}
    GET group/{id}/selection
selection
    GET selection/{id}/Pick
    POST selection
category
    GET category/{id}
    GET category/{id}/nominee
event
    GET event/{id}/category
    GET event/{id}
pick
    TODO(Leswing) POST pick

Models without Endpoints:
    nominee
