"""The smaller resources: design, pages, media, cards, e-tickets and voting tickets."""

from collections.abc import Mapping
from typing import Any

from cosplay2py._base_client import Endpoint
from cosplay2py.models import (
    CardDetails,
    EventDesign,
    MediaData,
    Page,
    PageDetails,
    PageType,
    PublicRequestDetails,
    TicketCreateMode,
    TicketKind,
    TicketStatistic,
    TopicsAndCards,
    TopicsAndRequests,
    VotingStatistics,
    VotingType,
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
    type = PageType(type)
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


def _add_photoalbum(user_title: str, url: str) -> Endpoint[Any]:
    return Endpoint(
        "POST",
        "/api/media/photoalbum_add",
        Any,
        json={"user_title": user_title, "url": url},
        idempotent=False,
    )


def _save_photoalbum_field(album_id: int, field: str, value: Any) -> Endpoint[Any]:
    return Endpoint(
        "POST",
        "/api/media/save_photoalbum_field",
        Any,
        json={"photoalbum_id": album_id, "field": field, "data": value},
        idempotent=False,
    )


def _delete_photoalbum(album_id: int) -> Endpoint[Any]:
    return Endpoint(
        "POST",
        "/api/media/photoalbum_delete",
        Any,
        json={"photoalbum_id": album_id},
        idempotent=False,
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


def _get_eticket_types(i_can_buy: bool) -> Endpoint[list[dict[str, Any]]]:
    if i_can_buy:
        return Endpoint(
            "POST",
            "/api/etickets/get_types",
            list[dict[str, Any]],
            key="etickets_types",
            json={"i_can_buy": True},
            idempotent=True,
        )
    return _ETICKETS_GET_TYPES


def _etickets_write(path: str, body: dict[str, Any]) -> Endpoint[Any]:
    return Endpoint("POST", f"/api/etickets/{path}", Any, json=body, idempotent=False)


def _save_eticket_field(
    eticket_id: int, field: str, value: Any
) -> Endpoint[dict[str, Any]]:
    return Endpoint(
        "POST",
        "/api/etickets/save_eticket_field",
        dict[str, Any],
        key="eticket",
        json={"eticket_id": eticket_id, "field": field, "data": value},
        idempotent=False,
    )


def _create_eticket(type_id: int) -> Endpoint[int]:
    return Endpoint(
        "POST",
        "/api/etickets/create_ticket",
        int,
        key="eticket_id",
        json={"etickets_type_id": type_id},
        idempotent=False,
    )


def _get_eticket(eticket_id: int) -> Endpoint[dict[str, Any]]:
    return Endpoint(
        "POST",
        "/api/etickets/get_ticket",
        dict[str, Any],
        json={"eticket_id": str(eticket_id)},
        idempotent=True,
    )


def _get_eticket_status(eticket_id: int) -> Endpoint[dict[str, Any]]:
    return Endpoint(
        "POST",
        "/api/etickets/get_ticket_status",
        dict[str, Any],
        key="eticket_status",
        json={"eticket_id": str(eticket_id)},
        idempotent=True,
    )


_TICKETS_GET_STATISTIC = Endpoint[TicketStatistic](
    "GET", "/api/tickets/get_statistic", TicketStatistic, idempotent=True
)
_TICKETS_GET_VOTING_STATISTICS = Endpoint[VotingStatistics](
    "GET", "/api/tickets/get_voting_statistics", VotingStatistics, idempotent=True
)
_TICKETS_CLEAR_VOTES = Endpoint[Any](
    "POST", "/api/tickets/clear_votes", Any, idempotent=False
)
_TICKETS_GET_TICKET = Endpoint[dict[str, Any]](
    "GET", "/api/tickets/get_ticket", dict[str, Any], idempotent=True
)
_TICKETS_GET_CARDS = Endpoint[list[dict[str, Any]]](
    "GET",
    "/api/tickets/get_cards",
    list[dict[str, Any]],
    key="requests",
    idempotent=True,
)


def _create_tickets(
    count: int, ticket_type: TicketKind, mode: TicketCreateMode
) -> Endpoint[Any]:
    if isinstance(ticket_type, bool):
        raise TypeError(f"{ticket_type!r} is not a valid TicketKind")
    ticket_type = TicketKind(ticket_type)
    mode = TicketCreateMode(mode)
    return Endpoint(
        "POST",
        "/api/tickets/create",
        Any,
        json={
            "tickets_count": count,
            "tickets_type": int(ticket_type),
            "create_type": mode,
        },
        idempotent=False,
    )


def _tickets_prize(action: str, body: dict[str, Any]) -> Endpoint[dict[str, Any]]:
    return Endpoint(
        "POST",
        f"/api/tickets/prize_{action}",
        dict[str, Any],
        json=body,
        idempotent=False,
    )


def _tickets_write(path: str, body: dict[str, Any]) -> Endpoint[Any]:
    return Endpoint("POST", f"/api/tickets/{path}", Any, json=body, idempotent=False)


def _check_for_voting(ticket_number: str) -> Endpoint[Any]:
    return Endpoint(
        "POST",
        "/api/tickets/check_for_voting",
        Any,
        json={"ticket_number": ticket_number},
        idempotent=True,
    )


def _get_voting_data(
    ticket_number: str, voting_type: VotingType
) -> Endpoint[dict[str, Any]]:
    voting_type = VotingType(voting_type)
    return Endpoint(
        "POST",
        "/api/tickets/get_voting_data",
        dict[str, Any],
        json={"ticket_number": ticket_number, "voting_type": voting_type},
        idempotent=True,
    )


def _select_winner(
    ticket_number: str,
    topic_id: int,
    winner_index: int,
    request_id: int,
    voting_type: VotingType,
) -> Endpoint[dict[str, Any]]:
    voting_type = VotingType(voting_type)
    return Endpoint(
        "POST",
        "/api/tickets/select_winner",
        dict[str, Any],
        json={
            "ticket_number": ticket_number,
            "topic_id": topic_id,
            "winner_index": winner_index,
            "request_id": request_id,
            "voting_type": voting_type,
        },
        idempotent=False,
    )


_CARDS_GET_TOPICS_AND_REQUESTS = Endpoint[TopicsAndRequests](
    "GET", "/api/cards/get_topics_and_requests", TopicsAndRequests, idempotent=True
)


def _get_topics_and_cards(preview: bool) -> Endpoint[TopicsAndCards]:
    return Endpoint(
        "GET",
        "/api/cards/get_topics_and_cards",
        TopicsAndCards,
        params={"preview": "1"} if preview else None,
        idempotent=True,
    )


def _get_card(request_id: int, preview: bool) -> Endpoint[CardDetails]:
    params: dict[str, str] = {"request_id": str(request_id)}
    if preview:
        params["preview"] = "1"
    return Endpoint(
        "GET",
        "/api/cards/get_card",
        CardDetails,
        params=params,
        idempotent=True,
    )


def _get_card_request(request_id: int) -> Endpoint[PublicRequestDetails]:
    return Endpoint(
        "GET",
        "/api/cards/get_request",
        PublicRequestDetails,
        params={"request_id": str(request_id)},
        idempotent=True,
    )


_DESIGN_DELETE_PANEL_LOGO = Endpoint[Any](
    "GET", "/api/event_design/delete_panel_logo", Any, idempotent=False
)
_DESIGN_DELETE_HEADER_LOGO = Endpoint[Any](
    "GET", "/api/event_design/delete_header_logo", Any, idempotent=False
)
_DESIGN_DELETE_SITE_BACKGROUND = Endpoint[Any](
    "GET", "/api/event_design/delete_site_background", Any, idempotent=False
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

    def delete_panel_logo(self) -> None:
        """Delete the top navigation bar logo."""
        self._request(_DESIGN_DELETE_PANEL_LOGO)

    def delete_header_logo(self) -> None:
        """Delete the site header logo."""
        self._request(_DESIGN_DELETE_HEADER_LOGO)

    def delete_site_background(self) -> None:
        """Delete the site background image."""
        self._request(_DESIGN_DELETE_SITE_BACKGROUND)


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

    async def delete_panel_logo(self) -> None:
        """Delete the top navigation bar logo."""
        await self._request(_DESIGN_DELETE_PANEL_LOGO)

    async def delete_header_logo(self) -> None:
        """Delete the site header logo."""
        await self._request(_DESIGN_DELETE_HEADER_LOGO)

    async def delete_site_background(self) -> None:
        """Delete the site background image."""
        await self._request(_DESIGN_DELETE_SITE_BACKGROUND)


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

    def add_album(self, user_title: str, url: str) -> None:
        """Link a photo album to the event.

        :param user_title: photographer's name.
        :param url: album URL (e.g. a VK album link).
        """
        self._request(_add_photoalbum(user_title, url))

    def save_album_field(self, album_id: int, field: str, value: Any) -> None:
        """Set an attribute of a linked photo album (``user_title`` or ``url``)."""
        self._request(_save_photoalbum_field(album_id, field, value))

    def delete_album(self, album_id: int) -> None:
        """Remove a linked photo album from the event."""
        self._request(_delete_photoalbum(album_id))


class AsyncMedia(AsyncResource):
    async def get_data(self) -> MediaData:
        """Photo albums and photos."""
        return await self._request(_MEDIA_GET_DATA)

    async def add_album(self, user_title: str, url: str) -> None:
        """Link a photo album to the event.

        :param user_title: photographer's name.
        :param url: album URL (e.g. a VK album link).
        """
        await self._request(_add_photoalbum(user_title, url))

    async def save_album_field(self, album_id: int, field: str, value: Any) -> None:
        """Set an attribute of a linked photo album (``user_title`` or ``url``)."""
        await self._request(_save_photoalbum_field(album_id, field, value))

    async def delete_album(self, album_id: int) -> None:
        """Remove a linked photo album from the event."""
        await self._request(_delete_photoalbum(album_id))


class ETickets(SyncResource):
    """Electronic ticket sales."""

    def get_list(self) -> list[dict[str, Any]]:
        """All electronic tickets of the event."""
        return self._request(_ETICKETS_GET_LIST)

    def get_types(self, *, i_can_buy: bool = False) -> list[dict[str, Any]]:
        """Electronic ticket tiers of the event.

        :param i_can_buy: Only return ticket tiers currently available to buy.
        """
        return self._request(_get_eticket_types(i_can_buy))

    def add_type(self) -> None:
        """Create a new electronic ticket tier."""
        self._request(_etickets_write("eticketstypes_add", {}))

    def delete_type(self, type_id: int) -> None:
        """Delete an electronic ticket tier."""
        self._request(
            _etickets_write("eticketstypes_delete", {"etickets_type_id": type_id})
        )

    def reorder_type(self, type_id: int, new_index: int) -> None:
        """Move an electronic ticket tier to a new position."""
        self._request(
            _etickets_write(
                "eticketstypes_reorder",
                {"etickets_type_id": type_id, "new_index": new_index},
            )
        )

    def save_type_field(self, type_id: int, field: str, value: Any) -> None:
        """Set an attribute of an electronic ticket tier."""
        self._request(
            _etickets_write(
                "save_eticketstypes_field",
                {"etickets_type_id": type_id, "field": field, "data": value},
            )
        )

    def save_field(self, eticket_id: int, field: str, value: Any) -> dict[str, Any]:
        """Set an organizer attribute of an electronic ticket and return it."""
        return self._request(_save_eticket_field(eticket_id, field, value))

    def delete(self, eticket_id: int) -> None:
        """Delete an electronic ticket."""
        self._request(_etickets_write("delete", {"eticket_id": eticket_id}))

    def create(self, type_id: int) -> int:
        """Create an electronic ticket of ``type_id`` and return its id."""
        return self._request(_create_eticket(type_id))

    def get(self, eticket_id: int) -> dict[str, Any]:
        """An electronic ticket with its tier and payment details."""
        return self._request(_get_eticket(eticket_id))

    def get_status(self, eticket_id: int) -> dict[str, Any]:
        """Payment status of an electronic ticket."""
        return self._request(_get_eticket_status(eticket_id))

    def save_personal_data(self, eticket_id: int, user_data: Mapping[str, Any]) -> None:
        """Save buyer personal data on an electronic ticket."""
        self._request(
            _etickets_write(
                "save_personal_data",
                {"eticket_id": str(eticket_id), "user_data": dict(user_data)},
            )
        )


class AsyncETickets(AsyncResource):
    """Electronic ticket sales."""

    async def get_list(self) -> list[dict[str, Any]]:
        """All electronic tickets of the event."""
        return await self._request(_ETICKETS_GET_LIST)

    async def get_types(self, *, i_can_buy: bool = False) -> list[dict[str, Any]]:
        """Electronic ticket tiers of the event.

        :param i_can_buy: Only return ticket tiers currently available to buy.
        """
        return await self._request(_get_eticket_types(i_can_buy))

    async def add_type(self) -> None:
        """Create a new electronic ticket tier."""
        await self._request(_etickets_write("eticketstypes_add", {}))

    async def delete_type(self, type_id: int) -> None:
        """Delete an electronic ticket tier."""
        await self._request(
            _etickets_write("eticketstypes_delete", {"etickets_type_id": type_id})
        )

    async def reorder_type(self, type_id: int, new_index: int) -> None:
        """Move an electronic ticket tier to a new position."""
        await self._request(
            _etickets_write(
                "eticketstypes_reorder",
                {"etickets_type_id": type_id, "new_index": new_index},
            )
        )

    async def save_type_field(self, type_id: int, field: str, value: Any) -> None:
        """Set an attribute of an electronic ticket tier."""
        await self._request(
            _etickets_write(
                "save_eticketstypes_field",
                {"etickets_type_id": type_id, "field": field, "data": value},
            )
        )

    async def save_field(
        self, eticket_id: int, field: str, value: Any
    ) -> dict[str, Any]:
        """Set an organizer attribute of an electronic ticket and return it."""
        return await self._request(_save_eticket_field(eticket_id, field, value))

    async def delete(self, eticket_id: int) -> None:
        """Delete an electronic ticket."""
        await self._request(_etickets_write("delete", {"eticket_id": eticket_id}))

    async def create(self, type_id: int) -> int:
        """Create an electronic ticket of ``type_id`` and return its id."""
        return await self._request(_create_eticket(type_id))

    async def get(self, eticket_id: int) -> dict[str, Any]:
        """An electronic ticket with its tier and payment details."""
        return await self._request(_get_eticket(eticket_id))

    async def get_status(self, eticket_id: int) -> dict[str, Any]:
        """Payment status of an electronic ticket."""
        return await self._request(_get_eticket_status(eticket_id))

    async def save_personal_data(
        self, eticket_id: int, user_data: Mapping[str, Any]
    ) -> None:
        """Save buyer personal data on an electronic ticket."""
        await self._request(
            _etickets_write(
                "save_personal_data",
                {"eticket_id": str(eticket_id), "user_data": dict(user_data)},
            )
        )


class Tickets(SyncResource):
    """Entry tickets used for audience voting."""

    def get_statistic(self) -> TicketStatistic:
        """Active ticket count and test voting tickets."""
        return self._request(_TICKETS_GET_STATISTIC)

    def get_voting_statistics(self) -> VotingStatistics:
        """Live audience voting statistics and prize winners."""
        return self._request(_TICKETS_GET_VOTING_STATISTICS)

    def create(
        self,
        count: int,
        *,
        ticket_type: TicketKind = TicketKind.WORK,
        mode: TicketCreateMode = TicketCreateMode.ADD,
    ) -> None:
        """Generate audience voting tickets.

        :param count: number of tickets to generate.
        :param ticket_type: test tickets or live working tickets.
        :param mode: add to existing tickets or replace them.
        """
        self._request(_create_tickets(count, ticket_type, mode))

    def clear_votes(self) -> None:
        """Clear all test votes."""
        self._request(_TICKETS_CLEAR_VOTES)

    def add_prize(self, title: str, quantity: int) -> dict[str, Any]:
        """Add a voter raffle prize and return the updated prizes payload."""
        return self._request(
            _tickets_prize("add", {"title": title, "quantity": quantity})
        )

    def delete_prize(self, prize_id: int) -> dict[str, Any]:
        """Delete a voter raffle prize and return the updated prizes payload."""
        return self._request(_tickets_prize("del", {"prize_id": prize_id}))

    def save_prize_field(self, prize_id: int, field: str, value: Any) -> None:
        """Set an attribute of a voter raffle prize (``title`` or ``quantity``)."""
        self._request(
            _tickets_write(
                "save_prize_field",
                {"prize_id": prize_id, "field": field, "data": value},
            )
        )

    def save_prize_handed(self, prize_winner_id: int, handed: bool) -> None:
        """Mark whether a raffle prize has been handed to its winner."""
        self._request(
            _tickets_write(
                "save_prize_handed",
                {"prize_winner_id": prize_winner_id, "data": int(handed)},
            )
        )

    def get_ticket(self) -> dict[str, Any]:
        """The voting ticket bound to the current user, if any."""
        return self._request(_TICKETS_GET_TICKET)

    def check_for_voting(self, ticket_number: str) -> None:
        """Verify that ``ticket_number`` can be used to vote."""
        self._request(_check_for_voting(ticket_number))

    def get_voting_data(
        self,
        ticket_number: str,
        *,
        voting_type: VotingType = VotingType.NORMAL,
    ) -> dict[str, Any]:
        """Topics, requests and current selections for ``ticket_number``."""
        return self._request(_get_voting_data(ticket_number, voting_type))

    def get_cards(self) -> list[dict[str, Any]]:
        """Participant cards shown on the voting page."""
        return self._request(_TICKETS_GET_CARDS)

    def select_winner(
        self,
        ticket_number: str,
        topic_id: int,
        winner_index: int,
        request_id: int,
        *,
        voting_type: VotingType = VotingType.NORMAL,
    ) -> dict[str, Any]:
        """Cast or change a vote for ``request_id`` in ``topic_id``."""
        return self._request(
            _select_winner(
                ticket_number, topic_id, winner_index, request_id, voting_type
            )
        )


class AsyncTickets(AsyncResource):
    """Entry tickets used for audience voting."""

    async def get_statistic(self) -> TicketStatistic:
        """Active ticket count and test voting tickets."""
        return await self._request(_TICKETS_GET_STATISTIC)

    async def get_voting_statistics(self) -> VotingStatistics:
        """Live audience voting statistics and prize winners."""
        return await self._request(_TICKETS_GET_VOTING_STATISTICS)

    async def create(
        self,
        count: int,
        *,
        ticket_type: TicketKind = TicketKind.WORK,
        mode: TicketCreateMode = TicketCreateMode.ADD,
    ) -> None:
        """Generate audience voting tickets.

        :param count: number of tickets to generate.
        :param ticket_type: test tickets or live working tickets.
        :param mode: add to existing tickets or replace them.
        """
        await self._request(_create_tickets(count, ticket_type, mode))

    async def clear_votes(self) -> None:
        """Clear all test votes."""
        await self._request(_TICKETS_CLEAR_VOTES)

    async def add_prize(self, title: str, quantity: int) -> dict[str, Any]:
        """Add a voter raffle prize and return the updated prizes payload."""
        return await self._request(
            _tickets_prize("add", {"title": title, "quantity": quantity})
        )

    async def delete_prize(self, prize_id: int) -> dict[str, Any]:
        """Delete a voter raffle prize and return the updated prizes payload."""
        return await self._request(_tickets_prize("del", {"prize_id": prize_id}))

    async def save_prize_field(self, prize_id: int, field: str, value: Any) -> None:
        """Set an attribute of a voter raffle prize (``title`` or ``quantity``)."""
        await self._request(
            _tickets_write(
                "save_prize_field",
                {"prize_id": prize_id, "field": field, "data": value},
            )
        )

    async def save_prize_handed(self, prize_winner_id: int, handed: bool) -> None:
        """Mark whether a raffle prize has been handed to its winner."""
        await self._request(
            _tickets_write(
                "save_prize_handed",
                {"prize_winner_id": prize_winner_id, "data": int(handed)},
            )
        )

    async def get_ticket(self) -> dict[str, Any]:
        """The voting ticket bound to the current user, if any."""
        return await self._request(_TICKETS_GET_TICKET)

    async def check_for_voting(self, ticket_number: str) -> None:
        """Verify that ``ticket_number`` can be used to vote."""
        await self._request(_check_for_voting(ticket_number))

    async def get_voting_data(
        self,
        ticket_number: str,
        *,
        voting_type: VotingType = VotingType.NORMAL,
    ) -> dict[str, Any]:
        """Topics, requests and current selections for ``ticket_number``."""
        return await self._request(_get_voting_data(ticket_number, voting_type))

    async def get_cards(self) -> list[dict[str, Any]]:
        """Participant cards shown on the voting page."""
        return await self._request(_TICKETS_GET_CARDS)

    async def select_winner(
        self,
        ticket_number: str,
        topic_id: int,
        winner_index: int,
        request_id: int,
        *,
        voting_type: VotingType = VotingType.NORMAL,
    ) -> dict[str, Any]:
        """Cast or change a vote for ``request_id`` in ``topic_id``."""
        return await self._request(
            _select_winner(
                ticket_number, topic_id, winner_index, request_id, voting_type
            )
        )


class Cards(SyncResource):
    """Public participant cards and submitted request listings."""

    def get_topics_and_cards(self, *, preview: bool = False) -> TopicsAndCards:
        """Topics and participant cards shown on the event site.

        :param preview: Include cards in organizer preview mode.
        """
        return self._request(_get_topics_and_cards(preview))

    def get_card(self, request_id: int, *, preview: bool = False) -> CardDetails:
        """A single participant card.

        :param preview: Fetch in organizer preview mode.
        """
        return self._request(_get_card(request_id, preview))

    def get_topics_and_requests(self) -> TopicsAndRequests:
        """Topics and submitted requests shown on the public request list."""
        return self._request(_CARDS_GET_TOPICS_AND_REQUESTS)

    def get_request(self, request_id: int) -> PublicRequestDetails:
        """A single request from the public request list."""
        return self._request(_get_card_request(request_id))


class AsyncCards(AsyncResource):
    """Public participant cards and submitted request listings."""

    async def get_topics_and_cards(self, *, preview: bool = False) -> TopicsAndCards:
        """Topics and participant cards shown on the event site.

        :param preview: Include cards in organizer preview mode.
        """
        return await self._request(_get_topics_and_cards(preview))

    async def get_card(self, request_id: int, *, preview: bool = False) -> CardDetails:
        """A single participant card.

        :param preview: Fetch in organizer preview mode.
        """
        return await self._request(_get_card(request_id, preview))

    async def get_topics_and_requests(self) -> TopicsAndRequests:
        """Topics and submitted requests shown on the public request list."""
        return await self._request(_CARDS_GET_TOPICS_AND_REQUESTS)

    async def get_request(self, request_id: int) -> PublicRequestDetails:
        """A single request from the public request list."""
        return await self._request(_get_card_request(request_id))
