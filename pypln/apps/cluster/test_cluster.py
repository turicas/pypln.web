# -*- coding: utf-8 -*-
u"""
Testing module for cmanager.py

license: GPL v3 or later
"""
__docformat__ = "restructuredtext en"

import unittest
from cmanager import Manager, get_ipv4_address
from slavedriver import SlaveDriver
import subprocess
import ConfigParser
import zmq
import time
import os,signal
from pypln.testing import zmqtesting

class TestManagerComm(unittest.TestCase):
    def setUp(self):
        self.config = ConfigParser.ConfigParser()
        self.config.read('pypln.test.conf')
        localip = get_ipv4_address().strip()
#        print "local ip: ",localip
        replyport = int(self.config.get('manager','replyport'))
        statusport = int(self.config.get('manager','statusport'))
#        print "==> ",statusport
        self.managerproc = subprocess.Popen(['./cmanager.py', '-c','pypln.test.conf','--nosetup'])
        self.sdproc = subprocess.Popen(['./slavedriver.py','tcp://%s:%s'%(localip,self.config.get('manager','conf_reply'))])
        self.context = zmq.Context()
        self.req_sock = zmqtesting.make_sock(context=self.context, sock_type=zmq.REQ, connect=(localip, replyport))
        self.status_sock = zmqtesting.make_sock(context=self.context, sock_type=zmq.REQ, connect=(localip, statusport))
#        self.status_sock = self.context.socket(zmq.SUB)
#        self.status_sock.connect('tcp://%s:%s'%(localip,statusport))
        self.pull_from_streamer_sock = zmqtesting.make_sock(context=self.context, sock_type=zmq.PULL, connect=(localip, 5571))
    def tearDown(self):
        self.req_sock.close()
        self.status_sock.close()
        self.pull_from_streamer_sock.close()
        os.kill(self.managerproc.pid,signal.SIGINT)
        os.kill(self.sdproc.pid,signal.SIGINT)
        self.managerproc.terminate()
        self.sdproc.terminate()
        self.context.term()

    def test_manager_send_one_message(self):
        self.req_sock.send_json({'jobid':self.managerproc.pid})
        msg = self.req_sock.recv_json()
        self.assertEqual(msg['ans'],'Job queued')

    def testing_sending_many_messages(self):
        msgs = [{'jobid':i, 'data':'fksdjfhlaksf'} for i in range(10)]
        self.req_sock.send_json(msgs)
        msg = self.req_sock.recv_json()
        self.assertEqual(msg['ans'],'Job queued')
        #send again
        self.req_sock.send_json(msgs)
        msg = self.req_sock.recv_json()
        self.assertEqual(msg['ans'],'Job queued')

    def test_job_control(self):
        msgs = [{'jobid':i, 'data':'fksdjfhlaksf'} for i in range(10)]
        self.req_sock.send_json(msgs)
        msg = self.req_sock.recv_json()
        self.assertEqual(msg['ans'],'Job queued')
        print "trying to get status"
        self.status_sock.send("status")
        msg = self.status_sock.recv_json()
        self.assertTrue(msg.has_key('cluster'))
        self.assertTrue(msg.has_key('active jobs'))
        self.assertTrue(isinstance(msg['cluster'],dict))
        self.assertTrue(isinstance(msg['active jobs'],list))

    def test_streamer(self):
        self.req_sock.send_json({'jobid':self.managerproc.pid})
        self.req_sock.recv_json()
        msg = self.pull_from_streamer_sock.recv_json()
        self.assertTrue(msg.has_key('jobid'))



class TestManagerInst(unittest.TestCase):
    def test_load_config_file(self):
        M = Manager('pypln.test.conf',False)
        self.assertTrue(M.config.has_section('cluster'))
        self.assertTrue(M.config.has_section('zeromq'))
        self.assertTrue(M.config.has_section('authentication'))
        self.assertTrue(M.config.has_section('streamer'))
        self.assertTrue(M.config.has_section('slavedriver'))
        self.assertTrue(M.config.has_section('worker'))
        self.assertTrue(M.config.has_section('sink'))

    def test_bootstrap_cluster(self):
        M = Manager('pypln.test.conf',True)



class TestSlavedriverInst(unittest.TestCase):
    """
    tests related with Slavedriver class instantiation
    """
    def setUp(self):
        self.config = ConfigParser.ConfigParser()
        self.config.read('pypln.test.conf')
        self.managerproc = subprocess.Popen(['./cmanager.py', '-c','pypln.test.conf','--nosetup'])
        self.localip = get_ipv4_address().strip()

    def tearDown(self):
        os.kill(self.managerproc.pid,signal.SIGINT)
        self.managerproc.terminate()

    def test_fetch_conf(self):
        SD = SlaveDriver(self.localip+":"+self.config.get('manager','conf_reply'),False)
        self.assertTrue(isinstance(SD.localconf,dict))


if __name__ == '__main__':
    unittest.main()