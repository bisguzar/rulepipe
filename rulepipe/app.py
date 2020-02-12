import falcon
import json

try:
    from .core import RuleManager
except ImportError:
    from core import RuleManager

api = falcon.API()
rulemanager = RuleManager()


class HomeResource(object):
    def on_get(self, req, resp):
        resp.content_type = falcon.MEDIA_TEXT
        resp.body = "Rulepipe is alive!"


class AddRuleResource(object):
    def on_post(self, req, resp, rule_name):
        rule = req.media

        try:
            rulemanager.add_rule_json(rule_name, rule)
        except KeyError as err:
            resp.status = falcon.HTTP_422
            resp.body = json.dumps(dict(err=err.args[0]))
            return
        except NameError as err:
            resp.status = falcon.HTTP_409
            resp.body = json.dumps(
                dict(
                    err=f"Couldn't create new rule, rule named by {rule_name} already exists."
                )
            )
            return 

        resp.status = falcon.HTTP_201
        resp.body = json.dumps(dict(msg="Rule created successfully."))


class RuleResource(object):
    def on_post(self, req, resp, rule_name):
        print('adding new rule')
        try:
            response = rulemanager.execute_rule_json(rule_name, req.media)
            resp.body = json.dumps(dict(msg=response))
        except KeyError as err:
            resp.status = falcon.HTTP_404
            resp.body = json.dumps(dict(err=f"Rule '{rule_name}' not found."))

    def on_delete(self, req, resp, rule_name):
        response = rulemanager.delete_rule(rule_name)
        resp.body = json.dumps(dict(msg=response))


class RuleListResource(object):
    def on_get(self, req, resp):
        resp.body = json.dumps(dict(rules=rulemanager.get_rule_list()))


api.add_route("/", HomeResource())
api.add_route("/add_rule/{rule_name}", AddRuleResource())
api.add_route("/rules", RuleListResource())
api.add_route("/rules/{rule_name}", RuleResource())
