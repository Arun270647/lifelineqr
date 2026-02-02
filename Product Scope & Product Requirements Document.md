> **Product** **Scope** **&** **Product** **Requirements** **Document**
>
> **Project** **Name:** **LifeLine** **QR** **–** **Emergency**
> **Medical** **Information** **Website**

Prepared For: Mr. Purvaj Sai

Prepared By: Track My Academy – Dev Ops

**1.** **Project** **Overview**

LifeLine QR is a small-scale medical information web project designed to
provide instant access to a patient’s critical health details during
emergencies using a QR code. The platform connects patients and doctors
through a simple login system and also includes a basic merchandise
module for QR cards.

This project is intentionally scoped for a minimalistic range, and is
implemented strictly using HTML, CSS, and Vanilla JavaScript only.

**2.** **Problem** **Statement**

In emergency situations, first responders or doctors may not know a
patient’s: - Blood group

\- Allergies

\- Existing medical conditions - Emergency contact details

Patients also struggle to carry medical documents everywhere. LifeLine
QR solves this by storing essential medical data online and linking it
to a QR code that can be scanned instantly.

**3.** **Project** **Scope**

**<u>Included Features</u>**

> ● Patient and Doctor registration & login ● Patient medical profile
> creation
>
> ● QR code generation for patients
>
> ● Emergency-only information display for public users ● Full medical
> view for logged-in doctors
>
> ● Medical document upload (basic)
>
> ● Simple merchandise module (QR cards)

**<u>Excluded Features</u>**

> ● Mobile application ● Real-time payments
>
> ● Real email / SMS services ● Hospital integrations
>
> ● Backend server

**4.** **Technology** **Constraints**

**<u>Mandatory Tech Stack:</u>**

> 1\. HTML – Page structure 2. CSS – Styling
>
> 3\. JavaScript – Functionality 4. Data Storage and Handling: 5. SQL
> (Local-System-Storage)

**5.** **User** **Roles**

**<u>5.1 Patient</u>**

> ● Register and login
>
> ● Enter and update medical details
>
> ● Upload medical records (PDF / JPG / PNG) ● Receive a unique QR code
>
> ● Order QR card merchandise

**<u>5.2 Doctor</u>**

> ● Register and login
>
> ● View patient information after QR scan ● Access uploaded medical
> documents
>
> ● Read-only access

**<u>5.3 Admin (Logical Role)</u>** ● Reset passwords

> ● Verify doctor accounts

**6.** **High-Level** **Workflow**

> 1.User visits the website
>
> 2.Chooses Doctor or Patient registration
>
> 3.Patient completes registration and receives QR code 4.QR can be
> printed on a card
>
> 5.When QR is scanned:
>
> Doctor logged in → Full medical profile Guest user → Emergency details
> only

**7.** **Page-Wise** **Requirements**

**<u>Page 1: Home Page</u>** **Purpose:** Entry page **Features:**

\- Navigation bar - Home

\- About - Login

\- Sign Up

\- Doctors List - Merchandise - Contact

**Short** **description** **of** **the** **website** **purpose** -
Centered Login & Sign Up buttons - “Upload Medical Records” button
(redirects to login if not authenticated)

**<u>Page 2: Role Selection Page</u>** **Button:** Register as Doctor
**Button:** Register as Patient

**<u>Page 3: Doctor Registration Page</u>** **Form** **Fields:**

\- Name - Age

\- Specialization

\- Hospital / Clinic

\- Years of experience

\- Working hours - Contact number

\- Email (used as login) **Actions:** - Submit - Back

**Logic:** - Temporary password generation (simulated)

**<u>Page 4: Patient Registration Page</u>** **Form** **Fields:**

\- Name - Age

\- Blood group - Allergies

\- Medical conditions - Regular medications - Address

\- Emergency contact numbers - Email (used as login)

**On** **Submit:**

\- Save patient details

\- Generate unique QR code - Redirect to login page

**<u>Page 5: Login Page</u>** **Fields:**

\- Email

\- Password

**Redirection:** - Patient → Patient Dashboard - Doctor → Doctor
Dashboard

**<u>Page 6: Patient Dashboard</u>** **Features:**

\- View & edit personal information - Upload medical documents

\- Add document description - Display generated QR code

\- Order QR card merchandise

**<u>Page 7: Doctor Dashboard</u>** **Features:**

\- Enter / scan patient QR code ID - View patient details

\- Access uploaded medical records

**<u>Page 8: Doctors List Page</u>** List of registered doctors

Display specialization and contact number

**<u>Page 9: Merchandise Page</u>** **Products:**

\- QR medical card (basic) **Features:**

\- Product details

\- Order form (address & QR selection)

\- Order confirmation message (simulated)

**<u>Page 10: Forgot Password Page</u>** Enter registered email

Reset password (simulated)

**<u>Page 11: Contact Us Page</u>** Support email

Contact number Feedback form

**8.** **QR** **Code** **Access** **Logic** One QR code per patient

QR redirects to patient profile page **Access** **Rules:**

\- Logged-in Doctor → Full medical data - Guest user → Emergency-only
details: - Name - Blood group - Allergies - Emergency contact

**9.** **Data** **Storage** **Design**

> 1\. Users (patients and doctors) 2. Medical records
>
> 3\. QR-to-patient mapping 4. Orders (merchandise)
>
> 5\. (All stored using LocalStorage / IndexedDB)

**10.** **UI** **/** **Design** **Guidelines** ● Simple, minimal UI

> ● Medical color palette (blue, white, red accents) ● Font: Arial
>
> ● Desktop browser focused

**11.** **Conclusion**

LifeLine QR is a low-cost, functional medical web project that
demonstrates how emergency medical information can be accessed quickly
using QR technology, while remaining simple enough for academic
evaluation.
