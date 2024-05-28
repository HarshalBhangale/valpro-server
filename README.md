# Property MastR Backend

This repository contains the backend for the Property MastR application, a property valuation tool. The backend is built using Flask and provides endpoints for user authentication and property valuation calculations.

## Table of Contents
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Endpoints](#endpoints)
- [License](#license)

## Features
- User authentication (login and registration)
- Property valuation calculations based on location and property type
- Integration with external APIs for geolocation

## Requirements
- Python 3.6+
- Flask
- Flask-CORS
- Pandas
- Werkzeug (for password hashing)
- Google Maps API key (for geolocation)

## Installation

**Clone the repository**:
   
   git clone https://github.com/NumberBoost/propmastr-backend.git
   cd propmastr-backend

**pip install -r requirements.txt**

**GOOGLE_MAPS_API_KEY=your_google_maps_api_key**

**python app.py**
