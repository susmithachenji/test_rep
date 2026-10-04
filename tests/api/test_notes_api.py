import pytest

from clients.notes_client import NotesClient

pytestmark = pytest.mark.api


def test_register_login_and_read_profile(registered_user: dict[str, str]) -> None:
    client = NotesClient()

    register_response = client.register(**registered_user)
    assert register_response.status_code == 201
    assert register_response.json()["message"] == "User account created successfully"

    token = client.login_and_store_token(registered_user["email"], registered_user["password"])
    assert token
    assert client.headers["x-auth-token"] == token

    profile = client.get_profile()
    assert profile.status_code == 200
    assert profile.json()["data"]["email"] == registered_user["email"]

    assert client.logout().status_code == 200
    client.delete_account()


def test_login_with_wrong_password_is_rejected(registered_notes_api: NotesClient) -> None:
    response = registered_notes_api.login(registered_notes_api.credentials["email"], "definitely-wrong")

    assert response.status_code == 401
    assert response.json()["message"] == "Incorrect email address or password"


def test_create_note_and_read_it_back(notes_api: NotesClient) -> None:
    title, description, category = "Playwright API note", "Created by pytest", "Home"

    create_response = notes_api.create_note(title, description, category)
    assert create_response.status_code == 200
    created = create_response.json()["data"]
    assert created["title"] == title
    assert created["description"] == description
    assert created["category"] == category
    assert created["completed"] is False
    assert created["id"]

    list_response = notes_api.list_notes()
    assert list_response.status_code == 200
    assert [note["id"] for note in list_response.json()["data"]] == [created["id"]]

    get_response = notes_api.get_note(created["id"])
    assert get_response.status_code == 200
    assert get_response.json()["data"] == created


@pytest.mark.parametrize(
    ("payload", "expected_message"),
    [
        ({"title": "abc", "description": "long enough description", "category": "Home"}, "Title must be between 4 and 100 characters"),
        ({"title": "Valid title", "description": "hi", "category": "Home"}, "Description must be between 4 and 1000 characters"),
    ],
    ids=["short-title", "short-description"],
)
def test_create_note_validation_errors(notes_api: NotesClient, payload: dict, expected_message: str) -> None:
    response = notes_api.create_note(**payload)

    assert response.status_code == 400
    body = response.json()
    assert body["success"] is False
    assert body["message"] == expected_message


def test_update_note_completion_and_content(notes_api: NotesClient) -> None:
    note = notes_api.create_sample_note()

    patch_response = notes_api.set_note_completed(note["id"], True)
    assert patch_response.status_code == 200
    assert patch_response.json()["data"]["completed"] is True

    put_response = notes_api.update_note(
        note["id"],
        title="Updated API note",
        description="Updated by pytest",
        category="Work",
        completed=False,
    )
    assert put_response.status_code == 200
    updated = put_response.json()["data"]
    assert (updated["title"], updated["category"], updated["completed"]) == ("Updated API note", "Work", False)


def test_delete_note_then_it_is_gone(notes_api: NotesClient) -> None:
    note = notes_api.create_sample_note(title="Temporary API note")

    delete_response = notes_api.delete_note(note["id"])
    assert delete_response.status_code == 200
    assert delete_response.json()["message"] == "Note successfully deleted"

    assert notes_api.get_note(note["id"]).status_code == 404
    assert notes_api.list_notes().json()["data"] == []


@pytest.mark.parametrize(
    ("note_id", "expected_status", "expected_message"),
    [
        ("not-an-object-id", 400, "Note ID must be a valid ID"),
        ("6ac2e1052d8551029606f5cd", 404, None),
    ],
    ids=["invalid-id", "unknown-id"],
)
def test_get_note_with_bad_id(notes_api: NotesClient, note_id: str, expected_status: int, expected_message: str | None) -> None:
    response = notes_api.get_note(note_id)

    assert response.status_code == expected_status
    if expected_message:
        assert response.json()["message"] == expected_message


def test_protected_endpoints_require_a_valid_token(anonymous_notes_api: NotesClient) -> None:
    without_token = anonymous_notes_api.list_notes()
    assert without_token.status_code == 401
    assert "No authentication token" in without_token.json()["message"]

    anonymous_notes_api.set_token("this-token-does-not-exist")
    with_invalid_token = anonymous_notes_api.list_notes()
    assert with_invalid_token.status_code == 401
    assert with_invalid_token.json()["success"] is False

    anonymous_notes_api.set_token(None)
    assert anonymous_notes_api.create_note("Title here", "Description here", "Home").status_code == 401