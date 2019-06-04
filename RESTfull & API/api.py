from flask import Flask, request, jsonify

app = Flask(__name__)




@app.route('/opinion_clustering',methods=['GET'])
def clustering():
    json = request.json

    k = 2
    if "k" in json:
        k= json["k"]

    if "data" not in json:
        return jsonify({"msg":"you should add list of hashtags for every opinion"})

    data = json["data"]

    if "algorithm" in json:
        if "name" not in json["algorithm"]:
            return jsonify({"msg":"You should choose algorithm name from these (Agglomarative, Connected_components, PIC, KMean)"})
        algorithm_name = json["algorithm"]["name"]
        if algorithm_name == "Agglomarative" and type(algorithm_name).__name__ == 'str':
            algorithm_SM = check_similarity_method(json)

            if algorithm_SM == "not in" :
                return jsonify({'msg': 'Your similarityMethod is not found ! you can choose one of these (TagJaccard, CharJaccard, EditDistance, Tree)'})

            elif algorithm_SM == "TagJaccard":
                prerequests = check_agglomarative_prerequests(json)

                if prerequests["affinity"] == "not in" and prerequests["linkage"] == "not in":
                    return jsonify({'msg': 'you should choose affinty from these (euclidean, l1, l2, manhattan, cosine, precomputed) and choose linkage from these (ward, complete, average, single)'})

                elif prerequests["affinity"] != "not in" and prerequests["linkage"] == "not in":
                    return jsonify({'msg': 'you should choose linkage from these (ward, complete, average, single)'})

                elif prerequests["affinity"] == "not in" and prerequests["linkage"] != "not in" :
                    return jsonify({'msg': 'you should choose affinty from these (euclidean, l1, l2, manhattan, cosine, precomputed)'})

                else:
                    return jsonify({'msg': 'i should call a function of agglomarative algorithm with TagJaccard'})

            elif algorithm_SM == "CharJaccard":
                prerequests = check_agglomarative_prerequests(json)

                if prerequests["affinity"] == "not in" and prerequests["linkage"] == "not in":
                    return jsonify({
                                       'msg': 'you should choose affinty from these (euclidean, l1, l2, manhattan, cosine, precomputed) and choose linkage from these (ward, complete, average, single)'})

                elif prerequests["affinity"] != "not in" and prerequests["linkage"] == "not in":
                    return jsonify(
                        {'msg': 'you should choose linkage from these (ward, complete, average, single)'})

                elif prerequests["affinity"] == "not in" and prerequests["linkage"] != "not in":
                    return jsonify({
                                       'msg': 'you should choose affinty from these (euclidean, l1, l2, manhattan, cosine, precomputed)'})

                else:
                    return jsonify({'msg': 'i should call a function of agglomarative algorithm with CharJaccard'})

            elif algorithm_SM == "EditDistance":
                prerequests = check_agglomarative_prerequests(json)

                if prerequests["affinity"] == "not in" and prerequests["linkage"] == "not in":
                    return jsonify({
                        'msg': 'you should choose affinty from these (euclidean, l1, l2, manhattan, cosine, precomputed) and choose linkage from these (ward, complete, average, single)'})

                elif prerequests["affinity"] != "not in" and prerequests["linkage"] == "not in":
                    return jsonify(
                        {'msg': 'you should choose linkage from these (ward, complete, average, single)'})

                elif prerequests["affinity"] == "not in" and prerequests["linkage"] != "not in":
                    return jsonify({
                        'msg': 'you should choose affinty from these (euclidean, l1, l2, manhattan, cosine, precomputed)'})

                else:
                    return jsonify({'msg': 'i should call a function of agglomarative algorithm with EditDistance'})

            elif algorithm_SM == "Tree":
                prerequests = check_agglomarative_prerequests(json)

                if prerequests["affinity"] == "not in" and prerequests["linkage"] == "not in":
                    return jsonify({
                        'msg': 'you should choose affinty from these (euclidean, l1, l2, manhattan, cosine, precomputed) and choose linkage from these (ward, complete, average, single)'})

                elif prerequests["affinity"] != "not in" and prerequests["linkage"] == "not in":
                    return jsonify(
                        {'msg': 'you should choose linkage from these (ward, complete, average, single)'})

                elif prerequests["affinity"] == "not in" and prerequests["linkage"] != "not in":
                    return jsonify({
                        'msg': 'you should choose affinty from these (euclidean, l1, l2, manhattan, cosine, precomputed)'})

                else:
                    return jsonify({'msg': 'i should call a function of agglomarative algorithm with Tree'})

        elif algorithm_name == "Connected_components" and type(algorithm_name).__name__ == 'str':
            algorithm_SM = check_similarity_method(json)

            if algorithm_SM == "not in":
                return jsonify({'msg': 'Your similarityMethod is not found ! you can choose one of these (TagJaccard, CharJaccard, EditDistance, Tree)'})

            elif algorithm_SM == "TagJaccard":
                prerequests = check_CC_prerequests(json)

                if prerequests["init_threshold"] == -1 and prerequests["increment"] == -1:
                    return jsonify({'msg': 'you should choose init_threshold 0 to 1 and choose increment from 0 to 0.2'})

                elif prerequests["init_threshold"] != -1 and prerequests["increment"] == -1:
                    return jsonify({'msg': 'you should choose increment from 0 to 0.2'})

                elif prerequests["init_threshold"] == -1 and prerequests["increment"] != -1:
                    return jsonify({'msg': 'you should choose init_threshold 0 to 1'})

                else:
                    return jsonify({'msg': 'i should call a function of Connected_components algorithm with TagJaccard'})

            elif algorithm_SM == "CharJaccard":
                prerequests = check_CC_prerequests(json)

                if prerequests["init_threshold"] == -1 and prerequests["increment"] == -1:
                    return jsonify(
                        {'msg': 'you should choose init_threshold 0 to 1 and choose increment from 0 to 0.2'})

                elif prerequests["init_threshold"] != -1 and prerequests["increment"] == -1:
                    return jsonify({'msg': 'you should choose increment from 0 to 0.2'})

                elif prerequests["init_threshold"] == -1 and prerequests["increment"] != -1:
                    return jsonify({'msg': 'you should choose init_threshold 0 to 1'})

                else:
                    return jsonify({'msg': 'i should call a function of Connected_components algorithm with CharJaccard'})

            elif algorithm_SM == "EditDistance":
                prerequests = check_CC_prerequests(json)

                if prerequests["init_threshold"] == -1 and prerequests["increment"] == -1:
                    return jsonify(
                        {'msg': 'you should choose init_threshold 0 to 1 and choose increment from 0 to 0.2'})

                elif prerequests["init_threshold"] != -1 and prerequests["increment"] == -1:
                    return jsonify({'msg': 'you should choose increment from 0 to 0.2'})

                elif prerequests["init_threshold"] == -1 and prerequests["increment"] != -1:
                    return jsonify({'msg': 'you should choose init_threshold 0 to 1'})

                else:
                    return jsonify({'msg': 'a function of Connected_components algorithm with EditDistance'})

            elif algorithm_SM == "Tree":
                prerequests = check_CC_prerequests(json)

                if prerequests["init_threshold"] == -1 and prerequests["increment"] == -1:
                    return jsonify(
                        {'msg': 'you should choose init_threshold 0 to 1 and choose increment from 0 to 0.2'})

                elif prerequests["init_threshold"] != -1 and prerequests["increment"] == -1:
                    return jsonify({'msg': 'you should choose increment from 0 to 0.2'})

                elif prerequests["init_threshold"] == -1 and prerequests["increment"] != -1:
                    return jsonify({'msg': 'you should choose init_threshold 0 to 1'})

                else:
                    return jsonify({'msg': 'i should call a function of Connected_components algorithm with Tree'})

        elif algorithm_name == "PIC" and type(algorithm_name).__name__ == 'str':
            algorithm_SM = check_similarity_method(json)

            if algorithm_SM == "not in":
                return jsonify({'msg': 'Your similarityMethod is not found ! you can choose one of these (TagJaccard, CharJaccard, EditDistance, Tree)'})

            elif algorithm_SM == "TagJaccard":
                prerequests = check_PIC_prerequests(json)

                if prerequests["threshold"] == -1 or prerequests["n_iterations"] == -1 or prerequests["initialization_mode"] == "not in":
                    return jsonify({'msg': 'you should choose threshold from 0 to 1, choose n_iterations more than 10 and choose initialization_mode from these (degree, random)'})

                else:
                    return jsonify({'msg': 'i should call a function of PIC algorithm with TagJaccard'})

            elif algorithm_SM == "CharJaccard":
                prerequests = check_PIC_prerequests(json)

                if prerequests["threshold"] == -1 or prerequests["n_iterations"] == -1 or prerequests["initialization_mode"] == "not in":
                    return jsonify({'msg': 'you should choose threshold from 0 to 1, choose n_iterations more than 10 and choose initialization_mode from these (degree, random)'})

                else:
                    return jsonify({'msg': 'i should call a function of PIC algorithm with CharJaccard'})

            elif algorithm_SM == "EditDistance":
                prerequests = check_PIC_prerequests(json)

                if prerequests["threshold"] == -1 or prerequests["n_iterations"] == -1 or prerequests["initialization_mode"] == "not in":
                    return jsonify({'msg': 'you should choose threshold from 0 to 1, choose n_iterations more than 10 and choose initialization_mode from these (degree, random)'})

                else:
                    return jsonify({'msg': 'i should call a function of PIC algorithm with EditDistance'})

            elif algorithm_SM == "Tree":
                prerequests = check_PIC_prerequests(json)

                if prerequests["threshold"] == -1 or prerequests["n_iterations"] == -1 or prerequests["initialization_mode"] == "not in":
                    return jsonify({'msg': 'you should choose threshold from 0 to 1, choose n_iterations more than 10 and choose initialization_mode from these (degree, random)'})

                else:
                    return jsonify({'msg': 'i should call a function of PIC algorithm with Tree'})

        elif algorithm_name == "KMean" and type(algorithm_name).__name__ == 'str':
            prerequests = check_KMean_prerequests(json)

            if type(prerequests["permutation"]).__name__ == 'float' and prerequests["method"] == "not in":
                return jsonify({'msg': 'you should choose method from these (sum, average) and choose permutation from these ((0, 1),(True, False), (true, false))'})

            if type(prerequests["permutation"]).__name__ == 'float':
                return jsonify({'msg': 'you should choose permutation from these ((0, 1),(True, False), (true, false))'})

            if prerequests["method"] == "not in":
                return jsonify({'msg': 'you should choose method from these (sum, average)'})

            else:
                return jsonify({'msg': 'i should call a function of KMean algorithm'})

        else:
            return jsonify({"msg": "You should choose algorithm name from these (Agglomarative, Connected_components, PIC, KMean)"})

    else:
        return jsonify({"msg":"add all data"})


