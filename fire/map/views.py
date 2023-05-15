from django.shortcuts import render, redirect
from django.contrib.gis.geos import Polygon
import json
from multiprocessing.connection import Client
from statistics import geometric_mean
from unittest import result
from .models import myProject
from . import mqtt

from signup.models import supervisor
from django.contrib.gis.geos import GEOSGeometry
from django.views.decorators.csrf import csrf_exempt

from django.http import JsonResponse
from django.contrib.gis.geos import Point
from .forms import *
import pyowm 
# from .mqtt import start_mqtt_client
from .status import result
import csv 
from .FWI import *
from datetime import datetime


def add_project(request,pseudo):
    supervisors = supervisor.objects.get(pseudo=pseudo)
    projects = myProject.objects.filter(supervisorp=supervisors)

    clients = client.objects.all()
    if request.method == 'POST':

        formulairep = Form_project(request.POST)
        # Get the other data from the form data
        nomp = request.POST.get('nomp')
        descp = request.POST.get('descp')
        debutp = request.POST.get('debutp')
        finp = request.POST.get('finp')
        cityp = request.POST.get('cityp')
        piece_joinde =request.POST.get('piece_joinde')


        if formulairep.is_valid():
            # Get the selected client from the form
            selected_client_id = request.POST.get('clientp')

            # Get the client object based on the selected ID
            
                 
            formulairep.enregistrerProj()

            # multiPolygone= request.POST.get('points')
            # multiPolygone_dict = json.loads(multiPolygone)
            
            # ,geomp=multipolygon///print(multiPolygone)
            # multipolygon = GEOSGeometry(multiPolygone, srid=4326)
            if selected_client_id:
                selected_client = client.objects.get(id=selected_client_id)

                instance = myProject(nomp=nomp,descp=descp,debutp=debutp,finp=finp,cityp=cityp,clientp=selected_client,supervisorp=supervisors,piece_joinde=piece_joinde)
                instance.save()
                return redirect('add_polygones',pseudo=pseudo,id=instance.polygon_id)
            else:
                instance = myProject(nomp=nomp,descp=descp,debutp=debutp,finp=finp,cityp=cityp,supervisorp=supervisors,piece_joinde=piece_joinde)
                instance.save()                
                return redirect('add_client',pseudo=pseudo,idd=instance.polygon_id)
            
            # polygons = []

            # for polygon_coords in multiPolygone_dict['coordinates']:
            #     print('-----------')
            #     for i in range(len(polygon_coords)): 
            #         poly_str = 'POLYGON(({0}))'.format(','.join([' '.join(map(str, c)) for c in polygon_coords[i]]))
            #         print('poly_str',poly_str)
            #         polygon = GEOSGeometry(poly_str, srid=4326)
            #         parcelle_obj = parcelle(poly=polygon,project=instance)
            #         # parcelle_obj.project = instance  # set the project attribute of the parcelle
            #         parcelle_obj.save()
            #         polygons.append(polygon)
                              
            # return redirect('add_client',id=instance.polygon_id)
            
        return render(request, 'addproj.html', {'form': formulairep,'projects':projects,'supervisor':supervisors})
    return render(request, 'addproj.html', {'form': Form_project(),'projects':projects,'supervisor':supervisors})







