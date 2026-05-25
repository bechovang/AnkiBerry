import os
import json
import base64
import requests
from bs4 import BeautifulSoup
from flask import Flask, jsonify, request, render_template

import ankiweb_pb2

app = Flask(__name__)

@app.after_request
def add_header(response):
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

# Core Session manager
class AnkiSessionManager:
    def __init__(self, cookie_dir=None):
        self.cookie_dir = cookie_dir or os.path.dirname(__file__)
        self.session = requests.Session()
        self.headers = {
            "sec-ch-ua": '"Chromium";v="148", "Google Chrome";v="148", "Not/A)Brand";v="99"',
            "sec-ch-ua-mobile": "?0",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36",
            "Accept": "*/*",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-site": "same-origin",
            "sec-fetch-mode": "cors",
            "sec-fetch-dest": "empty",
            "Origin": "https://ankiuser.net",
            "Referer": "https://ankiuser.net/study",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "vi-VN,vi;q=0.9,en-US;q=0.6,en;q=0.5"
        }
        self.load_cookies()

    def load_cookies(self):
        """Load cookies from cookie_ankiweb.txt and cookie_ankiuser.txt."""
        print("Loading cookies...")
        total = 0
        for filename in ["cookie_ankiweb.txt", "cookie_ankiuser.txt"]:
            path = os.path.join(self.cookie_dir, filename)
            if not os.path.exists(path):
                print(f"  {filename}: not found.")
                continue
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                if not isinstance(data, list):
                    data = [data]
                for c in data:
                    domain = c.get('domain', '').lstrip('.')
                    if not domain:
                        continue
                    self.session.cookies.set(
                        name=c['name'],
                        value=c['value'],
                        domain=domain,
                        path=c.get('path', '/')
                    )
                    total += 1
                print(f"  {filename}: OK")
            except Exception as e:
                print(f"  {filename}: error - {e}")

        if total == 0:
            print("WARNING: No cookies loaded!")
            print("  1. Dang nhap https://ankiweb.net > Cookie Editor > Export as JSON > luu thanh cookie_ankiweb.txt")
            print("  2. Mo deck vao https://ankiuser.net > Cookie Editor > Export as JSON > luu thanh cookie_ankiuser.txt")
        else:
            print(f"Total: {total} cookie(s) loaded.")
        return total > 0

    def fetch_decks(self):
        req_headers = self.headers.copy()
        req_headers["Content-Type"] = "application/octet-stream"
        req_headers["Origin"] = "https://ankiweb.net"
        req_headers["Referer"] = "https://ankiweb.net/decks"
        
        timezone_req = ankiweb_pb2.MinutesWestOfUtc()
        timezone_req.minutes_west_of_utc = -420 # Default ICT Time
        
        try:
            res = self.session.post(
                "https://ankiweb.net/svc/decks/deck-list-info",
                headers=req_headers,
                data=timezone_req.SerializeToString(),
                timeout=10
            )
            if res.status_code == 200:
                resp = ankiweb_pb2.DeckListResponse()
                resp.ParseFromString(res.content)
                return resp
            return None
        except Exception as e:
            print(f"Error fetching decks: {e}")
            return None

    def select_deck(self, deck_id):
        req_headers = self.headers.copy()
        req_headers["Content-Type"] = "application/octet-stream"
        req_headers["Origin"] = "https://ankiweb.net"
        req_headers["Referer"] = "https://ankiweb.net/decks"
        
        select_req = ankiweb_pb2.SelectDeckRequest()
        select_req.deck_id = deck_id
        
        try:
            res = self.session.post(
                "https://ankiweb.net/svc/decks/select-deck",
                headers=req_headers,
                data=select_req.SerializeToString(),
                timeout=10
            )
            return res.status_code == 200
        except Exception as e:
            print(f"Error selecting deck: {e}")
            return False

    def init_study_session(self):
        try:
            res = self.session.get("https://ankiuser.net/study", headers=self.headers, timeout=10)
            return res.status_code == 200
        except Exception as e:
            print(f"Error initializing study session: {e}")
            return False

    def fetch_cards(self):
        req_headers = self.headers.copy()
        req_headers["Content-Type"] = "application/octet-stream"
        
        study_req = ankiweb_pb2.StudyCardsRequest()
        try:
            res = self.session.post(
                "https://ankiuser.net/svc/study/study-cards",
                headers=req_headers,
                data=study_req.SerializeToString(),
                timeout=10
            )
            if res.status_code == 200:
                resp = ankiweb_pb2.StudyCardsResponse()
                resp.ParseFromString(res.content)
                return resp
            return res.status_code
        except Exception as e:
            print(f"Error fetching cards: {e}")
            return None

    def submit_answer(self, card_id, button_index, current_state_b64, next_state_b64, time_taken_ms=3000):
        study_req = ankiweb_pb2.StudyCardsRequest()
        ans = study_req.answer
        ans.card_id = card_id
        ans.answer_button = button_index
        ans.time_taken_millis = time_taken_ms
        
        # Extract timestamp
        import time
        ans.answered_at_millis = int(time.time() * 1000)
        
        if current_state_b64:
            curr_state = ankiweb_pb2.SchedulingState()
            curr_state.ParseFromString(base64.b64decode(current_state_b64))
            ans.current_state.CopyFrom(curr_state)
            
        if next_state_b64:
            next_state = ankiweb_pb2.SchedulingState()
            next_state.ParseFromString(base64.b64decode(next_state_b64))
            ans.next_state.CopyFrom(next_state)
            
        req_headers = self.headers.copy()
        req_headers["Content-Type"] = "application/octet-stream"
        
        try:
            res = self.session.post(
                "https://ankiuser.net/svc/study/study-cards",
                headers=req_headers,
                data=study_req.SerializeToString(),
                timeout=10
            )
            if res.status_code == 200:
                resp = ankiweb_pb2.StudyCardsResponse()
                resp.ParseFromString(res.content)
                return resp
            return None
        except Exception as e:
            print(f"Error submitting answer: {e}")
            return None