def check_similarity_method(json): # check similarity method
    if "similarityMethod" in json["algorithm"]:
        algorithm_SM = json["algorithm"]["similarityMethod"]
        algorithm_SM_list = ["TagJaccard","CharJaccard","EditDistance","Tree"]

        if algorithm_SM not in algorithm_SM_list or type(algorithm_SM).__name__ != 'str':
            return "not in"
        return algorithm_SM
    else:
        return "not in"

def check_agglomarative_prerequests (json): #check agglomarative prerequests
    jsonObj = {"affinity" : " ","linkage": " " }
    if "prerequest" in json["algorithm"] and type(json["algorithm"]["prerequest"]).__name__ == 'dict':
        if "affinity" in json["algorithm"]["prerequest"]:
            agglomarative_affinty = json["algorithm"]["prerequest"]["affinity"]
            agglomarative_affinty_list = ["euclidean", "l1", "l2", "manhattan","cosine", "precomputed"]

            if agglomarative_affinty not in agglomarative_affinty_list or type(agglomarative_affinty).__name__ != 'str':
                jsonObj["affinity"] = "not in"
            else:
                jsonObj["affinity"] = agglomarative_affinty
        else:
            jsonObj["affinity"] = "precomputed"

        if "linkage" in json["algorithm"]["prerequest"]:
            agglomarative_linkage = json["algorithm"]["prerequest"]["linkage"]
            agglomarative_linkage_list = ["ward", "complete", "average", "single"]

            if agglomarative_linkage not in agglomarative_linkage_list or type(agglomarative_linkage).__name__ != 'str':
                jsonObj["linkage"] = "not in"
            else:
                jsonObj["linkage"] = agglomarative_linkage
        else:
            jsonObj["linkage"] = "complete"
    elif "prerequest" in json["algorithm"] and type(json["algorithm"]["prerequest"]).__name__ != 'dict':
        jsonObj["affinity"] = "not in"
        jsonObj["linkage"] = "not in"
    else:
        jsonObj["affinity"] = "precomputed"
        jsonObj["linkage"] = "complete"

    return jsonObj