def add_polygones(request,pseudo,id):
    superviseur = supervisor.objects.get(pseudo=pseudo)
    projects = myProject.objects.filter(supervisorp=superviseur)
        
    project = myProject.objects.get(polygon_id=id)   
    if request.method == 'POST':

        multiPolygone= request.POST.get('points')
        multiPolygone_dict = json.loads(multiPolygone)
        multipolygon = GEOSGeometry(multiPolygone, srid=4326)

        # geometry = myProject(geomp=multipolygon)
        # geometry.save()

        project.geomp = multipolygon
        project.save()         
        
        polygons = []

        for polygon_coords in multiPolygone_dict['coordinates']:
            print('-----------')
            for i in range(len(polygon_coords)): 
                poly_str = 'POLYGON(({0}))'.format(','.join([' '.join(map(str, c)) for c in polygon_coords[i]]))
                print('poly_str',poly_str)
                polygon = GEOSGeometry(poly_str, srid=4326)
                parcelle_obj = parcelle(poly=polygon,project=project)
                    # parcelle_obj.project = instance  # set the project attribute of the parcelle
                parcelle_obj.save()
                polygons.append(polygon)       
                    
            # return redirect('add_client',id=instance.polygon_id)
        return redirect('addnode',pseudo=pseudo,id=project.polygon_id)
        
    return render(request, 'addpolyg.html', {'projects':projects,'supervisor':superviseur,'project':project})


def add_client(request,idd,pseudo):
        # project = myProject.objects.get(polygon_id=id)
        superviseur = supervisor.objects.get(pseudo=pseudo)
        projects = myProject.objects.filter(supervisorp=superviseur)
        print('----------',projects)
        project = myProject.objects.get(polygon_id=idd) 
        print('----------',project.polygon_id)
               
        if request.method == 'POST':
            formulaire = Form_client(request.POST)
            if formulaire.is_valid():
                
                formulaire.enregistrer(idd)
 
                return redirect('add_polygones',pseudo=pseudo,id=project.polygon_id)
            return render(request, 'addclient.html', {'form': formulaire,'supervisor':superviseur,'projects':projects,'project':project})
        return render(request, 'addclient.html', {'form': Form_client(),'supervisor':superviseur,'projects':projects,'project':project})


def display(request,pseudo):
    # projects = myProject.objects.all()
    # supervisors = supervisor.objects.get(pseudo=pseudo)
    
    supervisor_obj = supervisor.objects.get(pseudo=pseudo)
    projects = myProject.objects.filter(supervisorp=supervisor_obj)
    print("/////////", supervisor_obj.pseudo)
    print("/////projects////",projects )

    for proj in projects :
        print("/////proj////", proj)
        
    if request.method == 'POST':
    #     return redirect('project_1',pseudo)
        return redirect('add_project', pseudo=pseudo)

    return render(request, 'display.html', {'projects':projects,'supervisor_obj':supervisor_obj})
#-----------------------------------------------------------------------------

def display_polygone(request,id,pseudo):
    supervisor_obj = supervisor.objects.get(pseudo=pseudo)
    print("//supervisor_obj/", supervisor_obj)
    projects = myProject.objects.filter(supervisorp=supervisor_obj)
    project = myProject.objects.get(polygon_id=id)
    print("//project/", project.supervisorp)

    if request.method == 'POST':
        # id=instance.polygon_id

       
        return redirect('addnode',pseudo,id)
    return render(request, 'displaypoly.html', {'projects':projects,'project':project,'supervisor':supervisor_obj})


def add_node(request, id,pseudo):
    supervisor_obj = supervisor.objects.get(pseudo=pseudo)
    projects = myProject.objects.filter(supervisorp=supervisor_obj)
    project = myProject.objects.get(polygon_id=id)

    marker = node.objects.all()
    nodeq = node.objects.filter(polyg=project)
 
    if request.method == 'POST':
        node_name = request.POST.get('nom')
        Sensors = request.POST.get('Sensors') 
        reference = request.POST.get('reference') 
        range_str = request.POST.get('range')
        node_range = int(range_str) 
        mylatitude = request.POST.get('latitude') 
        mylongitude = request.POST.get('longitude') 
        point=Point(x=float(mylongitude),y=float(mylatitude))
        project_id = request.POST.get('polyg')
        namep = request.POST.get('parcelle')
       
        project_instance = myProject.objects.get(polygon_id=project_id)
        parcelles = parcelle.objects.filter(project=project_instance)
        list_p=[]
        for p in parcelles:
            list_p.append(p)
        print('----------------------',list_p)
        
        # parcelle_obj = parcelle.objects.filter(project=project_instance).first() # Retrieve the first parcelle object
        # print(parcelle_obj)
        # parcelle_obj.namep = namep # Update the namep attribute
        # parcelle_obj.save() # Save the changes to the database

                       

        instance = node(position=point,nom=node_name, polyg=project_instance,parc=list_p[node_range-1], latitude=mylatitude, longitude=mylongitude,reference=reference,node_range=node_range,Sensors=Sensors)
        instance.save()
        
        # parce=list_p[node_range-1]
        # parce.namep=namep
        # parce.save()

        new_data = Data(temperature=0, humidity=0, wind=0, node=instance)
        new_data.save()

        datas = Data.objects.filter(node=instance)
        print('hello')
        print(instance.nom)
        print(datas)
    

        return redirect('all',pseudo,id)

    return render(request, 'add_node.html', { 'projects': projects, 'project': project,'nodee':nodeq,'supervisor':supervisor_obj})
