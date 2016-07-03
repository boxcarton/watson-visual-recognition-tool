import os
import json
import requests

class WatsonVisualRecognition:

  end_point = "https://gateway-a.watsonplatform.net/visual-recognition/api"
  latest_version = '2016-05-20'
  
  def __init__(self, api_key, end_point=end_point, version=latest_version):
    self.api_key = api_key
    self.end_point = end_point
    self.version = version

  def list_classifiers(self):
    url = '/v3/classifiers'
    params = {'api_key': self.api_key, 'version': self.version}

    return requests.get(self.end_point + url, 
                        params=params).json()['classifiers']

  def get_classifier(self, classifier_id):
    url = '/v3/classifers'
    params = {'api_key': self.api_key, 'version': self.version}

  def create_classifier(self, classifier_name, class_files):
    url = '/v3/classifiers'
    params = {'api_key': self.api_key, 'version': self.version}

    files = {
      'name': (None, classifier_name)
    }

    for class_name, file in class_files.iteritems():
      files[class_name] = (class_name + ".zip",
                           file,
                           'application/zip')

    return requests.post(self.end_point + url,
                         files=files,
                         params=params,
                        ).json()

  def delete_classifier(self, classifier_id):
    url = '/v3/classifiers/' + classifier_id
    params = {'api_key': self.api_key, 'version': self.version}
    response = requests.delete(self.end_point + url,
                           params=params).json()
    return requests.delete(self.end_point + url,
                           params=params).json()

  def delete_all_classifiers(self):
    responses = []
    for classifier in self.list_classifiers():
      r = self.delete_classifier(classifier['classifier_id'])
      responses.append(r)

    return responses

  def classify_image(self, classifier_ids, image_file):
    url = '/v3/classify'
    params = {'api_key': self.api_key, 'version': self.version}

    if isinstance(classifier_ids, str):
      classifier_ids = [classifier_ids]
    else:
      if not isinstance(classifier_ids, list):
        raise TypeError("classifier_ids needs to be either string or list.")

    parameters = {
      'classifier_ids': classifier_ids,
      'threshold': 0
    }

    files = {
      'parameters': (None, json.dumps(parameters)),
      'images_file': (image_file,
                      open(image_file, 'rb').read(),
                      'image/jpg')
    }

    return requests.post(self.end_point + url,
                         files=files,
                         params=params).json()