def check_CC_prerequests (json): #check connected components prerequests
    jsonObj = {"init_threshold": 0.0, "increment": 0.0}
    if "prerequest" in json["algorithm"] and type(json["algorithm"]["prerequest"]).__name__ == 'dict':
        if "init_threshold" in json["algorithm"]["prerequest"]:
            CC_init_threshold = json["algorithm"]["prerequest"]["init_threshold"]
            if type(CC_init_threshold).__name__ == 'float' or type(CC_init_threshold).__name__ == 'int':
                if CC_init_threshold >= 0 and CC_init_threshold <= 1 :
                    jsonObj["init_threshold"] = CC_init_threshold
                else:
                    jsonObj["init_threshold"] = -1 # not in
            else:
                jsonObj["init_threshold"] = -1  # not in
        else:
            jsonObj["init_threshold"] = 0.3 #check defult

        if "increment" in json["algorithm"]["prerequest"]:
            CC_increment = json["algorithm"]["prerequest"]["increment"]
            if  type(CC_increment).__name__ == 'float':
                if CC_increment > 0 and CC_increment < 0.2:
                    jsonObj["increment"] = CC_increment
                else:
                    jsonObj["increment"] = -1 # not in
            else:
                jsonObj["increment"] = -1  # not in
        else:
            jsonObj["increment"] = 0.1 #check defult

    elif "prerequest" in json["algorithm"] and type(json["algorithm"]["prerequest"]).__name__ != 'dict':
        jsonObj["init_threshold"] = -1
        jsonObj["increment"] = -1

    else:
        jsonObj["init_threshold"] = 0.3
        jsonObj["increment"] = 0.1

    return jsonObj

