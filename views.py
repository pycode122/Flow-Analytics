from django.shortcuts import render

# Create your views here.
from django.shortcuts import render_to_response
from django.template import RequestContext
from models import Post
from django.views.generic.edit import FormView
from mongoengine import *
from graphos.sources.mongo import MongoDBDataSource
from graphos.renderers import gchart
from graphos.views import FlotAsJson, RendererAsJson
import datetime
import time
from time import mktime
import json,ast
from bson import json_util
from bson.json_util import dumps
#import Date
from datetime import timedelta

def selection(request):

    posts=Post.objects.all()
    return render_to_response('selection.html', {'Posts': posts},context_instance=RequestContext(request))

def historical(request):
    post = Post.objects.all()
    if request.method == 'POST':
        srs_value= request.POST['srs_value']
        destn_value= request.POST['destn_value']
        src_port= request.POST['src_port']
        destn_port= request.POST['destn_port']
        st_date= request.POST['st_date']
        print(st_date)
        e_date= request.POST['e_date']
        protocol_str= request.POST['protocol_str']

        if (st_date and e_date):
            st_date = datetime.datetime.strptime(st_date,'%Y-%m-%dT%H:%M')
            e_date = datetime.datetime.strptime(e_date,'%Y-%m-%dT%H:%M')
            if (srs_value and destn_value):
                x="both src and destn ip values are given...its working"
                query=list(Post._get_collection().find({'start_date' : { '$gt':st_date} , 'end_date' : {'$lt' : e_date},'source_ip':srs_value,'destination_ip':destn_value }))
                counting_list = int(Post._get_collection().find({'start_date' : { '$gt':st_date} , 'end_date' : {'$lt' : e_date},'source_ip':srs_value,'destination_ip':destn_value }).count())
                query=dumps(query)
                query= json.loads(query)
                query = epoch_to_time(query,counting_list)
                query = protocol_decode(query,counting_list)
                template = 'historical.html'
                params = {'posts':post,'x':x,'query':query}
                return render_to_response(template,params,context_instance=RequestContext(request))

            elif (srs_value):
                y="only source ip is given"
                query=list(Post._get_collection().find({'start_date' : { '$gt':st_date} , 'end_date' : {'$lt' : e_date},'source_ip':srs_value }))
                counting_list = int(Post._get_collection().find({'start_date' : { '$gt':st_date} , 'end_date' : {'$lt' : e_date},'source_ip':srs_value }).count())
                query=dumps(query)
                query= json.loads(query)
                query = epoch_to_time(query,counting_list)
                query = protocol_decode(query,counting_list)
                template = 'historical.html'
                params = {'posts':post,'y':y,'query':query,'t':'tcp'}
                return render_to_response(template,params,context_instance=RequestContext(request))

            elif (destn_value):
                z= "destination ip is given"
                query=list(Post._get_collection().find({'start_date' : { '$gt':st_date} , 'end_date' : {'$lt' : e_date},'destination_ip':destn_value }))
                counting_list = int(Post._get_collection().find({'start_date' : { '$gt':st_date} , 'end_date' : {'$lt' : e_date},'destination_ip':destn_value }).count())
                query=dumps(query)
                query= json.loads(query)
                query = epoch_to_time(query,counting_list)
                query = protocol_decode(query,counting_list)
                template = 'historical.html'
                params = {'posts':post,'z':z,'query':query}
                return render_to_response(template,params,context_instance=RequestContext(request))


            elif (src_port and destn_port):
