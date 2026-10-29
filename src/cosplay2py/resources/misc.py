"""The smaller resources: design, pages, media, e-tickets and voting tickets."""

from collections.abc import Mapping
from typing import Any

from cosplay2py._base_client import Endpoint
from cosplay2py.models import (
    EventDesign,
    MediaData,
    Page,
    PageDetails,
    PageType,
    PayMethods,
    TicketStatistic,
    VotingStatistics,
)
from cosplay2py.resources._base import AsyncResource, SyncResource

_DESIGN_GET = Endpoint[EventDesign](
    "GET", "/api/event_design/get", EventDesign, key="design", idempotent=True
)
_DESIGN_GET_IMAGES = Endpoint[dict[int, str]](
    "GET",
    "/api/event_design/get_eventimages",
    dict[int, str],
    key="eventimages",
    idempotent=True,
)
_PAGES_GET_LIST = Endpoint[list[Page]](
    "GET", "/api/pages/get_list", list[Page], idempotent=True
)


def _get_page(page_id: int) -> Endpoint[PageDetails]:
    return Endpoint(
        "POST",
        "/api/pages/get_page",
        PageDetails,
        json={"page_id": str(page_id)},
        idempotent=True,
    )


def _add_page(type: PageType, parent_id: int | None) -> Endpoint[int]:
    return Endpoint(
        "POST",
        "/api/pages/add_page",
        int,
        key="page_id",
        json={"parent_id": parent_id, "type": type},
        idempotent=False,
    )


def _save_page_field(page_id: int, field: str, value: Any) -> Endpoint[Any]:
    return Endpoint(
        "POST",
        "/api/pages/save_page_field",
        Any,
        json={"id": page_id, "field": field, "data": value},
        idempotent=False,
    )


def _save_page_fields(page_id: int, fields: Mapping[str, Any]) -> Endpoint[Any]:
    return Endpoint(
        "POST",
        "/api/pages/save_page_fields",
        Any,
        json={"id": page_id, "page_data": dict(fields)},
        idempotent=False,
    )


def _delete_page(page_id: int) -> Endpoint[Any]:
    return Endpoint(
        "POST",
        "/api/pages/delete_page",
        Any,
        json={"id": page_id},
        idempotent=False,
    )


_MEDIA_GET_DATA = Endpoint[MediaData](
    "GET", "/api/media/get_data", MediaData, idempotent=True
)
_ETICKETS_GET_LIST = Endpoint[list[dict[str, Any]]](
    "GET",
    "/api/etickets/get_list",
    list[dict[str, Any]],
    key="etickets",
    idempotent=True,
)
_ETICKETS_GET_TYPES = Endpoint[list[dict[str, Any]]](
    "GET",
    "/api/etickets/get_types",
    list[dict[str, Any]],
    key="etickets_types",
    idempotent=True,
)
_ETICKETS_GET_PAYMETHODS = Endpoint[PayMethods](
    "GET",
    "/api/etickets/get_paymethods",
    PayMethods,
    key="etickets_paymethods",
    idempotent=True,
)
_ETICKETS_GET_VAT = Endpoint[dict[str, int | None]](
    "GET",
    "/api/etickets/dictionary-yookassa-vat",
    dict[str, int | None],
    idempotent=True,
)
_TICKETS_GET_STATISTIC = Endpoint[TicketStatistic](
    "GET", "/api/tickets/get_statistic", TicketStatistic, idempotent=True
)
_TICKETS_GET_VOTING_STATISTICS = Endpoint[VotingStatistics](
    "GET", "/api/tickets/get_voting_statistics", VotingStatistics, idempotent=True
)


def _save_design(fields: Mapping[str, Any]) -> Endpoint[Any]:
    return Endpoint(
        "POST",
        "/api/event_design/save_design",
        Any,
        json=dict(fields),
        idempotent=False,
    )


def _upload_design_image(image: bytes, filename: str) -> Endpoint[dict[int, str]]:
    return Endpoint(
        "POST",
        "/api/event_design/upload_image",
        dict[int, str],
        key="eventimages",
        files={"eventimage": (filename, image)},
        idempotent=False,
    )


