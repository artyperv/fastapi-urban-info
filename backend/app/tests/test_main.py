from httpx import AsyncClient
import pytest
from app.models import Organization, Building
from app.schemas.organization import OrganizationRead


# make all test mark with `asyncio`
pytestmark = pytest.mark.asyncio

# Проверяем, что без токена доступ запрещён (ожидаем 401 Unauthorized)
async def test_access_without_token(async_client: AsyncClient):
    print(async_client.base_url)
    response = await async_client.get("/organizations/")
    print(response.headers)
    assert response.status_code == 401


# Проверяем доступ с токеном: возвращается список организаций, содержащий тестовую организацию
async def test_access_with_token(
    async_client: AsyncClient, auth_headers: dict,
    async_organization_orm: Organization
):
    response = await async_client.get("/organizations/", headers=auth_headers)
    assert response.status_code == 200
    orgs = response.json()
    assert any(str(async_organization_orm.id) == o["id"] for o in orgs)


# Проверяем получение организаций по ID здания
async def test_get_organizations_by_building(
    async_client: AsyncClient, auth_headers: dict,
    async_organization_orm: Organization
):
    response = await async_client.get(f"/organizations/by-building/{async_organization_orm.building_id}", headers=auth_headers)
    assert response.status_code == 200
    orgs = response.json()
    assert any(str(async_organization_orm.id) == o["id"] for o in orgs)


# Проверяем поиск организаций в радиусе 1 км от здания тестовой организации
async def test_get_organizations_by_radius(
    async_client: AsyncClient, auth_headers: dict,
    async_organization_orm: Organization
):
    # Точка около "ул. Пушкина, д.1"
    latitude = async_organization_orm.building.latitude
    longitude = async_organization_orm.building.longitude
    radius_km = 1.0

    response = await async_client.get(
        f"/organizations/by-radius/?latitude={latitude}&longitude={longitude}&radius_km={radius_km}",
        headers=auth_headers
    )
    assert response.status_code == 200
    orgs = response.json()
    assert any(str(async_organization_orm.id) == o["id"] for o in orgs)


# Проверяем поиск организаций по части имени
async def test_search_organizations_by_name(
    async_client: AsyncClient, auth_headers: dict,
    async_organization_orm: Organization
):
    name = async_organization_orm.name
    partial_name = name[:len(name)//2]
    response = await async_client.get(f"/organizations/?name={partial_name}", headers=auth_headers)
    assert response.status_code == 200
    orgs = response.json()
    assert any(str(async_organization_orm.id) == o["id"] for o in orgs)
