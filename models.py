from django.db import models

# Create your models here.
from mongoengine import *
from MyProject.settings import DBNAME
import datetime
connect(DBNAME)

class Post(Document):

    destination_ip=StringField(max_length=120, required=True)
    protocol=IntField(required=True)
    end_date=DateTimeField()
    source_port=IntField(min_value=None,max_value=None)
    destination_port=IntField(min_value=None,max_value=None)
    byte_size = LongField(required=True)
    source_ip=StringField(max_length=120, required=True)
    start_date=DateTimeField()
    packet_size=LongField(required=True)
    struct_time = DateTimeField()
    e_tm = DateTimeField()
    bandwidth = LongField()
    talkers_pps = StringField()
    talkers_bandwidth = StringField()
    pps = FloatField()
    struct_time = DateTimeField()
    graph_t = FloatField()
    bandwidth_port = LongField()
    pps_port = FloatField()
