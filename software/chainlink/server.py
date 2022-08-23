from http.server import BaseHTTPRequestHandler, HTTPServer
import logging
import simplejson
import urllib.parse
import random
import time
from datetime import datetime
import asyncio
import threading

from splitflap_proto import (
    ask_for_serial_port,
    splitflap_context,
)

context = ''
words = [
'absolute',
'abstract',
'academic',
'accepted',
'accident',
'accuracy',
'accurate',
'achieved',
'acquired',
'activity',
'actually',
'addition',
'adequate',
'adjacent',
'adjusted',
'advanced',
'advisory',
'advocate',
'affected',
'aircraft',
'alliance',
'although',
'aluminum',
'analysis',
'announce',
'anything',
'anywhere',
'apparent',
'appendix',
'approach',
'approval',
'argument',
'artistic',
'assembly',
'assuming',
'athletic',
'attached',
'attitude',
'attorney',
'audience',
'autonomy',
'aviation',
'bachelor',
'bacteria',
'baseball',
'bathroom',
'becoming',
'benjamin',
'birthday',
'boundary',
'breaking',
'breeding',
'building',
'bulletin',
'business',
'calendar',
'campaign',
'capacity',
'casualty',
'catching',
'category',
'Catholic',
'cautious',
'cellular',
'ceremony',
'chairman',
'champion',
'chemical',
'children',
'circular',
'civilian',
'clearing',
'clinical',
'clothing',
'collapse',
'colonial',
'colorful',
'commence',
'commerce',
'complain',
'complete',
'composed',
'compound',
'comprise',
'computer',
'conclude',
'concrete',
'conflict',
'confused',
'congress',
'consider',
'constant',
'consumer',
'continue',
'contract',
'contrary',
'contrast',
'convince',
'corridor',
'coverage',
'covering',
'creation',
'creative',
'criminal',
'critical',
'crossing',
'cultural',
'currency',
'customer',
'database',
'daughter',
'daylight',
'deadline',
'deciding',
'decision',
'decrease',
'deferred',
'definite',
'delicate',
'delivery',
'describe',
'designer',
'detailed',
'diabetes',
'dialogue',
'diameter',
'directly',
'director',
'disabled',
'disaster',
'disclose',
'discount',
'discover',
'disorder',
'disposal',
'distance',
'distinct',
'district',
'dividend',
'division',
'doctrine',
'document',
'domestic',
'dominant',
'dominate',
'doubtful',
'dramatic',
'dressing',
'dropping',
'duration',
'dynamics',
'earnings',
'economic',
'educated',
'efficacy',
'eighteen',
'election',
'electric',
'eligible',
'emerging',
'emphasis',
'employee',
'endeavor',
'engaging',
'engineer',
'enormous',
'entirely',
'entrance',
'envelope',
'equality',
'equation',
'estimate',
'evaluate',
'eventual',
'everyday',
'everyone',
'evidence',
'exchange',
'exciting',
'exercise',
'explicit',
'exposure',
'extended',
'external',
'facility',
'familiar',
'featured',
'feedback',
'festival',
'finished',
'firewall',
'flagship',
'flexible',
'floating',
'football',
'foothill',
'forecast',
'foremost',
'formerly',
'fourteen',
'fraction',
'franklin',
'frequent',
'friendly',
'frontier',
'function',
'generate',
'generous',
'genomics',
'goodwill',
'governor',
'graduate',
'graphics',
'grateful',
'guardian',
'guidance',
'handling',
'hardware',
'heritage',
'highland',
'historic',
'homeless',
'homepage',
'hospital',
'humanity',
'identify',
'identity',
'ideology',
'imperial',
'incident',
'included',
'increase',
'indicate',
'indirect',
'industry',
'informal',
'informed',
'inherent',
'initiate',
'innocent',
'inspired',
'instance',
'integral',
'intended',
'interact',
'interest',
'interior',
'internal',
'interval',
'intimate',
'intranet',
'invasion',
'involved',
'isolated',
'judgment',
'judicial',
'junction',
'keyboard',
'landlord',
'language',
'laughter',
'learning',
'leverage',
'lifetime',
'lighting',
'likewise',
'limiting',
'literary',
'location',
'magazine',
'magnetic',
'maintain',
'majority',
'marginal',
'marriage',
'material',
'maturity',
'maximize',
'meantime',
'measured',
'medicine',
'medieval',
'memorial',
'merchant',
'midnight',
'military',
'minimize',
'minister',
'ministry',
'minority',
'mobility',
'modeling',
'moderate',
'momentum',
'monetary',
'moreover',
'mortgage',
'mountain',
'mounting',
'movement',
'multiple',
'national',
'negative',
'nineteen',
'northern',
'notebook',
'numerous',
'observer',
'occasion',
'offering',
'official',
'offshore',
'operator',
'opponent',
'opposite',
'optimism',
'optional',
'ordinary',
'organize',
'original',
'overcome',
'overhead',
'overseas',
'overview',
'painting',
'parallel',
'parental',
'patented',
'patience',
'peaceful',
'periodic',
'personal',
'persuade',
'petition',
'physical',
'pipeline',
'platform',
'pleasant',
'pleasure',
'politics',
'portable',
'portrait',
'position',
'positive',
'possible',
'powerful',
'practice',
'precious',
'pregnant',
'presence',
'preserve',
'pressing',
'pressure',
'previous',
'princess',
'printing',
'priority',
'probable',
'probably',
'producer',
'profound',
'progress',
'property',
'proposal',
'prospect',
'protocol',
'provided',
'provider',
'province',
'publicly',
'purchase',
'pursuant',
'quantity',
'question',
'rational',
'reaction',
'received',
'receiver',
'recovery',
'regional',
'register',
'relation',
'relative',
'relevant',
'reliable',
'reliance',
'religion',
'remember',
'renowned',
'repeated',
'reporter',
'republic',
'required',
'research',
'reserved',
'resident',
'resigned',
'resource',
'response',
'restrict',
'revision',
'rigorous',
'romantic',
'sampling',
'scenario',
'schedule',
'scrutiny',
'seasonal',
'secondly',
'security',
'sensible',
'sentence',
'separate',
'sequence',
'sergeant',
'shipping',
'shortage',
'shoulder',
'simplify',
'situated',
'slightly',
'software',
'solution',
'somebody',
'somewhat',
'southern',
'speaking',
'specific',
'spectrum',
'sporting',
'standard',
'standing',
'standout',
'sterling',
'straight',
'strategy',
'strength',
'striking',
'struggle',
'stunning',
'suburban',
'suitable',
'superior',
'supposed',
'surgical',
'surprise',
'survival',
'sweeping',
'swimming',
'symbolic',
'sympathy',
'syndrome',
'tactical',
'tailored',
'takeover',
'tangible',
'taxation',
'taxpayer',
'teaching',
'tendency',
'terminal',
'terrible',
'thinking',
'thirteen',
'thorough',
'thousand',
'together',
'tomorrow',
'touching',
'tracking',
'training',
'transfer',
'traveled',
'treasury',
'triangle',
'tropical',
'turnover',
'ultimate',
'umbrella',
'universe',
'unlawful',
'unlikely',
'valuable',
'variable',
'vertical',
'victoria',
'violence',
'volatile',
'warranty',
'weakness',
'weighted',
'whatever',
'whenever',
'wherever',
'wildlife',
'wireless',
'withdraw',
'woodland',
'workshop',
'yourself',
]
letters = [
    ' ',
    'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
    'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
    '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
    '!',
    '?',
    ':',
]

