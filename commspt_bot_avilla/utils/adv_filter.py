from avilla.core.context import ContextSceneSelector, ContextClientSelector
from commspt_bot_avilla.utils.setting_manager import S_

Q_ = S_.defined_qq


def from_groups(allowed_groups: list[int]):
    def _wrapper(selector: ContextSceneSelector) -> bool:
        return int(selector.channel) in allowed_groups

    return _wrapper


def from_groups_preset_general():
    """
    Preset groups: `littleskin_main`, `commspt_group`, `dev_group`
    """
    return from_groups([Q_.littleskin_main, Q_.commspt_group, Q_.dev_group])


def by_admin_only():
    def _wrapper(selector: ContextClientSelector) -> bool:
        return int(selector.user) in S_.admin_list

    return _wrapper
