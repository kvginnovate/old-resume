/**
 * Gmail Browser Console Email Extractor
 * 
 * HOW TO USE:
 * 1. Open https://mail.google.com in Chrome and log in with chokkar.g@dish.com
 * 2. Press F12 (or Ctrl+Shift+J) to open Developer Tools
 * 3. Go to the "Console" tab
 * 4. Paste this entire script and press Enter
 * 5. Wait for extraction to complete
 * 6. A JSON file will download automatically
 */

(async function extractGmail() {
  const DELAY = 800; // ms between actions (be gentle with Gmail)
  const MAX_EMAILS = parseInt(prompt('How many emails to extract?', '100'), 10) || 100;

  function sleep(ms) { return new Promise(r => setTimeout(r, ms)); }

  // Helper: click element by selector with retry
  async function clickEl(selector, retries = 5) {
    for (let i = 0; i < retries; i++) {
      const el = document.querySelector(selector);
      if (el) { el.click(); return true; }
      await sleep(500);
    }
    return false;
  }

  // Helper: get text safely
  function txt(el) { return el ? el.textContent.trim() : ''; }

  // Step 1: Collect email list from current view
  console.log('📧 Step 1: Collecting email list...');

  async function getEmailList() {
    const rows = document.querySelectorAll('tr.zA');
    const emails = [];
    for (const row of rows) {
      const subjectEl = row.querySelector('span.bog');
      const senderEl = row.querySelector('span.yP, span.zF');
      const dateEl = row.querySelector('span.xW, span.xY.xY');
      const snippetEl = row.querySelector('span.y6');
      const labelEls = row.querySelectorAll('span.at');
      const hasAttachment = !!row.querySelector('br[data-adv]') || row.innerHTML.includes('rc');
      
      emails.push({
        subject: txt(subjectEl),
        sender: txt(senderEl),
        date: txt(dateEl),
        snippet: txt(snippetEl),
        labels: Array.from(labelEls).map(l => txt(l)).filter(Boolean),
        hasAttachment,
        element: row,
        link: row.querySelector('a')?.href || ''
      });
    }
    return emails;
  }

  // Scroll to load more emails
  async function loadMoreEmails(targetCount) {
    let lastCount = 0;
    let staleRounds = 0;
    while (staleRounds < 5) {
      const rows = document.querySelectorAll('tr.zA');
      if (rows.length >= targetCount) break;
      if (rows.length === lastCount) {
        staleRounds++;
      } else {
        staleRounds = 0;
        lastCount = rows.length;
      }
      // Scroll the email list
      const list = document.querySelector('div.AO');
      if (list) list.scrollTop = list.scrollHeight;
      // Also try scrolling the main content
      window.scrollBy(0, 1000);
      await sleep(DELAY);
      console.log(`  Loaded ${rows.length} emails so far...`);
    }
    return document.querySelectorAll('tr.zA').length;
  }

  // Load emails by scrolling
  console.log(`  Scrolling to load up to ${MAX_EMAILS} emails...`);
  const loaded = await loadMoreEmails(MAX_EMAILS);
  console.log(`  Found ${loaded} emails in list`);

  // Collect list data
  let emailList = await getEmailList();
  emailList = emailList.slice(0, MAX_EMAILS);
  console.log(`  Collected ${emailList.length} email summaries`);

  // Step 2: Open each email and extract full content
  console.log('\n📬 Step 2: Extracting full email content...');
  const results = [];

  for (let i = 0; i < emailList.length; i++) {
    const item = emailList[i];
    console.log(`  [${i + 1}/${emailList.length}] ${item.subject || '(no subject)'}`);

    // Click the email row
    try {
      item.element.click();
      await sleep(DELAY + 400);

      // Extract full email content
      const emailData = {
        index: i + 1,
        subject: item.subject,
        sender: item.sender,
        date: item.date,
        snippet: item.snippet,
        labels: item.labels,
        hasAttachment: item.hasAttachment,
        to: '',
        body: '',
        bodyHtml: ''
      };

      // Try to find To field
      const toEl = document.querySelector('span.g2');
      if (toEl) emailData.to = txt(toEl);

      // Try to find full body
      const bodyEl = document.querySelector('div.a3s.aiL') || document.querySelector('div.a3s');
      if (bodyEl) {
        emailData.body = bodyEl.innerText.trim();
        emailData.bodyHtml = bodyEl.innerHTML.substring(0, 2000); // limit HTML size
      }

      // Check for attachments in detail view
      const attachEls = document.querySelectorAll('div.aVX, span.aV3');
      if (attachEls.length > 0) {
        emailData.hasAttachment = true;
        emailData.attachmentCount = attachEls.length;
      }

      results.push(emailData);

      // Go back to inbox
      // Click back button or press Escape
      const backBtn = document.querySelector('div[act="20"]') // Back arrow
        || document.querySelector('img[act="20"]');
      if (backBtn) {
        backBtn.click();
      } else {
        // Try pressing Escape or clicking the back arrow in toolbar
        document.dispatchEvent(new KeyboardEvent('keydown', { key: 'Escape', keyCode: 27 }));
      }
      await sleep(DELAY);

    } catch (err) {
      console.warn(`  ⚠️ Error on email ${i + 1}: ${err.message}`);
      results.push({
        index: i + 1,
        subject: item.subject,
        sender: item.sender,
        date: item.date,
        snippet: item.snippet,
        error: err.message
      });
      // Try to go back
      document.dispatchEvent(new KeyboardEvent('keydown', { key: 'Escape', keyCode: 27 }));
      await sleep(DELAY);
    }
  }

  // Step 3: Export
  console.log('\n💾 Step 3: Exporting...');

  // JSON export
  const jsonBlob = new Blob([JSON.stringify(results, null, 2)], { type: 'application/json' });
  const jsonUrl = URL.createObjectURL(jsonBlob);
  const a1 = document.createElement('a');
  a1.href = jsonUrl;
  a1.download = `gmail_export_${new Date().toISOString().slice(0,10)}.json`;
  a1.click();

  // CSV export
  const csvHeader = 'Index,Subject,Sender,To,Date,Labels,HasAttachment,Body\n';
  const csvRows = results.map(r => {
    return [
      r.index,
      `"${(r.subject || '').replace(/"/g, '""')}"`,
      `"${(r.sender || '').replace(/"/g, '""')}"`,
      `"${(r.to || '').replace(/"/g, '""')}"`,
      `"${(r.date || '').replace(/"/g, '""')}"`,
      `"${(r.labels || []).join(', ')}"`,
      r.hasAttachment || false,
      `"${(r.body || '').replace(/"/g, '""').substring(0, 500)}"`
    ].join(',');
  }).join('\n');
  const csvBlob = new Blob([csvHeader + csvRows], { type: 'text/csv' });
  const csvUrl = URL.createObjectURL(csvBlob);
  const a2 = document.createElement('a');
  a2.href = csvUrl;
  a2.download = `gmail_export_${new Date().toISOString().slice(0,10)}.csv`;
  a2.click();

  console.log(`\n✅ Done! Extracted ${results.length} emails.`);
  console.log('📁 Downloaded: JSON + CSV files');
  console.log('\nSummary:');
  console.log(`  Total emails: ${results.length}`);
  console.log(`  Unique senders: ${new Set(results.map(r => r.sender)).size}`);
  console.log(`  With attachments: ${results.filter(r => r.hasAttachment).length}`);

})();