#--------------------------------------------------------------------

def start_mqtt(request,id):
    # Start the MQTT client
    # start_mqtt_client(id)
    # mqtt.client.loop_forever()
    
    # Return a simple response to indicate that the client has started
    #return HttpResponse('MQTT client started successfully.')
    return render(request, 'all.html', {})



def all_node(request,iid,pseudo):
    supervisor_obj = supervisor.objects.get(pseudo=pseudo)
    projects = myProject.objects.filter(supervisorp=supervisor_obj)
    my_project = myProject.objects.get(polygon_id=iid) 
    nodes = node.objects.filter(polyg=my_project).order_by('-Idnode')
     
    data_list = []
    for n in nodes :
        ds = Data.objects.filter(node=n).order_by('-IdData').first()
        data_list.append(
            ds,
        )
    print('---------data_list',data_list)

    for i in range(len(data_list)):
        ldn0 = data_list[i]
        #node = ldn0.node
        print('++++++++++++++++++ldn0',ldn0)

   
        temperature = ldn0.temperature
        humidity = ldn0.humidity
        wind_speed = ldn0.wind

        with open('testBatch.csv', mode='a', newline='') as file:
            writer = csv.writer(file)
            # writer.writerow([datetime.today().strftime('%m/%d/%Y'), temperature, humidity, wind_speed, '0'])

        batchFWI('testBatch.csv')



        with open('testBatch.csv', mode='r') as file:
            reader = csv.reader(file)
            rows = list(reader)
            for row in rows:
                print(row)
            if len(rows) > 0:
                last_row = rows[-1]
                FWI = last_row[-1]
            else:
                FWI = '0'

        fwi = float(FWI)
        print('heeeeeeeeeeeeeere',fwi)
        ldn0.node.FWI=fwi
        ldn0.node.save()
        resultatt= result(ldn0.node.Idnode)
        print (resultatt)
        ldn0.node.status=resultatt
        ldn0.node.save()  

    
    for data in data_list:
        print(data.node.FWI)
    
        lastd = data_list[0]
        
    
    if request.method == 'POST':
        return redirect('addnode',pseudo,iid)
        

    context = { 'projects':projects,'project':my_project,'nodee': nodes, 'ldn':data_list, 'lastd':lastd,'supervisor':supervisor_obj}
    return render(request, 'all.html',context)



