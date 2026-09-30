#!/usr/bin/env python3
"""
send_brief_email.py — Dispatches Frontier daily briefs via email to jgodgart@gmail.com
"""

import os
import sys
import json
import smtplib
import glob
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "..", "email_config.json")
BRIEFS_DIR = os.path.join(os.path.dirname(__file__), "..", "briefs")

def load_config():
    config = {
        "recipient_email": "jgodgart@gmail.com",
        "provider": "gmail_smtp",
        "gmail_smtp": {"sender_email": "jgodgart@gmail.com", "app_password": ""}
    }
    if os.path.exists(CONFIG_PATH):
        try:
            with open(CONFIG_PATH, "r") as f:
                loaded = json.load(f)
                config.update(loaded)
        except Exception as e:
            print(f"Error reading {CONFIG_PATH}: {e}")
            
    # Override with env vars if present
    if os.environ.get("EMAIL_SENDER"):
        config["gmail_smtp"]["sender_email"] = os.environ.get("EMAIL_SENDER")
    if os.environ.get("EMAIL_APP_PASSWORD"):
        config["gmail_smtp"]["app_password"] = os.environ.get("EMAIL_APP_PASSWORD")
        
    return config

def get_latest_brief():
    html_files = sorted(glob.glob(os.path.join(BRIEFS_DIR, "*.html")), key=os.path.getmtime, reverse=True)
    if html_files:
        return html_files[0]
    return None

import re
from email.mime.image import MIMEImage

def send_via_smtp(sender, password, recipient, subject, html_content, host="smtp.gmail.com", port=587):
    # Root message is multipart/related so images are linked to HTML
    msg_root = MIMEMultipart("related")
    msg_root["Subject"] = subject
    msg_root["From"] = sender
    msg_root["To"] = recipient

    # Alternative part for plain text + html
    msg_alt = MIMEMultipart("alternative")
    msg_root.attach(msg_alt)

    # Simple plain text fallback
    plain_text = f"{subject}\n\nPlease view this email in an HTML-compatible client to see the full Frontier Daily Briefing."
    part1 = MIMEText(plain_text, "plain")
    msg_alt.attach(part1)

    # Detect any img references: e.g. src="assets/filename.png" or src="cid:filename"
    asset_matches = re.findall(r'src=["\'](?:assets/)?([a-zA-Z0-9_\-]+)\.png["\']', html_content)
    cid_matches = re.findall(r'src=["\']cid:([a-zA-Z0-9_\-]+)["\']', html_content)
    all_cids = sorted(list(set(asset_matches + cid_matches)))

    # Replace in html_content so it's guaranteed src="cid:..."
    for cid in all_cids:
        html_content = re.sub(rf'src=["\'](?:assets/)?{cid}\.png["\']', f'src="cid:{cid}"', html_content)
        img_path = os.path.join(BRIEFS_DIR, "assets", f"{cid}.png")
        if os.path.exists(img_path):
            with open(img_path, "rb") as f:
                img_data = f.read()
            mime_img = MIMEImage(img_data, _subtype="png")
            mime_img.add_header('Content-ID', f'<{cid}>')
            mime_img.add_header('Content-Disposition', 'inline', filename=f"{cid}.png")
            msg_root.attach(mime_img)

    part2 = MIMEText(html_content, "html")
    msg_alt.attach(part2)

    try:
        server = smtplib.SMTP(host, port)
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(sender, password)
        server.sendmail(sender, recipient, msg_root.as_string())
        server.close()
        print(f"✅ Successfully sent brief to {recipient} via {host} with {len(all_cids)} inline chart images!")
        return True
    except Exception as e:
        print(f"❌ Failed to send email via SMTP: {e}")
        return False

def main():
    config = load_config()
    recipient = config.get("recipient_email", "jgodgart@gmail.com")
    
    # Determine which file to send
    if len(sys.argv) > 1:
        target_file = sys.argv[1]
    else:
        target_file = get_latest_brief()

    if not target_file or not os.path.exists(target_file):
        print("❌ No HTML brief found to send.")
        sys.exit(1)

    with open(target_file, "r", encoding="utf-8") as f:
        html_content = f.read()

    # Extract title from HTML
    subject = f"Frontier Morning Briefing — {datetime.now().strftime('%b %d, %Y')}"
    if "<title>" in html_content:
        title = html_content.split("<title>")[1].split("</title>")[0].strip()
        if title:
            subject = title

    provider = config.get("provider", "gmail_smtp")
    
    if provider == "gmail_smtp":
        sender = config.get("gmail_smtp", {}).get("sender_email", recipient)
        password = config.get("gmail_smtp", {}).get("app_password", "")
        if not password:
            print(f"⚠️ Gmail App Password not set in email_config.json. Please add your 16-character Google App Password to enable live email delivery.")
            print(f"Target Recipient: {recipient}")
            print(f"Subject: {subject}")
            print(f"File: {target_file}")
            sys.exit(1)
        send_via_smtp(sender, password, recipient, subject, html_content)
    elif provider == "custom_smtp":
        smtp_conf = config.get("custom_smtp", {})
        host = smtp_conf.get("host")
        port = smtp_conf.get("port", 587)
        user = smtp_conf.get("username")
        pw = smtp_conf.get("password")
        sender = smtp_conf.get("from_email", user)
        send_via_smtp(sender, pw, recipient, subject, html_content, host=host, port=port)
    else:
        print(f"Unknown provider: {provider}")

if __name__ == "__main__":
    main()
