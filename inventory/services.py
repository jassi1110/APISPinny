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
        
        # if 'minLength' in dict and 'maxLength' in dict and dict['minLength'] > dict['maxLength']:
        #     return None,True

    if 'minBreadth' in dict or 'maxBreadth' in dict :
        queryLength = Q()
        # if dict('minBreadth') is not None and dict.get('maxBreadth') is not None and dict['minBreadth'] > dict['maxBreadth']:
        #     return None,True
        
        if 'maxBreadth' in dict :
            queryLength &= Q(breadth__lte=dict['maxBreadth'])

        if 'minBreadth'in dict :
            queryLength &= Q(breadth__gte=dict['minBreadth'])
        query |= queryLength

    if 'minHeight' in dict or 'maxHeight'in dict :
        queryLength = Q()
        if 'minHeight' in dict :
            queryLength &= Q(height__gte=dict['minHeight'])

        if 'maxHeight' in dict :
            queryLength &= Q(height__lte=dict['maxHeight'])
        
        # if 'minHeight' in dict and 'maxHeight' in dict and dict['minHeight'] > dict['maxHeight']:
        #     return None,True
        query |= queryLength

    if 'minArea' in dict or 'maxArea'in dict :
        queryLength = Q()
        if 'minArea'in dict :
            queryLength &= Q(area__gte=dict['minArea'])

        if 'maxArea'in dict :
            queryLength &= Q(area__lte=dict['maxArea'])
            
        # if 'minArea' in dict and 'maxArea' in dict and dict['minArea'] > dict['maxArea']:
        #     return None,True
        query |= queryLength

    if 'minVolume' in dict or 'maxVolume'in dict :
        queryLength = Q()

        # if 'minVolume' in dict and 'maxVolume' in dict and dict['minVolume'] > dict['maxVolume']:
        #     return None,True
        if 'minVolume' in dict:
            queryLength &= Q(area__gte=dict['minVolume'])

        if 'maxVolume' in dict:
            queryLength &= Q(area__lte=dict['maxVolume'])
        
        query |= queryLength

    if status:
        if 'startDate' in dict or 'endDate'in dict :
            queryLength = Q()
            if 'startDate' in dict:
                startDate = datetime.strptime(dict['startDate'], '%d/%m/%y')
                queryLength &= Q(created_at__gte=startDate)

            if 'endDate' in dict:
                endDate = datetime.strptime(dict['endDate'], '%d/%m/%y')
                queryLength &= Q(created_at__lte=endDate)
            query |= queryLength

            # if 'startDate' in dict and 'endDate' in dict and startDate > endDate:
            #     return None,True
            
        if 'createdBy' in dict:
            query |= Q(created_by=dict['createdBy'])

    if query:
        return query,True
    else:
        return None,False
