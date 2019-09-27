# Package importation
import numpy as np
import json
#import lxml
from keras.models import Sequential
from keras.layers import Dense

def Result(xml_1):
    #TASK 1
    
    # Data extraction
    list_type_id = [i for i in range(1, 9)] + [i for i in range(10, 20)] + [41, 42, 44, 45] + [i for i in range(49, 62)] + [74]
    dico_type_id = {list_type_id[i]:i for i in range(len(list_type_id))}    
    list_qualifier_id = [1, 2, 3, 4, 5, 6, 7, 8, 9, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 23, 24, 25, 26, 28, 29, 31, 32, 33, 35, 36, 37, 38, 55, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 89, 94, 100, 101, 107, 108, 113, 114, 120, 121, 122, 123, 124, 132, 133, 136, 137, 138, 139, 152, 153, 154, 155, 156, 157, 158, 159, 160, 167, 168, 169, 170, 173, 174, 175, 176, 177, 178, 179, 180, 181, 182, 183, 184, 185, 186, 187, 188, 191, 192, 195, 196, 210, 211, 214, 215, 217, 218, 223, 224, 225, 228, 232, 236, 237, 238, 239, 240, 241, 245, 254, 264, 265, 273, 274, 275, 278, 279, 280, 285, 286, 287, 296, 297, 298, 300, 314]
    dico_qualifier_id = {list_qualifier_id[i]:i for i in range(len(list_qualifier_id))}
    dico_qualifier_id_56 = {"Right":0, "Left":1, "Back":2, "Center":3}
    
    type_id_player = [0 for i in range(len(list_type_id))]
    positive_outcome_player = 0
    total_outcome_player = 0
    assist_player = 0
    keypass_player = 0
    qualifier_id_player = [0 for i in range(len(list_qualifier_id))]
    qualifier_id_56_player = [0, 0, 0, 0]
    
    type_id_team = [0 for i in range(len(list_type_id))]
    positive_outcome_team = 0
    total_outcome_team = 0
    assist_team = 0
    keypass_team = 0
    qualifier_id_team = [0 for i in range(len(list_qualifier_id))]
    qualifier_id_56_team = [0, 0, 0, 0]
    
    considered_team = 0
    
    for Event in xml_1.xpath("/Games/Game/Event"):
        keys = Event.keys()
        if (("player_id" in keys) and ("team_id" in keys)):
            if (int(Event.get("player_id")) == 1):
                considered_team = int(Event.get("team_id"))
    
    for Event in xml_1.xpath("/Games/Game/Event"):
        keys = Event.keys()    
        if ("team_id" in keys):
            if (int(Event.get("team_id")) == considered_team):
                if ("type_id" in keys):
                    if (int(Event.get("type_id")) in list_type_id):
                        type_id_team[dico_type_id[int(Event.get("type_id"))]] += 1
                if ("outcome" in keys):
                    if (Event.get("outcome") != ''):
                        positive_outcome_team += int(Event.get("outcome"))
                        total_outcome_team += 1
                if ("assist" in keys):
                    assist_team += 1
                if ("keypass" in keys):
                    keypass_team += 1
                for qualifier in Event.getchildren():
                    if ("qualifier_id" in qualifier.keys()):
                        if (qualifier.get("qualifier_id") != ''):
                            if (int(qualifier.get("qualifier_id")) in list_qualifier_id):
                                qualifier_id_team[dico_qualifier_id[int(qualifier.get("qualifier_id"))]] += 1
                            if (int(qualifier.get("qualifier_id")) == 56):
                                if ("value" in qualifier.keys()):
                                    if (qualifier.get("value") != ''):
                                        qualifier_id_56_team[dico_qualifier_id_56[qualifier.get("value")]] += 1
            if ("player_id" in keys):
                if (int(Event.get("player_id")) == 1):
                    if ("type_id" in keys):
                        if (int(Event.get("type_id")) in list_type_id):
                            type_id_player[dico_type_id[int(Event.get("type_id"))]] += 1
                    if ("outcome" in keys):
                        if (Event.get("outcome") != ''):
                            positive_outcome_player += int(Event.get("outcome"))
                            total_outcome_player += 1
                    if ("assist" in keys):
                        assist_player += 1
                    if ("keypass" in keys):
                        keypass_player += 1
                    for qualifier in Event.getchildren():
                        if ("qualifier_id" in qualifier.keys()):
                            if (qualifier.get("qualifier_id") != ''):
                                if (int(qualifier.get("qualifier_id")) in list_qualifier_id):
                                    qualifier_id_player[dico_qualifier_id[int(qualifier.get("qualifier_id"))]] += 1
                                if (int(qualifier.get("qualifier_id")) == 56):
                                    if ("value" in qualifier.keys()):
                                        if (qualifier.get("value") != ''):
                                            qualifier_id_56_player[dico_qualifier_id_56[qualifier.get("value")]] += 1
                                        
    data_task_1 = type_id_player + [positive_outcome_player/total_outcome_player, assist_player, keypass_player] + qualifier_id_player + qualifier_id_56_player + type_id_team + [positive_outcome_team/total_outcome_team, assist_team, keypass_team] + qualifier_id_team + qualifier_id_56_team
    data_task_1 = np.array(data_task_1).reshape((1, len(data_task_1)))
    
    # Dictionary of players id
    with open('dico_id.txt', 'r') as file:
        dico_id = json.load(file)
    
    # NN model
    model_task_1 = Sequential()
    model_task_1.add(Dense(500, input_dim=380, activation='relu'))
    model_task_1.add(Dense(233, activation='softmax'))
    model_task_1.load_weights("500_01")
    
    # Prediction
    id_prediction = model_task_1.predict(data_task_1)
    id_prediction = np.argmax(id_prediction, axis=1)[0]
    id_prediction = int(list(dico_id.keys())[id_prediction])
    
    
    # TASK 2
    
    # Data extraction
    last_ten_events = []
    for Event in xml_1.xpath("/Games/Game/Event"):
        keys = Event.keys()
        if (("type_id" in keys) and ("team_id" in keys) and ("x" in keys) and ("y" in keys)):
            if ((float(Event.get("x")) != 0.0) and (float(Event.get("y")) != 0.0)):
                last_ten_events.append([int(Event.get("type_id")), int(Event.get("team_id")), float(Event.get("x")), float(Event.get("y"))])
    
    same_team_1 = 0
    if (last_ten_events[-3][1] == last_ten_events[-1][1]):
        same_team_1 = 1
    same_team_2 = 0
    if (last_ten_events[-2][1] == last_ten_events[-1][1]):
        same_team_2 = 1
        
    feature_one_hot_1 = [0 for j in range(79)]
    feature_one_hot_1[last_ten_events[-3][0]-1] += 1
    feature_one_hot_2 = [0 for j in range(79)]
    feature_one_hot_2[last_ten_events[-2][0]-1] += 1
    feature_one_hot_3 = [0 for j in range(79)]
    feature_one_hot_3[last_ten_events[-1][0]-1] += 1
        
    data_task_2 = [same_team_1, same_team_2, last_ten_events[-3][2], last_ten_events[-3][3], last_ten_events[-2][2], last_ten_events[-2][3], last_ten_events[-1][2], last_ten_events[-1][3]] + feature_one_hot_1 + feature_one_hot_2 + feature_one_hot_3
    data_task_2 = np.array(data_task_2).reshape((1, len(data_task_2)))
    
    # NN model
    model_task_2 = Sequential()
    model_task_2.add(Dense(2000, input_dim=245, activation='relu'))
    model_task_2.add(Dense(2, activation='softmax'))
    model_task_2.load_weights("2000_01")
    
    # Prediction
    team_prediction = model_task_2.predict(data_task_2)
    team_prediction = np.argmax(team_prediction, axis=1)[0]
    if (team_prediction == 1):
        team_prediction = last_ten_events[-1][1]
    else :
        team_prediction = 1 - last_ten_events[-1][1]
        
    
    # TASK 3
        
    # Data extraction
    data_task_3 = [last_ten_events[-1][2], last_ten_events[-1][3], last_ten_events[-2][2], last_ten_events[-2][3], last_ten_events[-3][2], last_ten_events[-3][3], same_team_1, same_team_2] + feature_one_hot_1 + feature_one_hot_2 + feature_one_hot_3
    data_task_3 = np.array(data_task_3).reshape((1, len(data_task_3)))
    
    # NN model
    model_task_3 = Sequential()
    model_task_3.add(Dense(2500, input_dim=245, activation='relu'))
    model_task_3.add(Dense(2, activation='linear'))
    model_task_3.load_weights("2500_03")
    
    # Prediction
    xy_prediction = model_task_3.predict(data_task_3)
    x_prediction = xy_prediction[0, 0]
    y_prediction = xy_prediction[0, 1]
    
    # Make the csv
    prediction = [id_prediction, team_prediction, y_prediction, x_prediction]
    prediction = np.array(prediction).reshape((1, len(prediction)))
    np.savetxt("res_psgx.csv", prediction, fmt='%f', delimiter = ",")
    
    return(None)

