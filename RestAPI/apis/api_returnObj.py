class Return_object:
    def __init__(self):
        self.Success_returnData = {
            "message": "Success"
        }
        self.Failed_returnData = {
            "message": "Failed"
        }

    def return_post_http_status_message(self, Type=bool):
        if Type is True:
            return self.Success_returnData, 201

        if Type is False:
            return self.Failed_returnData, 500

    def return_patch_http_status_message(self, Type=bool):
        if Type is True:
            return self.Success_returnData, 200

        if Type is False:
            return self.Failed_returnData, 500

