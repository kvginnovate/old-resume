"""
Gmail Email Fetcher
- Fetches all emails from inbox (paginated)
- Extracts: sender, subject, date, snippet, body
- Exports to CSV and JSON
"""

import os
import csv
import json
import base64
import email
from datetime import datetime
from pathlib import Path

try:
    from google.oauth2.credentials import Credentials
    from googleapiclient.discovery import build
    from google.auth.transport.requests import Request
except ImportError:
    print("[!] Install: pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib")
    exit(1)

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
TOKEN_FILE = 'token.json'
OUTPUT_DIR = Path('gmail_export')

def authenticate():
    """Load saved token and authenticate"""
    if not os.path.exists(TOKEN_FILE):
        print("[!] token.json not found. Run gmail_setup.py first.")
        exit(1)
    
    creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    if not creds.valid:
        if creds.expired and creds.refresh_token:
            creds.refresh(Request())
            with open(TOKEN_FILE, 'w') as token:
                token.write(creds.to_json())
    
    return build('gmail', 'v1', credentials=creds)

def get_message_headers(msg_data):
    """Extract common headers from message"""
    headers = {}
    for header in msg_data.get('payload', {}).get('headers', []):
        name = header['name'].lower()
        if name in ['from', 'to', 'cc', 'bcc', 'subject', 'date', 'reply-to']:
            headers[name] = header['value']
    return headers

def get_body(payload):
    """Recursively extract body from message payload"""
    body_parts = []
    
    if 'parts' in payload:
        for part in payload['parts']:
            body_parts.extend(get_body(part))
    else:
        mime_type = payload.get('mimeType', '')
        body_data = payload.get('body', {}).get('data', '')
        
        if body_data:
            decoded = base64.urlsafe_b64decode(body_data).decode('utf-8', errors='replace')
            if mime_type == 'text/plain':
                body_parts.append(('text', decoded))
            elif mime_type == 'text/html':
                body_parts.append(('html', decoded))
    
    return body_parts

def get_attachments(payload, msg_id):
    """Extract attachment metadata"""
    attachments = []
    
    if 'parts' in payload:
        for part in payload['parts']:
            if part.get('filename'):
                attachments.append({
                    'filename': part['filename'],
                    'mimeType': part.get('mimeType', 'unknown'),
                    'size': part.get('body', {}).get('size', 0),
                    'attachmentId': part.get('body', {}).get('attachmentId', '')
                })
            attachments.extend(get_attachments(part, msg_id))
    
    return attachments

def fetch_all_emails(service, max_results=None, label_ids=None):
    """Fetch all emails with pagination"""
    if label_ids is None:
        label_ids = ['INBOX']
    
    all_messages = []
    page_token = None
    page_count = 0
    
    print(f"[...] Fetching email list (labels: {label_ids})...")
    
    while True:
        page_count += 1
        results = service.users().messages().list(
            userId='me',
            labelIds=label_ids,
            pageToken=page_token,
            maxResults=min(max_results or 500, 500)
        ).execute()
        
        messages = results.get('messages', [])
        all_messages.extend(messages)
        print(f"  Page {page_count}: found {len(messages)} messages (total: {len(all_messages)})")
        
        page_token = results.get('nextPageToken')
        if not page_token:
            break
        
        if max_results and len(all_messages) >= max_results:
            all_messages = all_messages[:max_results]
            break
    
    print(f"[OK] Total messages to fetch: {len(all_messages)}")
    return all_messages

def fetch_message_detail(service, msg_id):
    """Fetch full message details"""
    msg = service.users().messages().get(
        userId='me',
        id=msg_id,
        format='full'
    ).execute()
    
    headers = get_message_headers(msg)
    bodies = get_body(msg.get('payload', {}))
    attachments = get_attachments(msg.get('payload', {}), msg_id)
    
    # Prefer text/plain body, fallback to html
    text_body = ''
    html_body = ''
    for btype, content in bodies:
        if btype == 'text':
            text_body = content
        elif btype == 'html' and not html_body:
            html_body = content
    
    return {
        'id': msg_id,
        'threadId': msg.get('threadId', ''),
        'labelIds': msg.get('labelIds', []),
        'snippet': msg.get('snippet', ''),
        'from': headers.get('from', ''),
        'to': headers.get('to', ''),
        'cc': headers.get('cc', ''),
        'bcc': headers.get('bcc', ''),
        'subject': headers.get('subject', '(no subject)'),
        'date': headers.get('date', ''),
        'replyTo': headers.get('reply-to', ''),
        'body_text': text_body[:5000],  # Limit body size
        'body_html': html_body[:5000] if html_body else '',
        'attachments': attachments,
        'hasAttachments': len(attachments) > 0,
        'labels': msg.get('labelIds', []),
        'sizeEstimate': msg.get('sizeEstimate', 0),
        'historyId': msg.get('historyId', ''),
    }