src_port = int(src_port)
                destn_port = int(destn_port)
                x="both src and destn port values are given...its working"
                query=list(Post._get_collection().find({'start_date' : { '$gt':st_date} , 'end_date' : {'$lt' : e_date},'source_port':src_port,'destination_port':destn_port }))
                counting_list = int(Post._get_collection().find({'start_date' : { '$gt':st_date} , 'end_date' : {'$lt' : e_date},'source_port':src_port,'destination_port':destn_port }).count())
                query=dumps(query)
                query= json.loads(query)
                query = epoch_to_time(query,counting_list)
                query = protocol_decode(query,counting_list)
                template = 'historical.html'
                params = {'posts':post,'x':x,'query':query}
                return render_to_response(template,params,context_instance=RequestContext(request))

            elif (src_port):
                src_port = int(src_port)
                y="only source port value is given"
                query=list(Post._get_collection().find({'start_date' : { '$gt':st_date} , 'end_date' : {'$lt' : e_date},'source_port':src_port }))
                counting_list = int(Post._get_collection().find({'start_date' : { '$gt':st_date} , 'end_date' : {'$lt' : e_date},'source_port':src_port }).count())
                query=dumps(query)
                query= json.loads(query)
                query = epoch_to_time(query,counting_list)
                query = protocol_decode(query,counting_list)
                template = 'historical.html'
                params = {'posts':post,'y':y,'query':query}
                return render_to_response(template,params,context_instance=RequestContext(request))

            elif (destn_port):
                destn_port = int(destn_port)
                z= "destination port value is given"
                query=list(Post._get_collection().find({'start_date' : { '$gt':st_date} , 'end_date' : {'$lt' : e_date},'destination_port':destn_port }))
                counting_list = int(Post._get_collection().find({'start_date' : { '$gt':st_date} , 'end_date' : {'$lt' : e_date},'destination_port':destn_port }).count())
                query=dumps(query)
                query= json.loads(query)
                query = epoch_to_time(query,counting_list)
                query = protocol_decode(query,counting_list)
                template = 'historical.html'
                params = {'posts':post,'z':z,'query':query}
                return render_to_response(template,params,context_instance=RequestContext(request))

            elif (protocol_str):
   z = 'only protocol with time'
                if(protocol_str == 'TCP'):
                    query=list(Post._get_collection().find({'start_date' : { '$gt':st_date} , 'end_date' : {'$lt' : e_date},'protocol' : 6 }))
                    print(query)
                    counting_list = int((Post._get_collection().find({'start_date' : { '$gt':st_date} , 'end_date' : {'$lt' : e_date},'protocol' : 6 })).count())
                elif(protocol_str == 'UDP'):
                    query=list(Post._get_collection().find({'start_date' : { '$gt':st_date} , 'end_date' : {'$lt' : e_date},'protocol' : 17 }))
                    counting_list = int((Post._get_collection().find({'start_date' : { '$gt':st_date} , 'end_date' : {'$lt' : e_date},'protocol' : 17 })).count())
                query=dumps(query)
                query= json.loads(query)
                query = epoch_to_time(query,counting_list)
                query = protocol_decode(query,counting_list)
                template = 'historical.html'
                params = {'posts':post,'z':z,'query':query}
                return render_to_response(template,params,context_instance=RequestContext(request))

            else:
                p ="only dates are given"
                query=list(Post._get_collection().find({'start_date' : { '$gt':st_date} , 'end_date' : {'$lt' : e_date} }))
                counting_list = int(Post._get_collection().find({'start_date' : { '$gt':st_date} , 'end_date' : {'$lt' : e_date} }).count())
                query=dumps(query)
                query= json.loads(query)
                query = epoch_to_time(query,counting_list)
                query = protocol_decode(query,counting_list)
                template = 'historical.html'
                params = {'posts':post,'p':p,'query':query}
                return render_to_response(template,params,context_instance=RequestContext(request))

        else:
            if (srs_value and destn_value):
                x="both src and destn ip values are given...its working and its without time"
                query=list(Post._get_collection().find({'source_ip':srs_value,'destination_ip':destn_value }))
                counting_list = int(Post._get_collection().find({'source_ip':srs_value,'destination_ip':destn_value }).count())
                query=dumps(query)
                query= json.loads(query)
                query = epoch_to_time(query,counting_list)
                query = protocol_decode(query,counting_list)
                template = 'historical.html'
                params = {'posts':post,'x':x,'query':query}
                return render_to_response(template,params,context_instance=RequestContext(request))

            elif (srs_value):
  y="only source ip is given without time"
                query=list(Post._get_collection().find({'source_ip':srs_value }))
                counting_list = int(Post._get_collection().find({'source_ip':srs_value }).count())
                query=dumps(query)
                query= json.loads(query)
                query = epoch_to_time(query,counting_list)
                query = protocol_decode(query,counting_list)
                template = 'historical.html'
                params = {'posts':post,'y':y,'query':query}
                return render_to_response(template,params,context_instance=RequestContext(request))

            elif (destn_value):
                z= "destination ip is given without time"
                query=list(Post._get_collection().find({'destination_ip':destn_value }))
                counting_list = int(Post._get_collection().find({'destination_ip':destn_value }).count())
                query=dumps(query)
                query= json.loads(query)
                query = epoch_to_time(query,counting_list)
                query = protocol_decode(query,counting_list)
                template = 'historical.html'
                params = {'posts':post,'z':z,'query':query}
                return render_to_response(template,params,context_instance=RequestContext(request))

            elif (src_port and destn_port):
                src_port = int(src_port)
                destn_port = int(destn_port)
                x="both src and destn port values are given...its working and its without time"
                query=list(Post._get_collection().find({'source_port':src_port,'destination_port':destn_port }))
                counting_list = int(Post._get_collection().find({'source_port':src_port,'destination_port':destn_port }).count())
                query=dumps(query)
                query= json.loads(query)
                query = epoch_to_time(query,counting_list)
                query = protocol_decode(query,counting_list)
                template = 'historical.html'
                params = {'posts':post,'x':x,'query':query}
                return render_to_response(template,params,context_instance=RequestContext(request))

            elif (src_port):
                src_port = int(src_port)
                y="only source port is given without time"
                query=list(Post._get_collection().find({'source_port':src_port }))
                print(type(src_port))
                counting_list = int(Post._get_collection().find({'source_port':src_port }).count())
  query=dumps(query)
                query= json.loads(query)
                query = epoch_to_time(query,counting_list)
                query = protocol_decode(query,counting_list)
                template = 'historical.html'
                params = {'posts':post,'y':y,'query':query}
                return render_to_response(template,params,context_instance=RequestContext(request))

            elif (destn_port):
                destn_port = int(destn_port)
                z= "destination port is given without time"
                query=list(Post._get_collection().find({'destination_port':destn_port }))
                counting_list = int(Post._get_collection().find({'destination_port':destn_port }).count())
                query=dumps(query)
                query= json.loads(query)
                query = epoch_to_time(query,counting_list)
                query = protocol_decode(query,counting_list)
                template = 'historical.html'
                params = {'posts':post,'z':z,'query':query}
                return render_to_response(template,params,context_instance=RequestContext(request))

            elif (protocol_str):
                z = 'only protocol without time'
                if(protocol_str == 'TCP'):
                    query=list(Post._get_collection().find({'protocol' : 6 }))
                    counting_list = int((Post._get_collection().find({'protocol' : 6 })).count())
                    query=dumps(query)
                    query= json.loads(query)
                    query = epoch_to_time(query,counting_list)
                    query = protocol_decode(query,counting_list)
                    template = 'historical.html'
                    params = {'posts':post,'z':z,'query':query}
                    return render_to_response(template,params,context_instance=RequestContext(request))



                elif(protocol_str == 'UDP'):
                    query=list(Post._get_collection().find({'protocol' : 17 }))
                    counting_list = int((Post._get_collection().find({'protocol' : 17 })).count())
                    query=dumps(query)
                    query= json.loads(query)
                    query = epoch_to_time(query,counting_list)
                    query = protocol_decode(query,counting_list)
