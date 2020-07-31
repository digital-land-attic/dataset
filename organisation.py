
def get_organisation_boundary(organisations, _id):
    if organisations.get(_id) and not organisations.get(_id)['boundary'] == "":
        return organisations[_id]['boundary']
    return None
    #return [org for org in organisations if org['organisation'] == _id and org['boundary'] is not None]


def get_boundaries(organisations, ids):
    boundaries = []
    for _id in ids:
        if get_organisation_boundary(organisations, _id) is not None:
            boundaries.append(get_organisation_boundary(organisations, _id))
    return boundaries
