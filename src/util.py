import tensorflow as tf


# function to delete selected symptoms from data DataFrame
def don_t_show_selected_symptoms(symptoms, data):

    for s in symptoms:
        data.drop(data.loc[data['ID'] == s].index, inplace=True)
    return data


def count_symptoms_per_country(list):          #walk trough list and count duplicates
    results =[]
    while list:
        i = list.pop(0)     #get first country, symptom pair
        elem = [i[1]]       #save symptom in first position
        count = 1           #initialise number of symptoms with 0
        cache = list.copy() #copy list
        while cache:        #while list is not empty
            if(i==cache.pop(0)):    #compare if loop element is equal
                count = count +1    # add one to counter
                list.remove(i)      #remove every counted element from list
        elem.append(count)          #append number of counted elements
        elem.append("Symptom: <b>"+i[0]+"</b><br>Number: <b>"+str(count)+"</b>")    #add tooltip description
        results.append(elem)
    return results


def find_most_common_symptom_per_country(list):          #walk trough list and find most common symptom for country
    results =[]
    while list:
        i = list.pop(0)     #get first element of list
        elem = i
        country = i[0]      #and its country
        count = i[1]        #and its number of occurence
        cache = list.copy()
        while cache:
            check = cache.pop(0)    #get comparision element
            if(country==check[0] and count<check[1]):
                elem = check            #count is larger, replace max
            if (country == check[0]):
                list.remove(check)      #remove counted element from list
        results.append(elem)
    return results

def find_most_common_symptom_per_age(list):          #walk trough list and find max count for age
    results =[]
    while list:             #while list not empty
        i = list.pop(0)     #get first
        cache = list.copy()
        count = 1
        while cache:
            check = cache.pop(0)    #get comparision element
            if(i==check):           #if equal, count +1
                count +=1
                list.remove(check)
        results.append([i,count])   # append Symptom, count
    max = 0         #number of most common symptom is 0
    maxsymp =""     #initialise name of most common symptom
    for i in results:
        if i[1]>max:    #search for maximum
            max = i[1]
            maxsymp=i[0]    #rewrite maximum
    return [maxsymp,max]