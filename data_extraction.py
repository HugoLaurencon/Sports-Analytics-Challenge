from lxml import etree
import numpy as np

id_first_match = 853139
id_last_match = 853328

def data_first_task(path_to_matches_directory):
    def one_match(path_to_matches_directory, match_index):
        events = []
        tree = etree.parse(path_to_matches_directory + "f24-24-2016-" + str(match_index) + "-eventdetails.xml")
        for event in tree.xpath("/Games/Game/Event"):
            liste_keys = event.keys()
            type_id = int(event.get("type_id"))
            if ("period_id" in liste_keys):
                period_id = int(event.get("period_id"))
            else:
                period_id = -1
            minute = int(event.get("min"))
            sec = int(event.get("sec"))
            if("player_id" in liste_keys):
                player_id = int(event.get("player_id"))
            else:
                player_id = -1
            team_id = int(event.get("team_id"))
            if ("outcome" in liste_keys):
                outcome = int(event.get("outcome"))
            else:
                outcome = -1
            if("assist" in liste_keys):
                assist=int(event.get("assist"))
            else:
                assist = 0
            if ("keypass" in liste_keys):
                keypass = int(event.get("keypass"))
            else:
                keypass = 0
            x = float(event.get("x"))
            y = float(event.get("y"))
            qualifiers = []
            for qualifier in event.getchildren():
                qualifiers_id = int(qualifier.get("qualifier_id"))
                if("value" in qualifier.keys()):
                    value = qualifier.get("value")
                else:
                    value = -1
                qualifiers.append([qualifiers_id, value])
            events.append([type_id, period_id, minute, sec, player_id, team_id, x, y, outcome, assist, keypass, qualifiers])
        
        play_time_first_half = max([event[2] for event in events if (event[1] == 1 and event[0] != 43)])
        play_time_second_half = max([event[2] for event in events if (event[1] == 2 and event[0] != 43)]) - 45
        
        players_quit_the_field = []
        players_enter_the_field = []
        for event in events:
            if (event[0] == 18):
                players_quit_the_field.append(event)
            elif (event[0] == 19):
                players_enter_the_field.append(event)
                
        players = set()
        for event in events:
            if (event[4] > -1):
                players.add(event[4])
        players = [player for player in players]
        
        dic_playerid_playtime = {}
        for player in players:
            dic_playerid_playtime[player] = play_time_first_half + play_time_second_half
            enters = (player in [event[4] for event in players_enter_the_field])
            quits = (player in [event[4] for event in players_quit_the_field])
            if (quits and not enters):
                event = [event for event in players_quit_the_field if event[4] == player][0]
                if (event[1] == 1):
                    dic_playerid_playtime[player] = event[2]
                elif (event[1] == 2):
                    dic_playerid_playtime[player] = event[2] - 45 + play_time_first_half
            elif (enters and not quits):
                event = [event for event in players_enter_the_field if event[4] == player][0]
                if (event[1] == 1):
                    dic_playerid_playtime[player] = play_time_first_half - event[2] + play_time_second_half
                elif (event[1] == 2):
                    dic_playerid_playtime[player] = play_time_second_half + 45 - event[2]
            elif (enters and quits):
                event_enters = [event for event in players_enter_the_field if event[4] == player][0]
                event_quits = [event for event in players_quit_the_field if event[4] == player][0]
                if ((event_enters[1] == 1) and (event_quits[1] == 1)):
                    dic_playerid_playtime[player] = event_quits[2] - event_enters[2]
                elif ((event_enters[1] == 1) and (event_quits[1] == 2)):
                    dic_playerid_playtime[player] = play_time_first_half - event_enters[2] + play_time_second_half - event_quits[2]
                elif ((event_enters[1] == 2) and (event_quits[1] == 2)):
                    dic_playerid_playtime[player] = event_quits[2] - event_enters[2]
                elif ((event_enters[1] == 2) and (event_quits[1] == 1)):
                    print("impossible")
                    
        return events, players, dic_playerid_playtime
    
    dic_playerid_globalplaytime = {}
    for i in range(id_first_match, id_last_match + 1):
        events, players, dic_playerid_playtime = one_match(path_to_matches_directory, i)
        for uID in dic_playerid_playtime:
            if uID in dic_playerid_globalplaytime:
                dic_playerid_globalplaytime[uID] += dic_playerid_playtime[uID]
            else:
                dic_playerid_globalplaytime[uID] = dic_playerid_playtime[uID]
    
    players_more_800_min = [uID for uID in dic_playerid_globalplaytime if dic_playerid_globalplaytime[uID] > 800]
    players_more_800_min = {e: 0 for e in players_more_800_min}
    actions = [i for i in range(1, 9)] + [i for i in range(10, 20)] + [41, 42, 44, 45] + [i for i in range(49, 62)] + [74]
    actions = {actions[i]: i for i in range(len(actions))}    
    qualifier_id = [1, 2, 3, 4, 5, 6, 7, 8, 9, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 23, 24, 25, 26, 28, 29, 31,
                    32, 33, 35, 36, 37, 38, 55, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 72, 73, 74, 75, 76, 77,
                    78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 89, 94, 100, 101, 107, 108, 113, 114, 120, 121, 122, 123,
                    124, 132, 133, 136, 137, 138, 139, 152, 153, 154, 155, 156, 157, 158, 159, 160, 167, 168, 169, 170,
                    173, 174, 175, 176, 177, 178, 179, 180, 181, 182, 183, 184, 185, 186, 187, 188, 191, 192, 195, 196,
                    210, 211, 214, 215, 217, 218, 223, 224, 225, 228, 232, 236, 237, 238, 239, 240, 241, 245, 254, 264,
                    265, 273, 274, 275, 278, 279, 280, 285, 286, 287, 296, 297, 298, 300, 314]
    qualifier_id = {qualifier_id[i]: i for i in range(len(qualifier_id))}
    
    data_task_1 = []
    
    def cond_period_half(event, period, half):
        cond_half = (event[1] == half)
        if (half == 1):
            cond_period = ((event[2] < ((period + 1) * 15)) and (event[2] >= period * 15))
        if (half == 2):
            cond_period = ((event[2] - 45 < ((period + 1) * 15)) and (event[2] - 45 >= period * 15))
        return (cond_half and cond_period)
        
    for i in range(id_first_match, id_last_match + 1):
        events, players, dic_playerid_playtime = one_match(path_to_matches_directory, i)        
        players = [player for player in players if player in players_more_800_min]
        period_events = [[[event for event in events if cond_period_half(event, period, half)] for period in [0,1,2]] for half in [1,2]]
                
        for ID in players:
            teams = {}
            team_player = -1
            teams_and_team_player_unknown = True
            n_event = 0
            while teams_and_team_player_unknown:
                if (events[n_event][5] > -1):
                    teams[events[n_event][5]] = 1
                if (events[n_event][4] == ID):
                    team_player = events[n_event][5]
                if ((team_player != -1) and (len(teams) == 2)):
                    teams_and_team_player_unknown = False
                n_event += 1
            
            for half in [1,2]:
                for period in [0,1,2]:
                    outcome_player = 0
                    outcome_1_player = 0
                    assist_player = 0
                    keypass_player = 0
                    actions_player = [0 for i in range(len(actions))]
                    qualifier_id_player = [0 for i in range(len(qualifier_id))]
                    qualifier_id_56_player = [0, 0, 0, 0]
                    
                    outcome_team = 0
                    outcome_1_team = 0
                    assist_team = 0
                    keypass_team = 0
                    actions_team = [0 for i in range(len(actions))]
                    qualifier_id_team = [0 for i in range(len(qualifier_id))]
                    qualifier_id_56_team = [0, 0, 0, 0]
                    
                    dic_qualifier_id_56 = {"Right": 0, "Left": 1, "Back": 2, "Center": 3}
                    for event in period_events[half-1][period]:
                        if (event[4] == ID):
                            if (event[0] in actions):
                                actions_player[actions[event[0]]] += 1
                            if (event[8] >- 1):
                                outcome_player += 1
                                outcome_1_player += event[8]
                            assist_player += event[9]
                            keypass_player += event[10]
                            for qual_id in event[-1]:
                                if (qual_id[0] in qualifier_id):
                                    qualifier_id_player[qualifier_id[qual_id[0]]] += 1
                                if (qual_id[0] == 56):
                                    qualifier_id_56_player[dic_qualifier_id_56[qual_id[1]]] += 1
                        
                        if (event[5] == team_player):
                            if (event[0] in actions):
                                actions_team[actions[event[0]]] += 1
                            if (event[8] > -1):
                                outcome_team += 1
                                outcome_1_team += event[8]
                            assist_team += event[9]
                            keypass_team += event[10]
                            for qual_id in event[-1]:
                                if (qual_id[0] in qualifier_id):
                                    qualifier_id_team[qualifier_id[qual_id[0]]] += 1
                                if (qual_id[0] == 56):
                                    qualifier_id_56_team[dic_qualifier_id_56[qual_id[1]]] += 1
                                
                    if (outcome_player > 0):
                        data_player = [ID] + actions_player + [outcome_1_player/outcome_player, assist_player, keypass_player] + qualifier_id_player + qualifier_id_56_player
                        data_team = actions_team + [outcome_1_team/outcome_team, assist_team, keypass_team] + qualifier_id_team + qualifier_id_56_team
                        data_task_1.append(data_player + data_team)
                        
    data_task_1 = np.asarray(data_task_1)
    return data_task_1
    
