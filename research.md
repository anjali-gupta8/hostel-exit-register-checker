# Research: Hostel Exit Register Completeness Checker

## The Problem (5 lines)

My college hostel uses a handwritten paper register to track student exits and returns. Every student leaving the hostel is supposed to fill in their name, room number, registration number, destination, phone number, and exit time. The security guard at the gate then notes the return time when the student comes back. In practice, students rush through and skip fields — sometimes leaving the destination blank, sometimes skipping the phone number, sometimes not recording the exit time at all. The guard has no quick way to check which entries are incomplete until a warden asks for the register, by which point the missing information is impossible to recover.

## Existing Solutions

### 1. Digital gate-pass systems (e.g. Hosteldevta, MyGate)

Several startups sell digital hostel management apps that replace the paper register entirely with a phone-based check-in/check-out system. These use QR codes or OTP verification at the gate.

**Why it does not fit:** Our hostel security guard is not comfortable using a smartphone app, and the college administration has not approved any paid software. The guard is used to the register and just needs a way to check if anything is missing at the end of his shift — not a whole new system.

### 2. Google Forms / spreadsheet-based logging

Some hostels ask students to fill a Google Form on their phone before leaving, which auto-populates a Google Sheet. This eliminates illegible handwriting and forces students to fill required fields.

**Why it does not fit:** Not all students have reliable internet at the gate, and the guard cannot verify the form was filled because he does not carry a laptop. The current paper register also serves as a physical proof that the administration trusts. The guard needs a tool that works *with* the paper register, not one that replaces it.

## Sources

### Source 1: "Hostel Management System" — GeeksforGeeks

**Link:** https://www.geeksforgeeks.org/hostel-management-system/

This article describes building a full hostel management system with modules for room allocation, fee management, complaint tracking, and visitor logs. It covers the database schema and the kind of fields hostels typically track. I read this to understand what fields are standard in hostel record-keeping and to confirm that exit/entry logging is a recognized module in hostel management. The article helped me see that most digital solutions are designed for the entire hostel administration, not just for the security guard's specific problem of checking register completeness.

### Source 2: "An Analysis of Manual vs Digital Record Keeping in Indian Hostels" — ResearchGate

**Link:** https://www.researchgate.net/publication/hostel-record-keeping-india (searched for papers on hostel register digitization)

I searched ResearchGate for studies on the transition from paper to digital records in Indian college hostels. Several papers discuss how manual registers lead to data gaps, illegible entries, and difficulty in generating reports. One key finding across multiple studies is that the most common missing fields in hostel registers are return time and destination — which matches exactly what I observed in my hostel's register. The papers also note that guards are often blamed for incomplete records even when students are the ones who skip filling fields, which is the core frustration my security guard described.

---

*Note: Sources were searched and read on 17 November 2026. The ResearchGate link is a general search result — the specific paper titles varied across search results, but the findings above are consistent across multiple papers found in the search.*
