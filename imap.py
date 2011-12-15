#!/usr/bin/env python
# -*- coding: utf-8; -*-
# IMAP Testing Utility
# Copyright © 2011 Francesco Gigli <jaramir@gmail.com>

import imaplib
import argparse

# TODO: TLS
# TODO: list folders?

# parse args

parser = argparse.ArgumentParser( description = "IMAP Testing Utility" )
    
parser.add_argument( "username",   action="store",      help="Username" )
parser.add_argument( "password",   action="store",      help="Password" )
parser.add_argument( "server",     action="store",      help="IMAP Server Hostname or IP" )
parser.add_argument( "message",    action="store",      help="Message ID to read", default=None, nargs="?" )
parser.add_argument( "--folder",   action="store",      help="IMAP Folder to test (defualt: INBOX)" )
parser.add_argument( "--port",     action="store",      help="IMAP Server TCP Port (default: 143 or 993)" )
parser.add_argument( "--ssl",      action="store_true", help="Use SSL to encrypt the connection" )
parser.add_argument( "--cram-md5", action="store_true", help="Use CRAM-MD5 authentication" )

args = parser.parse_args()

# set debug level

imaplib.Debug = 4

# connect

if args.ssl:
    port = args.port if args.port else 993 
    imap = imaplib.IMAP4_SSL( args.server, port )
else:
    port = args.port if args.port else 143
    imap = imaplib.IMAP4( args.server, port )

# auth

if args.cram_md5:
    imap.login_cram_md5( args.username, args.password )
else:
    imap.login( args.username, args.password )

# test

folder = args.folder if args.folder else "INBOX"
imap.select( folder )

if args.message:
    typ, data = imap.fetch( args.message, '(RFC822)' )
    print typ
    print data[0][0]
    print data[0][1] 
else:
    typ, data = imap.search( None, "ALL" )
    print " ".join( data )

imap.close()
imap.logout()