anki_manager = AnkiSessionManager()

# HTML formatting clean-up helper
def clean_html(html):
    if not html:
        return ""
    import re
    # Convert [sound:filename.mp3] to HTML5 audio tags
    html = re.sub(r'\[sound:([^\]]+)\]', r'<audio class="anki-audio" controls=""><source src="\1" type="audio/mpeg"></audio>', html)
    
    # Remove script and style elements
    html = re.sub(r'<(script|style).*?>.*?</\1>', '', html, flags=re.DOTALL | re.IGNORECASE)
    soup = BeautifulSoup(html, "html.parser")
    
    # Safely keep only formatting, audio, source, and img elements
    allowed_tags = ['audio', 'source', 'img', 'br', 'b', 'i', 'span', 'strong', 'em', 'p', 'div']
    for tag in soup.find_all(True):
        if tag.name not in allowed_tags:
            tag.unwrap()
            
    return str(soup).strip()

# Recursive deck tree formatter
def format_deck_node(node, deck_list):
    if node.deck_id > 0:
        deck_list.append({
            "deck_id": node.deck_id,
            "name": node.name,
            "level": node.level,
            "new_count": node.new_count,
            "learn_count": node.learn_count,
            "review_count": node.review_count
        })
    for child in node.children:
        format_deck_node(child, deck_list)

# Flask Route definitions for media proxying (audio/images)
@app.route('/study/<path:filename>')
@app.route('/<path:filename>')
def proxy_media(filename):
    # Extract only the actual file basename to query the sync server correctly
    actual_filename = os.path.basename(filename)
    
    # Check if the file is a known media format
    ext = os.path.splitext(actual_filename)[1].lower()
    mime_types = {
        '.mp3': 'audio/mpeg',
        '.wav': 'audio/wav',
        '.ogg': 'audio/ogg',
        '.aac': 'audio/aac',
        '.m4a': 'audio/mp4',
        '.png': 'image/png',
        '.jpg': 'image/jpeg',
        '.jpeg': 'image/jpeg',
        '.gif': 'image/gif',
        '.svg': 'image/svg+xml'
    }
    
    if ext not in mime_types:
        # Pass-through or abort for non-media paths
        return "Not Found", 404
        
    url = f"https://ankiuser.net/study/media/{actual_filename}"
    req_headers = {
        "User-Agent": anki_manager.headers["User-Agent"],
        "Referer": "https://ankiuser.net/study"
    }
    
    try:
        res = anki_manager.session.get(url, headers=req_headers, stream=True, timeout=15)
        if res.status_code == 200:
            from flask import Response
            return Response(
                res.raw.read(),
                mimetype=mime_types[ext],
                headers={
                    "Content-Disposition": f"inline; filename={actual_filename}",
                    "Cache-Control": "public, max-age=31536000"
                }
            )
        return f"Failed to fetch media: status {res.status_code}", res.status_code
    except Exception as e:
        return f"Error proxying media: {e}", 500

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/api/decks', methods=['GET'])
def get_decks():
    resp = anki_manager.fetch_decks()
    if not resp:
        return jsonify({"error": "Failed to fetch decks from AnkiWeb. Check cookie file."}), 500
        
    deck_list = []
    format_deck_node(resp.top_node, deck_list)
    return jsonify(deck_list)

