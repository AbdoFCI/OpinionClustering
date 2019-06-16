from flask import Flask, request, jsonify
from clustring_algorithms import agglomerative_clustering, connected_components, pic, spark_kmeans
from distance_measurement import similarity_methods
from entities import spark_connection

app = Flask(__name__)

SparkObj = spark_connection.SparkObject("appName")

def Agglomerative_PIC_sparkKmean_getClusters(model):
    """

    :param model: list of Label of each point
    :return: clusters_lists: list of lists of clusters
    """
    clusters_lists = []
    maxx = max(model)
    for clusterIndex in range(0,maxx+1):
        indices = [i for i, x in enumerate(model) if x == clusterIndex]
        clusters_lists.append(indices)
    return clusters_lists

def ConnectedComponents_getClusters(model):
    """

    :param model: dataframe carries id and lable of each point
    :return: clusters_lists: list of lists of clusters
    """
    clusters_lists = []
    cluster_index = 0
    opinion_indexs = []
    opinion_indexs.append(model[0].id)
    cluster_index = model[0].component
    for i in range(1, len(model)):
        if model[i].component == cluster_index:
            opinion_indexs.append(model[i].id)
        else:
            clusters_lists.append(opinion_indexs)
            opinion_indexs = []
            opinion_indexs.append(model[i].id)
            cluster_index = model[i].component

    clusters_lists.append(opinion_indexs)
    return clusters_lists

@app.route('/opinion_clustering/Agglomarative', methods=['GET'])
def AgglomarativeCluster():

    json = request.json
    clusters_number = 2

    if "k" in json:
        clusters_number = json["k"]
        if type(clusters_number).__name__ != 'int':
            return jsonify({"msg": "k is the number of clusters which should be more than 2"})

        elif clusters_number < 2:
            return jsonify({"msg": "k is the number of clusters which should be more than 2"})

    if "data" not in json:
        return jsonify({"msg": "you should add list of hashtags for every opinion"})

    if type(json["data"]).__name__ != 'list':
        return jsonify({"msg": "you should add list of hashtags for every opinion"})

    tags = json["data"]

    if "algorithm" in json:

        if "name" not in json["algorithm"]:
            return jsonify({"msg": "You should choose algorithm name Agglomarative"})

        algorithm_name = json["algorithm"]["name"]

        if algorithm_name == "Agglomarative" and type(algorithm_name).__name__ == 'str':
            algorithm_SM = check_similarity_method(json)

            if algorithm_SM == "not in":
                return jsonify({'msg': 'Your similarityMethod is not found ! you can choose one of these (TagJaccard, CharJaccard, EditDistance, Tree, Hamming, Levenshtein, JaroWinkler)'})

            prerequests = check_agglomarative_prerequests(json)

            if prerequests["affinity"] == "not in" and prerequests["linkage"] == "not in":
                return jsonify({'msg': 'you should choose affinty from these (euclidean, l1, l2, manhattan, cosine, precomputed) and choose linkage from these (ward, complete, average, single)'})

            elif prerequests["affinity"] != "not in" and prerequests["linkage"] == "not in":
                return jsonify({'msg': 'you should choose linkage from these (ward, complete, average, single)'})

            elif prerequests["affinity"] == "not in" and prerequests["linkage"] != "not in":
                return jsonify({'msg': 'you should choose affinty from these (euclidean, l1, l2, manhattan, cosine, precomputed)'})

            if algorithm_SM == "TagJaccard":
                agglomerative_obj = agglomerative_clustering.Agglomerative(similarity_methods.tag_jaccard_similarity_method)
                result = agglomerative_obj.cluster(tags=tags, n_clusters=clusters_number, affinity=prerequests["affinity"],
                                      linkage=prerequests["linkage"])

            elif algorithm_SM == "CharJaccard":
                agglomerative_obj = agglomerative_clustering.Agglomerative(
                    similarity_methods.character_jaccard_similarity_method)
                result = agglomerative_obj.cluster(tags=tags, n_clusters=clusters_number, affinity=prerequests["affinity"],
                                      linkage=prerequests["linkage"])

            elif algorithm_SM == "EditDistance":
                agglomerative_obj = agglomerative_clustering.Agglomerative(similarity_methods.edit_distance_method)
                result = agglomerative_obj.cluster(tags=tags, n_clusters=clusters_number, affinity=prerequests["affinity"],
                                      linkage=prerequests["linkage"])

            elif algorithm_SM == "Hamming":
                agglomerative_obj = agglomerative_clustering.Agglomerative(similarity_methods.hamming_similarity_method)
                result = agglomerative_obj.cluster(tags=tags, n_clusters=clusters_number, affinity=prerequests["affinity"],
                                      linkage=prerequests["linkage"])

            elif algorithm_SM == "Levenshtein":
                agglomerative_obj = agglomerative_clustering.Agglomerative(similarity_methods.levenshtein_similarity_method)
                result = agglomerative_obj.cluster(tags=tags, n_clusters=clusters_number, affinity=prerequests["affinity"],
                                      linkage=prerequests["linkage"])

            elif algorithm_SM == "JaroWinkler":
                agglomerative_obj = agglomerative_clustering.Agglomerative(similarity_methods.jaro_winkler_similarity_method)
                result = agglomerative_obj.cluster(tags=tags, n_clusters=clusters_number, affinity=prerequests["affinity"],
                                      linkage=prerequests["linkage"])

            elif algorithm_SM == "Tree":
                agglomerative_obj = agglomerative_clustering.Agglomerative(similarity_methods.tree_similarity_method)
                result = agglomerative_obj.cluster(tags=tags, n_clusters=clusters_number, affinity=prerequests["affinity"],
                                      linkage=prerequests["linkage"])

            agglomerative_clusters = Agglomerative_PIC_sparkKmean_getClusters(result)
            return jsonify({"msg": """You are using agglomerative clustering with this characteristics:-
                number of clusters: {:d},
                affinity: {:s},
                linkage: {:s}
            """.format(clusters_number,prerequests["affinity"],prerequests["linkage"]),
                            "clusters": agglomerative_clusters })

        else:
            return jsonify({"msg": "missing arguments to the url"})

    else:
        return jsonify({ "msg": "missing arguments to the url"})


