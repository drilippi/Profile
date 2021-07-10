from dataclasses import dataclass


@dataclass
class GuildPerks(object):
    """
    A class for the perks of a given guild.
    """

    guild_id: int
    max_template_count: int
    max_field_count: int
    max_profile_count: int


NO_GUILD_PERKS = GuildPerks(0, 3, 10, 5)
SUBSCRIBED_GUILD_PERKS = GuildPerks(0, 15, 20, 30)


async def get_perks_for_guild(db, guild_id: int) -> GuildPerks:
    """
    Get the perks for a given guild.
    """

    guild_settings = await db(
        """SELECT * FROM guild_settings WHERE guild_id=$1 OR guild_id=0 ORDER BY guild_id DESC""",
        guild_id,
    )
    guild_subscription = await db(
        """SELECT * FROM guild_subscriptions WHERE guild_id=$1""",
        guild_id,
    )
    perks = SUBSCRIBED_GUILD_PERKS if guild_subscription else NO_GUILD_PERKS
    return GuildPerks(
        guild_id=guild_id,
        max_template_count=max(
            guild_settings[0]['max_template_count'],
            perks.max_template_count,
            NO_GUILD_PERKS.max_template_count,
        ),
        max_field_count=max(
            guild_settings[0]['max_template_field_count'],
            perks.max_field_count,
            NO_GUILD_PERKS.max_field_count,
        ),
        max_profile_count=max(
            guild_settings[0]['max_template_profile_count'],
            perks.max_profile_count,
            NO_GUILD_PERKS.max_profile_count,
        ),
    )