def check_PIC_prerequests (json):
    jsonObj = {"threshold": 0.0, "n_iterations": 0, "initialization_mode": " " }
    if "prerequest" in json["algorithm"] and type(json["algorithm"]["prerequest"]).__name__ == 'dict':
        if "threshold" in json["algorithm"]["prerequest"]:
            PIC_threshold = json["algorithm"]["prerequest"]["threshold"]

            if type(PIC_threshold).__name__ == 'float' or type(PIC_threshold).__name__ == 'int':
                if PIC_threshold  >= 0 and PIC_threshold  <= 1:
                    jsonObj["threshold"] = PIC_threshold
                else:
                    jsonObj["threshold"] = -1  # not in
            else:
                jsonObj["threshold"] = -1  # not in
        else:
            jsonObj["threshold"] = 0.5  # check defult

        if "n_iterations" in json["algorithm"]["prerequest"]:
            PIC_n_iterations= json["algorithm"]["prerequest"]["n_iterations"]

            if type(PIC_n_iterations).__name__ == 'int':
                if PIC_n_iterations >= 10:
                    jsonObj["n_iterations"] = PIC_n_iterations
                else:
                    jsonObj["n_iterations"] = -1  # not in
            else:
                jsonObj["n_iterations"] = -1  # not in
        else:
            jsonObj["n_iterations"] = 25  # check defult

        if "initialization_mode" in json["algorithm"]["prerequest"]:
            PIC_initialization_mode= json["algorithm"]["prerequest"]["initialization_mode"]
            PIC_initialization_mode_list = ["degree", "random"]

            if PIC_initialization_mode not in PIC_initialization_mode_list or type(PIC_initialization_mode).__name__ != 'str':
                jsonObj["initialization_mode"] = "not in" # not in
            else:
                jsonObj["initialization_mode"] = PIC_initialization_mode
        else:
            jsonObj["initialization_mode"] = "degree"  # check defult
    elif "prerequest" in json["algorithm"] and type(json["algorithm"]["prerequest"]).__name__ != 'dict':
        jsonObj["threshold"] = -1
        jsonObj["n_iterations"] = -1
        jsonObj["initialization_mode"] = "not in"


    else:
        jsonObj["threshold"] = 0.5
        jsonObj["n_iterations"] = 25
        jsonObj["initialization_mode"] = "degree"

    return jsonObj

def check_KMean_prerequests (json):
    jsonObj = {"permutation": True, "method": " "}
    if "prerequest" in json["algorithm"] and type(json["algorithm"]["prerequest"]).__name__ == 'dict':
        if "permutation" in json["algorithm"]["prerequest"]:
            KM_permutation = json["algorithm"]["prerequest"]["permutation"]

            if type(KM_permutation).__name__ == 'int':
                if KM_permutation == 1:
                    jsonObj["permutation"] = True
                elif KM_permutation == 0 :
                    jsonObj["permutation"] = False
                else:
                    jsonObj["permutation"]= 0.5 #not in
            elif type(KM_permutation).__name__ == 'str':
                if KM_permutation == 'true' or KM_permutation == 'True':
                    jsonObj["permutation"] = True
                elif KM_permutation == 'false' or KM_permutation == 'False':
                    jsonObj["permutation"] = False
                else:
                    jsonObj["permutation"]= 0.5 #not in
            else:
                jsonObj["permutation"] = 0.5  # not in


        if "method" in json["algorithm"]["prerequest"]:
            KM_method = json["algorithm"]["prerequest"]["method"]

            if type(KM_method).__name__ == 'str':
                if KM_method == "sum" or KM_method == "average":
                    jsonObj["method"] = KM_method
                else:
                    jsonObj["method"] = "not in"  # not in
            else:
                jsonObj["method"] = "not in"  # not in
        else:
            jsonObj["method"] = "sum"  # check defult

    elif "prerequest" in json["algorithm"] and type(json["algorithm"]["prerequest"]).__name__ != 'dict':
        jsonObj["permutation"] = 0.5
        jsonObj["method"] = "not in"
    else:
        jsonObj["permutation"] = True
        jsonObj["method"] = "sum"

    return jsonObj


if __name__ == '__main__':
    app.run(debug=True)