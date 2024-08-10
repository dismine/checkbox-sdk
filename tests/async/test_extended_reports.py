from datetime import datetime, timezone, timedelta

import pytest
from pydantic import ValidationError

from checkbox_sdk.client.asynchronous import AsyncCheckBoxClient
from checkbox_sdk.storage.simple import SessionStorage
from ..models.extended_reports_models import PublicReportTaskSchema


@pytest.mark.asyncio
async def test_goods_report(auth_token, license_key, client_email):
    assert license_key, "License key is empty"

    async with AsyncCheckBoxClient() as client:
        await client.cashier.authenticate_token(auth_token, license_key=license_key)

        to_date = datetime.now(timezone.utc)
        from_date = to_date - timedelta(days=30)

        data = {"from_date": from_date.isoformat(), "to_date": to_date.isoformat()}

        # sourcery skip: no-conditionals-in-tests
        if client_email:
            data["emails"] = [client_email]

        report = await client.extended_reports.goods_report(data=data)
        try:
            model = PublicReportTaskSchema(**report)
            assert model is not None
        except ValidationError as e:  # pragma: no cover
            pytest.fail(f"Report validation schema failed: {e}")


@pytest.mark.asyncio
async def test_create_z_report(auth_token, license_key, client_email):
    assert license_key, "License key is empty"

    async with AsyncCheckBoxClient() as client:
        await client.cashier.authenticate_token(auth_token, license_key=license_key)

        to_date = datetime.now(timezone.utc)
        from_date = to_date - timedelta(days=30)

        data = {"from_date": from_date.isoformat(), "to_date": to_date.isoformat()}

        # sourcery skip: no-conditionals-in-tests
        if client_email:
            data["emails"] = [client_email]

        report = await client.extended_reports.create_z_report(data=data)
        try:
            model = PublicReportTaskSchema(**report)
            assert model is not None
        except ValidationError as e:  # pragma: no cover
            pytest.fail(f"Report validation schema failed: {e}")


@pytest.mark.asyncio
async def test_actual_revenue_report(auth_token, license_key, client_email):
    assert license_key, "License key is empty"

    async with AsyncCheckBoxClient() as client:
        await client.cashier.authenticate_token(auth_token, license_key=license_key)

        to_date = datetime.now(timezone.utc)
        from_date = to_date - timedelta(days=30)

        data = {"from_date": from_date.isoformat(), "to_date": to_date.isoformat()}

        # sourcery skip: no-conditionals-in-tests
        if client_email:
            data["emails"] = [client_email]

        report = await client.extended_reports.actual_revenue_report(data=data)
        try:
            model = PublicReportTaskSchema(**report)
            assert model is not None
        except ValidationError as e:  # pragma: no cover
            pytest.fail(f"Report validation schema failed: {e}")


@pytest.mark.asyncio
async def test_net_turnover_report(auth_token, license_key, client_email):
    assert license_key, "License key is empty"

    async with AsyncCheckBoxClient() as client:
        await client.cashier.authenticate_token(auth_token, license_key=license_key)

        to_date = datetime.now(timezone.utc)
        from_date = to_date - timedelta(days=30)

        data = {"from_date": from_date.isoformat(), "to_date": to_date.isoformat()}

        # sourcery skip: no-conditionals-in-tests
        if client_email:
            data["emails"] = [client_email]

        report = await client.extended_reports.net_turnover_report(data=data)
        try:
            model = PublicReportTaskSchema(**report)
            assert model is not None
        except ValidationError as e:  # pragma: no cover
            pytest.fail(f"Report validation schema failed: {e}")


@pytest.mark.asyncio
async def test_bookkeeper_z_report(auth_token, license_key, client_email):
    assert license_key, "License key is empty"

    async with AsyncCheckBoxClient() as client:
        await client.cashier.authenticate_token(auth_token, license_key=license_key)

        to_date = datetime.now(timezone.utc)
        from_date = to_date - timedelta(days=30)

        data = {"from_date": from_date.isoformat(), "to_date": to_date.isoformat()}

        # sourcery skip: no-conditionals-in-tests
        if client_email:
            data["emails"] = [client_email]

        report = await client.extended_reports.bookkeeper_z_report(data=data)
        try:
            model = PublicReportTaskSchema(**report)
            assert model is not None
        except ValidationError as e:  # pragma: no cover
            pytest.fail(f"Report validation schema failed: {e}")


@pytest.mark.asyncio
async def test_daily_cash_flow_report(auth_token, license_key, client_email):
    assert license_key, "License key is empty"

    storage = SessionStorage()
    async with AsyncCheckBoxClient(storage=storage) as client:
        await client.cashier.authenticate_token(auth_token, license_key=license_key)

        from_date = datetime.now(timezone.utc).date() - timedelta(days=30)

        data = {"from_date": from_date.isoformat(), "organization_id": [storage.cashier["organization"]["id"]]}

        # sourcery skip: no-conditionals-in-tests
        if client_email:
            data["emails"] = [client_email]

        report = await client.extended_reports.daily_cash_flow_report(data=data, storage=storage)
        try:
            model = PublicReportTaskSchema(**report)
            assert model is not None
        except ValidationError as e:  # pragma: no cover
            pytest.fail(f"Report validation schema failed: {e}")


@pytest.mark.asyncio
async def test_create_receipt_report(auth_token, license_key, client_email):
    assert license_key, "License key is empty"

    async with AsyncCheckBoxClient() as client:
        await client.cashier.authenticate_token(auth_token, license_key=license_key)

        to_date = datetime.now(timezone.utc)
        from_date = to_date - timedelta(days=30)

        data = {"from_date": from_date.isoformat(), "to_date": to_date.isoformat()}

        # sourcery skip: no-conditionals-in-tests
        if client_email:
            data["emails"] = [client_email]

        report = await client.extended_reports.create_receipt_report(data=data)
        try:
            model = PublicReportTaskSchema(**report)
            assert model is not None
        except ValidationError as e:  # pragma: no cover
            pytest.fail(f"Report validation schema failed: {e}")

        task = await client.extended_reports.get_report_task_by_id(report_task_id=report["id"])
        try:
            model = PublicReportTaskSchema(**task)
            assert model is not None
        except ValidationError as e:  # pragma: no cover
            pytest.fail(f"Report validation schema failed: {e}")

        task = await client.extended_reports.report_xlsx_task_by_id(report_task_id=report["id"])
        try:
            model = PublicReportTaskSchema(**task)
            assert model is not None
        except ValidationError as e:  # pragma: no cover
            pytest.fail(f"Report validation schema failed: {e}")

        task = await client.extended_reports.report_json_task_by_id(report_task_id=report["id"])
        try:
            model = PublicReportTaskSchema(**task)
            assert model is not None
        except ValidationError as e:  # pragma: no cover
            pytest.fail(f"Report validation schema failed: {e}")