def update_weather(request, id):
    # get updated weather information
    my_project = myProject.objects.get(polygon_id=id)

    # lasst node added
    nodes = node.objects.filter(polyg=my_project).order_by('-Idnode')
    onode = nodes[0]
    print('----onode',onode)
    
    datas = Data.objects.filter(node=onode).order_by('-IdData')
    # last data coming
    datao = datas.first()
    print('----datao',datao)
    ##################################################################""
    
    temperature = datao.temperature
    humidity = datao.humidity
    wind_speed = datao.wind

    with open('testBatch.csv', mode='a', newline='') as file:
            writer = csv.writer(file)
            # writer.writerow([datetime.today().strftime('%m/%d/%Y'), temperature, humidity, wind_speed, '0'])

    batchFWI('testBatch.csv')

    with open('testBatch.csv', mode='r') as file:
            reader = csv.reader(file)
            rows = list(reader)
            last_row = rows[-1]
            FWI = last_row[-1]

    fwi = float(FWI)
    onode.FWI=fwi
    onode.save()
    stat= result(onode.Idnode)
    print ('stattttt',stat)
    onode.status=stat
    onode.save() 
    
    node_status = onode.status
    node_fwi = onode.FWI
    node_rssi = onode.RSSI
    node_battery=onode.Battery_value
    node_name =onode.nom
    node_reference =onode.reference
   
############################################################################

    
    
    ldata =[]
    for n in nodes:
        dat= Data.objects.filter(node=n).order_by('-IdData').first()
        ldata.append( {
            
        'temperature': datao.temperature,
        'humidity': datao.humidity,
        'wind': datao.wind,
        'rain': datao.rain,
        'RSSI' : node_rssi,
        'battery' :node_battery,
        'reference' :node_reference,
        
        'fwi' : node_fwi,
        'status' : node_status,
        'node':node_name,
        }
            
        )
    

    dataa = {
        'temperature': datao.temperature,
        'humidity': datao.humidity,
        'wind': datao.wind,
        'rain': datao.rain,
        'RSSI' : node_rssi,
        'battery' :node_battery,
        'reference' :node_reference,
        
        'fwi' : node_fwi,
        'status' : node_status,
        'node':node_name,
        }
    print('fwi',dataa['fwi'])
    print('rssi',dataa['RSSI'])
    print('status',dataa['status'])

    print("dataaaaaa",dataa)
    

    # return a JsonResponse with the updated data
    return JsonResponse(dataa)
    # return JsonResponse({"datas": list(datas.values())})









def ALL(request,id,pseudo):
    supervisor_obj = supervisor.objects.get(pseudo=pseudo)
    projects = myProject.objects.filter(supervisorp=supervisor_obj)
    
    project = myProject.objects.get(polygon_id=id)
    nodes = node.objects.filter(polyg=project).order_by('-Idnode')
   
    onode = nodes[0] # =======node_instance// onlyy for the last one
    # print(onode) 

    datas = Data.objects.filter(node=onode).order_by('-IdData')
    data = datas.first()


    nodeq = node.objects.filter(polyg=project)
    nodes_data = []
    for node_instance in nodeq:
        datas = Data.objects.filter(node=node_instance).order_by('-IdData')
        data = datas.first()
        nodes_data.append({'node_instance': node_instance, 'data': data})
        
    data_list = []
    for n in nodes :
        ds = Data.objects.filter(node=n).order_by('-IdData').first()
        data_list.append(
            ds,
        )
    
    print('__________data_list',data_list)
           
    for i in range(len(data_list)):
        ldn0 = data_list[i]
        print(ldn0)
        print('______data_list node status',ldn0.node.status)
        
    # print('------nodes_data',nodes_data)
    context = {'nodes_data': nodes_data,'supervisor':supervisor_obj,'nodee': nodeq,'node':onode,'projects':projects, 'project': project,'parm':data,'ldn':data_list}
   

    return render(request, 'ALL_node.html',context )