def export_to_csv(emails, filepath):
    """Export emails to CSV"""
    fieldnames = [
        'id', 'date', 'from', 'to', 'cc', 'subject', 'snippet',
        'hasAttachments', 'labels', 'sizeEstimate'
    ]
    
    with open(filepath, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction='ignore')
        writer.writeheader()
        for email_data in emails:
            writer.writerow({
                'id': email_data['id'],
                'date': email_data['date'],
                'from': email_data['from'],
                'to': email_data['to'],
                'cc': email_data['cc'],
                'subject': email_data['subject'],
                'snippet': email_data['snippet'],
                'hasAttachments': email_data['hasAttachments'],
                'labels': ', '.join(email_data['labels']),
                'sizeEstimate': email_data['sizeEstimate'],
            })
    
    print(f"[OK] CSV exported: {filepath}")

def export_to_json(emails, filepath):
    """Export emails to JSON"""
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(emails, f, indent=2, ensure_ascii=False)
    
    print(f"[OK] JSON exported: {filepath}")

def print_summary(emails):
    """Print summary stats"""
    print()
    print("=" * 60)
    print("GMAIL EXPORT SUMMARY")
    print("=" * 60)
    print(f"  Total emails: {len(emails)}")
    
    # Unique senders
    senders = set()
    for e in emails:
        from_field = e.get('from', '')
        if '<' in from_field:
            senders.add(from_field.split('<')[-1].rstrip('>'))
        elif from_field:
            senders.add(from_field)
    print(f"  Unique senders: {len(senders)}")
    
    # Attachments count
    with_attachments = sum(1 for e in emails if e.get('hasAttachments'))
    print(f"  Emails with attachments: {with_attachments}")
    
    # Label distribution
    label_counts = {}
    for e in emails:
        for label in e.get('labels', []):
            label_counts[label] = label_counts.get(label, 0) + 1
    print(f"  Labels used: {len(label_counts)}")
    for label, count in sorted(label_counts.items(), key=lambda x: -x[1])[:10]:
        print(f"    - {label}: {count}")
    
    # Date range
    dates = [e['date'] for e in emails if e.get('date')]
    if dates:
        print(f"  Date range: {dates[-1][:16]} → {dates[0][:16]}")
    
    print("=" * 60)

def main():
    print("--- Gmail Email Fetcher ---")
    print()
    
    service = authenticate()
    
    # Get profile
    profile = service.users().getProfile(userId='me').execute()
    print(f"[OK] Connected as: {profile['emailAddress']}")
    print(f"[OK] Total messages in account: {profile['messagesTotal']}")
    print()
    
    # Options
    print("Fetch options:")
    print("  1. All emails (may take a while)")
    print("  2. Last 100 emails")
    print("  3. Last 500 emails")
    print("  4. Custom count")
    print("  5. Specific label (e.g., SENT, IMPORTANT, STARRED)")
    print()
    
    choice = input("Select option (1-5) [default: 2]: ").strip() or '2'
    
    max_results = None
    label_ids = ['INBOX']
    
    if choice == '1':
        max_results = None  # All
    elif choice == '2':
        max_results = 100
    elif choice == '3':
        max_results = 500
    elif choice == '4':
        max_results = int(input("How many emails? "))
    elif choice == '5':
        label_input = input("Enter label name (e.g., SENT, IMPORTANT): ").strip()
        label_ids = [label_input.upper()]
        max_results = 100
    else:
        max_results = 100
    
    # Fetch message list
    messages = fetch_all_emails(service, max_results=max_results, label_ids=label_ids)
    
    if not messages:
        print("[!] No messages found")
        return
    
    # Fetch details
    print(f"[...] Fetching details for {len(messages)} messages...")
    all_emails = []
    for i, msg in enumerate(messages, 1):
        try:
            email_data = fetch_message_detail(service, msg['id'])
            all_emails.append(email_data)
            if i % 25 == 0 or i == len(messages):
                print(f"  Fetched {i}/{len(messages)}")
        except Exception as e:
            print(f"  [!] Error fetching message {msg['id']}: {e}")
    
    # Create output directory
    OUTPUT_DIR.mkdir(exist_ok=True)
    
    # Export
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    csv_path = OUTPUT_DIR / f'gmail_export_{timestamp}.csv'
    json_path = OUTPUT_DIR / f'gmail_export_{timestamp}.json'
    
    export_to_csv(all_emails, csv_path)
    export_to_json(all_emails, json_path)
    print_summary(all_emails)
    
    # Save full body version (larger file)
    full_json_path = OUTPUT_DIR / f'gmail_full_{timestamp}.json'
    export_to_json(all_emails, full_json_path)
    print(f"\n[OK] Full export (with body): {full_json_path}")

if __name__ == '__main__':
    main()
