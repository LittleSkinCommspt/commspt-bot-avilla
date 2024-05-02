from avilla.core import Context
from avilla.core.context import ContextClientSelector, ContextSceneSelector
from avilla.core.tools.filter import Filter
from graia.saya.builtins.broadcast.shortcut import dispatch

from commspt_bot_avilla.utils.setting_manager import S_

Q_ = S_.defined_qq


def from_groups(allowed_groups: list[int]):
    def _wrapper(selector: ContextSceneSelector) -> bool:
        return int(selector.channel) in allowed_groups

    return _wrapper


def from_groups_preset_general():
    """
    Preset groups: `littleskin_main`, `littleskin_cafe`,  `commspt_group`, `dev_group`
    """
    return from_groups([Q_.littleskin_main, Q_.littleskin_cafe, Q_.commspt_group, Q_.dev_group])


def by_admin_only():
    def _wrapper(selector: ContextClientSelector) -> bool:
        return int(selector.user) in S_.admin_list

    return _wrapper


dispather_by_admin_only = dispatch(
    Filter().dispatch(Context).assert_true(lambda ctx: by_admin_only()(ctx.client))
)

dispatcher_from_preset_general = dispatch(
    Filter()
    .dispatch(Context)
    .assert_true(lambda ctx: from_groups_preset_general()(ctx.scene))
)


def dispatcher_from(groups: list[int]):
    return dispatch(
        Filter()
        .dispatch(Context)
        .assert_true(lambda ctx: from_groups(groups)(ctx.scene))
    )
