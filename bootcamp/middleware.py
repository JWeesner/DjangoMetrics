import os, sys, psutil, gc, uuid, __builtin__
from datetime import datetime
from types import StringType
from wsgiref.util import is_hop_by_hop
from wsgiref.handlers import BaseHandler

str_count = 0

class NewString(str):
    def __new__(cls, content):
        global str_count
        str_count += 1
        return super(NewString, cls).__new__(cls, content)

class DjangoMetrics(object):
    def __init__(self, get_response):
        #need to override WSGI response handler
        #original verison has assert failure due to new string type
        #BaseHandler.start_response = start_resp
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        global str_count
        str_count = 0
        #save the original string implementation to be reset later
        tmpStr = __builtin__.str
        #default all strings to our new string type to keep count
        __builtin__.str = NewString
        #mem = psutil.virtual_memory().used
        time = datetime.now().microsecond
        process = psutil.Process(os.getpid())
        rss_mem = process.memory_full_info().rss
        vms_mem = process.memory_full_info().vms
        uss_mem = process.memory_full_info().uss

        response = self.get_response(request)

        #print (request.path)
        response.uuid = str(uuid.uuid4())

        #reset string back to default string implementation
        __builtin__.str = tmpStr

        req_time = datetime.now().microsecond - time
        req_rss_mem = process.memory_full_info().rss - rss_mem
        req_vms_mem = process.memory_full_info().vms - vms_mem
        req_uss_mem = process.memory_full_info().uss -uss_mem
        #print type(request.build_absolute_uri())
        log_metrics(request, str_count, req_time, req_rss_mem, req_vms_mem, req_uss_mem)
        log_request(request)
        return response

def log_metrics(request, strings_made, time_used, rss_mem_used, vms_mem_used, uss_mem_used):
    time_used = time_used/1000000.0
    print "Page load took " , time_used , "seconds, " ,rss_mem_used ,"bytes of rss memory, " , vms_mem_used , "bytes of vms memory, " , uss_mem_used , " bytes of uss memory and created " , strings_made , "strings."
    file_name = 'metrics.log'
    if os.path.exists(file_name):
        request_file = open(file_name, "a")
    else:
        request_file = open(file_name, "w+")
    request_file.write(request.path + "," + str(time_used) + "," + str(uss_mem_used) + "," + str(strings_made) + "\n")
    return

def log_request(request):
    file_name = 'requests.log'
    if os.path.exists(file_name):
        request_file = open(file_name, "a")
    else:
        request_file = open(file_name, "w+")
    request_file.write(request.build_absolute_uri() + "\t" + str(uuid.uuid4()) + "\n")
    return


def start_resp(self, status, headers,exc_info=None):
    """'start_response()' callable as specified by PEP 333"""
    if exc_info:
        try:
            if self.headers_sent:
                # Re-raise original exception if headers sent
                raise exc_info[0], exc_info[1], exc_info[2]
        finally:
            exc_info = None        # avoid dangling circular ref
    elif self.headers is not None:
        raise AssertionError("Headers already set!")

    assert type(status) is StringType,"Status must be a string"
    assert len(status)>=4,"Status must be at least 4 characters"
    assert int(status[:3]),"Status message must begin w/3-digit code"
    assert status[3]==" ", "Status message must have a space after code"
    # if __debug__:
    #     for name,val in headers:
    #         #updated asserts to allow traditional string or new implementation
    #         assert isinstance(name, (StringType, NewString)),"Header names must be strings"
    #         assert isinstance(val, (StringType, NewString)),"Header values must be strings"
    #         assert not is_hop_by_hop(name),"Hop-by-hop headers not allowed"
    self.status = status
    self.headers = self.headers_class(headers)
    return self.write