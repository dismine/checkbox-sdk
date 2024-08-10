import pathlib

import pytest
from pydantic import ValidationError

from checkbox_sdk.client.synchronous import CheckBoxClient
from ..models.goods_models import GoodSchema, GoodGroupSchema


def test_get_goods(auth_token, license_key):
    assert license_key, "License key is empty"

    with CheckBoxClient() as client:
        client.cashier.authenticate_token(auth_token, license_key=license_key)

        tested = False

        # sourcery skip: no-loop-in-tests
        for good in client.goods.get_goods():
            try:
                model = GoodSchema(**good)
                assert model is not None
            except ValidationError as e:  # pragma: no cover
                pytest.fail(f"Good validation schema failed: {e}")

            # One test will be enough
            # sourcery skip: no-conditionals-in-tests
            if not tested:
                good_by_id = client.goods.get_good(good["id"])
                try:
                    model = GoodSchema(**good_by_id)
                    assert model is not None
                except ValidationError as e:  # pragma: no cover
                    pytest.fail(f"Group validation schema failed: {e}")

                tested = True


def test_get_groups(auth_token, license_key):
    assert license_key, "License key is empty"

    with CheckBoxClient() as client:
        client.cashier.authenticate_token(auth_token, license_key=license_key)

        # sourcery skip: no-loop-in-tests
        for group in client.goods.get_groups():
            try:
                model = GoodGroupSchema(**group)
                assert model is not None
            except ValidationError as e:  # pragma: no cover
                pytest.fail(f"Group validation schema failed: {e}")


def test_export_goods(auth_token, license_key):
    assert license_key, "License key is empty"

    with CheckBoxClient() as client:
        client.cashier.authenticate_token(auth_token, license_key=license_key)

        csv = client.goods.export_goods(
            export_extension="csv",
            timeout=15,
        )
        assert csv, "List is empty"

        json = client.goods.export_goods(
            export_extension="json",
            timeout=15,
        )
        assert json, "List is empty"

        excel = client.goods.export_goods(
            export_extension="excel",
            timeout=15,
        )
        assert excel, "List is empty"


def test_import_goods(auth_token, license_key):
    assert license_key, "License key is empty"

    with CheckBoxClient() as client:
        client.cashier.authenticate_token(auth_token, license_key=license_key)

        base_path = pathlib.Path(__file__).resolve().parent.parent

        goods_path = base_path / "test_data/checkbox_goods.csv"
        response = client.goods.import_goods(file=goods_path, timeout=15)
        assert response["status"] == "done"
        assert response["total_items"] == 2

        goods_path = base_path / "test_data/checkbox_goods.json"
        response = client.goods.import_goods(file=goods_path, timeout=15)
        assert response["status"] == "done"
        assert response["total_items"] == 2

        goods_path = base_path / "test_data/checkbox_goods.xlsx"
        response = client.goods.import_goods(file=goods_path, timeout=15)
        assert response["status"] == "done"
        assert response["total_items"] == 2
