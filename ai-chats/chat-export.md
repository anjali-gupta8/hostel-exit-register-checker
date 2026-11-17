# AI Chat Export — Hostel Exit Register Checker

## Overview

This file documents how AI was used during the development of this project. 
The assignment requires transparency about AI usage, and I'm including this 
to show exactly what AI helped with and what it didn't.

## What AI Helped With

### 1. Code Generation
- AI wrote the core Streamlit application (`app.py`)
- AI helped structure the CSV parsing and validation logic
- AI generated the missing-field detection functions
- AI created the download report functionality

### 2. Data Extraction
- AI helped read the handwritten register from the photograph
- I verified each extracted entry against the original photo
- Some entries required my manual correction where handwriting was unclear

### 3. Documentation
- AI helped structure `research.md` and format the documentation
- AI drafted the `README.md` template
- AI created the `fieldwork.md` structure with placeholders for my actual observations

### 4. Photo Privacy
- AI wrote the Python script to blur faces and sensitive information in photos
- I verified the redacted photos to make sure no private data was readable

## What AI Did NOT Do

- AI did not go to the hostel gate or talk to the security guard
- AI did not collect the data — I photographed the register myself
- AI did not write the reflection (that's my own writing)
- AI did not take the fieldwork photographs
- AI did not decide what the problem was — I observed it myself

## Tools Used

- **Antigravity (Claude)** — Code generation, documentation help, data extraction from photos
- **Python + Streamlit** — Application framework
- **Pillow (PIL)** — Photo redaction

## Note

The full AI conversation is available in this folder:
- [full-conversation.md](full-conversation.md) — Complete timeline of what AI helped with and what it didn't

The conversation shows the back-and-forth process of building the tool, including mistakes and corrections.
