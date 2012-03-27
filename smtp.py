#!/usr/bin/env python
# -*- coding: utf-8; -*-
# SMTP Testing Utility
# Copyright © 2011 Francesco Gigli <jaramir@gmail.com>

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
import email.utils
import argparse

GTUBE = "XJS*C4JDBQADN1.NSBN3*2IDNEN*GTUBE-STANDARD-ANTI-UBE-TEST-EMAIL*C.34X"
EICAR = "X5O!P%@AP[4\PZX54(P^)7CC)7}$EICAR-STANDARD-ANTIVIRUS-TEST-FILE!$H+H*"

# parse args

parser = argparse.ArgumentParser( description = "SMTP Testing Utility" )

argdef = (
    ( "from_addr", {
        "action": "store",
        "help": "Email FROM Address",
    } ),
    ( "rcpt_addr", {
        "action": "store",
        "help": "Email RCPT Address",
    } ),
    ( "server", {
        "action": "store",
        "help": "SMTP Server Hostname or IP",
    } ),
    ( "port", {
        "action": "store",
        "default": 25,
        "type": int,
        "nargs": "?",
        "help": "SMTP Server TCP Port",
    } ),
    ( "--gtube", {
        "action": "store_true",
        "help": "Send GTUBE AntiSpam Test",
    } ),
    ( "--eicar", {
        "action": "store_true",
        "help": "Send EICAR AntiVirus Test",
    } ),
    ( "--tls", {
        "action": "store_true",
        "help": "Use TLS to encrypt traffic",
    } ),
    ( "--ssl", {
        "action": "store_true",
        "help": "Use SSL to encrypt the connection",
    } ),
    ( "--auth", {
        "action": "store",
        "default": False,
        "nargs": 2,
        "metavar": ( "USERNAME", "PASSWORD" ),
        "help": "Use SMTP AUTH with provided credentials",
    } ),
    ( "--subject", {
        "action": "store",
        "default": "Test message",
        "help": "Email Subject",
    } ),
    ( "--text", {
        "action": "store",
        "default": "This is a test message",
        "help": "Email Text",
    } ),
    ( "--attachment", {
        "action": "store",
        "default": False,
        "type": int,
        "help": "Attach a binary file of the specified size in bytes",
    } ),
    )

for arg in argdef:
    parser.add_argument( arg[0], **arg[1] )

args = parser.parse_args()

# compose message

msg = MIMEMultipart()
msg["Subject"] = args.subject
msg["From"] = args.from_addr
msg["To"] = args.rcpt_addr
msg["Date"] = email.utils.formatdate()

msg.attach( MIMEText( args.text ) )

if args.gtube:
    msg.attach( MIMEText( GTUBE ) )

if args.eicar:
    msg.attach( MIMEText( EICAR ) )

if args.attachment:
    with open( "/dev/urandom" ) as rnd:
        attachment = MIMEApplication( rnd.read( args.attachment ) )
    attachment.add_header( "content-disposition", "attachment", filename="attach.bin" )
    msg.attach( attachment )

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
