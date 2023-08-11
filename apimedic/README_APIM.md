Hier befinden sich alle Skripte die genutzt wurden um die Informationen über die Symptome und Krankheiten in unserer Datenbank abzurufen.

auth_data.py: Enthält die Accountdaten, die zur Authentifikation auf der Webseite genutzt wurden

api_request.py:  - get_auth_token: Erstellt aus Zugangsdaten ein Token, das in die URL eingefügt wird um den LogIn per Hand auf der Webseite zu überspringen 
		         - get_item: sendet eine Anfrage an die Webseite und gibt die Antwort zurück.
		         
data_request.py: Unused

database_builder.py: Ruft due FUntkionen aus api_request.py auf, sendet die tatsächlichen Anfragen, speichert die Antworten und bringt die .Json Dateien ins richtige Format

Der Ordnder data enthält Symptome und Krankheiten aus Testläufen mit wenigen Anfragen.