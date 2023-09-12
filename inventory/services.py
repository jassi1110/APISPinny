from inventory.models import Box
from django.db.models import Q
from datetime import datetime

def queryString(dict,status):
    query = Q()
    if 'minLength' in dict or 'maxLength' in dict:
        queryLength = Q()
        if 'minLength' in dict:
            queryLength &= Q(length__gte=dict['minLength'])
        
        if 'maxLength' in dict:
            queryLength &= Q(length__lte=dict['maxLength'])
        
        if 'minLength' in dict and 'maxLength' in dict and dict['minLength'] > dict['maxLength']:
            return None
        query &= queryLength

    if 'minBreadth' in dict or 'maxBreadth' in dict :
        queryLength = Q()
        if 'maxBreadth' in dict :
            query &= Q(breadth__lte=dict['maxBreadth'])

        if 'minBreadth'in dict :
            query &= Q(breadth__gte=dict['minBreadth'])
        
        if 'minBreadth' in dict and 'maxBreadth' in dict and dict['minBreadth'] > dict['maxBreadth']:
            return None
        query &= queryLength

    if 'minHeight' in dict or 'maxHeight'in dict :
        queryLength = Q()
        if 'minHeight' in dict :
            query &= Q(height__gte=dict['minHeight'])

        if 'maxHeight' in dict :
            query &= Q(height__lte=dict['maxHeight'])
        
        if 'minHeight' in dict and 'maxHeight' in dict and dict['minHeight'] > dict['maxHeight']:
            return None
        query &= queryLength

    if 'minArea' in dict or 'maxArea'in dict :
        queryLength = Q()
        if 'minArea'in dict :
            query &= Q(area__gte=dict['minArea'])

        if 'maxArea'in dict :
            query &= Q(area__lte=dict['maxArea'])
            
        if 'minArea' in dict and 'maxArea' in dict and dict['minArea'] > dict['maxArea']:
            return None
        query &= queryLength

    if 'minVolume' in dict or 'maxVolume'in dict :
        queryLength = Q()
        if 'minVolume' in dict:
            query &= Q(area__gte=dict['minVolume'])

        if 'maxVolume' in dict:
            query &= Q(area__lte=dict['maxVolume'])

        if 'minVolume' in dict and 'maxVolume' in dict and dict['minVolume'] > dict['maxVolume']:
            return None
        query &= queryLength

    if status:
        if 'startDate' in dict or 'endDate'in dict :
            queryLength = Q()
            if 'startDate' in dict:
                startDate = datetime.strptime(dict['startDate'], '%d/%m/%y')
                query &= Q(created_at__gte=startDate)

            if 'endDate' in dict:
                endDate = datetime.strptime(dict['endDate'], '%d/%m/%y')
                query &= Q(created_at__lte=endDate)
            query &= queryLength

            if 'startDate' in dict and 'endDate' in dict and startDate > endDate:
                return None
        if 'createdBy' in dict:
            query &= Q(created_by=dict['createdBy'])

    return query
