# Jerusalem succession compatibility

Reviewed local EU4 1.37.2 scripts: `decisions/Jerusalem.txt`, `missions/SCA_Teutonic_Missions.txt`, and `missions/EMP_CrusaderMissions.txt`. Mission file fingerprints are in `project.json`.

Observation: the native formation decision changes TEU to KOJ and calls `swap_non_generic_missions`. The five Teutonic Crusader series require TEU. Emperor's five Crusader series accept KOJ and occupy the same columns. Merely widening the Teutonic tag condition would introduce competing series.

Policy: KOJ with `was_tag = TEU`, `teu_crusader_path`, and Lions of the North continues the committed Order campaign. Widen only those five series and the three shared opening series (Livonia, Danzig/Poland, army); the latter retain prerequisite missions. Exclude exactly that successor from the Emperor Crusader series. All original mission bodies, coordinates, icons and rewards remain unchanged apart from the pre-existing opening visibility gate. Other Jerusalem origins and Teutonic campaigns without Crusader commitment retain native assignment. No new campaign objectives or rewards are introduced.

Custom decisions use the same successor restriction. The existing refresh decision can reassign an already-formed successor missing `teux_e01`, without awarding completion or changing its tag. No formation decision or save file is modified. Native mission refresh and completion retention must still be checked in the engine by the user; offline tests do not guarantee old-save compatibility.

Offline checks compare the successor's full 87-node assignment to committed TEU, validate arrows and combined series spans, and cover native Jerusalem, uncommitted and Prussian Teutonic origins, foreign Crusaders, Knights, missing Lions of the North, and random maps. Emperor mission bodies are unchanged. The evaluator now distinguishes explicitly listed DLCs and the native random-new-world predicate. It does not simulate arbitrary mod priorities.