def _delete_design_image(eventimage: str) -> Endpoint[dict[int, str]]:
    return Endpoint(
        "POST",
        "/api/event_design/delete_eventimage",
        dict[int, str],
        key="eventimages",
        json={"eventimage": eventimage},
        idempotent=False,
    )


def _reorder_page(
    page_id: int, new_index: int, source_page_id: int | None, target_page_id: int | None
) -> Endpoint[Any]:
    return Endpoint(
        "POST",
        "/api/pages/page_reorder",
        Any,
        json={
            "page_id": page_id,
            "source_page_id": source_page_id,
            "target_page_id": target_page_id,
            "new_index": new_index,
        },
        idempotent=False,
    )


class Design(SyncResource):
    def get(self) -> EventDesign:
        """Colors and custom CSS of the event site."""
        return self._request(_DESIGN_GET)

    def get_images(self) -> dict[int, str]:
        """Uploaded design images: image ID -> file name."""
        return self._request(_DESIGN_GET_IMAGES)

    def save(self, fields: Mapping[str, Any]) -> None:
        """Update the supplied design settings."""
        self._request(_save_design(fields))

    def upload_image(self, image: bytes, filename: str) -> dict[int, str]:
        """Upload a design image and return the updated image mapping."""
        return self._request(_upload_design_image(image, filename))

    def delete_image(self, eventimage: str) -> dict[int, str]:
        """Delete a design image by file name and return the image mapping."""
        return self._request(_delete_design_image(eventimage))


class AsyncDesign(AsyncResource):
    async def get(self) -> EventDesign:
        """Colors and custom CSS of the event site."""
        return await self._request(_DESIGN_GET)

    async def get_images(self) -> dict[int, str]:
        """Uploaded design images: image ID -> file name."""
        return await self._request(_DESIGN_GET_IMAGES)

    async def save(self, fields: Mapping[str, Any]) -> None:
        """Update the supplied design settings."""
        await self._request(_save_design(fields))

    async def upload_image(self, image: bytes, filename: str) -> dict[int, str]:
        """Upload a design image and return the updated image mapping."""
        return await self._request(_upload_design_image(image, filename))

    async def delete_image(self, eventimage: str) -> dict[int, str]:
        """Delete a design image by file name and return the image mapping."""
        return await self._request(_delete_design_image(eventimage))


class Pages(SyncResource):
    def get_list(self) -> list[Page]:
        """Text pages of the event site."""
        return self._request(_PAGES_GET_LIST)

    def get(self, page_id: int) -> PageDetails:
        """A page with its content."""
        return self._request(_get_page(page_id))

    def create(self, type: PageType, *, parent_id: int | None = None) -> int:
        """Add an empty page, folder or link and return its id.

        :param parent_id: the folder (``Page.id``) to put it in; ``None`` for the
            top level.
        """
        return self._request(_add_page(type, parent_id))

    def save_field(self, page_id: int, field: str, value: Any) -> None:
        """Set an attribute of a page.

        :param field: the ``PageDetails`` attribute to set, e.g. ``title``,
            ``menu_title``, ``path``, ``type`` or ``show_in_menu``.
        """
        self._request(_save_page_field(page_id, field, value))

    def save_fields(self, page_id: int, fields: Mapping[str, Any]) -> None:
        """Set several attributes of a page at once.

        The page editor saves the text this way, with the same HTML in both
        ``source`` and ``content``.
        """
        self._request(_save_page_fields(page_id, fields))

    def delete(self, page_id: int) -> None:
        """Remove a page, folder or link.

        :raises BadRequestError: for a folder that still holds pages.
        """
        self._request(_delete_page(page_id))

    def reorder(
        self,
        page_id: int,
        new_index: int,
        *,
        source_page_id: int | None = None,
        target_page_id: int | None = None,
    ) -> None:
        """Move a page to a new position.

        :param source_page_id: source folder id, or ``None`` for the top level.
        :param target_page_id: target folder id, or ``None`` for the top level.
        """
        self._request(_reorder_page(page_id, new_index, source_page_id, target_page_id))