template = 'historical.html'
                    params = {'posts':post,'z':z,'query':query}
                    return render_to_response(template,params,context_instance=RequestContext(request))


    elif request.method == 'GET':
        params = {'posts':post}
        template = 'historical.html'
        return render_to_response(template,params,context_instance=RequestContext(request))

#This mrthod converts UNIX epoch into human readable time

def epoch_to_time(query,counting_list):
    q = 0
    for q in range(counting_list):
        json3_data = query[q]
        req_time = json3_data['start_date']
        epoch_t = req_time['$date']
        s = epoch_t / 1000.0
        conv_time = datetime.datetime.fromtimestamp(s).strftime('%Y-%m-%d %H:%M:%S.%f')
        query[q]['start_date'] = conv_time
    return query

def protocol_decode(query,counting_list):
    q = 0
    for q in range(counting_list):
        json4_data = query[q]
        protocol_code = json4_data['protocol']
        if (protocol_code == 6):
            query[q]['protocol'] = 'TCP'
        elif (protocol_code == 17):
            query[q]['protocol'] = 'UDP'
    return query

def dashboard(request):
    '''p = datetime.datetime.now() - datetime.timedelta(minutes = 5)
    time_limit = p.isoformat("T")
    posts = Post.objects(start_date__gte=time_limit)
    print(len(list(posts)))
   '''
    posts = Post.objects.all()
  if request.method == 'GET':

        for post in posts:
            bandwidth =list(Post._get_collection().aggregate([{'$match':{'source_ip':post.source_ip,'destination_ip':post.destination_ip}}, {'$group' : {"_id" : "null" , "bandwidth" : { '$sum' : "$byte_size"}}} ]))
            bandwidth = dumps(bandwidth)
            json1_data = json.loads(bandwidth)[0]
            band = json1_data['bandwidth']
            post.bandwidth = long(band)
            post.save()
            s_date=list(Post._get_collection().aggregate( [ { '$match' : {'source_ip' : post.source_ip,'destination_ip' : post.destination_ip} } ,{'$project' : {'start_date':1}},{'$sort' : {'start_date' : 1}},{'$limit' : 1} ] ))
            n1 = s_date[0]
            a = n1['start_date']#start time of pps
            print(a.time())

            e_date = list(Post._get_collection().aggregate( [ { '$match' : {'source_ip' : post.source_ip,'destination_ip' : post.destination_ip} } ,{'$project' : {'end_date':1}},{'$sort' : {'end_date' : -1}},{'$limit' : 1} ] ))
            n = e_date[0]
            b = n['end_date']#end time of pps
            print("b is:")
            print(b.time())

            c = b-a
            print("c is:")
            print(c)
            print("total sec is:")
            req_sec = c.total_seconds()
            if(req_sec == 0):
                continue
            else:
                print(req_sec)

                # do difference operation for pps
                total_packets=list(Post._get_collection().aggregate([{'$match':{'source_ip':post.source_ip,'destination_ip':post.destination_ip}}, {'$group' : {"_id" : "null" , "packets" : { '$sum' : "$packet_size"}}} ]))
                p = total_packets[0]
                q = p['packets']
                pps = (q/req_sec)
                post.pps = pps
                post.save()
  for post in posts:
            bandwidth_port =list(Post._get_collection().aggregate([{'$match':{'source_port':post.source_port,'destination_port':post.destination_port}}, {'$group' : {"_id" : "null" , "bandwidth_port" : { '$sum' : "$byte_size"}}} ]))
            bandwidth_port = dumps(bandwidth_port)
            json1_port = json.loads(bandwidth_port)[0]
            band_port = json1_port['bandwidth_port']
            post.bandwidth_port = band_port
            post.save()
            s_date_port=list(Post._get_collection().aggregate( [ { '$match' : {'source_port' : post.source_port,'destination_port' : post.destination_port} } ,{'$project' : {'start_date':1}},{'$sort' : {'start_date' : 1}},{'$limit' : 1} ] ))
            n1_port = s_date_port[0]
            a_port = n1_port['start_date']#start time of pps

            e_date_port = list(Post._get_collection().aggregate( [ { '$match' : {'source_port' : post.source_port,'destination_port' : post.destination_port} } ,{'$project' : {'end_date':1}},{'$sort' : {'end_date' : -1}},{'$limit' : 1} ] ))
            n_port = e_date_port[0]
            b_port = n_port['end_date']#end time of pps

            c_port = b_port-a_port
            req_sec_port = c_port.total_seconds()
            if(req_sec_port == 0):
                continue
            else:
                print(req_sec_port)

            # do difference operation for pps
                total_packets_port=list(Post._get_collection().aggregate([{'$match':{'source_port':post.source_port,'destination_port':post.destination_port}}, {'$group' : {"_id" : "null" , "packets_port" : { '$sum' : "$packet_size"}}} ]))
                p_port = total_packets_port[0]
                q_port = p_port['packets_port']
                pps_port = (q_port/req_sec_port)
                post.pps_port = pps_port
                post.save()
        post_query = list(Post._get_collection().find())
        data_source = MongoDBDataSource(post_query,fields=['source_ip','byte_size'])
        print(type(data_source))
        chart_1 = gchart.LineChart(data_source)
  template='dashboard.html'
        params={'posts':Post.objects.all(),'chart_1':chart_1,'g':"Graph"}
        return render_to_response(template,params,context_instance=RequestContext(request))

    elif request.method == 'POST':

        post_query = list(Post._get_collection().find())
        selected_talkers= request.POST['top_talkers_for']

        if(selected_talkers == "talkers_bandwidth"):
            #dont delete the below one...it is for main project

            '''p = datetime.datetime.now() - datetime.timedelta(minutes = 5)
            time_limit = p.isoformat("T")
            query = list(Post._get_collection().aggregate( [ { '$match' : {'start_date': { '$gt' : time_limit} } },{'$sort' : {'bandwidth' : -1}},{'$limit' : 5} ] ))
            '''
            query = list(Post._get_collection().aggregate( [ {'$sort' : {'bandwidth' : -1}},{'$limit' : 5} ] ))
            query=dumps(query)
            query= json.loads(query)
            query = epoch_to_time(query,5)
            data_source = MongoDBDataSource(post_query,fields=['source_ip','byte_size'])
            chart_2 = gchart.LineChart(data_source)
            params = {'query_1':query,'chart_2':chart_2,'h':"Graph"}
            template = 'dashboard.html'
            return render_to_response(template,params,context_instance=RequestContext(request))


        elif (selected_talkers == "talkers_pps"):
            #dont delete the below one...it is for main project

            '''p = datetime.datetime.now() - datetime.timedelta(minutes = 5)
            time_limit = p.isoformat("T")
            query = list(Post._get_collection().aggregate( [ { '$match' : {'start_date': { '$gt' : time_limit} } },{'$sort' : {'bandwidth' : -1}},{'$limit' : 5} ] ))
            '''
            query = list(Post._get_collection().aggregate( [ {'$sort' : {'pps' : -1}},{'$limit' : 5} ] ))
            query=dumps(query)
            query= json.loads(query)
            query = epoch_to_time(query,5)

            data_source = MongoDBDataSource(post_query,fields=['source_ip','byte_size'])
            chart_2 = gchart.LineChart(data_source)
            params = {'query_2':query,'chart_2':chart_2,'h':"Graph"}
            template = 'dashboard.html'
