#!/usr/bin/env python
# -*- coding: utf-8; -*-
# SMTP Testing Utility
# Copyright © 2011 Francesco Gigli <jaramir@gmail.com>

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import email.utils
import argparse

# parse args

parser = argparse.ArgumentParser( description = "SMTP Testing Utility" )
    
parser.add_argument( "from_addr", action="store",      help="Email FROM Address" )
parser.add_argument( "rcpt_addr", action="store",      help="Email RCPT Address" )
parser.add_argument( "server",    action="store",      help="SMTP Server Hostname or IP" )
parser.add_argument( "port",      action="store",      help="SMTP Server TCP Port", default=25, nargs="?" )
parser.add_argument( "--gtube",   action="store_true", help="Send GTUBE AntiSpam Test" )
parser.add_argument( "--eicar",   action="store_true", help="Send EICAR AntiVirus Test" )
parser.add_argument( "--tls",     action="store_true", help="Use TLS to encrypt traffic" )
parser.add_argument( "--ssl",     action="store_true", help="Use SSL to encrypt the connection" )
parser.add_argument( "--auth",    action="store",      help="Use SMTP AUTH with provided credentials",
                                                                                    default=False, nargs=2, metavar=( "USERNAME", "PASSWORD" ) )
parser.add_argument( "--subject", action="store",      help="Email Subject",        default="Test message" )
parser.add_argument( "--text",    action="store",      help="Email Text",           default="This is a test message" )

args = parser.parse_args()

# compose message

msg = MIMEMultipart()
msg["Subject"] = args.subject
msg["From"] = args.from_addr
msg["To"] = args.rcpt_addr
msg["Date"] = email.utils.formatdate()

msg.attach( MIMEText( args.text ) )

if args.gtube:
    msg.attach( MIMEText( "XJS*C4JDBQADN1.NSBN3*2IDNEN*GTUBE-STANDARD-ANTI-UBE-TEST-EMAIL*C.34X" ) )

if args.eicar:
    msg.attach( MIMEText( "X5O!P%@AP[4\PZX54(P^)7CC)7}$EICAR-STANDARD-ANTIVIRUS-TEST-FILE!$H+H*" ) )

# connect and send

if args.ssl:
    smtp = smtplib.SMTP_SSL( args.server, args.port )
else:
    smtp = smtplib.SMTP( args.server, args.port )

smtp.set_debuglevel( True )

if args.tls:
    smtp.starttls()

if args.auth:
    username, password = args.auth
    smtp.login( username, password )

smtp.sendmail( args.from_addr, args.rcpt_addr, msg.as_string() )
smtp.quit()