@app.route('/opinion_clustering/Connected_components', methods=['GET'])
def ConnectedComponentsCluster():

    json = request.json
    clusters_number = 2

    if "k" in json:
        clusters_number = json["k"]

        if type(clusters_number).__name__ != 'int':
            return jsonify({"msg": "k is the number of clusters which should be more than 2"})

        elif clusters_number < 2:
            return jsonify({"msg": "k is the number of clusters which should be more than 2"})

    if "data" not in json:
        return jsonify({"msg": "you should add list of hashtags for every opinion"})

    if type(json["data"]).__name__ != 'list':
        return jsonify({"msg": "you should add list of hashtags for every opinion"})

    tags = json["data"]

    if "algorithm" in json:

        if "name" not in json["algorithm"]:
            return jsonify({"msg": "You should choose algorithm name Connected_components"})

        algorithm_name = json["algorithm"]["name"]

        if algorithm_name == "Connected_components" and type(algorithm_name).__name__ == 'str':
            algorithm_SM = check_similarity_method(json)

            if algorithm_SM == "not in":
                return jsonify({'msg': 'Your similarityMethod is not found ! you can choose one of these (TagJaccard, CharJaccard, EditDistance, Tree, Hamming, Levenshtein, JaroWinkler)'})

            prerequests = check_CC_prerequests(json)

            if prerequests["init_threshold"] == -1 and prerequests["increment"] == -1:
                return jsonify({'msg': 'you should choose init_threshold 0 to 1 and choose increment from 0 to 0.2'})

            elif prerequests["init_threshold"] != -1 and prerequests["increment"] == -1:
                return jsonify({'msg': 'you should choose increment from 0 to 0.2'})

            elif prerequests["init_threshold"] == -1 and prerequests["increment"] != -1:
                return jsonify({'msg': 'you should choose init_threshold 0 to 1'})

            if algorithm_SM == "TagJaccard":
                connected_components_obj = connected_components.ConnectedComponents(similarity_methods.tag_jaccard_similarity_method,
                                                                SparkObj)
                result = connected_components_obj.cluster(tags=tags, n_clusters=clusters_number, init_threshold=prerequests["init_threshold"],
                                      increment=prerequests["increment"])

            elif algorithm_SM == "CharJaccard":
                connected_components_obj = connected_components.ConnectedComponents(similarity_methods.character_jaccard_similarity_method,
                                                                SparkObj)
                result = connected_components_obj.cluster(tags=tags, n_clusters=clusters_number, init_threshold=prerequests["init_threshold"],
                                      increment=prerequests["increment"])

            elif algorithm_SM == "EditDistance":
                connected_components_obj = connected_components.ConnectedComponents(similarity_methods.edit_distance_method,
                                                                SparkObj)
                result = connected_components_obj.cluster(tags=tags, n_clusters=clusters_number, init_threshold=prerequests["init_threshold"],
                                      increment=prerequests["increment"])

            elif algorithm_SM == "Hamming":
                connected_components_obj = connected_components.ConnectedComponents(similarity_methods.hamming_similarity_method,
                                                                SparkObj)
                result = connected_components_obj.cluster(tags=tags, n_clusters=clusters_number, init_threshold=prerequests["init_threshold"],
                                      increment=prerequests["increment"])

            elif algorithm_SM == "Levenshtein":
                connected_components_obj = connected_components.ConnectedComponents(similarity_methods.levenshtein_similarity_method,
                                                                SparkObj)
                result = connected_components_obj.cluster(tags=tags, n_clusters=clusters_number, init_threshold=prerequests["init_threshold"],
                                      increment=prerequests["increment"])

            elif algorithm_SM == "JaroWinkler":
                connected_components_obj = connected_components.ConnectedComponents(similarity_methods.jaro_winkler_similarity_method,
                                                                SparkObj)
                result = connected_components_obj.cluster(tags=tags, n_clusters=clusters_number, init_threshold=prerequests["init_threshold"],
                                      increment=prerequests["increment"])

            elif algorithm_SM == "Tree":
                connected_components_obj = connected_components.ConnectedComponents(similarity_methods.tree_similarity_method,
                                                                SparkObj)
                result = connected_components_obj.cluster(tags=tags, n_clusters=clusters_number, init_threshold=prerequests["init_threshold"],
                                      increment=prerequests["increment"])

            connected_component_clusters = ConnectedComponents_getClusters(result)
            return jsonify({"msg": """You are using PIC clustering with this characteristics:-
                                number of clusters: {:d},
                                init_threshold: {:3f},
                                increment: {:3f}
                            """.format(clusters_number, prerequests["init_threshold"],prerequests["increment"]),
                            "clusters": connected_component_clusters})

        else:
            return jsonify({ "msg": "missing arguments to the url"})


    else:
        return jsonify({ "msg": "missing arguments to the url"})