return render_to_response(template,params,context_instance=RequestContext(request))


        elif(selected_talkers == "ports_bandwidth"):
            #dont delete the below one...it is for main project

            '''p = datetime.datetime.now() - datetime.timedelta(minutes = 5)
            time_limit = p.isoformat("T")
            query = list(Post._get_collection().aggregate( [ { '$match' : {'start_date': { '$gt' : time_limit} } },{'$sort' : {'bandwidth_port' : -1}},{'$limit' : 5} ] ))
            '''
            query = list(Post._get_collection().aggregate( [ {'$sort' : {'bandwidth_port' : -1}},{'$limit' : 5} ] ))
            query=dumps(query)
            query= json.loads(query)
            query = epoch_to_time(query,5)
            #post_query = list(Post._get_collection().find())
            data_source = MongoDBDataSource(post_query,fields=['source_ip','byte_size'])
            chart_2 = gchart.LineChart(data_source)
            params = {'query_3':query,'chart_2':chart_2,'h':"Graph"}
            template = 'dashboard.html'
            return render_to_response(template,params,context_instance=RequestContext(request))


        elif (selected_talkers == "ports_pps"):
            #dont delete the below one...it is for main project
            '''
            p = datetime.datetime.now() - datetime.timedelta(minutes = 5)
            time_limit = p.isoformat("T")
            query = list(Post._get_collection().aggregate( [ { '$match' : {'start_date': { '$gt' : time_limit} } },{'$sort' : {'pps_port' : -1}},{'$limit' : 5} ] ))
            '''
            query = list(Post._get_collection().aggregate( [ {'$sort' : {'pps_port' : -1}},{'$limit' : 5} ] ))
            query=dumps(query)
            query= json.loads(query)
            query = epoch_to_time(query,5)


            data_source = MongoDBDataSource(post_query,fields=['source_ip','byte_size'])
            chart_2 = gchart.LineChart(data_source)
            params = {'query_4':query,'chart_2':chart_2,'h':"Graph"}
            template = 'dashboard.html'
            return render_to_response(template,params,context_instance=RequestContext(request))
