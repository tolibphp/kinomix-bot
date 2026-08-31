
import json
import re

log_path = r'C:\Users\user\.gemini\antigravity\brain\123578b8-3e46-4b8c-9f1f-50d65e52e655\.system_generated\logs\transcript_full.jsonl'
result = {}
with open(log_path, 'r', encoding='utf-8') as f:
    for line in f:
        data = json.loads(line)
        if data.get('type') == 'USER_INPUT' and 'Premium Emoji ID lari topildi:' in data.get('content', ''):
            content = data['content']
            matches = re.findall(r'Emoji:\s*(.+?)\nKod:\s*<tg-emoji emoji-id="(\d+)">', content)
            for emoji, eid in matches:
                result[emoji.strip()] = eid

with open('emojis.json', 'w', encoding='utf-8') as out:
    json.dump(result, out, ensure_ascii=False, indent=2)