@app.route('/opinion_clustering/PIC', methods=['GET'])
def PICCluster():

    json = request.json
    clusters_number = 2

    if "k" in json:
        clusters_number = json["k"]

        if type(clusters_number).__name__ != 'int':
            return jsonify({"msg": "k is the number of clusters which should be more than 2"})

        elif clusters_number < 2:
            return jsonify({"msg": "k is the number of clusters which should be more than 2"})

    if "data" not in json:
        return jsonify({"msg": "you should add list of hashtags for every opinion"})

    if type(json["data"]).__name__ != 'list':
        return jsonify({"msg": "you should add list of hashtags for every opinion"})

    tags = json["data"]

    if "algorithm" in json:

        if "name" not in json["algorithm"]:
            return jsonify({"msg": "You should choose algorithm name PIC"})

        algorithm_name = json["algorithm"]["name"]

        if algorithm_name == "PIC" and type(algorithm_name).__name__ == 'str':
            algorithm_SM = check_similarity_method(json)

            if algorithm_SM == "not in":
                return jsonify({'msg': 'Your similarityMethod is not found ! you can choose one of these (TagJaccard, CharJaccard, EditDistance, Tree)'})

            prerequests = check_PIC_prerequests(json)

            if prerequests["threshold"] == -1 or prerequests["n_iterations"] == -1 or prerequests[
                "initialization_mode"] == "not in":
                return jsonify({'msg': 'you should choose threshold from 0 to 1, choose n_iterations more than 10 and choose initialization_mode from these (degree, random)'})

            if algorithm_SM == "TagJaccard":
                pic_obj = pic.PIC(similarity_methods.tag_jaccard_similarity_method,SparkObj)
                result = pic_obj.cluster(tags=tags, n_clusters=clusters_number, threshold=prerequests["threshold"],
                                      n_iterations=prerequests["n_iterations"],
                                      initialization_mode=prerequests["initialization_mode"])

            elif algorithm_SM == "CharJaccard":
                pic_obj = pic.PIC(similarity_methods.character_jaccard_similarity_method,SparkObj)
                result = pic_obj.cluster(tags=tags, n_clusters=clusters_number, threshold=prerequests["threshold"],
                                      n_iterations=prerequests["n_iterations"],
                                      initialization_mode=prerequests["initialization_mode"])

            elif algorithm_SM == "EditDistance":
                pic_obj = pic.PIC(similarity_methods.edit_distance_method,SparkObj)
                result = pic_obj.cluster(tags=tags, n_clusters=clusters_number, threshold=prerequests["threshold"],
                                      n_iterations=prerequests["n_iterations"],
                                      initialization_mode=prerequests["initialization_mode"])

            elif algorithm_SM == "Hamming":
                pic_obj = pic.PIC(similarity_methods.hamming_similarity_method,SparkObj)
                result = pic_obj.cluster(tags=tags, n_clusters=clusters_number, threshold=prerequests["threshold"],
                                      n_iterations=prerequests["n_iterations"],
                                      initialization_mode=prerequests["initialization_mode"])

            elif algorithm_SM == "Levenshtein":
                pic_obj = pic.PIC(similarity_methods.levenshtein_similarity_method,SparkObj)
                result = pic_obj.cluster(tags=tags, n_clusters=clusters_number, threshold=prerequests["threshold"],
                                      n_iterations=prerequests["n_iterations"],
                                      initialization_mode=prerequests["initialization_mode"])

            elif algorithm_SM == "JaroWinkler":
                pic_obj = pic.PIC(similarity_methods.jaro_winkler_similarity_method,SparkObj)
                result = pic_obj.cluster(tags=tags, n_clusters=clusters_number, threshold=prerequests["threshold"],
                                      n_iterations=prerequests["n_iterations"],
                                      initialization_mode=prerequests["initialization_mode"])

            elif algorithm_SM == "Tree":
                pic_obj = pic.PIC(similarity_methods.tree_similarity_method,SparkObj)
                result = pic_obj.cluster(tags=tags, n_clusters=clusters_number, threshold=prerequests["threshold"],
                                      n_iterations=prerequests["n_iterations"],
                                      initialization_mode=prerequests["initialization_mode"])


            pic_clusters = Agglomerative_PIC_sparkKmean_getClusters(result)
            return jsonify({"msg": """You are using PIC clustering with this characteristics:-
                            number of clusters: {:d},
                            threshold: {:3f},
                            number of iteration: {:d},
                            initialization_mode: {:s}
                        """.format(clusters_number, prerequests["threshold"],prerequests["n_iterations"],prerequests["initialization_mode"]),
                            "clusters": pic_clusters})

        else:
            return jsonify({"msg": "missing arguments to the url"})

    else:
        return jsonify({ "msg": "missing arguments to the url"})


