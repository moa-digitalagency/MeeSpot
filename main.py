#
# MeetSpot
# MOA Digital Agency LLC
# Par : Aisance KALONJI
# Mail : moa@myoneart.com
# www.myoneart.com
#

from backend import create_app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

# Route pour la documentation API
@app.route('/docs/api')
def api_docs():
    from flask import send_file
    return send_file('static/pages/api-docs.html')
