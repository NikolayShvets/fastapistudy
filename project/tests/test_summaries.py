import json

import pytest


def test_create_summary__created(test_app_with_db):
    data = {"url": "https://foo.bar"}
    response = test_app_with_db.post("summaries", data=json.dumps(data))

    assert response.status_code == 201
    assert response.json()["url"] == data["url"]


def test_create_summary_invalid_json__not_created(test_app):
    response = test_app.post("/summaries/", data=json.dumps({}))
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "loc": ["body", "url"],
                "msg": "field required",
                "type": "value_error.missing"
            }
        ]
    }


def test_read_summary__ok(test_app_with_db):
    data = {"url": "https://foo.bar"}
    response = test_app_with_db.post("summaries", data=json.dumps(data))
    summary_id = response.json()["id"]

    response = test_app_with_db.get(f"/summaries/{summary_id}/")
    assert response.status_code == 200

    response_dict = response.json()
    assert response_dict["id"] == summary_id
    assert response_dict["url"] == "https://foo.bar"
    assert response_dict["summary"]
    assert response_dict["created_at"]


def test_read_summary_incorrect_id__not_found(test_app_with_db):
    incorrect_id = 999
    response = test_app_with_db.get(f"/summaries/{incorrect_id}/")
    assert response.status_code == 404
    assert response.json()["detail"] == "Summary not found"


def test_read_all_summaries(test_app_with_db):
    data = {"url": "https://foo.bar"}
    response = test_app_with_db.post("/summaries/", data=json.dumps(data))
    summary_id = response.json()["id"]

    response = test_app_with_db.get("/summaries/")
    assert response.status_code == 200

    response_list = response.json()
    assert len(list(filter(lambda d: d["id"] == summary_id, response_list))) == 1