def interface_c(request, id,pseudo):
    clientp = client.objects.get(pseudo=pseudo)
    projects = myProject.objects.filter(clientp=clientp)
    
    project = myProject.objects.get(clientp=clientp)
    proj = myProject.objects.get(polygon_id=id)
    nodes = node.objects.filter(polyg=project).order_by('-Idnode')
    
    data_list = []
    for n in nodes :
        ds = Data.objects.filter(node=n).order_by('-IdData').first()
        data_list.append(
            ds,
        )
           
    for i in range(len(data_list)):
        ldn0 = data_list[i]
        print(ldn0)
    
    
    for proj_instance in projects:
        print('namep',proj_instance.nomp)
        
    nodeq = node.objects.filter(polyg=proj_instance)
    for node_instance in nodeq:
        nom=node_instance.nom
        print(nom)


    nodes_data = []
    for node_instance in nodeq:
        datas = Data.objects.filter(node=node_instance).order_by('-IdData')
        data = datas.first()
        nodes_data.append({'node_instance': node_instance, 'data': data})
        print(data)

    context = {'ldn':data_list,'nodes_data': nodes_data,'nodee':nodeq,'clientp':clientp,'project': proj, 'pseudo': pseudo,'node_instance':node_instance}
    return render(request, 'interface_c.html', context)




def delete_project(request,pseudo,id):
    supervisor_obj = supervisor.objects.get(pseudo=pseudo)
    projects = myProject.objects.filter(supervisorp=supervisor_obj)
    
    project = myProject.objects.get(polygon_id=id)
    
    project.delete()
    return redirect('display',pseudo=supervisor_obj.pseudo)


from django.http import HttpResponse

def modify_1(request, pseudo, id):

    supervisors = supervisor.objects.get(pseudo=pseudo)
    projects = myProject.objects.filter(supervisorp=supervisors)
    project = myProject.objects.get(polygon_id=id)

    
    if request.method == 'POST':

        formulairep = Form_project(request.POST)
        # Get the other data from the form data
        new_name = request.POST.get('nomp')
        new_descp = request.POST.get('descp')
        new_debutp = request.POST.get('debutp')
        new_finp = request.POST.get('finp')
        new_cityp = request.POST.get('cityp')
        new_piece_joinde =request.POST.get('piece_joinde')


        if formulairep.is_valid():
            # Get the selected client from the form
            selected_client_id = request.POST.get('clientp')               
            formulairep.enregistrerProj()

            if selected_client_id:
                new_client = client.objects.get(id=selected_client_id)
                project.nomp=new_name
                project.descp=new_descp
                project.debutp=new_debutp
                project.finp=new_finp
                project.cityp=new_cityp
                project.clientp=new_client
                project.piece_joinde=new_piece_joinde
                project.save()
                return redirect('ALL_node',pseudo=pseudo,id=project.polygon_id)
            else:
                project.nomp=new_name
                project.descp=new_descp
                project.debutp=new_debutp
                project.finp=new_finp
                project.cityp=new_cityp
                project.piece_joinde=new_piece_joinde
                project.save()              
                return redirect('ALL_node',pseudo=pseudo,id=project.polygon_id)

            
        return render(request, 'modify_1.html', {'form': formulairep,'projects':projects,'supervisor':supervisors})
    return render(request, 'modify_1.html', {'form': Form_project(),'projects':projects,'supervisor':supervisors})



def modify_2(request, pseudo, id):
    supervisor_obj = supervisor.objects.get(pseudo=pseudo)
    projects = myProject.objects.filter(supervisorp=supervisor_obj)
    project = myProject.objects.get(polygon_id=id)
    nodes = node.objects.filter(polyg=project)
    
    for n in nodes:
        n.delete()
    
    project.geomp = ""
    project.save()

    return redirect('add_polygones', pseudo=supervisor_obj.pseudo,id=project.polygon_id)


def modify_3(request, pseudo, id):
    supervisor_obj = supervisor.objects.get(pseudo=pseudo)
    projects = myProject.objects.filter(supervisorp=supervisor_obj)
    project = myProject.objects.get(polygon_id=id)
    nodes = node.objects.filter(polyg=project)
    
    if request.method == 'POST':
        node_to_delete_name = request.POST.get('node_to_delete')
        node_to_delete = node.objects.get(nom=node_to_delete_name)
        node_to_delete.delete()
        return redirect('addnode', pseudo=supervisor_obj.pseudo, id=project.polygon_id)
        
  



    
        

    


        
 


