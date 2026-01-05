# RPM — Document + Face KYC (Flask)

RPM is a Flask-based prototype for document-based KYC (Know Your Customer) and face verification.  
It supports uploading identity documents (Aadhar, PAN, DL, Passport), extracts text/QR data from them, performs a phone OTP check, and verifies that the photos on the documents match a live or uploaded face image using a CNN model (VGG16-based pipeline).

## Key features

- Document upload endpoints (Aadhar, Passport, PAN, Driving Licence).
- OCR and field extraction for Aadhar / PAN / DL.
- QR extraction and Aadhar <-> QR cross-validation.
- Phone OTP generation and verification (SMS provider config required).
- Face extraction from documents using Haar cascade.
- Face verification using a VGG16-based binary classifier saved as `sface_recog.h5`.
- Optional webcam/video-based face capture/verification flow.
- Simple HTML templates (Flask `templates/`) to interact with the flows.

---

## Repository structure (high level)

- app.py — main Flask application and routes (upload, OTP, video KYC).
- model.py — model training and inference utilities (VGG16-based).
- face_capture.py — routines to capture face images (webcam utility).
- doc_Scan.py — document scanning utilities (image processing).
- get_aadhar_text.py — Aadhar OCR / extraction logic.
- get_pan_data.py — PAN OCR / extraction logic.
- get_license_data.py — Driving licence OCR / extraction logic.
- get_qr_details.py — QR code extraction from Aadhar.
- send_otp.py — OTP generation / SMS integration (configure SMS provider).
- haarcasacde_facefrontal_default.xml — Haar cascade used for face detection.
- sface_recog.h5 — pretrained Keras model used by the app (large binary).
- images/ — storage for uploaded images and intermediate files.
- faces/ — training / test images used by model (faces/train, faces/test).
- requirements.txt — Python dependencies.
- templates/ — Flask HTML templates.

(There are additional files and a virtualenv-like `OTP/env` folder in the repository — consider removing environment binaries from the repo and using a clean requirements file / venv.)

---

## Requirements

- Python 3.8+ recommended
- Dependencies in `requirements.txt` (install via pip)
  - Flask, OpenCV (cv2), TensorFlow / Keras, pytesseract (if OCR used), fuzzywuzzy, flask_session, requests, etc.

Install dependencies (recommended inside a virtualenv):

```bash
python -m venv venv
source venv/bin/activate     # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Note: The repository includes a lot of files from a Python environment under `OTP/env/` — you do not need to use these. Use `requirements.txt` to set up a fresh virtual environment.

---

## Quick start (run the app)

1. Ensure dependencies are installed.
2. Place/verify the following files are present:
   - `haarcasacde_facefrontal_default.xml`
   - `sface_recog.h5` (model) — if you want to skip training.
3. Start the Flask app:

```bash
python app.py
```

4. Open a browser and go to: `http://127.0.0.1:5000/`

Flows:
- Upload documents at the KYC upload page (`/kyc`) — Aadhar is required for phone extraction.
- OTP flow triggers SMS — configure `send_otp.py` with your SMS provider / API keys.
- After OTP, you can perform the video face verification (`/kyc_video`) or the image-based verification flow.

---

## Training / Retraining the face model

The model pipeline uses VGG16 as a feature extractor and a small binary head. The model code expects the image dataset in:

- `faces/train/<class_folders>`
- `faces/test/<class_folders>`

To train:

- Provide training images in the above folders (binary classes expected).
- From Python, call the training routine (see `model.py`):

```python
# from a Python REPL or script
from model import make_model
make_model.train_model()
```

This will save `sface_recog.h5` and the subsequent verification code reads that file.

Caveats:
- `model.py` in the repo contains methods declared without `self` inside a class (static-like). You may want to refactor to a clearer API (class methods or standalone functions).
- Training currently runs only for a few epochs in the provided snippet (epochs=3). Adjust parameters for real training.

---

## Important implementation notes & known issues

While exploring the code, I observed a few items you should be aware of:

- Typo / mismatch:
  - `app.py` checks for `'sface_recong.h5'` in one place and uses `sface_recog.h5` elsewhere — this will cause a mismatch. Standardize the filename to `sface_recog.h5`.
- The `make_model` class in `model.py` defines functions without `self` and calls `start()` directly (design needs cleanup).
- In `app.py`, there are uses of `is` for empty tuple comparison (`if faces is (): ...`) — this is not reliable; use `if len(faces) == 0:` or `if faces is None:` depending on the return value.
- The repository contains `OTP/env/` with many packaged files. Those are likely environment artifacts and should be removed (or added to `.gitignore`) to reduce repository size.
- `sface_recog.h5` is large (~59 MB in the repository) — consider using Git LFS if you need to keep large models under version control.
- `send_otp.py` likely needs API credentials / configuration to work — check the file to configure your SMS provider.

---

## Security & Privacy

- This project processes sensitive identity documents and personal data (phone numbers, document scans). Use with care.
- Do NOT commit real personal data or API keys to the public repository.
- If deploying, secure the app (HTTPS, authentication, proper request validation) and obey local laws/regulations for storing personal ID data.

---

## Contributing

- If you want to contribute:
  - Clean up the model code to make training/inference APIs clearer.
  - Move environment/vendor files out of the repo and keep `requirements.txt` as the canonical dependency list.
  - Add a LICENSE file.
  - Add tests and CI to validate the main flows.

---

## Suggested next improvements

- Refactor `model.py` to a clean class or functional API and document training parameters.
- Move OTP/SMS config to environment variables and document setup.
- Add automated unit/integration tests.
- Add Dockerfile for consistent development/runtime environment.
- Add README sections for each module with examples for maintainers.

---

## License & Credits

- No license file detected in the repository. If you intend to open-source this project, add a LICENSE (MIT/Apache-2.0 or other).
- Acknowledge used libs: TensorFlow/Keras, OpenCV, Flask, pytesseract (if used), fuzzywuzzy, etc.

---

If you want, I can:
- Generate a cleaned, improved README variation tuned to a target audience (developer vs end-user).
- Create a PR that replaces the repository's README with this content.
- Help refactor `model.py` and fix the filename / small bugs so the app runs smoother.

Which would you like me to do next?

**STEPS**
1)Home page. Click start to go ahead
![image](https://user-images.githubusercontent.com/66548981/112753999-bfa6b600-8ff7-11eb-8a15-48fe7c71be79.png)

2)Upload Documents. Here we take the documents from user in jpg format. The documents should be clear.
![image](https://user-images.githubusercontent.com/66548981/112754031-e5cc5600-8ff7-11eb-8ecf-3819c1a13f57.png)
 
3)OTP Verfication. Otp send on the number
![image](https://user-images.githubusercontent.com/66548981/112754116-54111880-8ff8-11eb-8f17-d5af647a2bd5.png)

4)Video KYC. On pressing start, the program will click images of the user and a create a CNN model.
![image](https://user-images.githubusercontent.com/66548981/112754139-6db26000-8ff8-11eb-8bee-8699fefb306f.png)

Clicking images 
![image](https://user-images.githubusercontent.com/66548981/112754180-92a6d300-8ff8-11eb-83e2-3320dfbe3852.png)

Making model
![image](https://user-images.githubusercontent.com/66548981/112754237-ca157f80-8ff8-11eb-841d-471ccc264fe3.png)

After test image
![image](https://user-images.githubusercontent.com/66548981/112754339-38f2d880-8ff9-11eb-94ed-85538a634bf3.png)
