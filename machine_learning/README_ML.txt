What you (probably) need before running (on Windows10): 

Anaconda Virtual Environment with
	Tensorflow(CPU)
	Keras 
-> Tutorial for Setup from Scratch: https://www.youtube.com/watch?v=ujTCoH21GlA&list=PLzMcBGfZo4-mP7qA9cagf68V06sko5otr


Directories:

machine_learning:
      |____model:

Files:

Build Model: 
>>>> builds model from given data and saves it to RoboDoc/machine_learning/model
>>>> Functions:
	 def df_to_dataset(dataframe, label_index, shuffle=True, batch_size=32) -> Converts a given Pandas Dataframe to a tensorflow dataset and shuffles Data.
	 def show_batch(dataset) -> Print function: Outputs given dataset on Console
	 def encode_labels(df, label_index) -> changes random labels to labels in [0, #Labels-1]. Returns new labels, dictionary with old and new labels, count of different labels
	 def save_model(model) -> saves built model into given directory
	 def export_label_dict(label_dict)
__main__ def build_model() -> here you can modify batchsize, epoch count, the used data,  size of train-, test- and validation datasets, Model layers


Robo Doctor:
>>>> Creates RoboDoctor Class instance which then generates the patients predicted Diseases through the model and returns them an an Array with Probabilities
	
Symptom Suggestor:	
>>>> Takes (input Symptoms) and (all Symptoms)\(input Symptoms): 
		look up Patiens who have the same Symptoms as input and lack the same Symptoms
			count the three most common Symptoms between these patients
				return them
	
