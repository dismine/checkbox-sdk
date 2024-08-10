import json
import pathlib
from datetime import datetime, timedelta, timezone

import pytest
from pydantic import ValidationError

from checkbox_sdk.client.synchronous import CheckBoxClient
from checkbox_sdk.storage.simple import SessionStorage
from .base import open_shift, close_shift
from ..models.reports_models import FiscalReportSchema


def test_get_periodical_report(license_key):
    assert license_key, "License key is empty"

    storage = SessionStorage()
    with CheckBoxClient() as client:
        client.set_license_key(storage, license_key)

        to_date = datetime.now(timezone.utc)
        from_date = to_date - timedelta(days=30)

        report = client.reports.get_periodical_report(from_date=from_date, to_date=to_date, storage=storage)
        assert report, "Report is empty"


def test_get_reports(auth_token, license_key):
    assert license_key, "License key is empty"

    with CheckBoxClient() as client:
        client.cashier.authenticate_token(auth_token, license_key=license_key)

        open_shift(client)

        to_date = datetime.now(timezone.utc)
        from_date = to_date - timedelta(days=30)

        get_report_tested = False

        # sourcery skip: no-loop-in-tests
        for report in client.reports.get_reports(from_date=from_date, to_date=to_date):
            try:
                model = FiscalReportSchema(**report)
                assert model is not None
            except ValidationError as e:  # pragma: no cover
                pytest.fail(f"Fiscal report validation schema failed: {e}")

            # One time will be enough
            # sourcery skip: no-conditionals-in-tests
            if not get_report_tested:
                report_by_id = client.reports.get_report(report["id"])
                try:
                    model = FiscalReportSchema(**report_by_id)
                    assert model is not None
                except ValidationError as e:  # pragma: no cover
                    pytest.fail(f"Fiscal report validation schema failed: {e}")

                report_text = client.reports.get_report_text(report["id"])
                assert report_text, "Report is empty"

                report_text = client.reports.get_report_png(report["id"])
                assert report_text, "Report is empty"

                get_report_tested = True

        close_shift(client)


def test_create_x_report(auth_token, license_key):
    assert license_key, "License key is empty"

    with CheckBoxClient() as client:
        client.cashier.authenticate_token(auth_token, license_key=license_key)

        open_shift(client)

        report = client.reports.create_x_report()
        try:
            model = FiscalReportSchema(**report)
            assert model is not None
        except ValidationError as e:  # pragma: no cover
            pytest.fail(f"Fiscal report validation schema failed: {e}")

        close_shift(client)


def test_get_search_reports(auth_token, license_key):
    assert license_key, "License key is empty"

    with CheckBoxClient() as client:
        client.cashier.authenticate_token(auth_token, license_key=license_key)

        # sourcery skip: no-loop-in-tests
        for report in client.reports.get_search_reports():
            try:
                model = FiscalReportSchema(**report)
                assert model is not None
            except ValidationError as e:  # pragma: no cover
                pytest.fail(f"Fiscal report validation schema failed: {e}")


def test_add_external_report(auth_token, license_key):
    assert license_key, "License key is empty"

    with CheckBoxClient() as client:
        client.cashier.authenticate_token(auth_token, license_key=license_key)

        open_shift(client)

        base_path = pathlib.Path(__file__).resolve().parent.parent
        report_path = base_path / "test_data/external_report.json"
        report_data = json.loads(report_path.resolve().read_text())

        report = client.reports.add_external_report(report=report_data)
        try:
            model = FiscalReportSchema(**report)
            assert model is not None
        except ValidationError as e:  # pragma: no cover
            pytest.fail(f"Fiscal report validation schema failed: {e}")

        close_shift(client)
