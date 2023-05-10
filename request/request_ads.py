import requests

from request_user import users_login


def ad_reg(url: str, data: dict, token: str) -> dict:
    response = requests.post(
        url=url + "/ads/create_ad/",
        json={
            "title": data['title'],
            "description": data['description']
            },
        headers={
            "Content-Type": "application/json",
            "Token": f"{token}"
                }    
        )
    return {"POST ad":
        {"status_code": response.status_code,
        "content": response.json()}
    }    


def ad_get(url, ad_id, token) -> dict:
    response = requests.get(
        url=url + f"/ads/{ad_id}",
        headers={
            "Content-Type": "application/json",
            "Token": f"{token}"
        }
    )
    return {"GET ad":
        {"status_code": response.status_code,
        "content": response.json()}
    }    


def ad_patch(url: str, ad_id: int, data: dict, token: str) -> dict:
    response = requests.patch(
        url=url + f"/ads/{ad_id}",
        json={
            "title": data['title']
            },
        headers={
            "Content-Type": "application/json",
            "Token": f"{token}"
        }
    )
    return {"PATCH ad":
        {"status_code": response.status_code,
        "content": response.json()}
    }    


def ad_delete(url: str, ad_id: int, token: str) -> dict:
    response = requests.delete(
        url=url + f"/ads/{ad_id}",
        headers={
            "Content-Type": "application/json",
            "Token": f"{token}"
        }
    )
    return {"DELETE ad":
        {"status_code": response.status_code,
        "content": response.content}
    }    



if __name__ == "__main__":
    url = 'http://127.0.0.1:8080'

    data_ad={
        "title": "Test",
        "description": "Test description"
    }
    new_data_ad={
        "title": "Test update"
    }

    data_user={
        "name": "Test",
        "surename": "Testov",
        "email": "test@test.ru",
        "password": "123"
    }

    token = users_login(url, data_user)["POST login"]["content"]["description"]["token"]

    ad = ad_reg(url, data_ad, token)
    print(ad)
    id_ad = ad["POST ad"]["content"]["description"]["data"]["id"]

    print(ad_get(url, id_ad, token))
    print(ad_patch(url, id_ad, new_data_ad, token))
    print(ad_get(url, id_ad, token))
    print(ad_delete(url, id_ad, token))
    print(ad_get(url, id_ad, token))