# Code map errors: the ACO option, canConstruct, missing default buildings and a missing technology

[`../0022-codemap-errors.patch`](../0022-codemap-errors.patch) applies to GitLab `main` `ede81881b7de`
and gives tree `e8368dea`. It serves P14, under hypothesis H9. It also applies unchanged to the
`builds/balance` source, which the harness arms of P14 use.

The errors were found by the code map's checks and are registered in
[`codemap/guides/systems-and-errors.md`](../../codemap/guides/systems-and-errors.md), section 5, under
the same IDs.

## The errors and the changes

| ID | Fact (GitLab `ede81881b7de`) | Change |
|---|---|---|
| C1 | `getCombatOddsSpecific` (`CvGameCoreUtils.cpp:1041`) reads the Advanced Combat Odds option "Ignore Barb Free Wins" as `GC.getDefineINT("ACO_IgnoreBarbFreeWins")`. No global define has that name, so the value is always 0 and the barbarian free-win rule is always applied. The option is the BUG option `ACO__IgnoreBarbFreeWins` (`Config/Advanced Combat Odds.xml`, default False). | `getCombatOddsSpecific` reads the option from `setCombatOddsIgnoreBarbFreeWins`, new in `CvGameCoreUtils`. |
| C1b | `CvGameTextMgr::setCombatPlotHelp` (`CvGameTextMgr.cpp:2225`) applies the free-win rule, and prints "free wins left", only when `getBugOptionBOOL("ACO__IgnoreBarbFreeWins")` is true. That is the opposite of the option's name and of the comment on the line ("Are we not going to ignore barb free wins? If not, skip this section"). Found while preparing C1. | `setCombatPlotHelp` reads the option once, next to its other ACO options. It applies the section when the option is off, and passes the value to `getCombatOddsSpecific`. |
| C2 | `CvCity::canConstruct` (`CvCity.cpp:2343`) binds `CvBuildingInfo& kBuilding = GC.getBuildingInfo(eBuilding)` before `if (eBuilding == NO_BUILDING) return false;`. For `NO_BUILDING` it reads `m_paBuildingInfo[-1]`. The original SDK tests first; the binding came in with RevDCM's "CanConstruct Performance" block. | The test comes first. |
| C3 | `Python/Revolution/Gameready/BarbarianCiv.py` passes the civilization's granary building, -1 (D1), to `city.canConstruct` in four places. | No change of its own. With C2, `canConstruct(-1)` returns false before reading the table. |
| D1 | 21 building classes name a `DefaultBuilding` that nothing the game loads defines: 16 in `XML/Buildings/CIV4BuildingClassInfos.xml` (`BUILDING_GRANARY`, `MODERN_GRANARY`, `MEETING_HALL`, `FISHERMAN_HUT`, `BUTCHERY`, `BAKERY`, `ARTESIAN_WELL`, `HEALERHUT`, `DOCTOR`, `TANNERY`, `BAZAAR`, `PAVED_ROADS`, `GROCER`, `SUPERMARKET`, `SHOPPING_DISTRICT`, `SEWER_SYSTEM`), and 5 in the Guilds module, `Modules/Projects/Vincentz/Guilds/Guildhalls_CIV4BuildingClassInfos.xml` (`BUILDING_GUILDHALL_32`, `36`, `39`, `41`, `43`). `CvBuildingClassInfo::readPass3` gets -1 from `getInfoTypeForString`, which logs it to `xml.log`, and the class keeps `NO_BUILDING`. | The 21 entries say `NONE`. Classes, indices and the game stay as loaded. |
| D2 | `BONUS_WOOL` (`XML/Terrain/CIV4BonusInfos.xml:4121`) names `TECH_WEAVING` as its `TechCityTrade`. No technology `TECH_WEAVING` exists. `CvBonusInfo::read` resolves it with `FindInInfoClass`, which shows the dialog "Tag: TECH_WEAVING in Info class was incorrect". The value is -1, and `CvTeam::isHasTech(NO_TECH)` returns true. | The entry says `NONE`. The game stays as loaded (wool tradeable from the start), without the dialog. |

What the patch leaves as it was:
- The five event triggers that require a building of an empty class still cannot fire:
  `EVENTTRIGGER_SPOILED_GRAIN`, `POISON_ARROWS`, `TANNERY_GLUE`, `RURAL_FARMERS`, `CRAB_CAKES`.
- No building is restored, and wool gets no trade technology.

Those are design decisions, not errors in the code or the data, and are left to the user.

## Effect on play

- The DLL changes affect only the combat-odds tooltip and a `canConstruct` call with `NO_BUILDING`.
  `getCombatOddsSpecific` has no caller outside `setCombatPlotHelp`.
- With the option at its default (off), the tooltip's per-round odds now include the barbarian
  free-win rule and show "free wins left". Before, only its outcome probabilities, which come from
  `getCombatOddsSpecific`, included the rule.
- The XML changes give the same loaded rules as before.
- Saves: nothing new is saved, and no index changes.

## Checks

| Check | Result |
|---|---|
| Release build, `toolchain/build_dll.sh`, MSVC 2003 | 0 errors, 0 warnings ([build](../../builds/codemap-errors/README.md)) |
| clang gate on the three changed C++ files against `ede81881b7de` | 0 new diagnostics ([clang-gate.log](clang-gate.log)) |
| `codemap/tool/check_links.py` on the patched tree | 0 type references defined nowhere (22 before); 2 undefined defines (3 before; the 2 left are D3 and C5, dormant, not in this patch) |
| `method/patchcheck.py` | passes |
| P14: harness runs, with and without the patch, 30 seeds each | pending |

The harness has no Python and draws no tooltip. So C1, C1b and C3 rest on the reading above; the
runs check that nothing else changes.