def data_task_2_3(path_to_matches_directory):
    def data_type_team_x_y(path_to_matches_directory):
        data_matches = []
        for i in range(id_first_match, id_last_match + 1):
            tree = etree.parse(path_to_matches_directory + "f24-24-2016-" + str(i) + "-eventdetails.xml")
            data_match = []
            for Event in tree.xpath("/Games/Game/Event"):
                keys = Event.keys()
                if (("type_id" in keys) and ("team_id" in keys) and ("x" in keys) and ("y" in keys)):
                    data_match.append([int(Event.get("type_id")), int(Event.get("team_id")), float(Event.get("x")), float(Event.get("y"))])
            data_matches.append(data_match)
        return(data_matches)
    
    data_task_2, data_task_3 = [], []
    data_matches = data_type_team_x_y(path_to_matches_directory)
    for match in data_matches:
        for i in range(len(match) // 3 - 1):
            feature_one_hot_1 = [0 for j in range(79)]
            feature_one_hot_1[match[3 * i][0] - 1] += 1
            feature_one_hot_2 = [0 for j in range(79)]
            feature_one_hot_2[match[3 * i + 1][0] - 1] += 1
            feature_one_hot_3 = [0 for j in range(79)]
            feature_one_hot_3[match[3 * i + 2][0] - 1] += 1
            same_team_1 = 0
            if (match[3 * i][1] == match[3 * i + 2][1]):
                same_team_1 = 1
            same_team_2 = 0
            if (match[3 * i + 1][1] == match[3 * i + 2][1]):
                same_team_2 = 1
            y = 0
            if (match[3 * i + 2][1] == match[3 * i + 3][1]):
                y = 1
            data_task_2.append([y, same_team_1, same_team_2, match[3 * i][2],
                              match[3 * i][3], match[3 * i + 1][2], match[3 * i + 1][3],
                              match[3 * i + 2][2], match[3 * i + 2][3]] + feature_one_hot_1 + feature_one_hot_2 + feature_one_hot_3)
            data_task_3.append([match[3*i+3][2], match[3*i+3][3], match[3*i+2][2], match[3*i+2][3],
                                match[3*i+1][2], match[3*i+1][3], match[3*i][2], match[3*i][3],
                                same_team_1, same_team_2] + feature_one_hot_1 + feature_one_hot_2 + feature_one_hot_3)
    data_task_2, data_task_3 = np.asarray(data_task_2), np.asarray(data_task_3)
    return data_task_2, data_task_3