@app.route('/api/select', methods=['POST'])
def select_deck():
    data = request.json or {}
    deck_id = data.get("deck_id")
    deck_name = data.get("name", "Active Deck")
    
    if not deck_id:
        return jsonify({"error": "Missing deck_id"}), 400
        
    if not anki_manager.select_deck(deck_id):
        return jsonify({"error": "Failed to select deck on server."}), 500
        
    # Trigger /study session setup
    anki_manager.init_study_session()
    return jsonify({"success": True, "deck_name": deck_name})

@app.route('/api/cards', methods=['GET'])
def get_cards():
    resp = anki_manager.fetch_cards()
    if resp == 404:
        return jsonify({
            "error_type": "404",
            "error": "Mất đồng bộ phiên làm việc học thẻ. Hãy mở AnkiWeb trên trình duyệt máy tính, nhấp vào bộ thẻ này để kích hoạt lại phòng học."
        }), 404
        
    if not resp or isinstance(resp, int):
        return jsonify({"error": "Failed to load study cards from server."}), 500
        
    cards_data = []
    for c in resp.cards:
        # Base64 encode state messages to pass safely to browser
        next_states = {}
        ns = c.next_states
        if ns.current.SerializeToString():
            next_states["current"] = base64.b64encode(ns.current.SerializeToString()).decode('ascii')
        if ns.again.SerializeToString():
            next_states["again"] = base64.b64encode(ns.again.SerializeToString()).decode('ascii')
        if ns.hard.SerializeToString():
            next_states["hard"] = base64.b64encode(ns.hard.SerializeToString()).decode('ascii')
        if ns.good.SerializeToString():
            next_states["good"] = base64.b64encode(ns.good.SerializeToString()).decode('ascii')
        if ns.easy.SerializeToString():
            next_states["easy"] = base64.b64encode(ns.easy.SerializeToString()).decode('ascii')

        cards_data.append({
            "card_id": c.card_id,
            "question": clean_html(c.question),
            "answer": clean_html(c.answer),
            "button_labels": list(c.button_labels),
            "next_states": next_states
        })
        
    return jsonify({
        "cards": cards_data,
        "new_count": resp.new_count,
        "learn_count": resp.learn_count,
        "review_count": resp.review_count
    })

@app.route('/api/answer', methods=['POST'])
def submit_answer():
    data = request.json or {}
    card_id = data.get("card_id")
    button_index = data.get("button_index")
    time_taken_ms = data.get("time_taken_ms", 3000)
    current_state = data.get("current_state")
    next_state = data.get("next_state")
    
    if not card_id or not button_index:
        return jsonify({"error": "Missing card_id or button_index"}), 400
        
    resp = anki_manager.submit_answer(card_id, button_index, current_state, next_state, time_taken_ms)
    if not resp:
        return jsonify({"error": "Failed to submit answer to server."}), 500
        
    # Return next cards details immediately
    cards_data = []
    for c in resp.cards:
        next_states = {}
        ns = c.next_states
        if ns.current.SerializeToString():
            next_states["current"] = base64.b64encode(ns.current.SerializeToString()).decode('ascii')
        if ns.again.SerializeToString():
            next_states["again"] = base64.b64encode(ns.again.SerializeToString()).decode('ascii')
        if ns.hard.SerializeToString():
            next_states["hard"] = base64.b64encode(ns.hard.SerializeToString()).decode('ascii')
        if ns.good.SerializeToString():
            next_states["good"] = base64.b64encode(ns.good.SerializeToString()).decode('ascii')
        if ns.easy.SerializeToString():
            next_states["easy"] = base64.b64encode(ns.easy.SerializeToString()).decode('ascii')

        cards_data.append({
            "card_id": c.card_id,
            "question": clean_html(c.question),
            "answer": clean_html(c.answer),
            "button_labels": list(c.button_labels),
            "next_states": next_states
        })
        
    return jsonify({
        "cards": cards_data,
        "new_count": resp.new_count,
        "learn_count": resp.learn_count,
        "review_count": resp.review_count
    })

if __name__ == '__main__':
    # Listen on port 5000 and bind to 0.0.0.0 so other devices on local WiFi can connect!
    app.run(host='0.0.0.0', port=5000, debug=False)
