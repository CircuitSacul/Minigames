from __future__ import annotations

from typing import Awaitable, Callable

import crescent
import hikari

from minigames.config import CONFIG


async def owner_only(ctx: crescent.Context) -> crescent.HookResult | None:
    if ctx.user.id not in CONFIG.owners:
        await ctx.respond("Only owners can use this command.", ephemeral=True)
        return crescent.HookResult(True)

    return None


async def guild_only(ctx: crescent.Context) -> crescent.HookResult | None:
    if not ctx.guild_id:
        await ctx.respond(
            "This command can only be used inside servers.", ephemeral=True
        )
        return crescent.HookResult(True)

    return None


def has_guild_perms(
    perms: hikari.Permissions,
) -> Callable[[crescent.Context], Awaitable[crescent.HookResult | None]]:
    async def check(ctx: crescent.Context) -> crescent.HookResult | None:
        await guild_only(ctx)
        assert ctx.guild_id is not None
        assert ctx.member is not None
        assert isinstance(member := ctx.member, hikari.InteractionMember)

        guild = ctx.app.cache.get_guild(ctx.guild_id)
        assert guild is not None

        if perms not in member.permissions:
            await ctx.respond(
                "You don't have permission to use this command.",
                ephemeral=True,
            )
            return crescent.HookResult(True)

        return None

    return check
