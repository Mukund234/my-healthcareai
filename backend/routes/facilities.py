from typing import List, Optional

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field
import math

router = APIRouter(prefix="/api/facilities", tags=["facilities"])


class Facility(BaseModel):
    name: str
    type: str
    latitude: float
    longitude: float
    address: str
    city: Optional[str] = None
    emergency_available: bool = False
    phone: Optional[str] = None
    distance_km: Optional[float] = None


# Minimal seeded facilities (can later come from Mongo/SQL or external APIs)
_FACILITIES: List[Facility] = [
    Facility(
        name="AIIMS New Delhi",
        type="tertiary_hospital",
        latitude=28.5665,
        longitude=77.2100,
        address="Sri Aurobindo Marg, Ansari Nagar",
        city="Delhi",
        emergency_available=True,
        phone="011-26588500",
    ),
    Facility(
        name="KEM Hospital",
        type="tertiary_hospital",
        latitude=18.9787,
        longitude=72.8330,
        address="Parel",
        city="Mumbai",
        emergency_available=True,
        phone="022-24136051",
    ),
    Facility(
        name="NIMHANS",
        type="specialty_hospital",
        latitude=12.9430,
        longitude=77.5950,
        address="Hosur Road",
        city="Bengaluru",
        emergency_available=True,
        phone="080-26995000",
    ),
]


def _haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Great-circle distance between two points (km)."""
    r = 6371.0
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(math.radians(lat1))
        * math.cos(math.radians(lat2))
        * math.sin(dlon / 2) ** 2
    )
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return r * c


@router.get("/nearby", response_model=List[Facility])
async def get_nearby_facilities(
    lat: float = Query(..., ge=-90, le=90),
    lng: float = Query(..., ge=-180, le=180),
    emergency_only: bool = Query(False),
    city: Optional[str] = Query(None),
):
    """
    Return a small list of nearest facilities.

    For MVP this uses a hard-coded facility list and distance calculation.
    In production you would:
    - Use Mongo/SQL with geo indexes; or
    - Integrate a provider like Google Places, Mapbox, or NDHM registries.
    """
    if not _FACILITIES:
        raise HTTPException(status_code=404, detail="No facilities configured")

    candidates: List[Facility] = []
    for fac in _FACILITIES:
        if emergency_only and not fac.emergency_available:
            continue
        if city and fac.city and fac.city.lower() != city.lower():
            continue
        distance = _haversine_km(lat, lng, fac.latitude, fac.longitude)
        fac_with_distance = fac.copy(update={"distance_km": round(distance, 2)})
        candidates.append(fac_with_distance)

    candidates.sort(key=lambda f: f.distance_km or 0.0)
    return candidates[:5]

