from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from .models import Map, Event

# Create your views here.

def listMaps(request):
    map_list = Map.objects.all()
    context = {'map_list': map_list}
    return render(request, 'eventmap/maplist.html', context)

def listEvents(request,mapid):
    if request.method == 'GET':
        event_list = Event.objects.filter(mapid__id=mapid)
        category = request.GET.get("category", None)
        text = request.GET.get("text", None)
        lattl = request.GET.get("lattl", None)
        lontl = request.GET.get("lontl", None)
        latbr = request.GET.get("latbr", None)
        lonbr = request.GET.get("lonbr", None)
        if category:
            event_list = event_list.filter(catlist__contains=category)
        if text:
            event_list = event_list.filter(title__contains=text) | event_list.filter(desc__contains=text)
        if lattl:
            event_list = event_list.filter(lat__gte=latbr, lat__lte=lattl, lon__gte=lontl, lon__lte=lonbr)
        
        context = {'event_list': event_list, 'mapid':mapid}  # Inserted mapid here for inserting event 
        return render(request,'eventmap/eventlist.html',context)
    else: # request.method == 'POST'
        if request.POST.get('eventToBeDeleted') != None:
            eventToDelete = Event.objects.get( id =  request.POST.get('eventToBeDeleted'))
            eventToDelete.delete()
            event_list = Event.objects.filter(mapid__id=mapid)
            context = {'event_list': event_list, 'mapid':mapid}  # Inserted mapid here for inserting event 
            return render(request,'eventmap/eventlist.html',context)
        if request.POST.get('eventToBeUpdated') != None:
            eventToUpdate = Event.objects.get( id =  request.POST.get('eventToBeUpdated'))
            context = {'event': eventToUpdate,'mapid':mapid}   # SENDING EVENT SO THAT INPUT FIELDS WILL NOT BE EMPTY
            return render(request,'eventmap/updateEvent.html',context)
        else:  # WHEN THE USER POST DATA(PUSH THE UPDATE EVENT BUTTON) FROM THE updateEvent.html THE USER COMES HERE
            return updateEvent(request,mapid)

def insertEvent(request,mapid):
    if request.method == 'GET':
        context = {'mapid': mapid}
        return render(request,'eventmap/insertEvent.html',context)
    if request.method == 'POST':
        lon = float(request.POST.get('lonfield',None))
        lat = float(request.POST.get('latfield',None))
        locname = request.POST.get('locnamefield',None) 
        title = request.POST.get('titlefield',None)
        desc = request.POST.get('descfield',None)
        catlist = request.POST.get('categoryfield',None) # ONLY GET 1 CATEGORY
        starttime = request.POST.get('starttimefield',None)
        endtime = request.POST.get('endtimefield',None)
        timetoann = request.POST.get('timetoannfield',None)
        ourMap = Map.objects.get(id=mapid)
        newEvent = Event(lon=lon,lat=lat,locname=locname,title=title,desc=desc,catlist=catlist,
            starttime=starttime,endtime=endtime,timetoann=timetoann,mapid=ourMap)
        newEvent.save()   #Insert event to database belonging to the map with id =  mapid
        event_list = Event.objects.filter(mapid__id=mapid)
        context = {'event_list': event_list, 'mapid':mapid}  # Inserted mapid here for inserting event 
        return HttpResponseRedirect("/eventmap/"+str(mapid) +"/")

def updateEvent(request,mapid):         # GET THE OBJECT AND UPDATE AND RETURN THE USER TO THE eventmap/{{mapid}}/  page
    event_id = int(request.POST.get('event_id',None))
    event = Event.objects.get(pk = event_id)    # PK: PRIMARY KEY
    event.lon = float(request.POST.get('lonfield',None))
    event.lat = float(request.POST.get('latfield',None))
    event.locname = request.POST.get('locnamefield',None) 
    event.title = request.POST.get('titlefield',None)
    event.desc = request.POST.get('descfield',None)
    event.catlist = request.POST.get('categoryfield',None) # ONLY GET 1 CATEGORY
    event.starttime = request.POST.get('starttimefield',None)
    event.endtime = request.POST.get('endtimefield',None)
    event.timetoann = request.POST.get('timetoannfield',None)
    event.save()   # SAVE THE CHANGES
    return HttpResponseRedirect("/eventmap/"+str(mapid) +"/")
