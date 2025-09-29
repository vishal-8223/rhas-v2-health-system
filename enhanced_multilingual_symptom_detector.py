#!/usr/bin/env python3
"""
🌐 Enhanced Multi-Language Symptom Detector for RHAS v2.0
Comprehensive support for Indian regional languages and symptom recognition
"""

from typing import Dict, List, Tuple
import re

class EnhancedMultilingualSymptomDetector:
    """Enhanced symptom detection for Indian regional languages"""
    
    def __init__(self):
        self.symptom_database = self._initialize_multilingual_symptoms()
        self.language_patterns = self._initialize_language_patterns()
        
    def _initialize_multilingual_symptoms(self) -> Dict[str, Dict]:
        """Comprehensive multilingual symptom database"""
        return {
            'fever': {
                'english': ['fever', 'temperature', 'hot', 'burning', 'chills', 'high fever', 'feverish', 'pyrexia'],
                'hindi_devanagari': ['बुखार', 'ज्वर', 'तेज बुखार', 'तापमान', 'गर्मी', 'ठंड लगना', 'कंपकंपी'],
                'hindi_roman': ['bukhar', 'jwar', 'tez bukhar', 'tapman', 'garmi', 'thand', 'kampkampi'],
                'bengali': ['জ্বর', 'জ্বর আছে', 'তাপমাত্রা', 'গরম লাগছে', 'কাঁপুনি'],
                'bengali_roman': ['jor', 'jor ache', 'tapmattra', 'gorom lagche', 'kampuni'],
                'tamil': ['காய்ச்சல்', 'வெப்பம்', 'கோய்ச்சல்', 'உடல் சூடு', 'நடுக்கம்'],
                'tamil_roman': ['kaichal', 'veppam', 'koichal', 'udal sudu', 'nadukkam'],
                'telugu': ['జ్వరం', 'వేడిమి', 'వేడుకలు', 'కంపనలు', 'చలిమి'],
                'telugu_roman': ['jvaram', 'vedimi', 'vedukalu', 'kampanalu', 'chalimi'],
                'marathi': ['ताप', 'गरमी', 'वेदना', 'थरथर', 'कापरे'],
                'marathi_roman': ['taap', 'garmi', 'vedana', 'tharthar', 'kapre'],
                'gujarati': ['તાવ', 'તાપ', 'જ્વર', 'ગરમી', 'ઠરણું'],
                'gujarati_roman': ['tav', 'tap', 'jvar', 'garmi', 'tharanum'],
                'kannada': ['ಜ್ವರ', 'ಬಿಸಿ', 'ತಾಪ', 'ನಡುಗು', 'ಚಳಿ'],
                'kannada_roman': ['jvara', 'bisi', 'tapa', 'nadugu', 'chali'],
                'malayalam': ['പനി', 'ചുട്ടുപനി', 'ചൂട്', 'വിറയൽ'],
                'malayalam_roman': ['pani', 'chuttupani', 'choot', 'virayal'],
                'punjabi': ['ਬੁਖ਼ਾਰ', 'ਤਾਪ', 'ਗਰਮੀ', 'ਕੰਬਣੀ'],
                'punjabi_roman': ['bukhar', 'tap', 'garmi', 'kambani'],
                'severity': 'Medium'
            },
            
            'headache': {
                'english': ['headache', 'head pain', 'head ache', 'severe headache', 'migraine', 'head hurts'],
                'hindi_devanagari': ['सिर दर्द', 'सिरदर्द', 'सिर में दर्द', 'माथे में दर्द', 'सिर दुखना'],
                'hindi_roman': ['sir dard', 'sirdard', 'sir me dard', 'mathe me dard', 'sir dukhna'],
                'bengali': ['মাথাব্যথা', 'মাথা ব্যথা', 'মাথা দুখছে', 'মাথার যন্ত্রণা'],
                'bengali_roman': ['mathabytha', 'matha bytha', 'matha dukhche', 'mathar jontrana'],
                'tamil': ['தலைவலி', 'தலை வலி', 'தலையில் வலி', 'நெற்றி வலி'],
                'tamil_roman': ['talaivali', 'talai vali', 'talaiyil vali', 'netri vali'],
                'telugu': ['తలనొప్పి', 'తల నొప్పి', 'తలలో నొప్పి', 'నొప్పి'],
                'telugu_roman': ['talanoppi', 'tala noppi', 'talalo noppi', 'noppi'],
                'marathi': ['डोकेदुखी', 'डोके दुखणे', 'कपाळ दुखी'],
                'marathi_roman': ['dokedukhi', 'doke dukhne', 'kapal dukhi'],
                'gujarati': ['માથાનો દુખાવો', 'માથું દુખવું', 'માથાનો દુખાર'],
                'gujarati_roman': ['mathano dukhavo', 'mathun dukhvun', 'mathano dukhar'],
                'kannada': ['ತಲೆನೋವು', 'ತಲೆ ನೋವು', 'ತಲೆ ಬಾಧೆ'],
                'kannada_roman': ['talenovu', 'tale novu', 'tale badhe'],
                'malayalam': ['തലവേദന', 'തല വേദന', 'തലയിൽ വേദന'],
                'malayalam_roman': ['talavedana', 'tala vedana', 'talayil vedana'],
                'punjabi': ['ਸਿਰ ਦਰਦ', 'ਸਿਰ ਵਿੱਚ ਦਰਦ', 'ਸਿਰ ਦੁੱਖਣਾ'],
                'punjabi_roman': ['sir dard', 'sir vich dard', 'sir dukhna'],
                'severity': 'Low'
            },
            
            'diarrhea': {
                'english': ['diarrhea', 'diarrhoea', 'loose stool', 'watery stool', 'loose motion', 'bloody diarrhea', 'loose bowels'],
                'hindi_devanagari': ['दस्त', 'पेचिश', 'दस्त लगना', 'पतले दस्त', 'खूनी दस्त', 'पेट खराब'],
                'hindi_roman': ['dast', 'pechish', 'dast lagna', 'patle dast', 'khooni dast', 'pet kharab'],
                'bengali': ['পাতলা পায়খানা', 'ডায়রিয়া', 'বার বার পায়খানা', 'তরল পায়খানা'],
                'bengali_roman': ['patla paykhana', 'diarrhea', 'bar bar paykhana', 'taral paykhana'],
                'tamil': ['வயிற்றுப்போக்கு', 'தண்ணீர் மலம்', 'கழிச்சல்', 'வயிறு கழிச்சல்'],
                'tamil_roman': ['vaiyatrupooku', 'thanneer malam', 'kazhichal', 'vairu kazhichal'],
                'telugu': ['విరేచనలు', 'అజీర్ణం', 'నీటిలాంటి మలం', 'కడుపు కలత'],
                'telugu_roman': ['virechanalu', 'ajeernam', 'neetilanti malam', 'kadupu kalatha'],
                'marathi': ['जुलाब', 'पातळ संडास', 'पेटाळा', 'अतिसार'],
                'marathi_roman': ['julab', 'patla sandas', 'petala', 'atisar'],
                'gujarati': ['ઝાડા', 'પાતળા ટટ્ટી', 'પેટમાં ખરાબ', 'અતિસાર'],
                'gujarati_roman': ['jhada', 'patla tatti', 'petma kharab', 'atisar'],
                'kannada': ['ಅತಿಸಾರ', 'ಎಳ್ಳು ಮಲ', 'ಹೊಟ್ಟೆ ಖರಾಬು', 'ದಸ್ತು'],
                'kannada_roman': ['atisara', 'ellu mala', 'hotte kharabu', 'dastu'],
                'malayalam': ['വയറിളക്കം', 'അതിസാരം', 'വെള്ളമല', 'വയറ് കുഴപ്പം'],
                'malayalam_roman': ['vayarilakkam', 'atisaram', 'vellamala', 'vayar kuzhappam'],
                'punjabi': ['ਦਸਤ', 'ਪਤਲੇ ਦਸਤ', 'ਢਿੱਡ ਖਰਾਬ', 'ਲੂਸ ਮੋਸ਼ਨ'],
                'punjabi_roman': ['dast', 'patle dast', 'dhid kharab', 'loose motion'],
                'severity': 'Medium'
            },
            
            'vomiting': {
                'english': ['vomiting', 'throw up', 'puke', 'throwing up', 'vomit', 'nausea vomiting', 'retching'],
                'hindi_devanagari': ['उल्टी', 'उल्टी आना', 'कै', 'उबकाई', 'जी मिचलाना', 'मतली उल्टी'],
                'hindi_roman': ['ulti', 'ulti ana', 'kai', 'ubkai', 'ji michalna', 'matli ulti'],
                'bengali': ['বমি', 'বমি হওয়া', 'বমি ভাব', 'বমি করা'],
                'bengali_roman': ['bomi', 'bomi howa', 'bomi bhav', 'bomi kora'],
                'tamil': ['வாந்தி', 'வயிற்றுக்கசப்பு', 'குமட்டல்', 'வாந்தி எடுத்தல்'],
                'tamil_roman': ['vanthi', 'vaiyatrukasappu', 'kumattal', 'vanthi eduthal'],
                'telugu': ['వాంతులు', 'కిరుకుతిన్నాను', 'వాంతిభావం', 'ఓకరించడం'],
                'telugu_roman': ['vantulu', 'kirukutinnanu', 'vantibhavam', 'okarinchardam'],
                'marathi': ['उलट्या', 'उलटी होणे', 'मळमळ', 'ओकारणे'],
                'marathi_roman': ['ultya', 'ulti hone', 'malmal', 'okarane'],
                'gujarati': ['ઉલટી', 'છાતીમાં બળતરા', 'મચકોડ', 'ઊલટાવવું'],
                'gujarati_roman': ['ulti', 'chatima baltara', 'machkod', 'ultavvun'],
                'kannada': ['ವಾಂತಿ', 'ಹೊಟ್ಟೆ ಮುರುಗು', 'ಕಿರುಕು', 'ಉಸಿರಾಟ'],
                'kannada_roman': ['vanti', 'hotte murugu', 'kiruku', 'usiraat'],
                'malayalam': ['ഛര്‍ദ്ദി', 'വാന്തി', 'ഓക്കാനം', 'കുമിള'],
                'malayalam_roman': ['charddi', 'vanthi', 'okkanam', 'kumila'],
                'punjabi': ['ਉਲਟੀ', 'ਕੈ', 'ਜੀ ਮਿਚਲਾਣਾ', 'ਉਬਕਾਈ'],
                'punjabi_roman': ['ulti', 'kai', 'ji michalna', 'ubkai'],
                'severity': 'High'
            },
            
            'cough': {
                'english': ['cough', 'coughing', 'dry cough', 'persistent cough', 'wet cough', 'chest congestion'],
                'hindi_devanagari': ['खांसी', 'खांसी आना', 'सूखी खांसी', 'कफ', 'छाती में जकड़न', 'गले में खराश'],
                'hindi_roman': ['khansi', 'khansi ana', 'sukhi khansi', 'kaph', 'chati me jakdan', 'gale me kharash'],
                'bengali': ['কাশি', 'শুকনো কাশি', 'কফ', 'গলায় খুসখুস', 'বুকে জমাট'],
                'bengali_roman': ['kashi', 'shukno kashi', 'kaph', 'golay khuskhus', 'buke jamat'],
                'tamil': ['இருமல்', 'வறட்டு இருமல்', 'கபம்', 'மார் சளி', 'தொண்டை வலி'],
                'tamil_roman': ['irumal', 'varattu irumal', 'kapam', 'mar chali', 'thondai vali'],
                'telugu': ['దగ్గు', 'ఎండు దగ్గు', 'కఫం', 'ఛాతీ రద్దీ', 'గొంతు నొప్పి'],
                'telugu_roman': ['daggu', 'endu daggu', 'kapham', 'chati raddi', 'gontu noppi'],
                'marathi': ['खोकला', 'सुका खोकला', 'कफ', 'छातीत जडणघडण'],
                'marathi_roman': ['khokla', 'suka khokla', 'kaph', 'chatit jadangadan'],
                'gujarati': ['ખાંસી', 'સુકી ખાંસી', 'કંઠમાં ખરાશ', 'છાતીમાં બળતરા'],
                'gujarati_roman': ['khansi', 'suki khansi', 'kanthma kharash', 'chatima baltara'],
                'kannada': ['ಕೆಮ್ಮು', 'ಒಣ ಕೆಮ್ಮು', 'ಕಫ', 'ಎದೆಯಲ್ಲಿ ನೋವು'],
                'kannada_roman': ['kemmu', 'ona kemmu', 'kapa', 'edeyalli novu'],
                'malayalam': ['ചുമ', 'വരണ്ട ചുമ', 'കഫം', 'നെഞ്ചിൽ വേദന'],
                'malayalam_roman': ['chuma', 'varanda chuma', 'kapham', 'nenjil vedana'],
                'punjabi': ['ਖੰਘ', 'ਸੁੱਕੀ ਖੰਘ', 'ਕਫ਼', 'ਛਾਤੀ ਵਿੱਚ ਭਾਰੀਪਨ'],
                'punjabi_roman': ['khangh', 'sukki khangh', 'kaph', 'chati vich bharipan'],
                'severity': 'Low'
            },
            
            'stomach_pain': {
                'english': ['stomach pain', 'abdominal pain', 'belly ache', 'belly pain', 'stomach ache', 'tummy ache', 'gut pain'],
                'hindi_devanagari': ['पेट दर्द', 'पेट में दर्द', 'पेटकी दर्द', 'उदर दर्द', 'नाभि दर्द', 'अमाशय दर्द'],
                'hindi_roman': ['pet dard', 'pet me dard', 'petki dard', 'udar dard', 'nabhi dard', 'amashay dard'],
                'bengali': ['পেটের ব্যথা', 'পেট দুখছে', 'উদর ব্যথা', 'কোমর ব্যথা'],
                'bengali_roman': ['peter bytha', 'pet dukhche', 'udar bytha', 'komar bytha'],
                'tamil': ['வயிற்று வலி', 'வயிறு வலி', 'அடிவயிறு வலி', 'குடல் வலி'],
                'tamil_roman': ['vaiyatru vali', 'vairu vali', 'adivairu vali', 'kudal vali'],
                'telugu': ['కడుపు నొప్పి', 'పొట్ట నొప్పి', 'కడుపులో నొప్పి', 'ఉదర నొప్పి'],
                'telugu_roman': ['kadupu noppi', 'potta noppi', 'kadupulo noppi', 'udara noppi'],
                'marathi': ['पोट दुखी', 'उदर वेदना', 'पेटात दुखी'],
                'marathi_roman': ['pot dukhi', 'udar vedana', 'petat dukhi'],
                'gujarati': ['પેટમાં દુખાવો', 'ઉદર દુખાવો', 'પેટ દર્દ'],
                'gujarati_roman': ['petma dukhavo', 'udar dukhavo', 'pet dard'],
                'kannada': ['ಹೊಟ್ಟೆ ನೋವು', 'ಉದರ ನೋವು', 'ಪೊಟ್ಟ ನೋವು'],
                'kannada_roman': ['hotte novu', 'udara novu', 'potta novu'],
                'malayalam': ['വയർ വേദന', 'ഉദര വേദന', 'വയറ്റിൽ വേദന'],
                'malayalam_roman': ['vayar vedana', 'udara vedana', 'vayattil vedana'],
                'punjabi': ['ਢਿੱਡ ਦਰਦ', 'ਪੇਟ ਦਰਦ', 'ਢਿੱਡ ਵਿੱਚ ਦਰਦ'],
                'punjabi_roman': ['dhid dard', 'pet dard', 'dhid vich dard'],
                'severity': 'Medium'
            },
            
            'weakness': {
                'english': ['weakness', 'fatigue', 'tired', 'weak', 'exhausted', 'lethargic', 'no energy'],
                'hindi_devanagari': ['कमजोरी', 'थकान', 'थकावट', 'कमजोर लगना', 'दुर्बलता', 'शक्ति कमी'],
                'hindi_roman': ['kamjori', 'thakan', 'thakavat', 'kamjor lagna', 'durbalata', 'shakti kami'],
                'bengali': ['দূর্বলতা', 'ক্লান্তি', 'অবসাদ', 'শক্তি নেই', 'ক্লান্ত লাগছে'],
                'bengali_roman': ['durbolata', 'klanti', 'abosad', 'shakti nei', 'klanto lagche'],
                'tamil': ['பலவீனம்', 'சோர்வு', 'களைப்பு', 'வலிமை இல்லை'],
                'tamil_roman': ['palaveenaam', 'sorvu', 'kalaippu', 'valimai illai'],
                'telugu': ['బలహీనత', 'అలసట', 'శక్తిలేకపోవడం', 'అలిసిపోవడం'],
                'telugu_roman': ['balaheenat', 'alasata', 'shaktilekapoadam', 'alisipovadam'],
                'marathi': ['अशक्तपणा', 'दुर्बलता', 'कमकुवत', 'थकवा'],
                'marathi_roman': ['ashaktapana', 'durbalata', 'kamkuvat', 'thakva'],
                'gujarati': ['નબળાઈ', 'થાક', 'કમજોરી', 'શક્તિ નથી'],
                'gujarati_roman': ['nabai', 'thak', 'kamjori', 'shakti nathi'],
                'kannada': ['ದೌರ್ಬಲ್ಯ', 'ಆಯಾಸ', 'ಶಕ್ತಿ ಇಲ್ಲ', 'ಬಲ ಇಲ್ಲ'],
                'kannada_roman': ['daurbalya', 'ayasa', 'shakti illa', 'bala illa'],
                'malayalam': ['ബലക്ഷയം', 'ക്ഷീണം', 'തളർച്ച', 'ശക്തി ഇല്ല'],
                'malayalam_roman': ['balakshayam', 'ksheenam', 'thalarcha', 'shakti illa'],
                'punjabi': ['ਕਮਜ਼ੋਰੀ', 'ਥਕਾਵਟ', 'ਸ਼ਕਤੀ ਨਹੀਂ', 'ਕਮਜ਼ੋਰ'],
                'punjabi_roman': ['kamjori', 'thakavat', 'shakti nahin', 'kamjor'],
                'severity': 'Low'
            },
            
            'breathing_difficulty': {
                'english': ['breathless', 'breathing problem', 'shortness of breath', 'difficulty breathing', 'hard to breathe', 'chest tightness'],
                'hindi_devanagari': ['सांस लेने में कठिनाई', 'सांस फूलना', 'दम फूलना', 'सांस की कमी', 'छाती में दम घुटना'],
                'hindi_roman': ['sans lene me kathinai', 'sans fulna', 'dam fulna', 'sans ki kami', 'chati me dam ghutna'],
                'bengali': ['শ্বাসকষ্ট', 'নিঃশ্বাস নিতে কষ্ট', 'হাঁপানি', 'দম বন্ধ লাগা'],
                'bengali_roman': ['shaskashta', 'nisshash nite kashta', 'hapani', 'dam bandha laga'],
                'tamil': ['மூச்சுத் திணறல்', 'சுவாசக் கஷ்டம்', 'மூச்சு வாங்கல்'],
                'tamil_roman': ['moochuth thinaral', 'suvasak kashtam', 'moochu vangal'],
                'telugu': ['ఊపిరి ఆడకపోవడం', 'శ్వాస కష్టం', 'ఊపిరి తీసుకోలేకపోవడం'],
                'telugu_roman': ['oopiri aadakapoadam', 'shwaasa kashtam', 'oopiri teesukoleka poadam'],
                'marathi': ['श्वासाची कमतरता', 'धाप लागणे', 'गुदमरणे'],
                'marathi_roman': ['shwasachi kamtarta', 'dhap lagne', 'gudmarne'],
                'gujarati': ['શ્વાસ લેવામાં તકલીફ', 'દમ ફૂલવો', 'છાતીમાં તકલીફ'],
                'gujarati_roman': ['shwas levama taklif', 'dam fulvo', 'chatima taklif'],
                'kannada': ['ಉಸಿರಾಟದ ತೊಂದರೆ', 'ಉಸಿರುಗಟ್ಟುವಿಕೆ', 'ಎದೆಯಲ್ಲಿ ಬಿಗಿತ'],
                'kannada_roman': ['usiraata tondare', 'usirugattuvike', 'edeyalli bigita'],
                'malayalam': ['ശ്വാസതടസ്സം', 'ശ്വസിക്കാൻ ബുദ്ധിമുട്ട്', 'നെഞ്ച് ഞെരിവ്'],
                'malayalam_roman': ['shvasathadassam', 'shvasikkan buddhimuttu', 'nenj njeriv'],
                'punjabi': ['ਸਾਹ ਲੈਣ ਵਿੱਚ ਤਕਲੀਫ਼', 'ਦਮ ਫੁੱਲਣਾ', 'ਸਾਹ ਚੜਨਾ'],
                'punjabi_roman': ['saah lain vich takleef', 'dam phullna', 'saah charna'],
                'severity': 'High'
            },
            
            'nausea': {
                'english': ['nausea', 'nauseous', 'feel sick', 'sick feeling', 'queasiness', 'feel like vomiting'],
                'hindi_devanagari': ['मतली', 'जी मिचलाना', 'उबकाई', 'जी घबराना', 'दिल उछलना'],
                'hindi_roman': ['matli', 'ji michalna', 'ubkai', 'ji ghabrana', 'dil uchalna'],
                'bengali': ['বমি ভাব', 'জি গুলিয়ে আসা', 'বমি বমি লাগা', 'বুক জ্বালা'],
                'bengali_roman': ['bomi bhaav', 'ji guliye asha', 'bomi bomi laga', 'buk jwala'],
                'tamil': ['குமட்டல்', 'வாந்தி உணர்வு', 'வயிற்றுக்கசப்பு'],
                'tamil_roman': ['kumattal', 'vanthi unarvu', 'vaiyatrukasappu'],
                'telugu': ['వాంతిభావం', 'అసహ్యం', 'కిరుకుతిన్నట్లు'],
                'telugu_roman': ['vantibhaavam', 'asahyam', 'kirukutinnattlu'],
                'marathi': ['मळमळ', 'जी मळमळणे', 'उलट्या सारखे वाटणे'],
                'marathi_roman': ['malmal', 'ji malmalne', 'ultya sarakhe vatne'],
                'gujarati': ['ઉબકાવો', 'જી ઘબરાવો', 'ઉલટી જેવું લાગવું'],
                'gujarati_roman': ['ubkavo', 'ji ghabravo', 'ulti jevu lagvu'],
                'kannada': ['ವಾಂತಿ ಭಾವ', 'ಜೀರ್ಣ ಸಮಸ್ಯೆ', 'ಉಸಿರಾಟದ ತೊಂದರೆ'],
                'kannada_roman': ['vanti bhaava', 'jeerna samasye', 'usiraata tondare'],
                'malayalam': ['ഓക്കാന വരിക', 'വേണ്ടാത്ത തോന്നല്', 'കുമിള വരിക'],
                'malayalam_roman': ['okkana varika', 'vendatha thonnal', 'kumila varika'],
                'punjabi': ['ਜੀ ਮਿਚਲਾਣਾ', 'ਉਬਕਾਈ', 'ਦਿਲ ਘਬਰਾਣਾ'],
                'punjabi_roman': ['ji michalna', 'ubkai', 'dil ghabrana'],
                'severity': 'Medium'
            }
        }
    
    def _initialize_language_patterns(self) -> Dict[str, str]:
        """Language detection patterns"""
        return {
            'hindi_devanagari': r'[\u0900-\u097F]+',
            'bengali': r'[\u0980-\u09FF]+',
            'tamil': r'[\u0B80-\u0BFF]+',
            'telugu': r'[\u0C00-\u0C7F]+',
            'marathi': r'[\u0900-\u097F]+',
            'gujarati': r'[\u0A80-\u0AFF]+',
            'kannada': r'[\u0C80-\u0CFF]+',
            'malayalam': r'[\u0D00-\u0D7F]+',
            'punjabi': r'[\u0A00-\u0A7F]+',
        }
    
    def detect_language(self, text: str) -> List[str]:
        """Detect languages present in the text"""
        detected_languages = ['english']  # English is always included
        
        for language, pattern in self.language_patterns.items():
            if re.search(pattern, text):
                detected_languages.append(language)
        
        # Check for Roman script patterns
        if any(word in text.lower() for word in ['bukhar', 'sir', 'dard', 'pet', 'ulti', 'khansi']):
            detected_languages.append('hindi_roman')
        
        return detected_languages
    
    def detect_symptoms_multilingual(self, message: str) -> Tuple[List[Dict], str]:
        """Enhanced multilingual symptom detection"""
        message_lower = message.lower()
        detected_symptoms = []
        max_severity = 'Low'
        detected_languages = self.detect_language(message)
        
        # Search through all symptom categories
        for symptom_name, symptom_data in self.symptom_database.items():
            symptom_found = False
            confidence = 0.0
            
            # Check each language variant
            for language in detected_languages:
                if language in symptom_data:
                    keywords = symptom_data[language]
                    for keyword in keywords:
                        if keyword.lower() in message_lower:
                            symptom_found = True
                            # Higher confidence for longer, more specific keywords
                            keyword_confidence = 0.7 + (len(keyword) * 0.02)
                            confidence = max(confidence, min(1.0, keyword_confidence))
                            break
                
                if symptom_found:
                    break
            
            if symptom_found:
                # Avoid duplicate symptoms
                if symptom_name not in [s['name'] for s in detected_symptoms]:
                    severity = symptom_data['severity']
                    detected_symptoms.append({
                        'name': symptom_name,
                        'severity': severity,
                        'confidence': confidence,
                        'languages_detected': detected_languages
                    })
                    
                    # Update max severity
                    if severity == 'High':
                        max_severity = 'High'
                    elif severity == 'Medium' and max_severity != 'High':
                        max_severity = 'Medium'
        
        # Return default if no symptoms detected
        if not detected_symptoms:
            detected_symptoms = [{'name': 'general_illness', 'severity': 'Low', 'confidence': 0.5, 'languages_detected': detected_languages}]
        
        return detected_symptoms, max_severity
    
    def get_multilingual_response(self, primary_language: str, message: str) -> str:
        """Generate response in detected primary language"""
        responses = {
            'english': "Thank you for your health report. Our system has analyzed your symptoms.",
            'hindi_devanagari': "आपकी स्वास्थ्य रिपोर्ट के लिए धन्यवाद। हमारे सिस्टम ने आपके लक्षणों का विश्लेषण किया है।",
            'hindi_roman': "Aapki swasthya report ke liye dhanyawad. Hamare system ne aapke lakshano ka vishleshan kiya hai.",
            'bengali': "আপনার স্বাস্থ্য রিপোর্টের জন্য ধন্যবাদ। আমাদের সিস্টেম আপনার লক্ষণগুলি বিশ্লেষণ করেছে।",
            'tamil': "உங்கள் ஆரோக்கிய அறிக்கைக்கு நன்றி। எங்கள் அமைப்பு உங்கள் அறிகுறிகளை பகுப்பாய்வு செய்துள்ளது।",
            'telugu': "మీ ఆరోగ్య నివేదిక కోసం ధన్యవాదాలు. మా సిస్టమ్ మీ లక్షణాలను విశ్లేషించింది।",
            'marathi': "तुमच्या आरोग्य अहवालाबद्दल धन्यवाद. आमच्या सिस्टमने तुमच्या लक्षणांचे विश्लेषण केले आहे।",
            'gujarati': "તમારા સ્વાસ્થ્ય રિપોર્ટ માટે આભાર. અમારી સિસ્ટમે તમારા લક્ષણોનું વિશ્લેષણ કર્યું છે।",
            'kannada': "ನಿಮ್ಮ ಆರೋಗ್ಯ ವರದಿಗೆ ಧನ್ಯವಾದಗಳು. ನಮ್ಮ ಸಿಸ್ಟಮ್ ನಿಮ್ಮ ಲಕ್ಷಣಗಳನ್ನು ವಿಶ್ಲೇಷಿಸಿದೆ।",
            'malayalam': "നിങ്ങളുടെ ആരോഗ്യ റിപ്പോർട്ടിനു നന്ദി. ഞങ്ങളുടെ സിസ്റ്റം നിങ്ങളുടെ ലക്ഷണങ്ങൾ വിശകലനം ചെയ്തു।",
            'punjabi': "ਤੁਹਾਡੀ ਸਿਹਤ ਰਿਪੋਰਟ ਲਈ ਧੰਨਵਾਦ। ਸਾਡੇ ਸਿਸਟਮ ਨੇ ਤੁਹਾਡੇ ਲੱਛਣਾਂ ਦਾ ਵਿਸ਼ਲੇਸ਼ਣ ਕੀਤਾ ਹੈ।"
        }
        
        return responses.get(primary_language, responses['english'])

# Global instance for easy import
enhanced_multilingual_detector = EnhancedMultilingualSymptomDetector()