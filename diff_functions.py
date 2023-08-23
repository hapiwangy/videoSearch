# set the functions for keyword
def setOptions() -> dict[str, str]:
    with open("nkw.csv","r", encoding="utf-8") as fp:
        newk = fp.readlines()
    newk = list(newk[0].split(',')) 
    options = {str(k): y for k, y in enumerate(newk)}
    return options

# return SAS value
def SASproducer()->str:    
    from azure.storage.blob import BlobServiceClient, generate_account_sas, ResourceTypes, AccountSasPermissions
    from datetime import datetime, timedelta
    from urllib.parse import quote

    STORAGE_ACCOUNT_NAME = "<your storage account name>"
    ACCOUNT_ACCESS_KEY = "<your account access key>"

    # get SAS token for photos
    def get_sas_token_blob():
        sas_token = generate_account_sas(
            account_name=STORAGE_ACCOUNT_NAME,
            account_key=ACCOUNT_ACCESS_KEY,
            resource_types=ResourceTypes(object=True),
            permission=AccountSasPermissions(read=True),
            expiry=datetime.utcnow() + timedelta(hours=1)
        )
        return sas_token
    return get_sas_token_blob()

# return the api search result
def VideoSearchApi(threshold: int, query: list[str])->dict[str,dict[str,list[dict[str,int|str]]]]:
    import json, requests
    classify = {}
    for q in query:
        # 限定某個關鍵字
        classify[q] = {}
        # 呼叫api
        response = requests.post(url="https://mcapscognitiveeastus.cognitiveservices.azure.com/vision-retrieval/retrieval/indexes/tsmc:query?api-version=2023-01-15-preview",
                             headers={"Ocp-Apim-Subscription-Key" : "<your ocp-Apim_subscription-key>",
                                      "Content-Type" : "application/json"},
                             data = json.dumps({"queryText":f"{q}"}))
        test_data = json.loads(response.text)
        for t in test_data["value"]:
            if t["relevance"] < threshold:
                break
            if t["documentId"] not in classify[q]:
                classify[q][t["documentId"]] = [t]
            else :
                classify[q][t["documentId"]].append(t)
    return classify
    # below for check the answer
    # for x, y in classify.items():
    #     print(f"query text is {x}")
    #     for k, v in y.items():
    #         print(k, v)

# return document name and it's url+sas
def VideoandUrl()->dict[str, str]:
    token = SASproducer()
    import requests
    response = requests.get("https://mcapscognitiveeastus.cognitiveservices.azure.com/vision-retrieval/retrieval/indexes/tsmc/documents?api-version=2023-01-15-preview",
                        headers = {"Ocp-Apim-Subscription-Key": "<your ocp-Apim_subscription-key>"})
    import json
    result = json.loads(response.text)
    result = result['value']
    answer = {}
    for x in result:
        answer[x['documentId']] = x['documentUrl']+f"?{token}"
    return answer
