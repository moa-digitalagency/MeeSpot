#!/usr/bin/env python3
#
# MatchSpot - WSGI Configuration File
# MOA Digital Agency LLC
# Par : Aisance KALONJI
# Mail : moa@myoneart.com
# www.myoneart.com
#

import os
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

# Importer l'application Flask
from main import app

if __name__ == "__main__":
    app.run()
