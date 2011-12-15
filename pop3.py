#!/usr/bin/env python
# -*- coding: utf-8; -*-
# POP3 Testing Utility
# Copyright © 2011 Francesco Gigli <jaramir@gmail.com>

import poplib
import argparse

# parse args

parser = argparse.ArgumentParser( description = "POP3 Testing Utility" )
    
parser.add_argument( "username",   action="store",      help="Username" )
parser.add_argument( "password",   action="store",      help="Password" )
parser.add_argument( "server",     action="store",      help="POP3 Server Hostname or IP" )
parser.add_argument( "message",    action="store",      help="Message ID to read", default=None, nargs="?" )
parser.add_argument( "--port",     action="store",      help="POP3 Server TCP Port (default: 110 or 995)" )
parser.add_argument( "--ssl",      action="store_true", help="Use SSL to encrypt the connection" )
parser.add_argument( "--apop",     action="store_true", help="Use APOP authentication" )

args = parser.parse_args()

# connect

if args.ssl:
    port = args.port if args.port else 995 
    pop3 = poplib.POP3_SSL( args.server, port )
else:
    port = args.port if args.port else 110
    pop3 = poplib.POP3( args.server, port )
    
print pop3.getwelcome()

# set debug level

pop3.set_debuglevel( 2 )

# auth

if args.apop:
    pop3.apop( args.username, args.password )
else:
    pop3.user( args.username )
    pop3.pass_( args.password )
    
# test

if args.message:
    data = pop3.retr( args.message )
    print data[0]
    print "\n".join( data[1] )
    print data[2]
else:
    print pop3.list()[0]

pop3.quit()