@app.route('/opinion_clustering/KMean', methods=['GET'])
def KmeanCluster():

    json = request.json
    clusters_number = 2

    if "k" in json:

        clusters_number = json["k"]

        if type(clusters_number).__name__ != 'int':
            return jsonify({"msg": "k is the number of clusters which should be more than 2"})

        elif clusters_number < 2:
            return jsonify({"msg": "k is the number of clusters which should be more than 2"})

    if "data" not in json:
        return jsonify({"msg": "you should add list of hashtags for every opinion"})

    tags = json["data"]

    if "algorithm" in json:

        if "name" not in json["algorithm"]:
            return jsonify({"msg": "You should choose algorithm name KMean"})

        algorithm_name = json["algorithm"]["name"]

        if algorithm_name == "KMean" and type(algorithm_name).__name__ == 'str':
            prerequests = check_KMean_prerequests(json)

            if type(prerequests["permutation"]).__name__ == 'float' and prerequests["method"] == "not in":
                return jsonify({'msg': 'you should choose method from these (sum, average) and choose permutation from these ((0, 1),(True, False), (true, false))'})

            if type(prerequests["permutation"]).__name__ == 'float':
                return jsonify({'msg': 'you should choose permutation from these ((0, 1),(True, False), (true, false))'})

            if prerequests["method"] == "not in":
                return jsonify({'msg': 'you should choose method from these (sum, average)'})

            kmeans_obj = spark_kmeans.KMeansClustering(SparkObj)
            result = kmeans_obj.cluster(tags=tags, n_clusters=clusters_number, permutation=prerequests["permutation"], permutation_drop=0.5,
                                  method=prerequests["method"])

            kmeans_cluster = Agglomerative_PIC_sparkKmean_getClusters(result)
            return jsonify({"msg": """You are using spark Kmeans clustering with this characteristics:-
                                        number of clusters: {:d},
                                        permutation: {:b},
                                        permutation drop: {:3f},
                                        method: {:s}
                                    """.format(clusters_number, prerequests["permutation"], 0.5,
                                               prerequests["method"]),
                            "clusters": kmeans_cluster})

    else:
        return jsonify({ "msg": "missing arguments to the url"})


