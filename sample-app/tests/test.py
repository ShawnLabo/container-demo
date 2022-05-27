from sys import stderr
import unittest

from app.main import is_google_cloud_service

class Test(unittest.TestCase):
    def test_is_google_cloud_service(self):
        yes_services = [
            "Cloud Run",
            "Cloud Functions",
            "Google Kubernetes Engine",
            "Google App Engine",
            "Google Compute Engine",
            "BigQuery",
            "Anthos",
        ]

        for name in yes_services:
            self.assertEqual(
                is_google_cloud_service(name),
                "Google Cloudのサービスです"
            )

        no_services = [
            "Amazon EC2",
            "Hoge",
            "Lambda",
            "Google",
            "Cloud",
        ]

        for name in no_services:
            self.assertEqual(
                is_google_cloud_service(name),
                "Google Cloudのサービスではありません"
            )

        maybe_services = [
            "Google Docs",
            "Cloud Spanner",
            "Google VMware Engine",
            "Cloud Natural Language",
        ]

        for name in maybe_services:
            self.assertEqual(
                is_google_cloud_service(name),
                "Google Cloudのサービスかもしれません"
            )


if __name__ == "__main__":
    unittest.main()
