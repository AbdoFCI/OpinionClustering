from flask import Flask, request, jsonify
from clustring_algorithms import AgglomerativeClustering, ConnectedComponents, pic, sparkKmeans
from distance_measurement_algorithms import  similarity_methods
from Entities import SparkConnection
app = Flask(__name__)


@app.route('/KmeansClustering',methods=['GET'])
def k_means_clustering():
    """

    :return:
    """

#========================================================
@app.route('/AgglomerativeClustering',methods=['GET'])
def agglomerative_clustering():
    """

    :return:
    """
    json = request.json
    k, data, similarity_name = None
    affinity = 'precomputed'
    linkage = 'complete'
    try:
        k = json["k"]
        data = json["data"]
        similarity_name = json["similarityMethod"]
        if "affinity"in json:
            affinity = json["affinity"]
        if "linkage" in json:
            linkage = json["linkage"]
    except:
        return jsonify({"msg": "missing arguments to the url"})
    similarity_function = _get_similarity_function(similarity_name)
    if similarity_function is None:
        return jsonify({"msg": "missing arguments to the url"})
    model = AgglomerativeClustering.AgglomerativeClustering(similarity_function)
    result = model.cluster(tags=data,n_clusters=k,affinity=affinity,linkage=linkage)
    return jsonify({"result":result})

#======================================================
@app.route('/PICClustering',methods=['GET'])
def pic_clustering():
    """

    :return:
    """
#=====================================================
@app.route('/ConnectedComponents',methods=['GET'])
def connected_components():
    """

    :return:
    """


def _get_similarity_function(similarity_name):
    """
    search about how to return function from function
    you can start with this
    link https://stackoverflow.com/questions/12738031/creating-a-new-function-as-return-in-python-function/12738091
    :param similarity_name:str name of the similarity
    :return: function
    """
    if(similarity_name == "tag_jaccard"):
        return similarity_methods.tag_jaccard_similarity_method
    else:
        return None

if __name__ == '__main__':
    app.run(debug=True)