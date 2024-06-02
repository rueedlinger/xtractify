from starlette.testclient import TestClient

from teal import api
from teal.model import ValidatePdfProfile
from tests import get_path


def test_pdfa_validate_compliant_pdfa():
    client = TestClient(api.app, raise_server_exceptions=False)
    with open(get_path("data/pdfa/pdfa_2b.pdf"), "rb") as f:
        response = client.post(url="/pdfa/validate", files={"file": f})
        assert response.status_code == 200
        assert response.json()["compliant"] is True
        assert response.json()["profile"] == "PDF/A-2B"


def test_pdfa_validate_non_compliant_pdfa():
    client = TestClient(api.app, raise_server_exceptions=False)
    with open(get_path("data/digital_pdf/normal_document.pdf"), "rb") as f:
        response = client.post(url="/pdfa/validate", files={"file": f})
        assert response.status_code == 200
        assert response.json()["compliant"] is False
        assert response.json()["profile"] == "PDF/A-1B"


def test_pdfa_validate_wrong_file_type():
    client = TestClient(api.app, raise_server_exceptions=False)
    with open(get_path("data/doc/normal_document.docx"), "rb") as f:
        response = client.post(url="/pdfa/validate", files={"file": f})
        assert response.status_code == 400
        assert response.json() == {
            "message": "file extension '.docx' is not supported (normal_document.docx)."
        }


def test_pdfa_validate_non_compliant_all_profiles():
    client = TestClient(api.app, raise_server_exceptions=False)
    with open(get_path("data/digital_pdf/normal_document.pdf"), "rb") as f:
        for p in ValidatePdfProfile:
            response = client.post(
                url=f"/pdfa/validate?profile={p.value}", files={"file": f}
            )
            assert response.status_code == 200
            assert response.json()["compliant"] is False
            if "PDF/UA" in response.json()["profile"]:
                assert response.json()["profile"] == "PDF/UA-" + p.value.replace(
                    "ua", ""
                )
            else:
                assert response.json()["profile"] == "PDF/A-" + p.value.upper()