class AsyncPages(AsyncResource):
    async def get_list(self) -> list[Page]:
        """Text pages of the event site."""
        return await self._request(_PAGES_GET_LIST)

    async def get(self, page_id: int) -> PageDetails:
        """A page with its content."""
        return await self._request(_get_page(page_id))

    async def create(self, type: PageType, *, parent_id: int | None = None) -> int:
        """Add an empty page, folder or link and return its id.

        :param parent_id: the folder (``Page.id``) to put it in; ``None`` for the
            top level.
        """
        return await self._request(_add_page(type, parent_id))

    async def save_field(self, page_id: int, field: str, value: Any) -> None:
        """Set an attribute of a page.

        :param field: the ``PageDetails`` attribute to set, e.g. ``title``,
            ``menu_title``, ``path``, ``type`` or ``show_in_menu``.
        """
        await self._request(_save_page_field(page_id, field, value))

    async def save_fields(self, page_id: int, fields: Mapping[str, Any]) -> None:
        """Set several attributes of a page at once.

        The page editor saves the text this way, with the same HTML in both
        ``source`` and ``content``.
        """
        await self._request(_save_page_fields(page_id, fields))

    async def delete(self, page_id: int) -> None:
        """Remove a page, folder or link.

        :raises BadRequestError: for a folder that still holds pages.
        """
        await self._request(_delete_page(page_id))

    async def reorder(
        self,
        page_id: int,
        new_index: int,
        *,
        source_page_id: int | None = None,
        target_page_id: int | None = None,
    ) -> None:
        """Move a page to a new position.

        :param source_page_id: source folder id, or ``None`` for the top level.
        :param target_page_id: target folder id, or ``None`` for the top level.
        """
        await self._request(
            _reorder_page(page_id, new_index, source_page_id, target_page_id)
        )


class Media(SyncResource):
    def get_data(self) -> MediaData:
        """Photo albums and photos."""
        return self._request(_MEDIA_GET_DATA)


class AsyncMedia(AsyncResource):
    async def get_data(self) -> MediaData:
        """Photo albums and photos."""
        return await self._request(_MEDIA_GET_DATA)


class ETickets(SyncResource):
    """Electronic ticket sales."""

    def get_list(self) -> list[dict[str, Any]]:
        return self._request(_ETICKETS_GET_LIST)

    def get_types(self) -> list[dict[str, Any]]:
        return self._request(_ETICKETS_GET_TYPES)

    def get_paymethods(self) -> PayMethods:
        return self._request(_ETICKETS_GET_PAYMETHODS)

    def get_vat_dictionary(self) -> dict[str, int | None]:
        """YooKassa VAT codes: human-readable name -> code."""
        return self._request(_ETICKETS_GET_VAT)


class AsyncETickets(AsyncResource):
    """Electronic ticket sales."""

    async def get_list(self) -> list[dict[str, Any]]:
        return await self._request(_ETICKETS_GET_LIST)

    async def get_types(self) -> list[dict[str, Any]]:
        return await self._request(_ETICKETS_GET_TYPES)

    async def get_paymethods(self) -> PayMethods:
        return await self._request(_ETICKETS_GET_PAYMETHODS)

    async def get_vat_dictionary(self) -> dict[str, int | None]:
        """YooKassa VAT codes: human-readable name -> code."""
        return await self._request(_ETICKETS_GET_VAT)


class Tickets(SyncResource):
    """Entry tickets used for audience voting."""

    def get_statistic(self) -> TicketStatistic:
        return self._request(_TICKETS_GET_STATISTIC)

    def get_voting_statistics(self) -> VotingStatistics:
        return self._request(_TICKETS_GET_VOTING_STATISTICS)


class AsyncTickets(AsyncResource):
    """Entry tickets used for audience voting."""

    async def get_statistic(self) -> TicketStatistic:
        return await self._request(_TICKETS_GET_STATISTIC)

    async def get_voting_statistics(self) -> VotingStatistics:
        return await self._request(_TICKETS_GET_VOTING_STATISTICS)