class S(BaseHTTPRequestHandler):
    running = True
    event = threading.Event()


    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        logging.info("GET request,\nPath: %s\nHeaders:\n%s\n", str(self.path), str(self.headers))
        self._set_response()
        self.wfile.write("GET request for {}".format(self.path).encode('utf-8'))

    def takeInput(self, word):
        p = ask_for_serial_port()
        with splitflap_context(p) as s:
            modules = s.get_num_modules()
            alphabet = s.get_alphabet()

            s.set_text(word)
            time.sleep(5)
            
    def randomWords(self):
        p = ask_for_serial_port()
        with splitflap_context(p) as s:
            modules = s.get_num_modules()
            alphabet = s.get_alphabet()
            
            while self.event.is_set():
                word = random.choice(words)
                print(word)
                s.set_text(word)
                time.sleep(5)
            
            
    def clockApp(self):
        p = ask_for_serial_port()
        with splitflap_context(p) as s:
            modules = s.get_num_modules()
            alphabet = s.get_alphabet()
            
            now = datetime.now()
            current_time = now.strftime("%I:%M")
            print("Current Time =", current_time)
            s.set_text("   " + current_time)

            while self.event.is_set():
                delta = datetime.now() - now
                if delta.seconds >= 60:
                    now = datetime.now()
                    current_time = now.strftime("%I:%M")
                    print(current_time)
                    s.set_text("   " + current_time)
            

    def cycleWords(self):
        p = ask_for_serial_port()
        with splitflap_context(p) as s:
            modules = s.get_num_modules()
            alphabet = s.get_alphabet()
            
            while self.event.is_set():
                for word in letters:
                    for i in range(2):
                        word = word + word
                    print(word)
                    s.set_text(word)
                    time.sleep(1)

    def do_POST(self):
        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        post_data = self.rfile.read(content_length) # <--- Gets the data itself
        # logging.info("POST request,\nPath: %s\nHeaders:\n%s\n\nBody:\n%s\n",
        #         str(self.path), str(self.headers), post_data.decode('utf-8'))
        # decoded = post_data.decode('utf-8')
        res = urllib.parse.parse_qs(self.path[2:])
        command = ''
        word = ''
        for key, value in res.items():
            command = key
            word = value[0]
        running = False
        if command == "input":
            self.takeInput(word)
        elif command == "random":
            self.event.clear()
            thread = threading.Thread(target=self.randomWords, args=())
            thread.daemon = True
            self.event.set()
            thread.start()
        elif command == "clock":
            self.event.clear()
            thread = threading.Thread(target=self.randomWords, args=())
            thread.daemon = True
            self.event.set()
            thread.start()
            self.clockApp()
        elif command == "cycle":
            self.event.clear()
            thread = threading.Thread(target=self.randomWords, args=())
            thread.daemon = True
            self.event.set()
            self.cycleWords()
        elif command == "stop":
            self.event.clear()
        self._set_response()
        self.wfile.write("POST request for {}".format(self.path).encode('utf-8'))

def run(server_class=HTTPServer, handler_class=S, port=8080):
        logging.basicConfig(level=logging.INFO)
        server_address = ('', port)
        httpd = server_class(server_address, handler_class)
        logging.info('Starting httpd...\n')
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            pass
        httpd.server_close()
        logging.info('Stopping httpd...\n')

if __name__ == '__main__':
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()