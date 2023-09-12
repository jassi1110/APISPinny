from inventory.models import Box
from django.db.models import Q

def queryString(dict):
    query = Q()
    if 'minLength' in dict or 'maxLength' in dict:
        queryLength = Q()
        if 'minLength' in dict:
            queryLength |= Q(length__gte=dict['minLength'])
        
        if 'maxLength' in dict:
            queryLength |= Q(length__lte=dict['maxLength'])
        
        query &= queryLength

    if 'minBreadth' in dict or 'maxBreadth' in dict :
        queryLength = Q()
        if 'maxBreadth' in dict :
            query |= Q(breadth__lte=dict['maxBreadth'])

        if 'minBreadth'in dict :
            query |= Q(breadth__gte=dict['minBreadth'])
        
        query &= queryLength

    if 'minHeight' in dict or 'maxHeight'in dict :
        queryLength = Q()
        if dict['minHeight'] in dict :
            query |= Q(height__gte=dict['minHeight'])

        if dict['maxHeight'] in dict :
            query |= Q(height__lte=dict['maxHeight'])
        
        query &= queryLength

    if 'minArea' in dict or 'maxArea'in dict :
        queryLength = Q()
        if 'minArea'in dict :
            query |= Q(area__gte=dict['minArea'])

        if 'maxArea'in dict :
            query |= Q(area__lte=dict['maxArea'])
        query &= queryLength

    if 'minVolume' in dict or 'maxVolume'in dict :
        queryLength = Q()
        if dict['minVolume'] in dict:
            query |= Q(area__gte=dict['minVolume'])

        if dict['maxVolume'] in dict:
            query |= Q(area__lte=dict['maxVolume'])
        query &= queryLength

    if 'userId' not in dict:
        if 'startDate' in dict or 'endDate'in dict :
            queryLength = Q()
            if dict['startDate'] in dict:
                query |= Q(created_at__gte=dict['startDate'])

            if dict['endDate'] in dict:
                query |= Q(created_at__lte=dict['endDate'])
            query &= queryLength

        if 'createdBy' in dict:
            query &= Q(created_by=dict['createdBy'])

    return query
