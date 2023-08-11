# Database Files
This directory has data files from the live API at https://apimedic.com/apitest (no sandbox data)

### diseases_20_db.json and diseases_100_db.json
20 or 100 diseases with partially common symptoms. Every diseases has entries for all associated symptoms and
their probability of being expressed. Some symptoms, that are more secondary for a given disease don't 
have a probability specified at API Medic. For those the probability is -1 and the patient generator is 
responsible for how these are processed.

### patients_2000.csv
The Pandas Dataframe of 2000 patients generated for 20 diseases.

### label_dict.json
The Neural Network Model needs labels ranging from [0, n_labels).
Therefore the IDs of the diseases are translated to an int in this range.
This is the dictionary to translate back to disease ID.

### sample_patients.csv
A Pandas Dataframe with all possible symptoms and 2 rows. It is used to
create a patient in a format, that can be predicted by the neural network.

### issues.json
Mapping of name and ID for all issues in the API Medic database.

### symptoms.json
Mapping of name and ID for all symptoms in the API Medic database.