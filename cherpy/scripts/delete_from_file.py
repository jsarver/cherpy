from cherpy.api import config_from_env
from cherpy.main import create_delete_requests, get_object_info, search_object,extract_data
# c = config_from_file(env="PROD_CHERPY")
c = config_from_env(env="qa_chewey")
c.login()


col,d =extract_data("C:\\Users\\jsarver\\Documents\\Cherwell\\Cherwell Load Data\\routing rules\\prod_remove_rules.csv")

def delete_object_batch(c, object_name, pageSize=10000):
    del_obj_info = get_object_info(c, object_name)
    del_dict = search_object(c, object_id=del_obj_info.busObId, fields=["RecId"], pageSize=pageSize).json()
    del_results = create_delete_requests(del_obj_info, del_dict['businessObjects'])

    return c.post("api/V1/deletebusinessobjectbatch", data=del_results)


obj = get_object_info(c,"ticketrouting")
dl=[{'busObRecId': i[0],"busObId":obj.busObId,"busObPublicId":""} for i in d]
dl_req={"deleteRequests": dl}
# r=c.post("api/V1/deletebusinessobjectbatch", data=dl_req)