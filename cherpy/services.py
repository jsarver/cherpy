import attr
import urllib.parse


@attr.s
class Services(object):
    client = attr.ib()

    def _generate_uri(self, uri_frag, **params):
        params = '&'.join(['{k}={v}'.format(k=k, v=v) for k, v in params.items()])
        if params:
            uri = "{uri}?{params}".format(uri=uri_frag, params=params)
        else:
            uri = uri_frag
        return uri

    def action(self, method, uri, **kwargs):
        if method == "GET":
            response = self.client.get(uri)
        if method == "POST":
            response = self.client.post(uri, kwargs)
        if method == "DELETE":
            response = self.client.delete(uri)
        if method == "PUT":
            response = self.client.put(uri)
        return response

    def token(self, version="V1"):
        """
        Get an access token
        Parameters expected:
        """
        uri = "/token".format(version=version)
        method = "POST"
        raise NotImplemented("just a stub, don't use yet")

        #
        #     def addusertoteam(self, version="V1"):
        #         """
        #         Add a user to a team
        #         Parameters expected:
        #         """
        #         uri = "/api/{version}/addusertoteam".format(version=version)
        #         method = "POST"
        #         raise NotImplemented("just a stub, don't use yet")
        #
        #     def addusertoteambybatch(self, version="V1"):
        #         """
        #         Add users to a team by batch
        #         Parameters expected:
        #         """
        #         uri = "/api/{version}/addusertoteambybatch".format(version=version)
        #         method = "POST"
        #         raise NotImplemented("just a stub, don't use yet")
        #
        #     def deletebusinessobject(self, version="V1", busobid=None,publicid=None):
        #         """
        #         Delete a Business Object by public ID
        #         Parameters expected: , busobid=None,publicid=None
        #         """
        #         uri = "/api/{version}/deletebusinessobject/busobid/{busobid}/publicid/{publicid}".format(version=version)
        #         method = "DELETE"
        #         raise NotImplemented("just a stub, don't use yet")
        #
        #     def deletebusinessobject(self, version="V1", busobid=None,busobrecid=None):
        #         """
        #         Delete a Business Object by record ID
        #         Parameters expected: , busobid=None,busobrecid=None
        #         """
        #         uri = "/api/{version}/deletebusinessobject/busobid/{busobid}/busobrecid/{busobrecid}".format(version=version)
        #         method = "DELETE"
        #         raise NotImplemented("just a stub, don't use yet")
        #
        #     def deletebusinessobjectbatch(self, version="V1"):
        #         """
        #         Delete Business Objects in a batch
        #         Parameters expected:
        #         """
        #         uri = "/api/{version}/deletebusinessobjectbatch".format(version=version)
        #         method = "POST"
        #         raise NotImplemented("just a stub, don't use yet")
        #
        #     def deleterelatedbusinessobject(self, version="V1", parentbusobid=None,parentbusobrecid=None,relationshipid=None,busobrecid=None):
        #         """
        #         Delete a related Business Object by record ID
        #         Parameters expected: , parentbusobid=None,parentbusobrecid=None,relationshipid=None,busobrecid=None
        #         """
        #         uri = "/api/{version}/deleterelatedbusinessobject/parentbusobid/{parentbusobid}/parentbusobrecid/{parentbusobrecid}/relationshipid/{relationshipid}/busobrecid/{busobrecid}".format(version=version)
        #         method = "DELETE"
        #         raise NotImplemented("just a stub, don't use yet")
        #
        #     def deleterelatedbusinessobject(self, version="V1", parentbusobid=None,parentbusobrecid=None,relationshipid=None,publicid=None):
        #         """
        #         Delete a related Business Object by public ID
        #         Parameters expected: , parentbusobid=None,parentbusobrecid=None,relationshipid=None,publicid=None
        #         """
        #         uri = "/api/{version}/deleterelatedbusinessobject/parentbusobid/{parentbusobid}/parentbusobrecid/{parentbusobrecid}/relationshipid/{relationshipid}/publicid/{publicid}".format(version=version)
        #         method = "DELETE"
        #         raise NotImplemented("just a stub, don't use yet")
        #
        #     def deleteuser(self, version="V1", userrecordid=None):
        #         """
        #         Delete a user by record ID
        #         Parameters expected: , userrecordid=None
        #         """
        #         uri = "/api/{version}/deleteuser/userrecordid/{userrecordid}".format(version=version)
        #         method = "DELETE"
        #         raise NotImplemented("just a stub, don't use yet")
        #
        #     def deleteuserbatch(self, version="V1"):
        #         """
        #         Delete a batch of users
        #         Parameters expected:
        #         """
        #         uri = "/api/{version}/deleteuserbatch".format(version=version)
        #         method = "POST"
        #         raise NotImplemented("just a stub, don't use yet")
        #
        #     def fieldvalueslookup(self, version="V1"):
        #         """
        #         Get lookup values for fields
        #         Parameters expected:
        #         """
        #         uri = "/api/{version}/fieldvalueslookup".format(version=version)
        #         method = "POST"
        #         raise NotImplemented("just a stub, don't use yet")
        #
        # def getbusinessobject(self, version="V1", scancode=None, busobname=None, publicid=None):
        #     """
        #     Get a Business Object by its scan code and Business Object name.
        #     Parameters expected: , scancode=None,busobname=None
        #     """
        #     uri = "/api/{version}/getbusinessobject/scancode/{scanCode}/busobname/{busobname}".format(version=version)
        #     method = "GET"
        #     raise NotImplemented("just a stub, don't use yet")

        # def getbusinessobject(self, version="V1", busobid=None, ):
        #     """
        #     Get a Business Object record
        #     Parameters expected: , busobid=None,publicid=None
        #     """
        #     uri = "/api/{version}/getbusinessobject/busobid/{busobid}/publicid/{publicid}".format(version=version)
        #     method = "GET"
        #     raise NotImplemented("just a stub, don't use yet")
        #
        # def getbusinessobject(self, version="V1", scancode=None, busobid=None):
        #     """
        #     Get a Business Object by its scan code and Business Object ID.
        #     Parameters expected: , scancode=None,busobid=None
        #     """
        #     uri = "/api/{version}/getbusinessobject/scancode/{scanCode}/busobid/{busobid}".format(version=version)
        #     method = "GET"
        #     raise NotImplemented("just a stub, don't use yet")
        #
        #     def getbusinessobjectattachment(self, version="V1", attachmentid=None,busobid=None,busobrecid=None):
        #         """
        #         Get an imported Business Object attachment
        #         Parameters expected: , attachmentid=None,busobid=None,busobrecid=None
        #         """
        #         uri = "/api/{version}/getbusinessobjectattachment/attachmentid/{attachmentid}/busobid/{busobid}/busobrecid/{busobrecid}".format(version=version)
        #         method = "GET"
        #         raise NotImplemented("just a stub, don't use yet")
        #
        #     def getbusinessobjectattachments(self, version="V1", busobname=None,publicid=None,type=None,attachmenttype=None):
        #         """
        #         Get attachments by Business Object name and public ID
        #         Parameters expected: , busobname=None,publicid=None,type=None,attachmenttype=None
        #         """
        #         uri = "/api/{version}/getbusinessobjectattachments/busobname/{busobname}/publicid/{publicid}/type/{type}/attachmenttype/{attachmenttype}".format(version=version)
        #         method = "GET"
        #         raise NotImplemented("just a stub, don't use yet")
        #
        #     def getbusinessobjectattachments(self, version="V1"):
        #         """
        #         Get Business Object attachments by request object
        #         Parameters expected:
        #         """
        #         uri = "/api/{version}/getbusinessobjectattachments".format(version=version)
        #         method = "POST"
        #         raise NotImplemented("just a stub, don't use yet")
        #
        #     def getbusinessobjectattachments(self, version="V1", busobname=None,busobrecid=None,type=None,attachmenttype=None):
        #         """
        #         Get attachments by Business Object name and record ID
        #         Parameters expected: , busobname=None,busobrecid=None,type=None,attachmenttype=None
        #         """
        #         uri = "/api/{version}/getbusinessobjectattachments/busobname/{busobname}/busobrecid/{busobrecid}/type/{type}/attachmenttype/{attachmenttype}".format(version=version)
        #         method = "GET"
        #         raise NotImplemented("just a stub, don't use yet")
        #
        #     def getbusinessobjectattachments(self, version="V1", busobid=None,publicid=None,type=None,attachmenttype=None):
        #         """
        #         Get attachments by Business Object public ID
        #         Parameters expected: , busobid=None,publicid=None,type=None,attachmenttype=None
        #         """
        #         uri = "/api/{version}/getbusinessobjectattachments/busobid/{busobid}/publicid/{publicid}/type/{type}/attachmenttype/{attachmenttype}".format(version=version)
        #         method = "GET"
        #         raise NotImplemented("just a stub, don't use yet")
        #
        #     def getbusinessobjectattachments(self, version="V1", busobid=None,busobrecid=None,type=None,attachmenttype=None):
        #         """
        #         Get attachments by Business Object record ID
        #         Parameters expected: , busobid=None,busobrecid=None,type=None,attachmenttype=None
        #         """
        #         uri = "/api/{version}/getbusinessobjectattachments/busobid/{busobid}/busobrecid/{busobrecid}/type/{type}/attachmenttype/{attachmenttype}".format(version=version)
        #         method = "GET"
        #         raise NotImplemented("just a stub, don't use yet")
        #
        #     def getbusinessobjectbatch(self, version="V1"):
        #         """
        #         Get a batch of Business Object records
        #         Parameters expected:
        #         """
        #         uri = "/api/{version}/getbusinessobjectbatch".format(version=version)
        #         method = "POST"
        #         raise NotImplemented("just a stub, don't use yet")
        #

    def getbusinessobjectschema(self, version="V1", busobId=None, **kwargs):
        """
        Get a Business Object schema
        Parameters expected: , busobid=None
        """
        uri = "/api/{version}/getbusinessobjectschema/busobid/{busobId}".format(version=version, busobId=busobId)
        method = "GET"
        uri = self._generate_uri(uri, **kwargs)
        return self.action(method, uri)

        #
        #     def getbusinessobjectsummaries(self, version="V1", type=None):
        #         """
        #         Get Business Object summaries by type
        #         Parameters expected: , type=None
        #         """
        #         uri = "/api/{version}/getbusinessobjectsummaries/type/{type}".format(version=version)
        #         method = "GET"
        #         raise NotImplemented("just a stub, don't use yet")
        #
        #     def getbusinessobjectsummary(self, version="V1", busobname=None):
        #         """
        #         Get a Business Object summary by name
        #         Parameters expected: , busobname=None
        #         """
        #         uri = "/api/{version}/getbusinessobjectsummary/busobname/{busobname}".format(version=version)
        #         method = "GET"
        #         raise NotImplemented("just a stub, don't use yet")
        #
        #     def getbusinessobjectsummary(self, version="V1", busobid=None):
        #         """
        #         Get a Business Object summary by ID
        #         Parameters expected: , busobid=None
        #         """
        #         uri = "/api/{version}/getbusinessobjectsummary/busobid/{busobid}".format(version=version)
        #         method = "GET"
        #         raise NotImplemented("just a stub, don't use yet")
        #
        #     def getbusinessobjecttemplate(self, version="V1"):
        #         """
        #         Get Business Object templates for create
        #         Parameters expected:
        #         """
        #         uri = "/api/{version}/getbusinessobjecttemplate".format(version=version)
        #         method = "POST"
        #         raise NotImplemented("just a stub, don't use yet")
        #
        #     def getgalleryimage(self, version="V1", name=None):
        #         """
        #         Get built-in images
        #         Parameters expected: , name=None
        #         """
        #         uri = "/api/{version}/getgalleryimage/name/{name}".format(version=version)
        #         method = "GET"
        #         raise NotImplemented("just a stub, don't use yet")
        #
        #     def getmobileformforbusob(self, version="V1", busobid=None,busobrecid=None):
        #         """
        #         Get mobile form by BusObId and BusObRecId
        #         Parameters expected: , busobid=None,busobrecid=None
        #         """
        #         uri = "/api/{version}/getmobileformforbusob/busobid/{busobid}/busobrecid/{busobrecid}".format(version=version)
        #         method = "GET"
        #         raise NotImplemented("just a stub, don't use yet")
        #
        #     def getmobileformforbusob(self, version="V1", busobname=None,publicid=None):
        #         """
        #         Get mobile form by BusObName and PublicId
        #         Parameters expected: , busobname=None,publicid=None
        #         """
        #         uri = "/api/{version}/getmobileformforbusob/busobname/{busobname}/publicid/{publicid}".format(version=version)
        #         method = "GET"
        #         raise NotImplemented("just a stub, don't use yet")
        #
        #     def getmobileformforbusob(self, version="V1", busobid=None,publicid=None):
        #         """
        #         Get mobile form by BusObId and PublicID
        #         Parameters expected: , busobid=None,publicid=None
        #         """
        #         uri = "/api/{version}/getmobileformforbusob/busobid/{busobid}/publicid/{publicid}".format(version=version)
        #         method = "GET"
        #         raise NotImplemented("just a stub, don't use yet")
        #
        #     def getmobileformforbusob(self, version="V1", busobname=None,busobrecid=None):
        #         """
        #         Get mobile form by BusObName and record ID.
        #         Parameters expected: , busobname=None,busobrecid=None
        #         """
        #         uri = "/api/{version}/getmobileformforbusob/busobname/{busobname}/busobrecid/{busobrecid}".format(version=version)
        #         method = "GET"
        #         raise NotImplemented("just a stub, don't use yet")
        #
        #     def getquicksearchconfigurationforbusobs(self, version="V1"):
        #         """
        #         Get a Quick Search from a list of Business Object IDs
        #         Parameters expected:
        #         """
        #         uri = "/api/{version}/getquicksearchconfigurationforbusobs".format(version=version)
        #         method = "POST"
        #         raise NotImplemented("just a stub, don't use yet")
        #
        #     def getquicksearchconfigurationforbusobswithviewrights(self, version="V1"):
        #         """
        #         Get a Quick Search by Business Objects with view rights
        #         Parameters expected:
        #         """
        #         uri = "/api/{version}/getquicksearchconfigurationforbusobswithviewrights".format(version=version)
        #         method = "GET"
        #         raise NotImplemented("just a stub, don't use yet")
        #
        #     def getquicksearchresults(self, version="V1"):
        #         """
        #         Execute a Quick Search from a list of Business Object IDs and search text
        #         Parameters expected:
        #         """
        #         uri = "/api/{version}/getquicksearchresults".format(version=version)
        #         method = "POST"
        #         raise NotImplemented("just a stub, don't use yet")
        #
        #     def getquicksearchspecificresults(self, version="V1"):
        #         """
        #         Execute a Quick Search on a specific Business Object
        #         Parameters expected:
        #         """
        #         uri = "/api/{version}/getquicksearchspecificresults".format(version=version)
        #         method = "POST"
        #         raise NotImplemented("just a stub, don't use yet")
        #
        #     def getrelatedbusinessobject(self, version="V1", parentbusobid=None,parentbusobrecid=None,relationshipid=None,gridid=None):
        #         """
        #         Get related Business Objects custom grid
        #         Parameters expected: , parentbusobid=None,parentbusobrecid=None,relationshipid=None,gridid=None
        #         """
        #         uri = "/api/{version}/getrelatedbusinessobject/parentbusobid/{parentbusobid}/parentbusobrecid/{parentbusobrecid}/relationshipid/{relationshipid}/gridid/{gridid}".format(version=version)
        #         method = "GET"
        #         raise NotImplemented("just a stub, don't use yet")
        #
        #     def getrelatedbusinessobject(self, version="V1", parentbusobid=None,parentbusobrecid=None,relationshipid=None):
        #         """
        #         Get related Business Objects by ID
        #         Parameters expected: , parentbusobid=None,parentbusobrecid=None,relationshipid=None
        #         """
        #         uri = "/api/{version}/getrelatedbusinessobject/parentbusobid/{parentbusobid}/parentbusobrecid/{parentbusobrecid}/relationshipid/{relationshipid}".format(version=version)
        #         method = "GET"
        #         raise NotImplemented("just a stub, don't use yet")
        #
        #     def getrelatedbusinessobject(self, version="V1"):
        #         """
        #         Get related Business Objects using a request object
        #         Parameters expected:
        #         """
        #         uri = "/api/{version}/getrelatedbusinessobject".format(version=version)
        #         method = "POST"
        #         raise NotImplemented("just a stub, don't use yet")
        #
        #     def getroles(self, version="V1"):
        #         """
        #         Get all available Roles
        #         Parameters expected:
        #         """
        #         uri = "/api/{version}/getroles".format(version=version)
        #         method = "GET"
        #         raise NotImplemented("just a stub, don't use yet")
        #
        #     def getsearchitems(self, version="V1", association=None,scope=None,scopeowner=None,folder=None):
        #         """
        #         Get all saved searches by Folder ID
        #         Parameters expected: , association=None,scope=None,scopeowner=None,folder=None
        #         """
        #         uri = "/api/{version}/getsearchitems/association/{association}/scope/{scope}/scopeowner/{scopeowner}/folder/{folder}".format(version=version)
        #         method = "GET"
        #         raise NotImplemented("just a stub, don't use yet")
        #
        #     def getsearchitems(self, version="V1", association=None):
        #         """
        #         Get all saved searches by Business Object association
        #         Parameters expected: , association=None
        #         """
        #         uri = "/api/{version}/getsearchitems/association/{association}".format(version=version)
        #         method = "GET"
        #         raise NotImplemented("just a stub, don't use yet")
        #
        #     def getsearchitems(self, version="V1", association=None,scope=None,scopeowner=None):
        #         """
        #         Get all saved searches by scope owner (sub scope)
        #         Parameters expected: , association=None,scope=None,scopeowner=None
        #         """
        #         uri = "/api/{version}/getsearchitems/association/{association}/scope/{scope}/scopeowner/{scopeowner}".format(version=version)
        #         method = "GET"
        #         raise NotImplemented("just a stub, don't use yet")
        #
        #     def getsearchitems(self, version="V1"):
        #         """
        #         Get all saved searches by default Business Object association
        #         Parameters expected:
        #         """
        #         uri = "/api/{version}/getsearchitems".format(version=version)
        #         method = "GET"
        #         raise NotImplemented("just a stub, don't use yet")
        #
        #     def getsearchitems(self, version="V1", association=None,scope=None):
        #         """
        #         Get all saved searches by scope
        #         Parameters expected: , association=None,scope=None
        #         """
        #         uri = "/api/{version}/getsearchitems/association/{association}/scope/{scope}".format(version=version)
        #         method = "GET"
        #         raise NotImplemented("just a stub, don't use yet")
        #
        #     def getsearchresults(self, version="V1"):
        #         """
        #         Run an ad-hoc search
        #         Parameters expected:
        #         """
        #         uri = "/api/{version}/getsearchresults".format(version=version)
        #         method = "POST"
        #         raise NotImplemented("just a stub, don't use yet")
        #
        #     def getsearchresults(self, version="V1", association=None,scope=None,scopeowner=None,searchid=None):
        #         """
        #         Run a saved search by internal ID
        #         Parameters expected: , association=None,scope=None,scopeowner=None,searchid=None
        #         """
        #         uri = "/api/{version}/getsearchresults/association/{association}/scope/{scope}/scopeowner/{scopeowner}/searchid/{searchid}".format(version=version)
        #         method = "GET"
        #         raise NotImplemented("just a stub, don't use yet")
        #
        #     def getsearchresults(self, version="V1", association=None,scope=None,scopeowner=None,searchname=None):
        #         """
        #         Run a saved search by name
        #         Parameters expected: , association=None,scope=None,scopeowner=None,searchname=None
        #         """
        #         uri = "/api/{version}/getsearchresults/association/{association}/scope/{scope}/scopeowner/{scopeowner}/searchname/{searchname}".format(version=version)
        #         method = "GET"
        #         raise NotImplemented("just a stub, don't use yet")
        #
        #     def getsearchresultsexport(self, version="V1", association=None,scope=None,scopeowner=None,searchname=None,exportformat=None):
        #         """
        #         Export a saved search by name
        #         Parameters expected: , association=None,scope=None,scopeowner=None,searchname=None,exportformat=None
        #         """
        #         uri = "/api/{version}/getsearchresultsexport/association/{association}/scope/{scope}/scopeowner/{scopeowner}/searchname/{searchname}/exportformat/{exportformat}".format(version=version)
        #         method = "GET"
        #         raise NotImplemented("just a stub, don't use yet")
        #
        #     def getsearchresultsexport(self, version="V1"):
        #         """
        #         Export an ad-hoc search
        #         Parameters expected:
        #         """
        #         uri = "/api/{version}/getsearchresultsexport".format(version=version)
        #         method = "POST"
        #         raise NotImplemented("just a stub, don't use yet")
        #
        #     def getsearchresultsexport(self, version="V1", association=None,scope=None,scopeowner=None,searchid=None,exportformat=None):
        #         """
        #         Export a saved search by ID
        #         Parameters expected: , association=None,scope=None,scopeowner=None,searchid=None,exportformat=None
        #         """
        #         uri = "/api/{version}/getsearchresultsexport/association/{association}/scope/{scope}/scopeowner/{scopeowner}/searchid/{searchid}/exportformat/{exportformat}".format(version=version)
        #         method = "GET"
        #         raise NotImplemented("just a stub, don't use yet")
        #
        #     def getsecuritygroupbusinessobjectpermissions(self, version="V1", groupname=None,busobname=None):
        #         """
        #         Get Business Object permissions by Security Group
        #         Parameters expected: , groupname=None,busobname=None
        #         """
        #         uri = "/api/{version}/getsecuritygroupbusinessobjectpermissions/groupname/{groupname}/busobname/{busobname}".format(version=version)
        #         method = "GET"
        #         raise NotImplemented("just a stub, don't use yet")
        #
        #     def getsecuritygroupbusinessobjectpermissions(self, version="V1", groupid=None,busobid=None):
        #         """
        #         Get Business Object permissions by Security Group
        #         Parameters expected: , groupid=None,busobid=None
        #         """
        #         uri = "/api/{version}/getsecuritygroupbusinessobjectpermissions/groupid/{groupid}/busobid/{busObId}".format(version=version)
        #         method = "GET"
        #         raise NotImplemented("just a stub, don't use yet")
        #
        #     def getsecuritygroupbusinessobjectpermissionsforcurrentuserbybusobid(self, version="V1", busobid=None):
        #         """
        #         Get Business Object permission for current user
        #         Parameters expected: , busobid=None
        #         """
        #         uri = "/api/{version}/getsecuritygroupbusinessobjectpermissionsforcurrentuserbybusobid/busobid/{busObId}".format(version=version)
        #         method = "GET"
        #         raise NotImplemented("just a stub, don't use yet")
        #
        #     def getsecuritygroupbusinessobjectpermissionsforcurrentuserbybusobname(self, version="V1", busobname=None):
        #         """
        #         Get Business Object permissions for current user
        #         Parameters expected: , busobname=None
        #         """
        #         uri = "/api/{version}/getsecuritygroupbusinessobjectpermissionsforcurrentuserbybusobname/busobname/{busobname}".format(version=version)
        #         method = "GET"
        #         raise NotImplemented("just a stub, don't use yet")
        #
        #     def getsecuritygroupcategories(self, version="V1"):
        #         """
        #         Get all Security Group categories
        #         Parameters expected:
        #         """
        #         uri = "/api/{version}/getsecuritygroupcategories".format(version=version)
        #         method = "GET"
        #         raise NotImplemented("just a stub, don't use yet")
        #
        #     def getsecuritygrouprights(self, version="V1", groupid=None,categoryid=None):
        #         """
        #         Get permissions for a Security Group by category
        #         Parameters expected: , groupid=None,categoryid=None
        #         """
        #         uri = "/api/{version}/getsecuritygrouprights/groupid/{groupid}/categoryid/{categoryid}".format(version=version)
        #         method = "GET"
        #         raise NotImplemented("just a stub, don't use yet")
        #
        #     def getsecuritygrouprights(self, version="V1", groupname=None,categoryname=None):
        #         """
        #         Get permissions for a Security Group by category
        #         Parameters expected: , groupname=None,categoryname=None
        #         """
        #         uri = "/api/{version}/getsecuritygrouprights/groupname/{groupname}/categoryname/{categoryname}".format(version=version)
        #         method = "GET"
        #         raise NotImplemented("just a stub, don't use yet")
        #
        #     def getsecuritygrouprightsforcurrentuserbycategoryid(self, version="V1", categoryid=None):
        #         """
        #         Get current user's permissions by Security Group category by ID
        #         Parameters expected: , categoryid=None
        #         """
        #         uri = "/api/{version}/getsecuritygrouprightsforcurrentuserbycategoryid/categoryid/{categoryid}".format(version=version)
        #         method = "GET"
        #         raise NotImplemented("just a stub, don't use yet")
        #
        #     def getsecuritygrouprightsforcurrentuserbycategoryname(self, version="V1", categoryname=None):
        #         """
        #         Get current user's permissions by Security Group category by name
        #         Parameters expected: , categoryname=None
        #         """
        #         uri = "/api/{version}/getsecuritygrouprightsforcurrentuserbycategoryname/categoryname/{categoryname}".format(version=version)
        #         method = "GET"
        #         raise NotImplemented("just a stub, don't use yet")
        #
        #     def getsecuritygroups(self, version="V1"):
        #         """
        #         Get all available Security Groups
        #         Parameters expected:
        #         """
        #         uri = "/api/{version}/getsecuritygroups".format(version=version)
        #         method = "GET"
        #         raise NotImplemented("just a stub, don't use yet")
        #
        #     def getteams(self, version="V1"):
        #         """
        #         Get all available Teams
        #         Parameters expected:
        #         """
        #         uri = "/api/{version}/getteams".format(version=version)
        #         method = "GET"
        #         raise NotImplemented("just a stub, don't use yet")
        #
        #     def getuserbatch(self, version="V1"):
        #         """
        #         Get user information in a batch
        #         Parameters expected:
        #         """
        #         uri = "/api/{version}/getuserbatch".format(version=version)
        #         method = "POST"
        #         raise NotImplemented("just a stub, don't use yet")
        #
        #     def getuserbyloginid(self, version="V1", loginid=None):
        #         """
        #         Get a user by login ID
        #         Parameters expected: , loginid=None
        #         """
        #         uri = "/api/{version}/getuserbyloginid/loginid/{loginid}".format(version=version)
        #         method = "GET"
        #         raise NotImplemented("just a stub, don't use yet")
        #
        #     def getuserbyloginid(self, version="V1"):
        #         """
        #         Get a user by login ID and login ID type
        #         Parameters expected:
        #         """
        #         uri = "/api/{version}/getuserbyloginid".format(version=version)
        #         method = "GET"
        #         raise NotImplemented("just a stub, don't use yet")
        #
        #     def getuserbypublicid(self, version="V1", publicid=None):
        #         """
        #         Get a user by public ID
        #         Parameters expected: , publicid=None
        #         """
        #         uri = "/api/{version}/getuserbypublicid/publicid/{publicid}".format(version=version)
        #         method = "GET"
        #         raise NotImplemented("just a stub, don't use yet")
        #
        #     def getusersinsecuritygroup(self, version="V1", groupid=None):
        #         """
        #         Get users in a Security Group
        #         Parameters expected: , groupid=None
        #         """
        #         uri = "/api/{version}/getusersinsecuritygroup/groupid/{groupid}".format(version=version)
        #         method = "GET"
        #         raise NotImplemented("just a stub, don't use yet")
        #
        #     def getusersteams(self, version="V1", userrecordid=None):
        #         """
        #         Get Team assignments for a user
        #         Parameters expected: , userrecordid=None
        #         """
        #         uri = "/api/{version}/getusersteams/userrecordid/{userRecordId}".format(version=version)
        #         method = "GET"
        #         raise NotImplemented("just a stub, don't use yet")
        #
        #     def getworkgroups(self, version="V1"):
        #         """
        #         Get all available Workgroups
        #         Parameters expected:
        #         """
        #         uri = "/api/{version}/getworkgroups".format(version=version)
        #         method = "GET"
        #         raise NotImplemented("just a stub, don't use yet")
        #

    def linkrelatedbusinessobject(self, version="V1", parentbusobid=None, parentbusobrecid=None, relationshipid=None,
                                  busobid=None, busobrecid=None):
        """
        Link related Business Objects
        Parameters expected: , parentbusobid=None,parentbusobrecid=None,relationshipid=None,busobid=None,busobrecid=None
        """
        uri = "/api/{version}/linkrelatedbusinessobject/parentbusobid/{parentbusobid}/parentbusobrecid/{parentbusobrecid}/relationshipid/{relationshipid}/busobid/{busobid}/busobrecid/{busobrecid}".format(
            version=version, parentbusobid=parentbusobid,parentbusobrecid=parentbusobrecid,busobid=busobid,busobrecid=busobrecid,relationshipid=relationshipid)
        method = "GET"
        return self.action(method, uri)
        #
        #     def logout(self, version="V1"):
        #         """
        #         Log out user by token
        #         Parameters expected:
        #         """
        #         uri = "/api/{version}/logout".format(version=version)
        #         method = "DELETE"
        #         raise NotImplemented("just a stub, don't use yet")
        #
        #     def removebusinessobjectattachment(self, version="V1", attachmentid=None,busobname=None,publicid=None):
        #         """
        #         Remove an attachment by Business Object name and public ID
        #         Parameters expected: , attachmentid=None,busobname=None,publicid=None
        #         """
        #         uri = "/api/{version}/removebusinessobjectattachment/attachmentid/{attachmentid}/busobname/{busobname}/publicid/{publicid}".format(version=version)
        #         method = "DELETE"
        #         raise NotImplemented("just a stub, don't use yet")
        #
        #     def removebusinessobjectattachment(self, version="V1", attachmentid=None,busobid=None,publicid=None):
        #         """
        #         Remove an attachment by Business Object ID and public ID
        #         Parameters expected: , attachmentid=None,busobid=None,publicid=None
        #         """
        #         uri = "/api/{version}/removebusinessobjectattachment/attachmentid/{attachmentid}/busobid/{busobid}/publicid/{publicid}".format(version=version)
        #         method = "DELETE"
        #         raise NotImplemented("just a stub, don't use yet")
        #
        #     def removebusinessobjectattachment(self, version="V1", attachmentid=None,busobname=None,busobrecid=None):
        #         """
        #         Remove an attachment by Business Object name and record ID
        #         Parameters expected: , attachmentid=None,busobname=None,busobrecid=None
        #         """
        #         uri = "/api/{version}/removebusinessobjectattachment/attachmentid/{attachmentid}/busobname/{busobname}/busobrecid/{busobrecid}".format(version=version)
        #         method = "DELETE"
        #         raise NotImplemented("just a stub, don't use yet")
        #
        #     def removebusinessobjectattachment(self, version="V1", attachmentid=None,busobid=None,busobrecid=None):
        #         """
        #         Remove an attachment by Business Object ID and record ID
        #         Parameters expected: , attachmentid=None,busobid=None,busobrecid=None
        #         """
        #         uri = "/api/{version}/removebusinessobjectattachment/attachmentid/{attachmentid}/busobid/{busobid}/busobrecid/{busobrecid}".format(version=version)
        #         method = "DELETE"
        #         raise NotImplemented("just a stub, don't use yet")
        #
        #     def removeuserfromteam(self, version="V1", teamid=None,userrecordid=None):
        #         """
        #         Remove a user from a team
        #         Parameters expected: , teamid=None,userrecordid=None
        #         """
        #         uri = "/api/{version}/removeuserfromteam/teamid/{teamId}/userrecordid/{userrecordid}".format(version=version)
        #         method = "DELETE"
        #         raise NotImplemented("just a stub, don't use yet")
        #
        #     def savebusinessobject(self, version="V1"):
        #         """
        #         Create or Update a Business Object
        #         Parameters expected:
        #         """
        #         uri = "/api/{version}/savebusinessobject".format(version=version)
        #         method = "POST"
        #         raise NotImplemented("just a stub, don't use yet")
        #
        #     def savebusinessobjectattachmentbusob(self, version="V1"):
        #         """
        #         Attach a Business Object to a Business Object
        #         Parameters expected:
        #         """
        #         uri = "/api/{version}/savebusinessobjectattachmentbusob".format(version=version)
        #         method = "PUT"
        #         raise NotImplemented("just a stub, don't use yet")
        #
        #     def savebusinessobjectattachmentlink(self, version="V1"):
        #         """
        #         Attach a file via UNC
        #         Parameters expected:
        #         """
        #         uri = "/api/{version}/savebusinessobjectattachmentlink".format(version=version)
        #         method = "PUT"
        #         raise NotImplemented("just a stub, don't use yet")
        #
        #     def savebusinessobjectattachmenturl(self, version="V1"):
        #         """
        #         Attach a URL path
        #         Parameters expected:
        #         """
        #         uri = "/api/{version}/savebusinessobjectattachmenturl".format(version=version)
        #         method = "PUT"
        #         raise NotImplemented("just a stub, don't use yet")
        #
        #     def savebusinessobjectbatch(self, version="V1"):
        #         """
        #         Create or update a batch of Business Objects
        #         Parameters expected:
        #         """
        #         uri = "/api/{version}/savebusinessobjectbatch".format(version=version)
        #         method = "POST"
        #         raise NotImplemented("just a stub, don't use yet")
        #
        #     def saverelatedbusinessobject(self, version="V1"):
        #         """
        #         Create or update a related Business Object
        #         Parameters expected:
        #         """
        #         uri = "/api/{version}/saverelatedbusinessobject".format(version=version)
        #         method = "POST"
        #         raise NotImplemented("just a stub, don't use yet")
        #
        #     def saveteam(self, version="V1"):
        #         """
        #         Create or update a team
        #         Parameters expected:
        #         """
        #         uri = "/api/{version}/saveteam".format(version=version)
        #         method = "POST"
        #         raise NotImplemented("just a stub, don't use yet")
        #
        #     def saveuser(self, version="V1"):
        #         """
        #         Create or update a user
        #         Parameters expected:
        #         """
        #         uri = "/api/{version}/saveuser".format(version=version)
        #         method = "POST"
        #         raise NotImplemented("just a stub, don't use yet")
        #
        #     def saveuserbatch(self, version="V1"):
        #         """
        #         Create or update users in a batch
        #         Parameters expected:
        #         """
        #         uri = "/api/{version}/saveuserbatch".format(version=version)
        #         method = "POST"
        #         raise NotImplemented("just a stub, don't use yet")
        #
        #     def serviceinfo(self, version="V1"):
        #         """
        #         Get information about the REST Api and CSM
        #         Parameters expected:
        #         """
        #         uri = "/api/{version}/serviceinfo".format(version=version)
        #         method = "GET"
        #         raise NotImplemented("just a stub, don't use yet")
        #
        #     def unlinkrelatedbusinessobject(self, version="V1", parentbusobid=None,parentbusobrecid=None,relationshipid=None,busobid=None,busobrecid=None):
        #         """
        #         UnLink related Business Objects
        #         Parameters expected: , parentbusobid=None,parentbusobrecid=None,relationshipid=None,busobid=None,busobrecid=None
        #         """
        #         uri = "/api/{version}/unlinkrelatedbusinessobject/parentbusobid/{parentbusobid}/parentbusobrecid/{parentbusobrecid}/relationshipid/{relationshipid}/busobid/{busobid}/busobrecid/{busobrecid}".format(version=version)
        #         method = "DELETE"
        #         raise NotImplemented("just a stub, don't use yet")
        #
        #     def uploadbusinessobjectattachment(self, version="V1", filename=None,busobid=None,publicid=None,offset=None,totalsize=None):
        #         """
        #         Upload an attachment by Business Object ID and public ID
        #         Parameters expected: , filename=None,busobid=None,publicid=None,offset=None,totalsize=None
        #         """
        #         uri = "/api/{version}/uploadbusinessobjectattachment/filename/{filename}/busobid/{busobid}/publicid/{publicid}/offset/{offset}/totalsize/{totalsize}".format(version=version)
        #         method = "POST"
        #         raise NotImplemented("just a stub, don't use yet")
        #
        #     def uploadbusinessobjectattachment(self, version="V1", filename=None,busobid=None,busobrecid=None,offset=None,totalsize=None):
        #         """
        #         Upload an attachment by Business Object ID and record ID
        #         Parameters expected: , filename=None,busobid=None,busobrecid=None,offset=None,totalsize=None
        #         """
        #         uri = "/api/{version}/uploadbusinessobjectattachment/filename/{filename}/busobid/{busobid}/busobrecid/{busobrecid}/offset/{offset}/totalsize/{totalsize}".format(version=version)
        #         method = "POST"
        #         raise NotImplemented("just a stub, don't use yet")
        #
        #     def uploadbusinessobjectattachment(self, version="V1", filename=None,busobname=None,publicid=None,offset=None,totalsize=None):
        #         """
        #         Upload an attachment by Business Object name and public ID
        #         Parameters expected: , filename=None,busobname=None,publicid=None,offset=None,totalsize=None
        #         """
        #         uri = "/api/{version}/uploadbusinessobjectattachment/filename/{filename}/busobname/{busobname}/publicid/{publicid}/offset/{offset}/totalsize/{totalsize}".format(version=version)
        #         method = "POST"
        #         raise NotImplemented("just a stub, don't use yet")
        #
        #     def uploadbusinessobjectattachment(self, version="V1", filename=None,busobname=None,busobrecid=None,offset=None,totalsize=None):
        #         """
        #         Upload an attachment by Business Object name and record ID
        #         Parameters expected: , filename=None,busobname=None,busobrecid=None,offset=None,totalsize=None
        #         """
        #         uri = "/api/{version}/uploadbusinessobjectattachment/filename/{filename}/busobname/{busobname}/busobrecid/{busobrecid}/offset/{offset}/totalsize/{totalsize}".format(version=version)
        #         method = "POST"
        #         raise NotImplemented("just a stub, don't use yet")
        #
