IBVAP — Intelligent Border Video Analytics Platform
Team: CODE AURAS
Institution: Seshadri Rao Gudlavalleru Engineering College
Hackathon: CODEQUEST: National Tech Hackathon 2026
Overview
IBVAP is a prototype for video-based person detection and restricted-zone monitoring. This repository currently contains an educational video-processing application that uses a pretrained YOLO model and OpenCV to annotate uploaded videos.

The prototype also calculates SHA-256 hashes for the uploaded video and generated output, and exports a JSON event report. These hashes help identify whether a file has changed; they do not, by themselves, prove who created a file or provide blockchain-based storage.
Features currently implemented
- Upload an MP4, AVI, MOV, or MKV video through a Streamlit interface.
- Detect people with the pretrained Ultralytics YOLO11n model.
- Draw an adjustable rectangular demo restricted zone.
- Mark detected people whose bounding-box center falls inside that zone.
- Export an annotated MP4 video.
- Calculate SHA-256 hashes for the input and output files.
- Download a JSON report containing frame-based alert events.
Technology
- Python
- Streamlit
- Ultralytics YOLO
- OpenCV
- SHA-256 (hashlib)
Project structure
IBVAP-Intelligent-Border-Video-Analytics/
├── app.py
├── requirements.txt
├── README.md
└── .gitignore
Run locally
1. Clone the repository
git clone https://github.com/guruVemula61-cmyk/IBVAP-Intelligent-Border-Video-Analytics.git
cd IBVAP-Intelligent-Border-Video-Analytics
2. Create and activate a virtual environment (recommended)
Windows:
python -m venv .venv
.venv\Scripts\activate
macOS / Linux:
python3 -m venv .venv
source .venv/bin/activate
3. Install dependencies
python -m pip install --upgrade pip
pip install -r requirements.txt
4. Start the application
streamlit run app.py
Open the local URL printed by Streamlit in your browser, upload a short test video, adjust the demo zone, and select Run IBVAP analysis.

The first run may download the pretrained YOLO model. An internet connection is needed for that initial download unless the model file is already available locally.
Important prototype limitations
- The current application uses a pretrained YOLO11n model; it does not include a custom-trained 6-channel RGB–thermal fusion model.
- The restricted zone is a user-adjustable rectangle, not a perspective-calibrated polygon.
- Alerts are frame-based detections, not verified real-world intrusion events. Human review is required.
- ByteTrack person tracking, RGB–thermal synchronization, Ed25519 signing, Hyperledger Fabric integration, user authentication, and a multi-camera live CCTV connection are not implemented in this initial version.
- SHA-256 hashes are generated locally. No blockchain transaction or independent timestamp authority is used by this version.
Responsible use
Use only video that you are authorized to process. Test with consented, non-sensitive footage where possible. This prototype is for learning and demonstration; it is not a certified surveillance or access-control system and should not be used as the sole basis for consequential decisions.
Team
CODE AURAS
Team Leader: Vemula Guru Prasad
