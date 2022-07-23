from multiprocessing.connection import wait
from locust import HttpUser, task, constant
import gevent
from gevent.pool import Group


class LoadTest(HttpUser):
    # wait_time = constant(10)
    host="https://config-service.loadus1.ciscoccservice.com"
    def on_start(self):

        self.client.headers['Authorization']="Bearer eyJhbGciOiJSUzI1NiJ9.eyJjbHVzdGVyIjoiQTUyRCIsInByaXZhdGUiOiJleUpqZEhraU9pSktWMVFpTENKbGJtTWlPaUpCTVRJNFEwSkRMVWhUTWpVMklpd2lZV3huSWpvaVpHbHlJbjAuLk5ud0J0QWh6cGxYUjJpTnpTM2VSVmcuOVJTVjJEY1hZd05TbF9Pck1CYlpRZy1fYkJ4SmllUVpJdlNMN1k2enl2YjdZYm1HRnRzclA2bkpIRkxyZ1JFYjFhdG4xWGRBXzV1Z21NY04ycWpfamJhM1Vwc0pMSU9Da2dKQ0xmVTU3ZjgtaHNOV2w3U2Z6M294V3NOUmRZNEZmeW5mdWtYM2F1NlRmcldURExiTWJES2hua2xjUVN3QW5xaWlJU1QxNGtEWUxrenlJQ1RlWEFfVDlMQXdxWDhXRlNxMXo0QlNKcDh4ZGtzOE8tbGE3VVlfN1hEUjF4RTFFWVNFc25OTWRXUnhPbEV4NUxKVzlucTBfbzk4X1VQdHVyUkQyX1A4SEx0Y0xiNHZwU3pzUUhKZ1NtUUM5U0VyQUdjN1hOOFVMR1VyWmRiVXJpbnFRT0w2MndZTUZHLVctSXRxY3d1VVBCZ3FIRTlNNkRScmJ6MXdWY2tGNWx5OXVvM0RMaHZCYzE1d0hfdjdXLUtHU3owRldoWF8zTVBxSUhVOU5IR1pVbFdVSm05NXRWelptM0VmYnotQ0xfWlJJbjhzblJvUW85RGVBUU9QTUJMMkFrdXlMRGMyOTRSWUszSXlRek9ZWWpEN3N3V29jNTlZOVF0SjRFS2t4MVlOWWpBOERoU2ktOU5ocFBXS2VJYXhOcXprSDJBSmtGa1JsYTNtWWgtNGJWbnVoODdBUDI3R1VEUVhBS3VEbkIyTGpVaVpMSHBNSnpGdFJJME5LbVhxUzBKTm5KdERWdFV4V0VOOFgzUEczMk93UGt6SXFwdGV1VU81OGh2UVhtN1pMUlZzR2lveFdLUHI1eWJLQ2tpMk1tQWh0TTg1WWFNRlZzUjJYUzNhQnEtTWRUQ3dIazBNNVlsS0hld0hhZDY2aXhoUnVDX011dG8wckVmZ3VaSllibzgtVFNWR1JKdW1QTW1tNWRkUWZTUG5zNklTekgyX1h6eHc2a1JuQXhBLWYyUnRXdFloVW4tWUpTbG1YeEVjUVppbkhoX2JiOXgzQ2t4VE5fSU5WSS03ZURHOVV5aUY1T2JrSFBrQUNVQ21LMjhGWVQ5NThTVWpoWVo4ajRKVTFSMzZXUlJqZ3A3UmJaaVhQdExHMjlGTms0ZmpIbVBtR1hMYzNlVFdQclMzT1NJOWNDX2p4cncuZk9ISVZlUWF0bW1lZFVNb2dQS2JxZyIsInVzZXJfdHlwZSI6InVzZXIiLCJ0b2tlbl9pZCI6IkFhWjNyME0yRTJPV1JsTW1RdFpHRm1NQzAwTURGakxUazNPVEl0TUdZMll6bGlNV1U0WlRKaU4yUTVNVGs1T0RVdFpHSmoiLCJyZWZlcmVuY2VfaWQiOiI4MDUzYTE5YS0wZWE2LTQ4NzgtYmU3My0wOGYwNmZjM2I1NWMiLCJpc3MiOiJodHRwczpcL1wvaWRicm9rZXJidHMud2ViZXguY29tXC9pZGIiLCJ1c2VyX21vZGlmeV90aW1lc3RhbXAiOiIyMDIyMDYyMjE3NDM0NC40MDVaIiwicmVhbG0iOiI4OWI0NzRhMy0xN2Q5LTQxZmYtOGZiMC01MzRiZWJkZmIxNjAiLCJjaXNfdXVpZCI6IjIxOWRlOWNkLTFkNjgtNDZlMi04ZWE1LWYxZDI5ZjhjYmVlYiIsInRva2VuX3R5cGUiOiJCZWFyZXIiLCJleHBpcnlfdGltZSI6MTY1NjU0NjIzMDUxNSwiY2xpZW50X2lkIjoiQ2UwNTk5NmFjZjhmMDVlYTk3NDM0M2FiYTA4MGQ4ZTFkMDU3NDAxYzk1MDZjYTY5ODI1YTA4ZWY2OWNmYjg3NWEifQ.WjXLqI9aaMUY0OxK0KErU6EzMvHgZuEuBmSnkphxF-FjnudGYG1n46cU_DD-lx03djdKUkGAMjoAnEpb4XHDgUQh2KfCIo3WokoiJY2TeTQgDlmJj9PwDSHe4SUkLWlWmJMinBBqopN3_9OZuJ_x9WubRunl3Omw2dlPgeqYq_7QPTyZhzN0dseLnhx62kcgk_Xejln74rRqdXE7ejapGELwyYCO_LRWVANhbx4vpZVhVsStdKBtJdQoT5_Qe6No2OwZJy0LL0dOaAPVK10XSRYiVgyhpEFe_c5T1dSGlofC7b_WR6HFUR1Yjav7siA5o1JMn3O8G8u6y6N1Ue3TEw"
        self.client.headers['Content-Type']="application/json"
        self.client.headers['X-ORGANIZATION-ID']="89b474a3-17d9-41ff-8fb0-534bebdfb160"

    @task
    def allapi(self):
        group = Group()
        params = "?agentView=true"
        group.spawn(lambda:self.client.get(url="/cms/api/organization/89b474a3-17d9-41ff-8fb0-534bebdfb160"+params))
        group.spawn(lambda:self.client.get(url="/cms/api/organization/89b474a3-17d9-41ff-8fb0-534bebdfb160/organization-setting"+params))
        group.spawn(lambda:self.client.get(url="/cms/api/organization/89b474a3-17d9-41ff-8fb0-534bebdfb160/tenant-configuration"+params))
        group.spawn(lambda:self.client.get(url="/cms/api/organization/89b474a3-17d9-41ff-8fb0-534bebdfb160/v2/team"+params))
        group.spawn(lambda:self.client.get(url="/cms/api/organization/89b474a3-17d9-41ff-8fb0-534bebdfb160/auxiliary-code"+params))
        group.spawn(lambda:self.client.get(url="/cms/api/organization/89b474a3-17d9-41ff-8fb0-534bebdfb160/v2/entry-point"+params))
        group.spawn(lambda:self.client.get(url="/cms/api/organization/89b474a3-17d9-41ff-8fb0-534bebdfb160/v2/contact-service-queue"+params))
        group.spawn(lambda:self.client.get(url="/cms/api/organization/89b474a3-17d9-41ff-8fb0-534bebdfb160/org-url-mapping"+params))
        group.spawn(lambda:self.client.get(url="/cms/api/organization/89b474a3-17d9-41ff-8fb0-534bebdfb160/user/by-ci-user-id/e900549f-ee14-40f7-8d58-8b021a59556c"))
        group.spawn(lambda:self.client.get(url="/cms/api/organization/89b474a3-17d9-41ff-8fb0-534bebdfb160/address-book/6b6b3671-a170-4e39-88e6-d346b197c9fc"))
        group.spawn(lambda:self.client.get(url="/cms/api/organization/89b474a3-17d9-41ff-8fb0-534bebdfb160/outdial-ani/3fc03e60-55c0-4056-864a-77cab78f23d7"))
        group.spawn(lambda:self.client.get(url="/cms/api/organization/89b474a3-17d9-41ff-8fb0-534bebdfb160/site/439391b3-0de3-4552-91c5-ab69602fc586"+params))
        group.spawn(lambda:self.client.get(url="/cms/api/organization/89b474a3-17d9-41ff-8fb0-534bebdfb160/agent-profile/575805a8-d45a-44f2-9113-5d04a9eb9821"))
        group.spawn(lambda:self.client.get(url="/cms/api/organization/89b474a3-17d9-41ff-8fb0-534bebdfb160/dial-plan"+params))
        group.join()