def check_similarity_method(json):
    """

    Check similarity method name in request json
    :param json: json object
    :return: str if exist => similarity method name, else => not in
    """
    if "similarityMethod" in json["algorithm"]:
        algorithm_SM = json["algorithm"]["similarityMethod"]
        algorithm_SM_list = ["TagJaccard", "CharJaccard", "EditDistance", "Tree", "Hamming", "Levenshtein", "JaroWinkler"]

        if algorithm_SM not in algorithm_SM_list or type(algorithm_SM).__name__ != 'str':
            return "not in"
        return algorithm_SM
    else:
        return "not in"


def check_agglomarative_prerequests(json):
    """

    Check agglomerative prerequests in request json
    :param json: json object
    :return: json object
    """
    jsonObj = {"affinity": " ", "linkage": " "}
    if "prerequest" in json["algorithm"] and type(json["algorithm"]["prerequest"]).__name__ == 'dict':
        if "affinity" in json["algorithm"]["prerequest"]:
            agglomarative_affinty = json["algorithm"]["prerequest"]["affinity"]
            agglomarative_affinty_list = ["euclidean", "l1", "l2", "manhattan", "cosine", "precomputed"]

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


def check_CC_prerequests(json):
    """

    Check connected components prerequests in request json
    :param json: json object
    :return: json object
    """

    jsonObj = {"init_threshold": 0.0, "increment": 0.0}
    if "prerequest" in json["algorithm"] and type(json["algorithm"]["prerequest"]).__name__ == 'dict':
        if "init_threshold" in json["algorithm"]["prerequest"]:
            CC_init_threshold = json["algorithm"]["prerequest"]["init_threshold"]
            if type(CC_init_threshold).__name__ == 'float' or type(CC_init_threshold).__name__ == 'int':
                if CC_init_threshold >= 0 and CC_init_threshold <= 1:
                    jsonObj["init_threshold"] = CC_init_threshold
                else:
                    jsonObj["init_threshold"] = -1  # not in
            else:
                jsonObj["init_threshold"] = -1  # not in
        else:
            jsonObj["init_threshold"] = 0.3  # check defult

        if "increment" in json["algorithm"]["prerequest"]:
            CC_increment = json["algorithm"]["prerequest"]["increment"]
            if type(CC_increment).__name__ == 'float':
                if CC_increment > 0 and CC_increment < 0.2:
                    jsonObj["increment"] = CC_increment
                else:
                    jsonObj["increment"] = -1  # not in
            else:
                jsonObj["increment"] = -1  # not in
        else:
            jsonObj["increment"] = 0.1  # check defult

    elif "prerequest" in json["algorithm"] and type(json["algorithm"]["prerequest"]).__name__ != 'dict':
        jsonObj["init_threshold"] = -1
        jsonObj["increment"] = -1

    else:
        jsonObj["init_threshold"] = 0.3
        jsonObj["increment"] = 0.1

    return jsonObj


