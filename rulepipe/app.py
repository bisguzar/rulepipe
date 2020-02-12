from flask import Flask, request
from core.rulepipe import *

app = Flask(__name__)
rules = RuleManager()

@app.route('/')
def root():
  return 'Rulepipe!\n'

@app.route('/add_rule/<name>', methods=['POST'])
def add_rule(name):
  rules.add_rule_json(name, request.get_json())
  return 'OK\n'

@app.route('/delete_rule/<name>', methods=['DELETE'])
@app.route('/remove_rule/<name>', methods=['DELETE'])
def delete_rule(name):
  response = rules.delete_rule(name)
  return {'delete_status': response}

@app.route('/execute_rule/<name>', methods=['POST'])
def execute_rule(name):
  print(request.get_json())
  response = rules.execute_rule_json(name, request.get_json())
  return {"response": str(response)}

@app.route('/rules', methods=['GET'])
@app.route('/get_rules', methods=['GET'])
@app.route('/get_rule_list', methods=['GET'])
@app.route('/get_rules_list', methods=['GET'])
def get_rules():
  response = rules.get_rule_list()
  return {"rule_list": str(response)}
