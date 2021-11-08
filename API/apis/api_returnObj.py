class ReturnObject:
    def __init__(self):
        self.Success_returnData = {
            "message": "Success"
        }
        self.Failed_returnData = {
            "message": "Failed"
        }

    def Return_POST_HTTPStatusMessage(self, Type=bool):
        if Type is True:
            return self.Success_returnData, 201

        if Type is False:
            return self.Failed_returnData, 500

    def Return_PATCH_HTTPStatusMessage(self, Type=bool):
        if Type is True:
            return self.Success_returnData, 200

        if Type is False:
            return self.Failed_returnData, 500