def check_PIC_prerequests(json):
    """

    Check pic prerequests in request json
    :param json: json object
    :return: json object
    """

    jsonObj = {"threshold": 0.0, "n_iterations": 0, "initialization_mode": " "}
    if "prerequest" in json["algorithm"] and type(json["algorithm"]["prerequest"]).__name__ == 'dict':
        if "threshold" in json["algorithm"]["prerequest"]:
            PIC_threshold = json["algorithm"]["prerequest"]["threshold"]

            if type(PIC_threshold).__name__ == 'float' or type(PIC_threshold).__name__ == 'int':
                if PIC_threshold >= 0 and PIC_threshold <= 1:
                    jsonObj["threshold"] = PIC_threshold
                else:
                    jsonObj["threshold"] = -1  # not in
            else:
                jsonObj["threshold"] = -1  # not in
        else:
            jsonObj["threshold"] = 0.5  # check defult

        if "n_iterations" in json["algorithm"]["prerequest"]:
            PIC_n_iterations = json["algorithm"]["prerequest"]["n_iterations"]

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
            PIC_initialization_mode = json["algorithm"]["prerequest"]["initialization_mode"]
            PIC_initialization_mode_list = ["degree", "random"]

            if PIC_initialization_mode not in PIC_initialization_mode_list or type(
                    PIC_initialization_mode).__name__ != 'str':
                jsonObj["initialization_mode"] = "not in"  # not in
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


def check_KMean_prerequests(json):
    """

    Check kmean prerequests in request json
    :param json: json object
    :return: json object
    """

    jsonObj = {"permutation": True, "method": " "}
    if "prerequest" in json["algorithm"] and type(json["algorithm"]["prerequest"]).__name__ == 'dict':
        if "permutation" in json["algorithm"]["prerequest"]:
            KM_permutation = json["algorithm"]["prerequest"]["permutation"]

            if type(KM_permutation).__name__ == 'int':
                if KM_permutation == 1:
                    jsonObj["permutation"] = True
                elif KM_permutation == 0:
                    jsonObj["permutation"] = False
                else:
                    jsonObj["permutation"] = 0.5  # not in
            elif type(KM_permutation).__name__ == 'str':
                if KM_permutation == 'true' or KM_permutation == 'True':
                    jsonObj["permutation"] = True
                elif KM_permutation == 'false' or KM_permutation == 'False':
                    jsonObj["permutation"] = False
                else:
                    jsonObj["permutation"] = 0.5  # not in
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