# youtube-slides-to-ppt
Convert YouTube video lecture frames into PowerPoint (PPT) and PDF slides automatically.
# 🎓 YouTube Video to Slides (PPT & PDF) Converter

यह एक ऑटोमेटेड Python टूल है जो किसी भी YouTube लेक्चर/क्लास वीडियो की बोर्ड स्लाइड्स और विजुअल नोट्स को सीधे **PPTX (.pptx)** और **PDF** फाइल में बदल देता है।

---

## ✨ मुख्य विशेषताएँ (Key Features)

* **बिना वीडियो डाउनलोड किए काम करता है:** YouTube स्ट्रीम से सीधे फ्रेम्स रीड करता है, जिससे इंटरनेट और स्टोरेज की बचत होती है।
* **स्मार्ट स्लाइड डिटेक्शन:** OpenCV की मदद से केवल तभी स्क्रीनशॉट लेता है जब स्क्रीन या बोर्ड का कंटेंट बदलता है (डुप्लिकेट इमेजेस अपने आप स्किप हो जाती हैं)।
* **GitHub Actions सपोर्ट:** बिना अपना कंप्यूटर/फोन चलाए, GitHub के फ्री क्लाउड सर्वर पर 1-क्लिक में पूरी वीडियो प्रोसेस करें।
* **ड्यूल आउटपुट:** एक साथ **PowerPoint (.pptx)** और **PDF** दोनों फाइलें तैयार मिलती हैं।

---

## 🚀 GitHub Actions से 1-Click में कैसे चलाएँ (Cloud Method)

अपने फोन या कंप्यूटर से बिना किसी कोडिंग के चलाने के लिए:

1. अपनी इस Repository के ऊपर **Actions** टैब पर जाएँ।
2. बाईं तरफ **Generate Slides from YouTube** पर क्लिक करें।
3. दाईं तरफ **Run workflow** बटन पर टैप करें।
4. इनपुट बॉक्स में अपना **YouTube Video URL** डालें और **Run workflow** दबा दें।
5. 1 से 2 मिनट में प्रोसेस पूरा होने के बाद रन पर क्लिक करें और नीचे **Artifacts** सेक्शन से **`lecture-slides`** (ZIP फ़ाइल) डाउनलोड कर लें।

---

## 💻 अपने कंप्यूटर पर लोकल रन करने का तरीका (Local Setup)

### 1. Requirements इंस्टॉल करें
```bash
pip install -r requirements.txt
