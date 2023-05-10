import requests


def users_reg(url: str, data: dict) -> dict:
    response = requests.post(
        url=url + "/users/",
        json={
            "name": data['name'],
            "surename": data['surename'],
            "email": data['email'],
            "password": data['password']
            },
        headers={"Content-Type": "application/json"}
    )
    return {"POST register":
        {"status_code": response.status_code,
        "content": response.json()}
    }    


def users_login(url: str, data: dict) -> dict:
    response = requests.post(
        url=url + "/login",
        json={
            "email": data['email'],
            "password": data['password']
            },
        headers={"Content-Type": "application/json"}
    )
    return {"POST login":
       { "status_code": response.status_code,
        "content": response.json()}
    }    


def users_get(url: str, user_id: int, token: str) -> dict:
    response = requests.get(
        url=url + f"/users/{user_id}",
        headers={
            "Content-Type": "application/json",
            "Token": token
        }
    )
    return {"GET user":
        {"status_code": response.status_code,
        "content": response.json()}
    }    


def users_patch(url: str, user_id: int, data: dict, token: str) -> dict:
    response = requests.patch(
        url=url + f"/users/{user_id}",
        json={
            "name": data['name']
            },
        headers={
            "Content-Type": "application/json",
            "Token": token
        }
    )
    return {"PATCH user":
        {"status_code": response.status_code,
        "content": response.json()}
    }    


def users_delete(url: str, user_id: int, token: str) -> dict:
    response = requests.delete(
        url=url + f"/users/{user_id}",
        headers={
            "Content-Type": "application/json",
            "Token": token
        }
    )
    return {"DELETE user":
        {"status_code": response.status_code,
        "content": response.content}
    }    



if __name__ == "__main__":
    url = 'http://127.0.0.1:8080'

    data_user={
        "name": "Test",
        "surename": "Testov",
        "email": "test@test.ru",
        "password": "123"
        }
    new_data_user={
        "name":"Test Updateovich"
    }

    user = users_reg(url, data_user)
    print(user)

    token = users_login(url, data_user)["POST login"]["content"]["description"]["token"]
    id = user["POST register"]["content"]["description"]["data"]["id"]

    print(users_get(url, id, token))
    print(users_patch(url, id, new_data_user, token))
    print(users_get(url, id, token))
    print(users_delete(url, id, token))
    print(users_get(url, id, token))

    users_reg(url, data_user)