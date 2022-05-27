def is_google_cloud_service(name):
    """Python 3.9"""

    words = name.lower().split()

    if words[0] == "cloud" and len(words) > 1:
        if words[1:] == ["run"] or words[1:] == ["functions"]:
            return "Google Cloudのサービスです"
        else:
            return "Google Cloudのサービスかもしれません"
    elif words[0] == "google" and len(words) > 1:
        if words[2:] == ["engine"] and (words[1] == "kubernetes" or words[1] == "app" or words[1] == "compute"):
            return "Google Cloudのサービスです"
        else:
            return "Google Cloudのサービスかもしれません"
    elif words == ["bigquery"] or words == ["anthos"]:
        return "Google Cloudのサービスです"
    else:
        return "Google Cloudのサービスではありません"


# def is_google_cloud_service(name):
#     """Python 3.10"""

#     match name.lower().split():
#         case ["cloud", ("run" | "functions")]:
#             return "Google Cloudのサービスです"
#         case ["google", ("kubernetes" | "app" | "compute"), "engine"]:
#             return "Google Cloudのサービスです"
#         case [("bigquery" | "anthos")]:
#             return "Google Cloudのサービスです"
#         case [("cloud" | "google"), suffix1, *suffix]:
#             return "Google Cloudのサービスかもしれません"
#         case _:
#             return "Google Cloudのサービスではありません"


if __name__ == "__main__":
    while True:
        print(is_google_cloud_service(input("サービス名を入力してください: ")))
        print("")
