from typing import Any

from cosplay2py._base_client import Endpoint
from cosplay2py.models import (
    Friend,
    UserDetails,
    UserEvents,
    UserFeed,
    UserSearchResult,
)
from cosplay2py.resources._base import AsyncResource, SyncResource

_GET_FRIENDS = Endpoint[list[Friend]](
    "GET", "/api/users/get_friends", list[Friend], key="users", idempotent=True
)


def _get(user_id: int) -> Endpoint[UserDetails]:
    return Endpoint(
        "POST",
        "/api/users/get",
        UserDetails,
        params={"user_id": str(user_id)},
        idempotent=True,
    )


def _search(query: str) -> Endpoint[list[UserSearchResult]]:
    return Endpoint(
        "POST",
        "/api/users/search",
        list[UserSearchResult],
        key="users",
        json={"query": query},
        idempotent=True,
    )


def _save_field(user_id: int, field: str, value: str) -> Endpoint[Any]:
    return Endpoint(
        "POST",
        "/api/users/save",
        Any,
        json={"userId": user_id, "field": field, "data": value},
        idempotent=False,
    )


def _friend_action(action: str, user_id: int) -> Endpoint[Any]:
    return Endpoint(
        "POST",
        f"/api/users/{action}",
        Any,
        json={"friend_id": user_id},
        idempotent=False,
    )


def _accept_friend_invite(user_id: int) -> Endpoint[UserDetails]:
    return Endpoint(
        "POST",
        "/api/users/friend_invite_accept",
        UserDetails,
        json={"friend_id": user_id},
        idempotent=False,
    )


def _get_events(user_id: int, filter: str | None) -> Endpoint[UserEvents]:
    body: dict[str, Any] = {"userId": user_id}
    if filter is not None:
        body["filter"] = filter
    return Endpoint(
        "POST",
        "/api/users/get_events",
        UserEvents,
        json=body,
        idempotent=True,
    )


def _get_feeds(user_id: int, limit: int, only_new: bool) -> Endpoint[list[UserFeed]]:
    return Endpoint(
        "POST",
        "/api/users/get_feeds",
        list[UserFeed],
        key="feeds",
        json={"user_id": user_id, "limit": limit, "onlynew": int(only_new)},
        idempotent=False,
    )


def _mark_feeds_read(user_id: int) -> Endpoint[Any]:
    return Endpoint(
        "POST",
        "/api/users/mark_feeds_readed",
        Any,
        json={"user_id": user_id},
        idempotent=False,
    )


class Users(SyncResource):
    def get(self, user_id: int) -> UserDetails:
        """A user's profile and friends."""
        return self._request(_get(user_id))

    def save_field(self, user_id: int, field: str, value: str) -> None:
        """Change a field of a user's profile.

        :param field: the ``UserProfile`` attribute to set: ``first_name``,
            ``second_name``, ``third_name``, ``sex``, ``birthday``, ``city``,
            ``email``, ``mobile`` or ``vk``.
        :param value: the new value as the site shows it, e.g. ``"female"`` for
            ``sex`` or ``"DD.MM.YYYY"`` for ``birthday``.
        """
        self._request(_save_field(user_id, field, value))

    def add_friend(self, user_id: int) -> None:
        """Send a friend invitation to a user."""
        self._request(_friend_action("friend_add", user_id))

    def accept_friend_invite(self, user_id: int) -> UserDetails:
        """Accept a friend invitation from a user, returning their unlocked profile."""
        return self._request(_accept_friend_invite(user_id))

    def decline_friend_invite(self, user_id: int) -> None:
        """Decline a friend invitation from a user."""
        self._request(_friend_action("friend_invite_decline", user_id))

    def cancel_friend_invite(self, user_id: int) -> None:
        """Withdraw a friend invitation you sent to a user."""
        self._request(_friend_action("friend_invite_cancel", user_id))

    def remove_friend(self, user_id: int) -> None:
        """Remove a user from your friends."""
        self._request(_friend_action("friend_remove", user_id))

    def get_events(self, user_id: int, *, filter: str | None = "actual") -> UserEvents:
        """Events the user takes part in, with their role in each.

        :param filter: ``"actual"`` (current and upcoming) or ``None`` for all
            events as on the profile page.
        """
        return self._request(_get_events(user_id, filter))

    def get_feeds(
        self, user_id: int, *, limit: int = 30, only_new: bool = True
    ) -> list[UserFeed]:
        """The user's notification feed."""
        return self._request(_get_feeds(user_id, limit, only_new))

    def mark_feeds_read(self, user_id: int) -> None:
        """Mark a user's notifications as read."""
        self._request(_mark_feeds_read(user_id))

    def get_friends(self) -> list[Friend]:
        """Friends of the token's owner."""
        return self._request(_GET_FRIENDS)

    def search(self, query: str) -> list[UserSearchResult]:
        """Users whose nickname contains ``query``, as in the site's user picker.

        A two-letter query came back empty where three letters found matches.
        """
        return self._request(_search(query))


class AsyncUsers(AsyncResource):
    async def get(self, user_id: int) -> UserDetails:
        """A user's profile and friends."""
        return await self._request(_get(user_id))

    async def save_field(self, user_id: int, field: str, value: str) -> None:
        """Change a field of a user's profile.

        :param field: the ``UserProfile`` attribute to set: ``first_name``,
            ``second_name``, ``third_name``, ``sex``, ``birthday``, ``city``,
            ``email``, ``mobile`` or ``vk``.
        :param value: the new value as the site shows it, e.g. ``"female"`` for
            ``sex`` or ``"DD.MM.YYYY"`` for ``birthday``.
        """
        await self._request(_save_field(user_id, field, value))

    async def add_friend(self, user_id: int) -> None:
        """Send a friend invitation to a user."""
        await self._request(_friend_action("friend_add", user_id))

    async def accept_friend_invite(self, user_id: int) -> UserDetails:
        """Accept a friend invitation from a user, returning their unlocked profile."""
        return await self._request(_accept_friend_invite(user_id))

    async def decline_friend_invite(self, user_id: int) -> None:
        """Decline a friend invitation from a user."""
        await self._request(_friend_action("friend_invite_decline", user_id))

    async def cancel_friend_invite(self, user_id: int) -> None:
        """Withdraw a friend invitation you sent to a user."""
        await self._request(_friend_action("friend_invite_cancel", user_id))

    async def remove_friend(self, user_id: int) -> None:
        """Remove a user from your friends."""
        await self._request(_friend_action("friend_remove", user_id))

    async def get_events(
        self, user_id: int, *, filter: str | None = "actual"
    ) -> UserEvents:
        """Events the user takes part in, with their role in each.

        :param filter: ``"actual"`` (current and upcoming) or ``None`` for all
            events as on the profile page.
        """
        return await self._request(_get_events(user_id, filter))

    async def get_feeds(
        self, user_id: int, *, limit: int = 30, only_new: bool = True
    ) -> list[UserFeed]:
        """The user's notification feed."""
        return await self._request(_get_feeds(user_id, limit, only_new))

    async def mark_feeds_read(self, user_id: int) -> None:
        """Mark a user's notifications as read."""
        await self._request(_mark_feeds_read(user_id))

    async def get_friends(self) -> list[Friend]:
        """Friends of the token's owner."""
        return await self._request(_GET_FRIENDS)

    async def search(self, query: str) -> list[UserSearchResult]:
        """Users whose nickname contains ``query``, as in the site's user picker.

        A two-letter query came back empty where three letters found matches.
        """
        return await self._request(_search(query))
