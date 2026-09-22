from typing import Any, Callable, Dict

from v14.app_dry_run import run_app_dry_run


CONTRACT_VERSION = "V14_APP_SHADOW_DRY_RUN_V1"


def run_app_shadow_dry_run(
    *,
    enabled: bool,
    legacy_result: Any,
    data: Any,
    code: Any,
    name: Any,
    market: Any,
    symbol: Any,
    dry_run_fn: Callable[..., Dict[str, Any]] = run_app_dry_run,
) -> Dict[str, Any]:
    """V14 App Shadow Dry-Run Wiring V1.

    Safety boundary:
      - Shadow OFF - dry-run calls
      - Shadow ON - one dry-run call
      - preserve Legacy inputs
      - isolate Shadow exceptions
      - no Runtime Writer
      - no Supabase client
      - no network I/O
      - no production write
    """

    if not enabled:
        return {
            "version": CONTRACT_VERSION,
            "state": "SKIPPED",
            "reason": "SHADOW_DISABLED",
        }

    try:
        return dry_run_fn(
            legacy_result=legacy_result,
            data=data,
            code=code,
            name=name,
            market=market,
            symbol=symbol,
        )
    except Exception:
        return {
            "version": CONTRACT_VERSION,
            "state": "BLOCKED",
            "reason": "SHADOW_EXCEPTION",
        }
