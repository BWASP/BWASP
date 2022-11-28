class Return_object:
    def __init__(self):
        self.success_response = {
            "message": "Success"
        }
        self.failed_response = {
            "message": "Failed"
        }

    def return_post_http_status_message(self, Type=bool):
        if Type is True:
            return self.success_response, 201

        if Type is False:
            return self.failed_response, 500

    def return_patch_http_status_message(self, Type=bool):
        if Type is True:
            return self.success_response, 200

        if Type is False:
            return self.failed_response, 500

